# oc_stats

Display OpenCode usage stats: cost, tokens, agents, and models. Covers the last 7 days by default, today only, or a single session with its full delegation tree.

![oc_stats default output](../ressources/oc_stats.png)

## Install

```bash
mkdir -p ~/.local/bin
ln -sf "$(pwd)/oc_stats/oc_stats" ~/.local/bin/oc_stats
```

Make sure `~/.local/bin` is in your `PATH`.

## Usage

```bash
# 7-day summary (default)
oc_stats

# Today only
oc_stats --today

# Single session detail with delegation tree
oc_stats --session <ID>
```

## Output

### Default — 7-day summary

```
  OMO STATS — Jun 05 → Jun 11  (7 days)
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  COST    $150.24 total   $21.46/day avg   463 sessions
  TOKENS  84.0M in   17.8M out   1.4M reasoning
  CACHE   98.7% hit rate

  ─── By Agent ──────────────────────────────
  Sisyphus          13   $110.77   $8.52   29.4M
  Sisyphus-Junior   35    $13.63   $0.39    2.3M
  ...
```

### --today

```
  OMO STATS — Jun 11
  ━━━━━━━━━━━━━━━━━━

  COST    $19.45    54 sessions    2.6M tokens

  Sisyphus          $14.22   claude-opus-4.8
  ...
```

### --session \<ID\>

```
  SESSION — "Refactor auth module"   $29.11   52 min
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  PARENT    Sisyphus (claude-opus-4.6)   $22.84
  ├─ child  Sisyphus-Junior (sonnet-4.6)  $3.12
  └─ child  oracle (gpt-5.5)             $1.88
```

## Requirements

- [OpenCode](https://github.com/anomalyco/opencode) (authenticated)
- Python 3.6+
