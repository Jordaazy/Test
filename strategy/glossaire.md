# Glossaire mesurable

Pour chaque concept : **ce qu'il en dit** (cité), puis une **définition mesurable** utilisable en code.
Quand il ne chiffre rien, la définition mesurable est une **PROPOSITION** (marquée comme telle) ; les
valeurs à tester sont dans `questions.md`. Conventions de statut : voir `notes/README.md`.

Notations : bougies OHLC `o, h, l, c` ; `HTF` = timeframe du FVG (15 min, 1 h, 4 h) ; `LTF` = timeframe
d'entrée ; `tick` NQ = 0,25 point ; heures en **heure de New York (ET)**.

---

## 1. Les bougies HTF : C1, C2, C3, C4

> « this gap was created by three candles. This is the first candle, this is the second, and this is the third » [Tea-SeT3-OU @ 0:02:17](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=137s) ; « When this third candle closes, a fourth candle will open » [Tea-SeT3-OU @ 0:03:27](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=207s).

**Mesurable** : quatre bougies HTF consécutives `C1, C2, C3, C4` sur la grille d'horloge du HTF :
- 15 min : bougies qui ouvrent à :00, :15, :30, :45 (ex. bougie de « 10:30 » [Tea-SeT3-OU @ 0:09:27](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=567s)) ;
- 1 h : bougies qui ouvrent à l'heure pile (ex. « 9 to 10 a.m. candle » [v1rIJOeAv2c @ 0:01:56](https://www.youtube.com/watch?v=v1rIJOeAv2c&t=116s), « 8:00 a.m. 1-hour candle » [6jM0S5_Um9M @ 0:17:10](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1030s)) ;
- 4 h : ancrage non précisé → **PROPOSITION** : grille de TradingView pour les futures CME (bougies de 18:00, 22:00, 02:00, 06:00, 10:00, 14:00 ET). Voir Q16.

## 2. Fair Value Gap (FVG)

> Haussier : « the up wick of the first candle doesn't touch the down wick of the third » [Tea-SeT3-OU @ 0:00:41](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=41s). Baissier : « the first candle's down wick doesn't touch the third candle's up wick » [Tea-SeT3-OU @ 0:01:23](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=83s).

**Mesurable** (EXPLICITE) :
- FVG **haussier** si `l(C3) > h(C1)` ; zone = `[h(C1), l(C3)]`.
- FVG **baissier** si `h(C3) < l(C1)` ; zone = `[h(C3), l(C1)]`.
- Taille `G = l(C3) − h(C1)` (haussier) ou `l(C1) − h(C3)` (baissier).
- Taille minimale : **jamais donnée** → PROPOSITION `G ≥ G_min`, avec `G_min` dans {1 tick, 2, 5 points} (Q5).

