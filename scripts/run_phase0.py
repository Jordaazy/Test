#!/usr/bin/env python3
"""Phase 0 complète, identique sous Windows / macOS / Linux :
index -> sous-titres -> transcriptions propres -> pré-classement, puis résumé de contrôle.

  python scripts/run_phase0.py --test     # essai sur les 3 vidéos les plus récentes (~1 min)
  python scripts/run_phase0.py            # toute la chaîne (reprend là où il s'est arrêté)
  python scripts/run_phase0.py --sleep 3  # plus lent, si YouTube renvoie des erreurs 429
"""
import argparse
import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def summary():
    index = list(csv.DictReader((DATA / "index.csv").open(encoding="utf-8")))
    full = sum(1 for r in index if r.get("meta") == "full")
    manifest_path = DATA / "subs_manifest.csv"
    manifest = list(csv.DictReader(manifest_path.open(encoding="utf-8"))) if manifest_path.exists() else []
    got = sum(1 for r in manifest if r["file"])
    no_subs = sum(1 for r in manifest if r["note"] == "no-subtitles")
    failed = sum(1 for r in manifest if "download-failed" in r["note"])
    transcripts = len(list((DATA / "transcripts").glob("*.md")))
    print("\n========== RÉSUMÉ PHASE 0 ==========")
    print(f"Vidéos listées                     : {len(index)}")
    print(f"Avec métadonnées complètes (dates) : {full}")
    print(f"Sous-titres téléchargés            : {got}")
    print(f"Sans aucun sous-titre              : {no_subs}")
    print(f"Échecs de téléchargement           : {failed}")
    print(f"Transcriptions propres (.md)       : {transcripts}")
    if full < len(index) or failed:
        print("-> Incomplet : relance la même commande, elle reprend là où elle s'est arrêtée.")
    else:
        print("-> Terminé. Tu peux envoyer le dossier data/ sur GitHub.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="essai sur 3 vidéos")
    ap.add_argument("--sleep", type=float, default=1.0)
    ap.add_argument("--cookies", default=None)
    args = ap.parse_args()

    common = ["--sleep", str(args.sleep)] + (["--cookies", args.cookies] if args.cookies else [])
    steps = [
        ["p0_index.py", *common, *(["--limit", "3"] if args.test else [])],
        ["p0_subs.py", *common],
        ["p0_clean.py"],
        ["p0_classify.py"],
    ]
    for step in steps:
        print(f"\n>>> {step[0]}", flush=True)
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / step[0]), *step[1:]], cwd=ROOT)
        if r.returncode:
            sys.exit(f"Échec à l'étape {step[0]} (code {r.returncode}). Copie les dernières lignes ci-dessus à Claude.")
    summary()


if __name__ == "__main__":
    main()
