# Shared Skills

Skills auto-loaded by [OpenCode](https://github.com/anomalyco/opencode) across all projects via `skills.paths` in the global config. OpenCode scans recursively for `**/SKILL.md`.

## Setup

Already configured in `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": ["/Users/jean/Documents/CODE/omo_toolbox/skills"]
  }
}
```

## Available skills

| Skill | Description |
|-------|-------------|
| [skill-pdf-ingestion](./skill-pdf-ingestion/) | PDF → Markdown via Marker (SOTA): text, scans, slides, tables, math, multi-column. Includes a mandatory cleanup pipeline (footers, multi-column, artifacts). |

## Adding a skill

Each skill is self-contained in its own folder:

```
skills/
  my-skill/
    SKILL.md          # instructions (required)
    pyproject.toml    # dependencies (optional)
    tool.py           # bundled tool (optional)
```

Restart OpenCode after adding a new skill.
