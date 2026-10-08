# Livre de règles

Trois modèles, par ordre d'importance dans le corpus :

- **A. Unfilled FVG model** (« reversal model ») : le modèle principal, toutes les vidéos de 2026.
- **B. Continuation model** (Candle Projection Theory) : une seule vidéo, 3LrXQDS187Y (2026-09-30).
- **C. Modèle « bougie 9h-10h »** : une seule vidéo, v1rIJOeAv2c (2025-12-24).

La version de référence du modèle A est celle de **mai à octobre 2026** (Tea-SeT3-OU, 6jM0S5_Um9M,
4BLGd9GMo8U, 3LrXQDS187Y, lives de septembre). Les variantes plus anciennes sont dans `evolution.md`,
les conflits dans `contradictions.md`, les paramètres non chiffrés dans `questions.md` (renvois « Qn »).

Statut de chaque règle : **EXPLICITE** · **DÉDUITE** · **DISCRÉTIONNAIRE** · **CONTRADICTOIRE**.

---

## A. Unfilled FVG model

### A.0 Arbre de décision

```
Chaque nouvelle bougie HTF (15 min / 1 h / 4 h) :
│
├─ 1. La bougie qui vient de clôturer = C2 ; la bougie en cours = C3.
│     Un FVG est-il en train de se former entre C1 et C3 ?            (A.2.1)
│     ├─ non → rien.
│     └─ oui → sens du trade = OPPOSÉ au FVG                            (A.2.2)
│               [option] C2 est-elle un displacement ?                  (A.2.4, Q4)
│
├─ 2. Pendant C3 — fenêtre d'ANTICIPATION (W1)                         (A.3.1)
│     t_rem ≤ T_ant  ET  C3 n'a pas clôturé au-delà de C2 (évident)
│     ET prix « loin » de l'extrême de C2                               (A.3.2, Q7)
│     ET gap toujours en formation (C3 n'a pas touché la mèche de C1)
│     ├─ modèle d'entrée LTF valide (A.4) → ENTRÉE ANTICIPÉE
│     └─ sinon → attendre la clôture de C3
│
├─ 3. Clôture de C3 — VALIDATION DU SETUP                               (A.2.3)
│     FVG réel (taille ≥ G_min) ET C3 n'a pas clôturé au-delà de C2 ?
│     ├─ non → setup annulé (une position anticipée garde son stop)    (A.5.8)
│     └─ oui → C4 attendue dans le sens du trade (projection)
│
├─ 4. Pendant C4 — fenêtre W2                                           (A.3.3)
│     [option] manipulation puis flip de l'open de C4                   (A.3.4)
│     ├─ modèle d'entrée LTF valide (A.4) ET R:R 1:1 possible (A.5.4) → ENTRÉE
│     ├─ gap atteint avant toute entrée → setup consommé                (Q19)
│     └─ fin de C4 sans entrée → setup expiré                           (A.7, Q10)
│
└─ 5. En position : objectif dans le gap, stop à 1:1                    (A.5)
      [option] break-even                                               (A.5.7, Q14)
      Une seule position par jour                                       (A.0.2)
```

### A.0 Cadre général

