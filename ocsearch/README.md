# ocsearch

```
❯ ocsearch
Usage: ocsearch list          - list all sessions
       ocsearch search QUERY  - search sessions that match content
```

![ocsearch list](./assets/screenshot.png)


Search and browse all OpenCode sessions across every project on your machine, with interactive [fzf](https://github.com/junegunn/fzf) selection.

## Features

- **List all sessions** — sorted by last activity, with message count, token usage, and session age
- **Full-text search** — find which session discussed a specific topic (case-sensitive)
- **Interactive selection** — pick a session in fzf, instantly opens it in OpenCode
- **Cross-project** — queries the central OpenCode database, not limited to current directory
- **Color-coded** — date (white), directory (green), title (orange) for quick scanning

## Requirements

- Python 3.6+
- [fzf](https://github.com/junegunn/fzf) (`brew install fzf`)
- [OpenCode](https://github.com/opencode-ai/opencode) (with its default SQLite database)

## Install

```bash
# Symlink (updates automatically with git pull)
mkdir -p ~/.local/bin
ln -sf "$(pwd)/ocsearch" ~/.local/bin/ocsearch
```

Make sure `~/.local/bin` is in your `PATH`.

## Usage

```bash
# List all sessions (most recent first)
ocsearch list

# Search for a topic across all session content
ocsearch search "kubernetes"
ocsearch search "auth middleware"
```

### Pipe mode

When stdout is not a TTY, ocsearch dumps plain output for scripting:

```bash
ocsearch list | grep "my-project"
ocsearch search "bug" | wc -l
```

## Output columns

| Column | Description |
|--------|-------------|
| last active | Timestamp of the most recent message |
| dir | Project directory (~ shortened) |
| title | Session title |
| msgs | Message count |
| tokens | Total tokens used (input + output) |
| age | Time since session creation |

## How it works

Reads directly from OpenCode's SQLite database at `~/.local/share/opencode/opencode.db`. Only queries root sessions (excludes sub-agent sessions). Selection opens the session via `opencode -s <id>` in the session's original working directory.
