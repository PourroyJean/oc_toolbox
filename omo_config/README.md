# omo_config

Configuration files for [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) (OpenCode plugin).

## Contents

| File | Description |
|------|-------------|
| `oh-my-openagent.json` | Agents, categories, provider chains, background task limits |

## Install

```bash
ln -sf "$(pwd)/oh-my-openagent.json" ~/.config/opencode/oh-my-openagent.json
```

## Maintenance

Use [`omo_copilot_sync`](../omo_copilot_sync/) to audit model availability and detect stale references after provider updates.
