# omo_vs_copilot_sync

## OpenCode Prompt

Use this prompt in OpenCode to run a full audit and upgrade cycle:

```
- Run `omo_vs_copilot_sync` to test my GitHub Copilot model availability and validate my OMO config. 
- Then read the OMO reference docs at https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/reference/configuration.md (sections "Agent Provider Chains" and "Category Provider Chains"). 
- Compare my current config (~/.config/opencode/oh-my-openagent.json) against the official recommendations, only proposing models confirmed available by the script.
- Present a table of recommended changes with justification, then ask me for validation before applying.
```

---

Test all models available from your GitHub Copilot subscription, then cross-check your `oh-my-openagent.json` config to detect broken or retired model references.


```
❯ omo_vs_copilot_sync --help
Usage: omo_vs_copilot_sync [options]

Verify GitHub Copilot model availability and validate OMO config.

Options:
  -c, --config PATH   Path to oh-my-openagent.json
  -t, --timeout SEC   Per-model test timeout in seconds (default: 30)
  -p, --provider NAME Provider to test (default: github-copilot)
  -q, --quick         Skip live tests, only check config against provider list
  -h, --help          Show this help
```
## How it works

1. Runs `opencode models github-copilot` to get the current provider model list
2. For each model, runs `opencode run -m <model> --pure "Say only: OK"` with a timeout
3. Parses all `"model": "github-copilot/..."` entries from `oh-my-openagent.json`
4. Cross-references tested results to flag broken config entries


## Features

- **Dynamic model discovery** — fetches the live model list from `opencode models`, no hardcoded list
- **Live availability test** — calls each model with a minimal prompt to confirm real access
- **Config validation** — parses `oh-my-openagent.json` and flags any model that is broken or missing from the provider
- **Quick mode** — skip live tests, just verify config models exist in the provider listing
- **Exit codes** — `0` if config is valid, `1` if issues found (scriptable)

## Requirements

- [OpenCode](https://github.com/opencode-ai/opencode) (in PATH, authenticated)
- [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) plugin configured

## Install

```bash
# Symlink (updates automatically with git pull)
mkdir -p ~/.local/bin
ln -sf "$(pwd)/omo_vs_copilot_sync" ~/.local/bin/omo_vs_copilot_sync
```

Make sure `~/.local/bin` is in your `PATH`.

## Usage

```bash
# Full test: probe every model + validate config (~3 min)
omo_vs_copilot_sync

# Quick check: just verify config models are listed by the provider (instant)
omo_vs_copilot_sync --quick

# Custom config path
omo_vs_copilot_sync --config ~/my-project/oh-my-openagent.json

# Shorter timeout per model
omo_vs_copilot_sync --timeout 15
```

## Output

### Phase 1 — Model availability

```
❯ omo_vs_copilot_sync

Fetching models from provider 'github-copilot'...
Found 25 models.

MODEL                               STATUS     TIME
-----                               ------     ----
claude-haiku-4.5                    OK         4s
claude-opus-4.5                     OK         3s
claude-opus-4.6                     OK         6s
claude-opus-4.6-fast                OK         4s
claude-opus-4.7                     OK         4s
claude-opus-4.7-fast                OK         3s
claude-opus-4.8                     OK         4s
claude-opus-4.8-fast                OK         4s
claude-sonnet-4                     FAIL       3s
claude-sonnet-4.5                   OK         5s
claude-sonnet-4.6                   OK         6s
gemini-2.5-pro                      OK         5s
gemini-3-flash-preview              OK         4s
gemini-3.1-pro-preview              OK         5s
gemini-3.5-flash                    OK         3s
gpt-4.1                             OK         4s
gpt-5-mini                          OK         3s
gpt-5.2                             FAIL       3s
gpt-5.2-codex                       FAIL       2s
gpt-5.3-codex                       OK         4s
gpt-5.4                             OK         5s
gpt-5.4-mini                        OK         3s
gpt-5.4-nano                        FAIL       3s
gpt-5.5                             OK         4s
raptor-mini                         FAIL       3s

--
Available: 20/25
Unavailable: 5/25
Tested: 2026-06-11 09:54

--
Validating config: /Users/jean/.config/opencode/oh-my-openagent.json

CONFIG MODEL                             STATUS       ISSUE
------------                             ------       -----
claude-haiku-4.5                         OK
claude-opus-4.6                          OK
claude-opus-4.7                          OK
claude-sonnet-4.6                        OK
gemini-3-flash-preview                   OK
gemini-3.1-pro-preview                   OK
gpt-5-mini                               OK
gpt-5-nano                               NOT LISTED   Not in provider model list
gpt-5.5                                  OK

--
CONFIG ISSUES: 1/9 models broken or missing.
Available models: opencode models github-copilot
```

