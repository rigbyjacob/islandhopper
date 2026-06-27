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
    nohup uv run --python 3.14 python -m http.server {{port}} --directory "{{justfile_directory()}}" > "{{logf}}" 2>&1 &
    echo $! > "{{pidf}}"
    sleep 0.6
    echo "serving {{justfile_directory()}} → {{url}}  (pid $(cat {{pidf}}))"

# Open the page in your default browser (starts the server first if needed)
open: serve
    open "{{url}}"

# Hard-refresh: re-open the tab/page (server keeps running)
refresh: serve
    open "{{url}}"

# Live-reload: bump the touchfile so any open localhost tab reloads itself (no need to re-focus the browser)
reload:
    @date +%s > reload.txt && echo "reload triggered"

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

# Bundle index.html + data/*.js into one self-contained dist/index.html for distribution.
# Dev keeps the heavy GIS blobs in data/*.js (classic scripts → window.*) so index.html
# stays editable; packing inlines them back into a single portable file.
pack:
    node build/pack.js
    @ls -lh dist/index.html docs/index.html

# Clear stale git lock files (a concurrent host git process keeps leaving .git/*.lock behind,
# which blocks commits). Safe to run whenever a commit fails with "Unable to create ... .lock".
unlock:
    @rm -f .git/index.lock .git/HEAD.lock .git/refs/heads/*.lock .git/objects/*/tmp_obj_* 2>/dev/null; echo "git locks cleared"

# Clear locks, then stage + commit everything:  just save "your message"
save msg:
    @rm -f .git/index.lock .git/HEAD.lock .git/refs/heads/*.lock 2>/dev/null || true
    git add -A && git commit -m "{{msg}}"

# Build the real star catalog (one-time / when you want fresh data): node fetches d3-celestial data
stars:
    node build/build_starmap.js

# Purge the big GEBCO source files from ALL git history. They're gitignored now, but the old
# committed tiles (a 118M .asc + 41M .nc + copies) still live in history — bloating .git to ~176M
# and tripping GitHub's 100M-per-file limit, which blocks pushes. Re-download tiles from gebco.net
# whenever you need them. Verified: removes 9 blobs (~170M), .git → ~13M, HEAD tree unchanged,
# all 202 commits preserved. REWRITES history → afterwards force-push (printed at the end).
# Requires git-filter-repo:  brew install git-filter-repo
purge-gebco:
    #!/usr/bin/env sh
    set -e
    command -v git-filter-repo >/dev/null 2>&1 || { echo "git-filter-repo missing → brew install git-filter-repo"; exit 1; }
    if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
      echo "Tracked changes present — commit or stash them first (filter-repo rewrites tracked files; untracked files are left alone)."; exit 1
    fi
    bk="../PID-backup-$(date +%Y%m%d-%H%M%S).bundle"
    git bundle create "$bk" --all >/dev/null && echo "backup → $bk"
    before="$(du -sh .git | cut -f1)"
    git filter-repo --force --invert-paths --path-glob '*GEBCO*'
    git reflog expire --expire=now --all 2>/dev/null || true
    git gc --prune=now --aggressive --quiet
    git remote get-url origin >/dev/null 2>&1 || git remote add origin git@github.com:rigbyjacob/islandhopper.git
    echo "leftover GEBCO blobs: $(git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(rest)' 2>/dev/null | grep -c 'GEBCO' || true)"
    echo ".git: $before → $(du -sh .git | cut -f1)"
    echo "Done. Review, then force-push:  git push --force origin main"
