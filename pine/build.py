#!/usr/bin/env python3
"""Assemble les deux scripts Pine v6 à partir de la logique commune (pine/core.pine).

  python3 pine/build.py   ->   pine/amas_ufvg_indicator.pine, pine/amas_ufvg_strategy.pine
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORE = (HERE / "core.pine").read_text(encoding="utf-8")

BANNER = """// Modèle « Unfilled FVG » d'AMAS PFT, formalisé à partir de ses vidéos (dépôt Jordaazy/Test, branche
// claude/amas-pft-phase0 : strategy/regles.md, strategy/pseudocode.md). Généré par pine/build.py.
// Usage éducatif ; aucune garantie de résultat.
"""

IND_HEAD = """//@version=6
indicator("AMAS PFT — Unfilled FVG", shorttitle="UFVG", overlay=true, max_bars_back=1000,
     max_boxes_count=300, max_lines_count=500, max_labels_count=500)
""" + BANNER

STRAT_HEAD = """//@version=6
strategy("AMAS PFT — Unfilled FVG (stratégie)", shorttitle="UFVG strat", overlay=true, max_bars_back=1000,
     process_orders_on_close=false, default_qty_type=strategy.fixed, default_qty_value=1,
     initial_capital=50000, commission_type=strategy.commission.cash_per_contract, commission_value=2.25,
     slippage=1, max_lines_count=500, max_labels_count=500)
""" + BANNER

COMMON_DRAW = """
// ───────── Affichage commun
grpV = "5. Affichage"
showGap = input.bool(true, "Zone du gap armé", group=grpV)
showWin = input.bool(true, "Fond des fenêtres W1 / W2", group=grpV)
colL = input.color(color.new(color.teal, 0), "Long", group=grpV)
colS = input.color(color.new(color.red, 0), "Short", group=grpV)

if armedNow and showGap
    box.new(gLeft, gTop, aC4Open + htfMs, gBot, xloc=xloc.bar_time, border_color=color.new(color.gray, 40),
         bgcolor=aBull ? color.new(color.red, 88) : color.new(color.teal, 88), text=aBull ? "UFVG ↓" : "UFVG ↑",
         text_size=size.tiny, text_color=color.gray)

w1Live = canW1 and ((cur.l - b1.h >= gapMin and close < b2.h) or (b1.l - cur.h >= gapMin and close > b2.l))
w2Live = inC4 and not isLast and ((aBull and not aConsBull) or (aBear and not aConsBear))
bgcolor(showWin and w1Live ? color.new(color.orange, 88) : showWin and w2Live ? color.new(color.blue, 90) : na)
"""

IND_FOOT = COMMON_DRAW + """
// ───────── Position virtuelle : n'affiche que les trades que la stratégie prendrait
var int   vDir = 0
var float vE = na
var float vSL = na
var float vTP = na
var int   vForced = na
var bool  vPendMkt = false
var bool  vPendLim = false
var float vLimPx = na
var int   vExpire = na
var int   vDay = na
var int   vCount = 0
var int   pDir = 0
var float pSL = na
var float pTP = na
var int   pForced = na
var float vR = na

if tradingDay != vDay
    vDay := tradingDay
    vCount := 0

// 0. ordre au marché décidé à la bougie précédente : rempli à l'ouverture
if vPendMkt
    vPendMkt := false
    vDir := pDir
    vE := open
    vSL := pSL
    vTP := pTP
    vForced := pForced
    vR := math.abs(vE - vSL)
    vCount += 1
// 1. ordre limite
if vPendLim
    if time_close > vExpire
        vPendLim := false
    else if (pDir > 0 and low <= vLimPx - syminfo.mintick) or (pDir < 0 and high >= vLimPx + syminfo.mintick)
        vPendLim := false
        vDir := pDir
        vE := vLimPx
        vSL := pSL
        vTP := pTP
        vForced := pForced
        vR := math.abs(vE - vSL)
        vCount += 1
// 2. gestion
string vExit = ""
if vDir != 0
    bool hitSL = vDir > 0 ? low <= vSL : high >= vSL
    bool hitTP = vDir > 0 ? high >= vTP + syminfo.mintick : low <= vTP - syminfo.mintick
    if hitSL
        vExit := "SL"
    else if hitTP
        vExit := "TP"
    else if not na(vForced) and time_close >= vForced
        vExit := "temps"
    if vExit != ""
        label.new(time, vExit == "SL" ? vSL : vExit == "TP" ? vTP : close, vExit, xloc=xloc.bar_time,
             style=label.style_label_left, size=size.tiny, textcolor=color.white,
             color=vExit == "TP" ? color.new(color.green, 20) : vExit == "SL" ? color.new(color.maroon, 20) : color.new(color.gray, 20))
        vDir := 0

