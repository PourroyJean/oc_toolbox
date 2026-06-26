---
name: skill-pdf-ingestion
description: "PDF to Markdown conversion via Marker (SOTA). Handles text, scans, slides, tables, math, multi-column layouts. Use for \"Extrait PDF\", \"Convertis PDF\", \"PDF to markdown\", \"traite pdf\", \"convertir pdf\"."
metadata:
  triggers: ["Extrait PDF", "Convertis PDF", "marker", "PDF to markdown", "extraire PDF", "traite pdf", "pdf vers md", "convertir pdf"]
  version: "3.0"
---

## Workflow d'execution (OBLIGATOIRE — suivre dans l'ordre)

NE JAMAIS livrer l'output brut comme resultat final. Le resultat final est TOUJOURS le produit du pipeline complet.

```
ETAPE A : Localiser le PDF
ETAPE B : Extraire via Marker → sauver le brut dans /tmp/<nom_pdf>.md
ETAPE C : Lire le brut, post-traiter (pipeline 3 etapes — OBLIGATOIRE)
ETAPE D : Sauvegarder le .md final a destination, supprimer le fichier brut
```

### ETAPE A — Localiser le PDF

Chemin explicite fourni → utiliser directement. Sinon aucun → demander le chemin

### ETAPE B — Extraire via Marker

```bash
uv run --project <skill_dir> pdf-to-md /chemin/absolu/fichier.pdf --output-dir /tmp/
```

Le fichier brut atterrit dans `/tmp/<nom_pdf>.md`. C'est la matiere premiere, PAS le livrable.

Options selon le type de PDF :

| Flag | Effet | Quand |
|---|---|---|
| `--force-ocr` | Re-OCR tout, maths → LaTeX | PDF scanne, texte corrompu |
| `--pages "0,5-10,20"` | Pages specifiques | PDF > 50 pages |
| `--copilot MODEL` | LLM via copilot-api | Tables/maths complexes |
| `--use-llm` | LLM via Gemini | Alternative a --copilot |

Si Marker echoue (output vide, erreur) → Le dire et arreter.

### ETAPE C — Post-traiter (OBLIGATOIRE)

Lire `/tmp/<nom_pdf>.md`. Appliquer les 3 etapes du pipeline. Marker produit du bruit (unicode garble, footers dans le code, layouts entrelaces). Le cleanup est TOUJOURS necessaire.

1. **Footers → separateurs** : identifier le pattern de footer repetitif, remplacer par `---`
2. **Multi-colonnes** : separer les blocs de code entrelaces en sections distinctes
3. **Cleanup general** : artefacts unicode/HTML, lang tags sur les code blocks, ligatures

Detail de chaque etape : voir section "Pipeline" ci-dessous.

### ETAPE D — Sauvegarder

Ecrire le .md final dans le meme dossier que le PDF source (sauf demande contraire de l'utilisateur). Supprimer le fichier brut dans `/tmp/`.

---

## Setup

Ce skill embarque son outil dans le meme dossier :

```
skills/skill-pdf-ingestion/
  SKILL.md          # ce fichier
  pyproject.toml    # marker-pdf
  pdf_to_md.py     # wrapper CLI
```

`<skill_dir>` = le dossier contenant ce SKILL.md.

Premiere fois (installe le .venv localement, une seule fois) :
```bash
uv sync --project <skill_dir>
```

Ensuite, executer depuis N'IMPORTE OU :
```bash
uv run --project <skill_dir> pdf-to-md input.pdf [options]
```

---

## Pipeline post-extraction (detail des 3 etapes)

### Etape 1 : Footers → separateurs de pages

1. Scanner les premieres pages. Reperer les lignes identiques a intervalles reguliers (seul le numero change).
2. Patterns typiques :
   - `Conference YYYY | Titre N`
   - `© YYYY Company | Slide N`
   - `Page N / Total`
3. Remplacer chaque occurrence par `\n---\n`.
4. Supprimer aussi les footers a l'interieur de blocs de code.

### Etape 2 : Reconstruction multi-colonnes

**Symptomes** : lignes numerotees entrelacees, deux en-tetes de colonnes, code melange.

**Procedure** :
1. Identifier les en-tetes de colonnes
2. Creer `### Titre colonne gauche` + bloc de code
3. Creer `### Titre colonne droite` + bloc de code
4. Si ambigu → `<!-- LAYOUT MULTI-COLONNES : separation incertaine -->`

### Etape 3 : Cleanup general

Purement formatage — aucune invention de contenu.

```
AUTORISE :
- Supprimer unicode garbles (ʣ, ʵ, etc.) et artefacts (cid:XXX)
- Supprimer footers/headers repetitifs RESTANTS
- Supprimer lettres isolees parasites de watermarks
- Supprimer lignes de points "......"
- Supprimer artefacts HTML (`</pre>`, `<br>`, etc.)
- Ajouter le langage aux blocs de code (```c, ```python, ```bash, etc.)
- Corriger sauts de ligne casses
- NE PAS toucher aux separateurs `---`

INTERDIT : ajouter, inventer ou modifier du contenu.
Passage illisible → <!-- ILLISIBLE -->.
```

---

## Troubleshooting

### "Marker not installed"
**Solution** : `cd <skill_dir> && uv sync`

### Conversion echoue sur PDF complexe
**Solution (dans cet ordre)** :
1. `--force-ocr`
2. `--pages "0-10"`
3. `--copilot gpt-4o`

### Output vide ou illisible
**Cause** : PDF scanne, protege ou 100% image. **Solution** : essayer `--force-ocr`. Si toujours vide → le dire a l'utilisateur et arreter (ne pas inventer de contenu).

## Edge cases

- **PDF protege** : Marker echoue. Demander deprotection a l'utilisateur.
- **PDF > 50 pages** : decouper avec `--pages` si memoire limitee.
- **PDF purement visuel** (photos, scans sans texte) : Le dire et arreter.
