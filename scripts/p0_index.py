#!/usr/bin/env python3
"""Phase 0.1 — Index de toutes les vidéos de la chaîne.

Étapes :
  1. extraction "flat" des onglets videos / shorts / streams (liste des IDs) ;
  2. extraction complète par vidéo (sans téléchargement) -> data/meta/<id>.json
     (reprise possible : les vidéos déjà présentes sont sautées) ;
  3. écriture de data/index.csv.

Usage :
  python3 scripts/p0_index.py [--channel URL] [--cookies cookies.txt] [--sleep 1.5]
"""
import argparse
import csv
import json
import sys
from pathlib import Path

import yt_dlp

ROOT = Path(__file__).resolve().parent.parent
META_DIR = ROOT / "data" / "meta"
INDEX_CSV = ROOT / "data" / "index.csv"
TABS = {"videos": "video", "shorts": "short", "streams": "live"}

# Champs conservés dans data/meta/<id>.json (on jette les formats, très lourds).
KEEP = [
    "id", "title", "upload_date", "timestamp", "duration", "view_count", "like_count",
    "description", "language", "tags", "categories", "chapters", "live_status",
    "was_live", "channel", "channel_id", "webpage_url", "availability",
]


def hms(seconds):
    if seconds is None:
        return ""
    s = int(round(seconds))
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def base_opts(args):
    opts = {
        "quiet": True,
        "no_warnings": False,
        "skip_download": True,
        "ignoreerrors": True,
        "sleep_interval_requests": args.sleep,
        "extractor_retries": 3,
        "js_runtimes": {"node": {}, "deno": {}, "bun": {}},  # défis JS YouTube (yt-dlp-ejs)
    }
    if args.cookies:
        opts["cookiefile"] = args.cookies
    return opts


def list_ids(args):
    """Retourne {video_id: type} à partir des onglets de la chaîne."""
    found = {}
    opts = base_opts(args) | {"extract_flat": "in_playlist"}
    with yt_dlp.YoutubeDL(opts) as ydl:
        for tab, vtype in TABS.items():
            url = f"{args.channel.rstrip('/')}/{tab}"
            info = ydl.extract_info(url, download=False)
            entries = (info or {}).get("entries") or []
            n = 0
            for e in entries:
                if e and e.get("id") and e["id"] not in found:
                    found[e["id"]] = vtype
                    n += 1
            print(f"[index] onglet {tab}: {n} vidéos", file=sys.stderr)
    return found


def fetch_meta(vid, args):
    out = META_DIR / f"{vid}.json"
    if out.exists():
        return json.loads(out.read_text())
    with yt_dlp.YoutubeDL(base_opts(args)) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False)
    if not info:
        return None
    meta = {k: info.get(k) for k in KEEP}
    # On ne garde que la liste des langues + extensions dispo pour les sous-titres.
    meta["subtitles"] = {
        lang: [t.get("ext") for t in tracks] for lang, tracks in (info.get("subtitles") or {}).items()
    }
    meta["automatic_captions"] = {
        lang: [t.get("ext") for t in tracks]
        for lang, tracks in (info.get("automatic_captions") or {}).items()
        if lang.endswith("-orig") or lang.split("-")[0] in ("fr", "en")
    }
    out.write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", default="https://www.youtube.com/@amaspft")
    ap.add_argument("--cookies", default=None)
    ap.add_argument("--sleep", type=float, default=1.0)
    args = ap.parse_args()

    META_DIR.mkdir(parents=True, exist_ok=True)
    ids = list_ids(args)
    if not ids:
        sys.exit("[index] aucune vidéo trouvée (accès YouTube ?)")

    rows, failed = [], []
    for i, (vid, vtype) in enumerate(ids.items(), 1):
        meta = fetch_meta(vid, args)
        if not meta:
            failed.append(vid)
            continue
        d = meta.get("upload_date") or ""
        rows.append({
            "video_id": vid,
            "upload_date": f"{d[:4]}-{d[4:6]}-{d[6:]}" if len(d) == 8 else "",
            "title": meta.get("title") or "",
            "duration_s": meta.get("duration") or "",
            "duration": hms(meta.get("duration")),
            "url": f"https://www.youtube.com/watch?v={vid}",
            "type": vtype,
            "language": meta.get("language") or "",
            "manual_subs": ";".join(sorted(meta.get("subtitles") or {})),
            "auto_orig": ";".join(sorted(k for k in (meta.get("automatic_captions") or {}) if k.endswith("-orig"))),
            "view_count": meta.get("view_count") or "",
            "chapters": len(meta.get("chapters") or []),
        })
        if i % 25 == 0:
            print(f"[index] {i}/{len(ids)}", file=sys.stderr)

    rows.sort(key=lambda r: (r["upload_date"], r["video_id"]))
    with INDEX_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"[index] {len(rows)} vidéos -> {INDEX_CSV.relative_to(ROOT)} ; échecs : {len(failed)} {failed[:10]}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
