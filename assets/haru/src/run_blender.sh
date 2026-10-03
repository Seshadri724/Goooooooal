#!/usr/bin/env bash
# Run a Blender Python script headless and wait for it. The Store build only exposes blender-launcher.exe,
# which detaches, so each script writes "<script>.log" ending in DONE or a traceback and we poll for that.
# usage: run_blender.sh <script.py> [file.blend] [timeout_s]
set -u
script="$(cd "$(dirname "$1")" && pwd -W)/$(basename "$1")"
log="${script%.py}.log"
blend="${2:-}"
timeout="${3:-300}"
rm -f "$log"
launcher="$LOCALAPPDATA/Microsoft/WindowsApps/blender-launcher.exe"
if [ -n "$blend" ]; then "$launcher" --background "$blend" --python "$script"; else "$launcher" --background --factory-startup --python "$script"; fi
for ((i = 0; i < timeout; i++)); do
  if [ -f "$log" ] && grep -qE '^(DONE|FAILED)' "$log"; then cat "$log"; grep -q '^DONE' "$log"; exit $?; fi
  sleep 1
done
echo "timed out after ${timeout}s"; [ -f "$log" ] && cat "$log"; exit 1
