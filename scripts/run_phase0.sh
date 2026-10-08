#!/usr/bin/env bash
# Raccourci macOS / Linux pour scripts/run_phase0.py (mêmes options : --test, --sleep, --cookies).
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/run_phase0.py "$@"
