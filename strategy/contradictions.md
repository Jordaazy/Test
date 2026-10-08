# Contradictions entre vidéos (et à l'intérieur d'une même vidéo)

Pour chacune : ce qui s'oppose, l'arbitrage proposé pour le code, et la question associée dans `questions.md`.

## C1 — Placement du stop

| Position | Sources |
|---|---|
| Extrême de **C3** (high pour un short) : énoncé de la thèse | « hit our stop loss, which would be at the high of that third candle on the 15-minute or the hourly chart » [Tea-SeT3-OU @ 0:03:39](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=219s) ; « below 716, which is the low of that 15, I will take a small loss » [4BLGd9GMo8U @ 0:21:40](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=1300s) |
| **Bougie / swing LTF** de l'entrée (la majorité des trades) | « stop loss right below this candle's low » [4BLGd9GMo8U @ 0:12:01](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=721s), [6jM0S5_Um9M @ 0:05:13](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=313s) ; « below this internal low » [Tea-SeT3-OU @ 0:26:23](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1583s) |
| Calculé à **1:1 depuis l'objectif** | [Tea-SeT3-OU @ 0:22:46](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1366s) ; [4BLGd9GMo8U @ 0:25:13](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=1513s) ; « if my target is 4.1, I will have my stop loss also being 4.1 » [6jM0S5_Um9M @ 0:19:16](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1156s) |
| **Large**, puis BE (lives) | [nxYi6bd9enA @ 0:13:08](https://www.youtube.com/watch?v=nxYi6bd9enA&t=788s) ; [oSqLOXBP7NY @ 0:12:53](https://www.youtube.com/watch?v=oSqLOXBP7NY&t=773s) |

**Arbitrage proposé** : trois modes paramétrés (`TP-first` par défaut, `structure`, `C3-extreme`) — Q2.

## C2 — Profondeur de l'objectif

| Position | Sources |
|---|---|
| Bord proche du gap | « this internal low which is the upper portion of that bullish gap » [3LrXQDS187Y @ 0:32:20](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1940s) |
| « Within » | [6jM0S5_Um9M @ 0:05:13](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=313s) ; [4BLGd9GMo8U @ 0:12:01](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=721s) |
| Comblement total | « fill the entirety of that gap » [4BLGd9GMo8U @ 0:02:29](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=149s) ; [nxYi6bd9enA @ 0:10:33](https://www.youtube.com/watch?v=nxYi6bd9enA&t=633s) |
| 1:1 prioritaire vs gap prioritaire | « Is the one to one risk toward [reward] extremely important? No » [CsV2m7miTyk @ 0:10:55](https://www.youtube.com/watch?v=CsV2m7miTyk&t=655s) vs « I always go for a one-to-one » [Tea-SeT3-OU @ 0:18:32](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1112s) |

**Arbitrage proposé** : objectif = bord proche + `d × G`, `d = 0` par défaut, `d` de 0 à 1 en test de robustesse — Q1.

## C3 — Forme exigée pour C3

| Position | Sources |
|---|---|
| Inside bar acceptée | [Tea-SeT3-OU @ 0:15:09](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=909s) |
| Sweep + grande mèche | « close back within the range and form a big up wick » [4BLGd9GMo8U @ 0:02:07](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=127s) ; « sweeps the previous candle's high, closes back within the range bearish with a super large up wick » [oSqLOXBP7NY @ 0:08:46](https://www.youtube.com/watch?v=oSqLOXBP7NY&t=526s) |
| Couleur indifférente | « It could close back bearish. It could close back bullish » [3LrXQDS187Y @ 0:25:28](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1528s) |

**Arbitrage proposé** : règle minimale `c(C3) < h(C2)` par défaut ; variantes « sweep obligatoire » et « mèche ≥ w » — Q3.

## C4 — Liste des modèles d'entrée

« This is the only entry models that I use » (breaker, IFVG, OB) [Tea-SeT3-OU @ 0:06:23](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=383s) → seulement IFVG et CISD
[4BLGd9GMo8U @ 0:02:59](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=179s) → OB de nouveau cité en live [nxYi6bd9enA @ 0:11:53](https://www.youtube.com/watch?v=nxYi6bd9enA&t=713s).
**Arbitrage proposé** : IFVG + CISD/breaker par défaut, OB en option — Q8.

## C5 — Alignement des timeframes

« I will not be looking for a 1-minute entry if my framework is being applied on … an hourly » [6jM0S5_Um9M @ 0:09:26](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=566s)
vs l'entrée en 3 min sur un FVG 1 h dans la même vidéo [6jM0S5_Um9M @ 0:24:34](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1474s) et la lecture en 2 min d'un FVG 15 min [oSqLOXBP7NY @ 0:11:30](https://www.youtube.com/watch?v=oSqLOXBP7NY&t=690s).
**Arbitrage proposé** : table stricte par défaut ; LTF alternatif en test — Q13.

## C6 — Biais : contexte HTF, puis aucun, puis continuation

- V0 : le contexte daily / 4 h conditionne l'entrée [CsV2m7miTyk @ 0:02:04](https://www.youtube.com/watch?v=CsV2m7miTyk&t=124s).
- V1 : « don't need no daily bias » [Tea-SeT3-OU @ 0:29:10](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1750s).
- V3 (continuation) : « we do not believe in … equal lows or equal highs » près d'un swing externe [3LrXQDS187Y @ 0:06:41](https://www.youtube.com/watch?v=3LrXQDS187Y&t=401s), alors que le modèle reversal parie justement sur une C3 qui rejette après avoir balayé l'extrême de C2.

**Arbitrage proposé** : coder le modèle A **sans** filtre de contexte (version de référence), puis tester un filtre
« pas de reversal si un swing HTF non pris est à moins de X points dans le sens de C2 » comme approximation du
modèle B — Q20.

## C7 — Fréquence

« one trade a day » [6jM0S5_Um9M @ 0:02:56](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=176s) vs revues de 3 à 5 opportunités par jour (ex. 3z6qgc66RA8). Les revues
sont a posteriori, ce n'est donc pas une contradiction stricte.
**Arbitrage proposé** : 1 trade par jour par défaut, 2-3 en test — Q11.

## C8 — Moment de l'entrée

Tard dans C3, 1 à 4 min avant la clôture [4BLGd9GMo8U @ 0:16:45](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=1005s) vs pendant toute la durée de C4 (« any shorts
within that next hour » [nxYi6bd9enA @ 0:07:19](https://www.youtube.com/watch?v=nxYi6bd9enA&t=439s)). Les deux coexistent (« within that third candle printing … then
… when the fourth candle is going to open » [Tea-SeT3-OU @ 0:08:48](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=528s)).
**Arbitrage proposé** : W1 et W2 activables séparément — Q6.

## C9 — « Mechanical » contre discrétion

« it's mechanical … I don't trade with discretion, which is other words for gambling » [4BLGd9GMo8U @ 0:00:20](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=20s)
vs « my stop loss is pretty mental » [Tea-SeT3-OU @ 0:26:44](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1604s), prediction plays [6jM0S5_Um9M @ 0:21:26](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1286s), sélection
au jugé [Tea-SeT3-OU @ 0:32:00](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1920s), short refusé sans raison [oSqLOXBP7NY @ 0:15:56](https://www.youtube.com/watch?v=oSqLOXBP7NY&t=956s).
**Conséquence** : le backtest mesurera la version mécanique, qui peut différer de ses résultats réels.

## C10 — Statistique des retournements

« full-on perfect reversal candles they only happen between 30 to 35% of the time » [3LrXQDS187Y @ 0:15:01](https://www.youtube.com/watch?v=3LrXQDS187Y&t=901s)
(et « around 35% of the time » [v1rIJOeAv2c @ 0:01:23](https://www.youtube.com/watch?v=v1rIJOeAv2c&t=83s)) : chiffre avancé pour **rejeter** les reversals, alors que
le modèle A est présenté comme son « reversal pattern » [nxYi6bd9enA @ 0:03:32](https://www.youtube.com/watch?v=nxYi6bd9enA&t=212s). Le retour dans le gap n'est pas
forcément un retournement complet, mais le chiffre est à mesurer dans le backtest.