// 3. nouveau signal
taken = sig and vDir == 0 and not vPendMkt and not vPendLim and vCount < maxPerDay
if taken
    pDir := sDir
    pSL := sSL
    pTP := sTP
    pForced := sForced
    if sLimit
        vPendLim := true
        vLimPx := sEntry
        vExpire := sExpire
    else
        vPendMkt := true
    int xEnd = na(sForced) ? time + 30 * 60000 : sForced
    color c = sDir > 0 ? colL : colS
    line.new(time, sEntry, xEnd, sEntry, xloc=xloc.bar_time, color=c, width=2)
    line.new(time, sSL, xEnd, sSL, xloc=xloc.bar_time, color=color.new(color.maroon, 0), style=line.style_dashed)
    line.new(time, sTP, xEnd, sTP, xloc=xloc.bar_time, color=color.new(color.green, 0), style=line.style_dashed)
    label.new(time, sEntry, (sDir > 0 ? "▲ " : "▼ ") + sModel + " " + sWin + (sLimit ? " (limite)" : ""),
         xloc=xloc.bar_time, style=sDir > 0 ? label.style_label_up : label.style_label_down, size=size.small,
         color=c, textcolor=color.white,
         tooltip="Entrée " + str.tostring(sEntry) + "\\nSL " + str.tostring(sSL) + "\\nTP " + str.tostring(sTP))

plotshape(sig and not taken, "Signal ignoré (position / plafond)", shape.circle, location.abovebar,
     color.new(color.gray, 40), size=size.tiny)
alertcondition(taken and sDir > 0, "UFVG long", "UFVG long : entrée {{close}}")
alertcondition(taken and sDir < 0, "UFVG short", "UFVG short : entrée {{close}}")

// ───────── Tableau d'état
var table tb = table.new(position.top_right, 2, 6, bgcolor=color.new(color.black, 80), border_width=1)
if barstate.islast
    string st = aBull and not aConsBull ? "armé ↓ (C4)" : aBear and not aConsBear ? "armé ↑ (C4)" : w1Live ? "en formation (W1)" : "—"
    table.cell(tb, 0, 0, "HTF", text_color=color.white, text_size=size.small)
    table.cell(tb, 1, 0, htf + " min", text_color=color.white, text_size=size.small)
    table.cell(tb, 0, 1, "Reste (min)", text_color=color.white, text_size=size.small)
    table.cell(tb, 1, 1, str.tostring(tRem), text_color=color.white, text_size=size.small)
    table.cell(tb, 0, 2, "Setup", text_color=color.white, text_size=size.small)
    table.cell(tb, 1, 2, st, text_color=color.white, text_size=size.small)
    table.cell(tb, 0, 3, "Objectif armé", text_color=color.white, text_size=size.small)
    table.cell(tb, 1, 3, aBull ? str.tostring(aTpBull) : aBear ? str.tostring(aTpBear) : "—", text_color=color.white, text_size=size.small)
    table.cell(tb, 0, 4, "Trades du jour", text_color=color.white, text_size=size.small)
    table.cell(tb, 1, 4, str.tostring(vCount) + " / " + str.tostring(maxPerDay), text_color=color.white, text_size=size.small)
    table.cell(tb, 0, 5, "Session", text_color=color.white, text_size=size.small)
    table.cell(tb, 1, 5, inSess ? "ouverte" : "fermée", text_color=color.white, text_size=size.small)
"""

STRAT_FOOT = COMMON_DRAW + """
// ───────── Ordres
var int  dayKey = na
var int  dayCount = 0
var int  posForced = na
var int  pendExpire = na
var int  pendForced = na
if tradingDay != dayKey
    dayKey := tradingDay
    dayCount := 0

opened = strategy.position_size != 0 and strategy.position_size[1] == 0
if opened
    dayCount += 1
    posForced := pendForced

// ordre limite non rempli à l'expiration
if strategy.position_size == 0 and not na(pendExpire) and time_close >= pendExpire
    strategy.cancel("UFVG")
    pendExpire := na

// sortie forcée
if strategy.position_size != 0 and not na(posForced) and time_close >= posForced
    strategy.close_all(comment="temps")

flat = strategy.position_size == 0 and na(pendExpire)
if sig and flat and dayCount < maxPerDay
    dirStr = sDir > 0 ? strategy.long : strategy.short
    if sLimit
        strategy.entry("UFVG", dirStr, limit=sEntry, comment=sModel + " " + sWin)
        pendExpire := sExpire
    else
        strategy.entry("UFVG", dirStr, comment=sModel + " " + sWin)
    strategy.exit("UFVG sortie", from_entry="UFVG", stop=sSL, limit=sTP)
    pendForced := sForced
    alert((sDir > 0 ? "UFVG long " : "UFVG short ") + sModel + " " + sWin + " SL " + str.tostring(sSL) + " TP " + str.tostring(sTP), alert.freq_once_per_bar_close)
if opened
    pendExpire := na
"""


def main():
    (HERE / "amas_ufvg_indicator.pine").write_text(IND_HEAD + "\n" + CORE + IND_FOOT, encoding="utf-8")
    (HERE / "amas_ufvg_strategy.pine").write_text(STRAT_HEAD + "\n" + CORE + STRAT_FOOT, encoding="utf-8")
    for f in ("amas_ufvg_indicator.pine", "amas_ufvg_strategy.pine"):
        n = len((HERE / f).read_text(encoding="utf-8").splitlines())
        print(f"[pine] {f} : {n} lignes")


if __name__ == "__main__":
    main()
