# Caribbean PID Helmsman — local dev server (uv + Python 3.14)
# Usage: `just serve`, `just open`, `just refresh`, `just restart`, `just stop`, `just status`
# Requires: `just` (brew install just) and `uv` (https://docs.astral.sh/uv/).
# uv auto-installs the pinned Python 3.14 (.python-version) on first run — no system python needed.

port := "8080"
url  := "http://localhost:" + port + "/index.html"
pidf := ".server.pid"
logf := ".server.log"

# Show available recipes
default:
    @just --list

# One-time: make sure uv has Python 3.14 on hand
setup:
    uv python install 3.14

# Start the static server in the background (no-op if already running)
serve:
    #!/usr/bin/env sh
    if [ -f "{{pidf}}" ] && kill -0 "$(cat {{pidf}})" 2>/dev/null; then
      echo "already running (pid $(cat {{pidf}})) → {{url}}"; exit 0
    fi
    nohup uv run --no-project --python 3.14 python -m http.server {{port}} --directory "{{justfile_directory()}}" > "{{logf}}" 2>&1 &
    echo $! > "{{pidf}}"
    sleep 0.6
    echo "serving {{justfile_directory()}} → {{url}}  (pid $(cat {{pidf}}))"

# Open the page in your default browser (starts the server first if needed)
open: serve
    open "{{url}}"

# Hard-refresh: re-open the tab/page (server keeps running)
refresh: serve
    open "{{url}}"

# Stop, then start fresh
restart: stop serve

# Stop the background server (kills the process group so uv's child python dies too)
stop:
    #!/usr/bin/env sh
    if [ -f "{{pidf}}" ]; then
      pid="$(cat {{pidf}})"
      kill "$pid" 2>/dev/null && echo "stopped (pid $pid)" || echo "was not running"
      pkill -P "$pid" 2>/dev/null || true
      rm -f "{{pidf}}"
    else
      echo "not running"
    fi

# Is the server up?
status:
    #!/usr/bin/env sh
    if [ -f "{{pidf}}" ] && kill -0 "$(cat {{pidf}})" 2>/dev/null; then
      echo "UP   pid $(cat {{pidf}})  →  {{url}}"
    else
      echo "DOWN"
    fi

# Tail the server log
logs:
    @tail -n 40 -f "{{logf}}"

# Stop the server and remove generated cruft (pid, log, and any stray .venv)
clean: stop
    @rm -rf .venv "{{logf}}" && echo "cleaned"
