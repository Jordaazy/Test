#!/usr/bin/env bash
# Phase 0 complète : index -> sous-titres -> transcriptions propres -> pré-classement.
# Reprise possible à tout moment (les étapes déjà faites sont sautées).
#   bash scripts/run_phase0.sh                 # sans cookies
#   COOKIES=cookies.txt bash scripts/run_phase0.sh   # si YouTube demande "confirm you're not a bot"
set -euo pipefail
cd "$(dirname "$0")/.."
EXTRA=()
[[ -n "${COOKIES:-}" ]] && EXTRA=(--cookies "$COOKIES")
SLEEP="${SLEEP:-1.0}"

python3 scripts/p0_index.py --sleep "$SLEEP" "${EXTRA[@]}"
python3 scripts/p0_subs.py  --sleep "$SLEEP" "${EXTRA[@]}"
python3 scripts/p0_clean.py
python3 scripts/p0_classify.py