Pendant que C3 se forme, le gap est « en formation » tant que C3 n'a pas touché la mèche de C1
(« if I don't trade back towards 529, which is that first candle's down wick, then I'm going to have a gap above me » [4BLGd9GMo8U @ 0:09:55](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=595s)).

## 3. Unfilled FVG (gap non comblé)

> « this area will act as a magnet, and you will want to trade back towards that gap as soon as possible » [4BLGd9GMo8U @ 0:01:00](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=60s) ; « I treat this gap as a magnet. So as my drawn liquidity » [nxYi6bd9enA @ 0:04:59](https://www.youtube.com/watch?v=nxYi6bd9enA&t=299s).

**Mesurable** : un FVG est *unfilled* à l'instant `t` si aucun prix entre la clôture de C3 et `t` n'est entré
dans la zone (haussier : `min(l) > l(C3)` ; baissier : `max(h) < h(C3)`).
Le **sens du trade est opposé au FVG** : FVG haussier → short vers le gap ; FVG baissier → long
(« when we create a bearish fair value gap I am bullish and when we create a bullish fair value gap, I am bearish » [Tea-SeT3-OU @ 0:01:53](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=113s)) — EXPLICITE.

## 4. Niveaux de l'objectif dans le gap

Il emploie trois formulations (voir `contradictions.md` C2) :
- **bord proche** : « this internal low which is the upper portion of that bullish gap » [3LrXQDS187Y @ 0:32:20](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1940s) → haussier : `l(C3)` ; baissier : `h(C3)` ;
- « within » : « take profit at a one-to-one risk-to-reward back within the unfilled fair value gap » [6jM0S5_Um9M @ 0:05:13](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=313s) ;
- **comblement total** : « fill the entirety of that gap » [4BLGd9GMo8U @ 0:02:29](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=149s) → haussier : `h(C1)` ; baissier : `l(C1)`.

**Mesurable** : `TP_level = bord_proche ± d × G` avec `d ∈ [0 ; 1]` (0 = bord proche, 0,5 = milieu, 1 = comblement). PROPOSITION par défaut : `d = 0` (Q1).

## 5. Displacement

> « When I see a displacement candle on the second candle, I know I have a potential unfilled fair value gap scenario » [6jM0S5_Um9M @ 0:09:47](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=587s) ; « aggressive candle closures which we can call displacement » [3LrXQDS187Y @ 0:03:23](https://www.youtube.com/watch?v=3LrXQDS187Y&t=203s).

**Jamais chiffré**. PROPOSITION : C2 est un displacement si `|c(C2) − o(C2)| ≥ k × ATR14(HTF)` et
`|c − o| / (h − l) ≥ r`, avec `k` dans {0 (désactivé) ; 1,0 ; 1,5} et `r` dans {0 ; 0,5 ; 0,6} (Q4).
NB : l'existence d'un FVG suppose déjà une C2 ample ; ce filtre est donc optionnel.

## 6. Étape 2 — C3 « fails to close » / « closes back inside C2 »

> « the third candle right here that created the gap failing to close above the second candle's high » [Tea-SeT3-OU @ 0:02:24](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=144s) ; « I need to see the candle number three close back inside candle number two » [4BLGd9GMo8U @ 0:01:24](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=84s) ; « It could close back bearish. It could close back bullish, but I need to see that we failed to close above candle number two » [3LrXQDS187Y @ 0:25:28](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1528s).

**Mesurable** (EXPLICITE) :
- FVG haussier : `c(C3) < h(C2)` ;
- FVG baissier : `c(C3) > l(C2)`.

Variantes à tester (Q3) :
- **(a)** la règle seule — une inside bar est valide (« it is called an inside bar candle. So, yes, the second step is actually ticked » [Tea-SeT3-OU @ 0:15:09](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=909s)) ;
- **(b)** + **sweep** de l'extrême de C2 (`h(C3) > h(C2)`, resp. `l(C3) < l(C2)`), comme dans la plupart des exemples (« buy-side liquidity sweep … this 15 minute bar's high getting swept by the third candle » [4BLGd9GMo8U @ 0:18:05](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=1085s)) ;
- **(c)** + **mèche** dominante : `(h(C3) − max(o,c)(C3)) / (h − l)(C3) ≥ w` (« form a big up wick » [4BLGd9GMo8U @ 0:02:07](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=127s)).

## 7. Projection de C4 et profil PO3 (OHLC / OLHC)

> « When we create a bullish gap, I am projecting a bearish C4 candle » [3LrXQDS187Y @ 0:26:10](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1570s) ; « open high flip below the opening price low close » [3LrXQDS187Y @ 0:29:04](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1744s).

**Mesurable** : biais de C4 = opposé du FVG. Profil baissier attendu (OHLC) : C4 dépasse d'abord `o(C4)`
vers le haut (**manipulation**), puis repasse sous `o(C4)` (**flip**), puis atteint l'objectif.
- **Flip** : premier passage de `c(LTF) < o(C4)` après `h(C4) > o(C4)` (« We flip back below the opening price right there, showing me a concept called the flip » [Tea-SeT3-OU @ 0:17:08](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1028s)) — EXPLICITE.

## 8. Temps restant (« cues of time »)

> « there is 8 minutes left … it is too early » [4BLGd9GMo8U @ 0:16:27](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=987s) ; « one, two, three, maybe four minutes left … then I'm going to be certain » [4BLGd9GMo8U @ 0:16:45](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=1005s).

**Mesurable** : `t_rem = heure de clôture de C3 − heure courante`.
Fenêtre d'anticipation (**W1**) : `t_rem ≤ T_ant`, avec `T_ant = 4 min` en 15 min (EXPLICITE) et
5 à 10 min en 1 h (« 5 to 10 minutes left for that hourly bar to close » [6jM0S5_Um9M @ 0:24:37](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1477s)).
Fenêtre **W2** : pendant C4 (« any shorts within that next hour for me would have been a good short » [nxYi6bd9enA @ 0:07:19](https://www.youtube.com/watch?v=nxYi6bd9enA&t=439s)).

## 9. Alignement des timeframes

> « If I want to trade a 15-minute … gap, then I need to answer on the one minute. If I want to trade an hourly gap, then I need to trade on the M5 … 4hour gap … 15-minute entry … daily gap … an hourly entry » [3LrXQDS187Y @ 0:27:59](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1679s).

**Mesurable** (EXPLICITE) : `LTF = {15m→1m, 1h→5m, 4h→15m, D→1h}`. Exceptions observées : 1h→3m
[6jM0S5_Um9M @ 0:24:34](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1474s), 15m→2m [oSqLOXBP7NY @ 0:11:30](https://www.youtube.com/watch?v=oSqLOXBP7NY&t=690s) (Q13).

## 10. Swings et cassure de structure (LTF)

Il décrit tout en séquences de swings : « high, low, higher high, lower low » [Tea-SeT3-OU @ 0:04:24](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=264s).

**Mesurable** (PROPOSITION) : swing high = bougie dont le `h` dépasse les `n` bougies de chaque côté
(fractal), `n` dans {1, 2, 3} ; **BOS** = clôture au-delà du dernier swing opposé (Q8).

## 11. Modèles d'entrée LTF

### 11.1 Breaker block / CISD (version 2026)

> « change in the state of delivery or what we call a breaker block. So, we would need a low, high, lower low, higher high » [6jM0S5_Um9M @ 0:02:26](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=146s) ; « that failed order block, which changes into a breaker block, as an area of support » [4BLGd9GMo8U @ 0:08:28](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=508s).

**Mesurable** (long ; inverser pour un short) : swings `L1 < H1`, puis `L2 < L1`, puis une clôture `> H1` (BOS).
Zone du breaker = range de la **dernière bougie haussière (c > o) avant la jambe H1→L2** (l'order block baissier « raté »).
Entrée : retour dans la zone (limite au bord haut de la zone) ou au marché à la clôture du BOS.

### 11.2 CISD (version 2025, par l'opening price)

> « you break above the opening price of the series of down close candles that created the sweep » [CsV2m7miTyk @ 0:10:26](https://www.youtube.com/watch?v=CsV2m7miTyk&t=626s).

**Mesurable** (long) : série maximale de bougies LTF baissières consécutives se terminant au plus bas du
sweep ; niveau CISD = `o` de la première bougie de la série ; déclenchement = première clôture `> niveau`.
Entrée : ordre limite au niveau CISD (« long limit order just right here in the change in the state of delivery » [CsV2m7miTyk @ 0:11:17](https://www.youtube.com/watch?v=CsV2m7miTyk&t=677s)).

### 11.3 IFVG (« 180 »)

> « price pushes very aggressively on one side, creating a bullish fair value gap … if you're bearish though … you will disrespect that 1-minute structure » [4BLGd9GMo8U @ 0:03:08](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=188s) ; « we want to see it get disrespected by one or two candles » [Tea-SeT3-OU @ 0:05:13](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=313s).

**Mesurable** (short) : FVG **haussier** LTF (règle §2 en LTF) formé dans la jambe de C3/C4 ; il est *inversé*
quand une bougie LTF clôture **sous le bas de sa zone**. Entrée au marché à cette clôture, ou en limite sur le
retour dans la zone. Plusieurs FVG empilés : « we actually closed above those gaps » [Tea-SeT3-OU @ 0:20:30](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1230s) →
PROPOSITION : prendre le **dernier** FVG formé (« this was the last fair value gap within the range » [4BLGd9GMo8U @ 0:20:53](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=1253s)).

### 11.4 Order block (« break and retest »)

> « the order block, which is a regular break and retest » [Tea-SeT3-OU @ 0:06:00](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=360s) ; « that last down move before the break of structure to the upside is what I'll use as my order block » [Tea-SeT3-OU @ 0:29:35](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1775s).

**Mesurable** (long) : swings `L1, H1, L2 > L1`, puis clôture `> H1` ; OB = dernière bougie baissière avant
la jambe L2→BOS ; entrée en limite au haut de l'OB. **Retiré** de la liste en juillet 2026 (`evolution.md`).

## 12. Sweep et liquidités nommées

> « We swept London low. So, I'm bullish » [3z6qgc66RA8 @ 0:01:44](https://www.youtube.com/watch?v=3z6qgc66RA8&t=104s) ; « we're sweeping the lunch low » [Tea-SeT3-OU @ 0:28:51](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1731s).

**Mesurable** : sweep d'un niveau `X` = `l < X` puis clôture `> X` (pour un low). Niveaux :
low/high de C2 (cœur du modèle), London (PROPOSITION 02:00-05:00 ET), lunch (PROPOSITION 12:00-13:00 ET),
high/low de la veille. Confluence seulement à partir de 2026 (Q22).

## 13. SMT

> « ES swept this internal low while ENQ [NQ] didn't. Okay, created a higher low » [3z6qgc66RA8 @ 0:02:16](https://www.youtube.com/watch?v=3z6qgc66RA8&t=136s).

**Mesurable** : sur la fenêtre du sweep, `l_ES < l_ES,préc` et `l_NQ ≥ l_NQ,préc`. Seulement en octobre 2025 ; non retenu par défaut.

## 14. Risque / rendement et gestion

- **1:1** : « I risk the same amount as I'm willing to make » [4BLGd9GMo8U @ 0:00:00](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=0s) → `|TP − entrée| = |entrée − SL|`.
- **Un trade par jour** : « focused on taking one trade a day » [6jM0S5_Um9M @ 0:02:56](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=176s).
- **Break-even** (lives de septembre 2026 seulement) : « Going to go break even very soon » [nxYi6bd9enA @ 0:02:30](https://www.youtube.com/watch?v=nxYi6bd9enA&t=150s) ; « I will put it below this swing low or even break even » [oSqLOXBP7NY @ 0:03:24](https://www.youtube.com/watch?v=oSqLOXBP7NY&t=204s) → PROPOSITION : stop à l'entrée après `+x R`, `x` dans {0,5 ; 0,7} ou désactivé (Q14).

## 15. Modèle de continuation : draw on liquidity et Candle Projection Theory

> Critères : « the closer we get to a high … the more chances we have of sweeping it » [3LrXQDS187Y @ 0:01:51](https://www.youtube.com/watch?v=3LrXQDS187Y&t=111s) ; « what is being respected, disrespected and created on the higher time frame » [3LrXQDS187Y @ 0:02:34](https://www.youtube.com/watch?v=3LrXQDS187Y&t=154s) ; « aggressive candle closures which we can call displacement » [3LrXQDS187Y @ 0:03:23](https://www.youtube.com/watch?v=3LrXQDS187Y&t=203s).

**Mesurable** (PROPOSITION, automatisable en partie) :
- proximité : distance au swing HTF le plus proche dans le sens du draw `≤ p × ATR14(HTF)` ;
- PD arrays : dernier FVG HTF dans le sens du draw respecté **et** dernier FVG opposé inversé ;
- displacement : dernière bougie HTF clôturée vers le draw, corps `≥ k × ATR` ;
- projection : la bougie HTF suivante va vers le draw ; tout passage de l'autre côté de son open est un
  fake-out (« anything that occurs below that opening price is a fake out » [3LrXQDS187Y @ 0:12:30](https://www.youtube.com/watch?v=3LrXQDS187Y&t=750s)) ;
- entrée : squeeze level LTF (IFVG / breaker / OB) après le fake-out ; objectif = le swing visé.

## 16. Modèle « bougie horaire 9h-10h » (décembre 2025)

> « If the 9 to 10 a.m. candle closes bullish, then I am going to be bullish for the whole silver bullet hour, which is from 10 to 11 » [v1rIJOeAv2c @ 0:01:56](https://www.youtube.com/watch?v=v1rIJOeAv2c&t=116s).

**Mesurable** (EXPLICITE sauf le choix du swing) : biais = signe de `c − o` de la bougie 1 h de 9:00 ET ;
fenêtre 10:00-11:00 ET ; attendre sur le 1 min un MSS contre le biais (clôture sous le dernier swing low
pour un biais haussier), puis l'invalidation de ses PD arrays (clôture au-dessus du dernier FVG ou OB
baissier) → long ; stop sous le low de la jambe ; objectif 1:1 / le high interne.
Instrument : ES [v1rIJOeAv2c @ 0:00:44](https://www.youtube.com/watch?v=v1rIJOeAv2c&t=44s).
