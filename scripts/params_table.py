#!/usr/bin/env python3
"""Génère strategy/parametres.md à partir de strategy/parametres.json (source unique des paramètres).

  python3 scripts/params_table.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "strategy" / "parametres.json"
OUT = ROOT / "strategy" / "parametres.md"


def fmt(v):
    if isinstance(v, (list, dict)):
        return "`" + json.dumps(v, ensure_ascii=False) + "`"
    if v is None:
        return "`null`"
    return f"`{v}`"


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    lines = ["# Paramètres (généré depuis `parametres.json`, ne pas éditer à la main)", "",
             data["_doc"], ""]
    for groupe, params in data["groupes"].items():
        lines += [f"## {groupe}", "", "| Paramètre | Défaut | Plage de test | Statut | Q | Note |",
                  "|---|---|---|---|---|---|"]
        for p in params:
            test = " · ".join(fmt(t) for t in p["test"])
            lines.append(f"| `{p['nom']}` | {fmt(p['default'])} | {test} | {p['statut']} | {p['q']} | {p.get('note', '')} |")
        lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[params] {sum(len(v) for v in data['groupes'].values())} paramètres -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