| # | Règle | Statut | Sources |
|---|---|---|---|
| A.0.1 | Instrument : **NQ / MNQ** (futures Nasdaq) | EXPLICITE | « We were trading NQ » [Tea-SeT3-OU @ 0:28:08](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1688s) ; MNQ en live [nxYi6bd9enA @ 0:03:12](https://www.youtube.com/watch?v=nxYi6bd9enA&t=192s) |
| A.0.2 | **Un trade par jour** | EXPLICITE | « focused on taking one trade a day » [6jM0S5_Um9M @ 0:02:56](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=176s) |
| A.0.3 | **R:R 1:1** fixe, sortie totale à l'objectif | EXPLICITE | « I always go for a one-to-one and take out full profits at the unfilled gap » [Tea-SeT3-OU @ 0:18:32](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1112s) ; « a one-to-one risk-to-reward system » [4BLGd9GMo8U @ 0:00:00](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=0s) |
| A.0.4 | **Pas de biais journalier** requis | EXPLICITE | « Scalp model, don't need no daily bias » [Tea-SeT3-OU @ 0:29:10](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1750s) |
| A.0.5 | Sessions : **aucune restriction énoncée** ; trades montrés de 8:30 à 15:00 ET | DÉDUITE | « this can happen during the Asia, New York session, London session » [3LrXQDS187Y @ 0:36:07](https://www.youtube.com/watch?v=3LrXQDS187Y&t=2167s) ; 8:30 [4BLGd9GMo8U @ 0:19:19](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=1159s), 14:58 [Tea-SeT3-OU @ 0:30:02](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1802s) — Q12 |
| A.0.6 | Visée : « base hits », 10 à 35 points | EXPLICITE | « 20 to 35 points » [6jM0S5_Um9M @ 0:01:27](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=87s) ; « 10-15 points » [Tea-SeT3-OU @ 0:19:16](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1156s) |

### A.1 Timeframes

| # | Règle | Statut | Sources |
|---|---|---|---|
| A.1.1 | FVG (HTF) en **15 min ou 1 h** ; **4 h** ajouté en septembre 2026 | EXPLICITE | [Tea-SeT3-OU @ 0:00:37](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=37s) ; « 15minut, the hourly or the 4 hour » [3LrXQDS187Y @ 0:23:07](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1387s) |
| A.1.2 | Entrée (LTF) : **15m→1m, 1h→5m, 4h→15m** (D→1h) | EXPLICITE | [3LrXQDS187Y @ 0:27:59](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1679s) ; [6jM0S5_Um9M @ 0:09:16](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=556s) |
| A.1.3 | Pas de 1 min pour un cadre 1 h / 4 h | EXPLICITE | « those are going to fake you out way way too much » [6jM0S5_Um9M @ 0:09:26](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=566s) |
| A.1.4 | Exceptions : 1h→3m, 15m→2m | CONTRADICTOIRE (avec A.1.2) | [6jM0S5_Um9M @ 0:24:34](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1474s) ; [oSqLOXBP7NY @ 0:11:30](https://www.youtube.com/watch?v=oSqLOXBP7NY&t=690s) — Q13 |

### A.2 Setup HTF

| # | Règle | Statut | Sources |
|---|---|---|---|
| A.2.1 | **FVG** : haussier si `l(C3) > h(C1)`, baissier si `h(C3) < l(C1)` | EXPLICITE | [Tea-SeT3-OU @ 0:00:41](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=41s), [Tea-SeT3-OU @ 0:01:23](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=83s) |
| A.2.2 | **Sens opposé** : FVG haussier → short vers le gap ; FVG baissier → long | EXPLICITE | [Tea-SeT3-OU @ 0:01:53](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=113s) ; « You're using them as an exit » [6jM0S5_Um9M @ 0:08:44](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=524s) |
| A.2.3 | **C3 ne clôture pas au-delà de C2** : haussier `c(C3) < h(C2)` ; baissier `c(C3) > l(C2)` | EXPLICITE | [Tea-SeT3-OU @ 0:02:24](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=144s) ; [4BLGd9GMo8U @ 0:01:24](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=84s) ; [3LrXQDS187Y @ 0:25:28](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1528s) |
| A.2.3b | Forme de C3 : inside bar acceptée **ou** sweep + grande mèche exigés | CONTRADICTOIRE | inside bar [Tea-SeT3-OU @ 0:15:09](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=909s) vs « big up wick » [4BLGd9GMo8U @ 0:02:07](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=127s) — Q3 |
| A.2.4 | **C2 = displacement** | EXPLICITE mais non chiffré → DISCRÉTIONNAIRE | [6jM0S5_Um9M @ 0:09:47](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=587s) ; « not enough displacement » comme motif de refus [Tea-SeT3-OU @ 0:32:00](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1920s) — Q4 |
| A.2.5 | Taille minimale du FVG | non abordée → à fixer | — Q5 |
| A.2.6 | Le gap doit être **non comblé** au moment de l'entrée ; mieux s'il n'a pas encore été touché | DÉDUITE | « if the gap is not entered … yet, it is even better » [nxYi6bd9enA @ 0:07:19](https://www.youtube.com/watch?v=nxYi6bd9enA&t=439s) — Q19 |
| A.2.7 | Confluences non obligatoires : sweep de l'extrême de C2, du London low, du lunch low | DÉDUITE | [4BLGd9GMo8U @ 0:18:05](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=1085s) ; [Tea-SeT3-OU @ 0:24:13](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1453s) ; [Tea-SeT3-OU @ 0:28:51](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1731s) |

### A.3 Timing

| # | Règle | Statut | Sources |
|---|---|---|---|
| A.3.1 | **W1 (anticipation pendant C3)** : entrée possible quand il reste **1 à 4 min** avant la clôture de C3 (15 min) ; **5 à 10 min** en 1 h | EXPLICITE | « one, two, three, maybe four minutes left » [4BLGd9GMo8U @ 0:16:45](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=1005s) ; « 5 to 10 minutes left for that hourly bar to close » [6jM0S5_Um9M @ 0:24:37](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1477s) |
| A.3.1b | **Trop tôt** : 8 min avant (15 min) ; 40 min avant (1 h) | EXPLICITE | [4BLGd9GMo8U @ 0:16:27](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=987s) ; [6jM0S5_Um9M @ 0:04:10](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=250s) ; [6jM0S5_Um9M @ 0:10:40](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=640s) |
| A.3.2 | Pendant W1, le prix doit rester **loin de l'extrême de C2** ; trop près = « gamble » | EXPLICITE, non chiffré | [4BLGd9GMo8U @ 0:24:09](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=1449s) ; « if we're too close, it is a gamble » [6jM0S5_Um9M @ 0:28:14](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1694s) — Q7 |
| A.3.3 | **W2 (pendant C4)** : sans entrée pendant C3, chercher l'entrée pendant C4 | EXPLICITE | « I'm going to require the fourth candle to actually create my entry model » [Tea-SeT3-OU @ 0:16:39](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=999s) ; « any shorts within that next hour » [nxYi6bd9enA @ 0:07:19](https://www.youtube.com/watch?v=nxYi6bd9enA&t=439s) |
| A.3.4 | Dans C4 : attendre la **manipulation** (mèche contre le trade) puis le **flip** de l'open | EXPLICITE comme lecture, DÉDUITE comme condition | [Tea-SeT3-OU @ 0:16:27](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=987s) ; « As soon as it flips below that opening price, I'm super confident » [nxYi6bd9enA @ 0:02:09](https://www.youtube.com/watch?v=nxYi6bd9enA&t=129s) — option, Q6 |
| A.3.5 | Raison du timing : entrer tard dans C3, sinon on risque un R:R négatif | EXPLICITE | « If I don't enter right here, then I could be forced to be in a negative risk to reward scenario » [6jM0S5_Um9M @ 0:07:35](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=455s) |

### A.4 Modèles d'entrée (LTF)

| # | Règle | Statut | Sources |
|---|---|---|---|
| A.4.1 | **IFVG** : un FVG LTF dans le sens contraire au trade, cassé en clôture → entrée dans le sens du trade | EXPLICITE | [Tea-SeT3-OU @ 0:05:13](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=313s) ; [4BLGd9GMo8U @ 0:03:08](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=188s) |
| A.4.2 | **CISD / breaker** : low, high, lower low, higher high (long) ; zone = OB raté devenu breaker | EXPLICITE | [6jM0S5_Um9M @ 0:02:26](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=146s) ; [4BLGd9GMo8U @ 0:08:28](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=508s) |
| A.4.3 | **Order block** (break and retest) | EXPLICITE en mai 2026, **absent** de la liste de juillet 2026 | [Tea-SeT3-OU @ 0:06:00](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=360s) vs [4BLGd9GMo8U @ 0:02:59](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=179s) — option |
| A.4.4 | Les modèles d'entrée **seuls** ne suffisent pas : sans l'alignement HTF ils « wouldn't work » | EXPLICITE | [4BLGd9GMo8U @ 0:08:48](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=528s) ; [6jM0S5_Um9M @ 0:16:47](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1007s) |
| A.4.5 | Type d'ordre : limite sur le pullback de préférence, ou marché à la confirmation près de la clôture HTF | EXPLICITE | « It's way better to wait for a pullback » [3z6qgc66RA8 @ 0:06:00](https://www.youtube.com/watch?v=3z6qgc66RA8&t=360s) ; marché [6jM0S5_Um9M @ 0:11:53](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=713s) — Q9 |
| A.4.6 | **Prediction play** (entrée agressive avant confirmation, stop large) | DISCRÉTIONNAIRE | [6jM0S5_Um9M @ 0:21:26](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1286s) — exclu par défaut |

### A.5 Stop, objectif, gestion

| # | Règle | Statut | Sources |
|---|---|---|---|
| A.5.1 | **Objectif dans le gap** | EXPLICITE | [6jM0S5_Um9M @ 0:05:13](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=313s) |
| A.5.1b | Profondeur : bord proche / « within » / comblement total | CONTRADICTOIRE | « upper portion of that bullish gap » [3LrXQDS187Y @ 0:32:20](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1940s) vs « fill the entirety of that gap » [4BLGd9GMo8U @ 0:02:29](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=149s) — Q1 |
| A.5.2 | **1:1** | EXPLICITE | A.0.3 |
| A.5.3 | Stop : sous/au-dessus de la bougie ou du swing LTF d'entrée (pratique) **ou** à l'extrême de C3 (thèse) ; parfois objectif posé d'abord puis stop à 1:1 | CONTRADICTOIRE | « stop loss right below this candle's low » [4BLGd9GMo8U @ 0:12:01](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=721s) ; « our stop loss, which would be at the high of that third candle » [Tea-SeT3-OU @ 0:03:39](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=219s) ; objectif d'abord [Tea-SeT3-OU @ 0:22:46](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1366s), [4BLGd9GMo8U @ 0:25:13](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=1513s) — Q2 |
| A.5.4 | Si le gap est trop proche pour un 1:1 → pas d'entrée au marché : ordre limite sur retracement (« force an open low ») | EXPLICITE | [Tea-SeT3-OU @ 0:21:15](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1275s) |
| A.5.5 | FVG 1 h à très grand range (> 150 points) : entrée vers 50 % du range et stop large qui survit à un retour à 50 % | EXPLICITE | [6jM0S5_Um9M @ 0:18:30](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1110s) ; [6jM0S5_Um9M @ 0:20:20](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1220s) — Q15 |
| A.5.6 | Pas de partiels, pas de trailing ; ne pas viser plus loin que le gap | EXPLICITE | « Do I need more? No » [4BLGd9GMo8U @ 0:25:13](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=1513s) ; « next fair value » [6jM0S5_Um9M @ 0:27:05](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1625s) |
| A.5.7 | **Break-even / réduction du risque** après une bonne réaction (lives de septembre 2026) | EXPLICITE dans les lives ; déclencheur DISCRÉTIONNAIRE | [nxYi6bd9enA @ 0:02:30](https://www.youtube.com/watch?v=nxYi6bd9enA&t=150s) ; [oSqLOXBP7NY @ 0:03:24](https://www.youtube.com/watch?v=oSqLOXBP7NY&t=204s) — Q14 |
| A.5.8 | Après une entrée anticipée, si C3 clôture finalement au-delà de C2 : on ne coupe pas, on accepte la petite perte au stop | EXPLICITE | « I will take a super small loss » [6jM0S5_Um9M @ 0:07:41](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=461s) |
| A.5.9 | Taille : entrer léger puis renforcer avec les confirmations | EXPLICITE (conseil a posteriori), DISCRÉTIONNAIRE | [6jM0S5_Um9M @ 0:23:06](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1386s) — non retenu |

### A.6 Cas où il NE prend PAS le trade

| # | Filtre | Statut | Sources |
|---|---|---|---|
| A.6.1 | C3 clôture au-delà de C2 → pas de remplissage attendu | EXPLICITE | [4BLGd9GMo8U @ 0:23:25](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=1405s) |
| A.6.2 | Trop tôt dans la bougie HTF | EXPLICITE | A.3.1b |
| A.6.3 | Trop près de l'extrême de C2 | EXPLICITE | A.3.2 |
| A.6.4 | Gap trop proche pour un 1:1, sans retracement | EXPLICITE | A.5.4 |
| A.6.5 | Pas assez de confirmations / de displacement / d'alignement | EXPLICITE, non chiffré | [Tea-SeT3-OU @ 0:32:00](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1920s) |
| A.6.6 | Déjà un trade dans la journée | EXPLICITE | A.0.2 |
| A.6.7 | Marché en range sans displacement | EXPLICITE (oct. 2025) | « how do you want me to locate myself and take a trade inside this shop [chop]? It's impossible » [CsV2m7miTyk @ 0:04:53](https://www.youtube.com/watch?v=CsV2m7miTyk&t=293s) |
| A.6.8 | IFVG formé trop tôt : attendre une seconde confirmation | EXPLICITE | [6jM0S5_Um9M @ 0:21:06](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1266s) |

### A.7 Expiration

| # | Règle | Statut | Sources |
|---|---|---|---|
| A.7.1 | Fenêtre de validité d'une prédiction = **la durée de C4** (15 min, 1 h, 4 h) | EXPLICITE | « Any shorts within this next 15 minutes is a good short. If this was an hourly chart, any short within the next hour » [3LrXQDS187Y @ 0:35:44](https://www.youtube.com/watch?v=3LrXQDS187Y&t=2144s) |
| A.7.2 | Position ouverte au-delà de C4 : pas de règle (un trade a duré ~30 min en 15 min) | non abordée | [6jM0S5_Um9M @ 0:16:25](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=985s) — Q10 |
| A.7.3 | Durée typique : TP en moins de 5 min | EXPLICITE (constat) | « we usually smash take profit within the next 5 minutes » [4BLGd9GMo8U @ 0:26:35](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=1595s) |

---

## B. Continuation model (Candle Projection Theory)

Source unique : 3LrXQDS187Y, de 0:01:26 à 0:22:35.

| # | Règle | Statut | Sources |
|---|---|---|---|
| B.1 | Trouver le **draw on liquidity** avec 3 critères HTF : proximité d'un high/low, PD arrays respectés / cassés / créés, clôture agressive vers le draw | EXPLICITE | [3LrXQDS187Y @ 0:01:51](https://www.youtube.com/watch?v=3LrXQDS187Y&t=111s) ; [3LrXQDS187Y @ 0:02:34](https://www.youtube.com/watch?v=3LrXQDS187Y&t=154s) ; [3LrXQDS187Y @ 0:03:23](https://www.youtube.com/watch?v=3LrXQDS187Y&t=203s) |
| B.2 | Le displacement est le critère le plus important ; la proximité seule ne compte pas | EXPLICITE | [3LrXQDS187Y @ 0:06:16](https://www.youtube.com/watch?v=3LrXQDS187Y&t=376s) ; « If we don't see any closures on the higher time frame close to that high, I do not care » [3LrXQDS187Y @ 0:18:16](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1096s) |
| B.3 | Pas de retournement près d'un swing externe ou de liquidité : « we do not believe in … equal lows or equal highs » | EXPLICITE | [3LrXQDS187Y @ 0:06:41](https://www.youtube.com/watch?v=3LrXQDS187Y&t=401s) |
| B.4 | Projeter la prochaine bougie HTF (lire le HTF comme un graphique 1 min) | EXPLICITE | [3LrXQDS187Y @ 0:11:30](https://www.youtube.com/watch?v=3LrXQDS187Y&t=690s) ; [3LrXQDS187Y @ 0:12:30](https://www.youtube.com/watch?v=3LrXQDS187Y&t=750s) |
| B.5 | Tout passage de l'autre côté de l'open de la bougie projetée = fake-out | EXPLICITE | [3LrXQDS187Y @ 0:12:30](https://www.youtube.com/watch?v=3LrXQDS187Y&t=750s) |
| B.6 | Entrée : attendre l'invalidation du MSS contraire, puis un squeeze level (IFVG / breaker / OB) | EXPLICITE | [3LrXQDS187Y @ 0:13:11](https://www.youtube.com/watch?v=3LrXQDS187Y&t=791s) |
| B.7 | Objectif : le high/low visé | EXPLICITE | [3LrXQDS187Y @ 0:22:18](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1338s) |
| B.8 | Rareté : « multiple hours » d'attente par jour | EXPLICITE | [3LrXQDS187Y @ 0:22:10](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1330s) |
| B.9 | Stop, entrée exacte : réservés au groupe privé | EXPLICITE (non divulgué) | [3LrXQDS187Y @ 0:39:58](https://www.youtube.com/watch?v=3LrXQDS187Y&t=2398s) |
| B.10 | Variante live : jouer la création d'un breaker HTF vers un gap non comblé | EXPLICITE | [oSqLOXBP7NY @ 0:13:20](https://www.youtube.com/watch?v=oSqLOXBP7NY&t=800s) |

---

## C. Modèle « bougie horaire 9h-10h » (ES)

Source unique : v1rIJOeAv2c (2025-12-24). Pas repris ensuite.

| # | Règle | Statut | Sources |
|---|---|---|---|
| C.1 | Biais = couleur de la bougie 1 h **9:00-10:00** ET | EXPLICITE | [v1rIJOeAv2c @ 0:00:58](https://www.youtube.com/watch?v=v1rIJOeAv2c&t=58s) ; [v1rIJOeAv2c @ 0:01:56](https://www.youtube.com/watch?v=v1rIJOeAv2c&t=116s) |
| C.2 | Fenêtre : **10:00-11:00** (« silver bullet hour ») | EXPLICITE | [v1rIJOeAv2c @ 0:01:56](https://www.youtube.com/watch?v=v1rIJOeAv2c&t=116s) |
| C.3 | Tout MSS contre le biais = fake-out (mèche d'une future bougie dans le sens du biais) | EXPLICITE | [v1rIJOeAv2c @ 0:01:47](https://www.youtube.com/watch?v=v1rIJOeAv2c&t=107s) |
| C.4 | Ne pas entrer au MSS ; attendre que ses PD arrays (FVG, OB, breaker) soient cassés, puis entrer sur pullback | EXPLICITE | [v1rIJOeAv2c @ 0:02:30](https://www.youtube.com/watch?v=v1rIJOeAv2c&t=150s) ; [v1rIJOeAv2c @ 0:04:37](https://www.youtube.com/watch?v=v1rIJOeAv2c&t=277s) |
| C.5 | Stop sous le low de la bougie ou du swing ; objectif 1:1 vers le high interne | EXPLICITE | [v1rIJOeAv2c @ 0:05:19](https://www.youtube.com/watch?v=v1rIJOeAv2c&t=319s) |
| C.6 | Instrument : ES | EXPLICITE | [v1rIJOeAv2c @ 0:00:44](https://www.youtube.com/watch?v=v1rIJOeAv2c&t=44s) |
