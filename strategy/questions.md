# Questions ouvertes et propositions de formalisation

Chaque point flou, discrétionnaire ou contradictoire reçoit :
- ce qu'il en dit (sources) ;
- une **valeur par défaut** proposée, utilisée en Phase 3-4 sauf décision contraire ;
- une **plage de test** de robustesse (on cherche des zones stables, pas l'optimum) ;
- le degré d'automatisation : **100 %**, **partiel** ou **non**.

Les valeurs par défaut suivent en priorité la version la plus récente (V2-V3, juillet-octobre 2026).

---

## Setup HTF

### Q1 — Profondeur de l'objectif dans le gap
- **Il dit** : « upper portion of that bullish gap » [3LrXQDS187Y @ 0:32:20](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1940s) ; « within » [6jM0S5_Um9M @ 0:05:13](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=313s) ; « fill the entirety » [4BLGd9GMo8U @ 0:02:29](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=149s).
- **Défaut** : `d = 0`, l'objectif est le **bord proche** du gap (`l(C3)` pour un FVG haussier). C'est sa formulation la plus récente et la plus prudente.
- **Test** : `d ∈ {0 ; 0,25 ; 0,5 ; 1}`, en points ou en ticks depuis le bord (0, 2, 4 ticks à l'intérieur).
- **Automatisation** : 100 %.

### Q2 — Méthode de stop
- **Il dit** : extrême de C3 [Tea-SeT3-OU @ 0:03:39](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=219s) ; bougie / swing LTF [4BLGd9GMo8U @ 0:12:01](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=721s) ; objectif d'abord puis stop à 1:1 [Tea-SeT3-OU @ 0:22:46](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1366s).
- **Défaut** : mode **TP-first**. Objectif = niveau du gap (Q1), stop = entrée ∓ (objectif − entrée), donc 1:1 exact. Contrôle de cohérence : le trade est rejeté si ce stop est **plus près** que l'invalidation du modèle d'entrée (le swing LTF à l'origine du signal), ce qui couvre le cas « we are so close to the gap » [Tea-SeT3-OU @ 0:21:02](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1262s).
- **Variantes** :
  - **(S)** stop au swing LTF + `b` ticks, objectif à 1R, trade rejeté si 1R n'atteint pas le gap ;
  - **(H)** stop à l'extrême de C3 + `b` ticks, objectif à 1R.
- **Test** : modes {TP-first, S, H} ; `b ∈ {0, 2, 4}` ticks.
- **Automatisation** : 100 %.

### Q3 — Forme de C3
- **Il dit** : inside bar acceptée [Tea-SeT3-OU @ 0:15:09](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=909s) ; « big up wick » [4BLGd9GMo8U @ 0:02:07](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=127s) ; couleur indifférente [3LrXQDS187Y @ 0:25:28](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1528s).
- **Défaut** : règle minimale `c(C3) < h(C2)` (FVG haussier) / `c(C3) > l(C2)` (baissier).
- **Test** : + sweep obligatoire de l'extrême de C2 ; + mèche côté C2 ≥ `w × range(C3)` avec `w ∈ {0,3 ; 0,5}`.
- **Automatisation** : 100 %.

### Q4 — Displacement de C2
- **Il dit** : C2 doit être « a displacement candle » [6jM0S5_Um9M @ 0:09:47](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=587s), sans chiffre.
- **Défaut** : **pas de filtre** au-delà de l'existence du FVG (qui exige déjà une C2 ample).
- **Test** : corps de C2 `≥ k × ATR14(HTF)`, `k ∈ {0,75 ; 1,0 ; 1,5}` ; corps / range `≥ r`, `r ∈ {0,5 ; 0,7}`.
- **Automatisation** : 100 % une fois le seuil choisi (le jugement d'origine est discrétionnaire).

### Q5 — Taille minimale du FVG et distance minimale à l'objectif
- **Il dit** : rien sur la taille du gap ; vise « 10-15 points » [Tea-SeT3-OU @ 0:19:16](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1156s) à « 20 to 35 points » [6jM0S5_Um9M @ 0:01:27](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=87s) ; refuse un R:R de 0,5 [Tea-SeT3-OU @ 0:21:23](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1283s).
- **Défaut** : `G ≥ 1 tick` ; **distance entrée → objectif ≥ 8 points** en 15 min (sinon le coût mange l'edge) ; ≥ 15 points en 1 h.
- **Test** : `G_min ∈ {1 tick ; 2 ; 5 points}` et en fraction d'ATR ; distance mini `∈ {5 ; 8 ; 12 ; 20}` points.
- **Automatisation** : 100 %.

### Q19 — Gap touché avant l'entrée
- **Il dit** : « if the gap is not entered … yet, it is even better » [nxYi6bd9enA @ 0:07:19](https://www.youtube.com/watch?v=nxYi6bd9enA&t=439s).
- **Défaut** : un setup est **consommé** dès que le prix atteint le niveau d'objectif sans position (on ne court pas après).
- **Test** : autoriser l'entrée tant que le gap n'est pas comblé à 50 %.
- **Automatisation** : 100 %.

## Timing

### Q6 — Fenêtres d'entrée W1 / W2 et condition de flip
- **Il dit** : 1 à 4 min avant la clôture de C3 [4BLGd9GMo8U @ 0:16:45](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=1005s) ; 5 à 10 min en 1 h [6jM0S5_Um9M @ 0:24:37](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1477s) ; sinon pendant C4 [Tea-SeT3-OU @ 0:16:39](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=999s) ; flip de l'open de C4 [nxYi6bd9enA @ 0:02:09](https://www.youtube.com/watch?v=nxYi6bd9enA&t=129s).
- **Défaut** :
  - W1 active : `t_rem ≤ 4 min` (15 min), `≤ 10 min` (1 h), `≤ 30 min` (4 h, PROPOSITION par proportionnalité) ;
  - W2 active : toute la durée de C4 ;
  - flip **non exigé** (c'est une lecture, pas une condition explicite).
- **Test** : W1 seule / W2 seule / les deux ; `T_ant ∈ {2, 4, 6}` min en 15 min ; flip exigé en W2 oui / non.
- **Automatisation** : 100 %.

### Q7 — « Loin » de l'extrême de C2 pendant W1
- **Il dit** : « we are pretty far from that second candle's low » [4BLGd9GMo8U @ 0:24:09](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=1449s) ; « too close … it is a gamble » [6jM0S5_Um9M @ 0:28:14](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1694s).
- **Défaut** : au moment de l'entrée anticipée, `|prix − extrême(C2)| ≥ 0,25 × range(C2)`.
- **Test** : `{0 ; 0,15 ; 0,25 ; 0,5} × range(C2)` ; ou en points `{5 ; 10}`.
- **Automatisation** : 100 % une fois le seuil choisi.

### Q10 — Expiration et sortie temporelle
- **Il dit** : la prédiction vaut pour la durée de C4 [3LrXQDS187Y @ 0:35:44](https://www.youtube.com/watch?v=3LrXQDS187Y&t=2144s) ; un trade a pourtant duré ~30 min [6jM0S5_Um9M @ 0:16:25](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=985s).
- **Défaut** : pas d'entrée après la clôture de C4 ; une position ouverte reste jusqu'au SL/TP, avec une **sortie forcée à la clôture de C5** (garde-fou).
- **Test** : sortie forcée à la clôture de C4 / C5 / jamais.
- **Automatisation** : 100 %.

## Entrée LTF

### Q8 — Modèles d'entrée et définition des swings
- **Il dit** : IFVG + CISD [4BLGd9GMo8U @ 0:02:59](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=179s) ; OB en mai [Tea-SeT3-OU @ 0:06:00](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=360s) ; jamais de définition chiffrée d'un swing.
- **Défaut** : **IFVG + CISD/breaker** ; swing = fractal `n = 2` ; BOS en clôture ; IFVG = le **dernier** FVG LTF de sens opposé formé depuis l'ouverture de C3, cassé en clôture.
- **Test** : `n ∈ {1, 2, 3}` ; chaque modèle seul ; + OB ; + CISD par opening price (version 2025) ; taille mini de l'IFVG `∈ {1 tick ; 1 ; 2}` points.
- **Automatisation** : 100 % (les définitions choisies remplacent son œil, qui reste [VISUEL]).

### Q9 — Type d'ordre
- **Il dit** : limite sur pullback de préférence [3z6qgc66RA8 @ 0:06:00](https://www.youtube.com/watch?v=3z6qgc66RA8&t=360s) ; marché quand la clôture HTF est imminente [6jM0S5_Um9M @ 0:11:53](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=713s).
- **Défaut** : **marché à la clôture** de la bougie LTF qui valide le modèle (exécution à l'ouverture de la suivante, plus le slippage).
- **Test** : limite au bord de la zone (IFVG / breaker), annulée à la fin de la fenêtre.
- **Automatisation** : 100 %.

### Q13 — Timeframes testés et LTF alternatifs
- **Il dit** : 15m / 1h / 4h avec la table [3LrXQDS187Y @ 0:27:59](https://www.youtube.com/watch?v=3LrXQDS187Y&t=1679s) ; exceptions 3 min [6jM0S5_Um9M @ 0:24:34](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1474s) et 2 min [oSqLOXBP7NY @ 0:11:30](https://www.youtube.com/watch?v=oSqLOXBP7NY&t=690s).
- **Défaut** : **15m→1m** comme cœur (« unfilled 15-minute fair value gap model » [4BLGd9GMo8U @ 0:00:00](https://www.youtube.com/watch?v=4BLGd9GMo8U&t=0s)), puis 1h→5m ; 4h→15m en dernier.
- **Test** : 15m→2m, 1h→3m.
- **Automatisation** : 100 %.

## Gestion

### Q11 — Trades par jour
- **Défaut** : **1** ([6jM0S5_Um9M @ 0:02:56](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=176s)). **Test** : 2, 3, illimité (pour mesurer la qualité des setups suivants).
- **Automatisation** : 100 %.

### Q14 — Break-even
- **Il dit** : BE ou stop sous le swing après « a good reaction », en live seulement [oSqLOXBP7NY @ 0:03:24](https://www.youtube.com/watch?v=oSqLOXBP7NY&t=204s).
- **Défaut** : **pas de BE**, comme dans le modèle exposé en V1-V2.
- **Test** : BE à `+0,5R` / `+0,7R`.
- **Automatisation** : 100 % (son déclencheur réel est discrétionnaire).

### Q15 — Grands ranges en 1 h
- **Il dit** : au-delà de 150 handles, survivre à un retour à 50 % ; meilleure entrée à 50 % [6jM0S5_Um9M @ 0:20:20](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1220s).
- **Défaut** : FVG 1 h dont le range de C3 dépasse **150 points** → entrée seulement en **limite à 50 %** du range de C3, objectif et stop 1:1 depuis ce point.
- **Test** : seuil `∈ {100, 150, 200}` ; exclure ces cas.
- **Automatisation** : 100 %, mais le cas est **ambigu** (sur quelle bougie tirer le Fibonacci ? [VISUEL] [6jM0S5_Um9M @ 0:18:30](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1110s)).

## Cadre

### Q12 — Sessions
- **Il dit** : pas de restriction [3LrXQDS187Y @ 0:36:07](https://www.youtube.com/watch?v=3LrXQDS187Y&t=2167s) ; trades montrés entre 8:30 et 15:00 ET ; lives à 10:00, 10:20, 10:40.
- **Défaut** : **8:30-16:00 ET** (couvre tous les trades montrés).
- **Test** : 24 h ; 9:30-11:30 ; 9:30-16:00 ; répartition des résultats par heure (statistique demandée en Phase 4).
- **Automatisation** : 100 %.

### Q16 — Ancrage des bougies
- **Défaut** : 15 min et 1 h sur l'horloge ET (:00) ; 4 h ancré à 18:00 ET (session CME), comme TradingView.
- **Test** : 4 h ancré à 00:00 ET.
- **Automatisation** : 100 %.

### Q17 — Instrument et données
- **Défaut** : NQ (contrat continu, roll au volume) pour le modèle A ; ES pour le modèle C ; MNQ = même signal.
- **Automatisation** : 100 %.

### Q18 — Coûts et slippage (Phase 4)
- **Défaut** : commission de 4,50 $ aller-retour par contrat NQ (à confirmer selon ton courtier), slippage **1 tick** par ordre marché et par stop, 0 sur les limites touchées (`trade-through` d'un tick exigé).
- **Test** : slippage 0 / 1 / 2 ticks.

### Q23 — Setups qui se chevauchent
- **Défaut** : chaque nouvelle bougie HTF peut lancer un setup ; si plusieurs sont actifs, le premier signal d'entrée gagne ; un seul trade à la fois.
- **Automatisation** : 100 %.

## Hors modèle A

### Q20 — Filtre de contexte / continuation
- **Il dit** : 3 critères de draw on liquidity [3LrXQDS187Y @ 0:01:51](https://www.youtube.com/watch?v=3LrXQDS187Y&t=111s) ; pas de reversal près d'un swing externe [3LrXQDS187Y @ 0:06:41](https://www.youtube.com/watch?v=3LrXQDS187Y&t=401s).
- **Défaut** : **aucun filtre** dans la version de référence.
- **Test** (approximation) : refuser le setup si un swing HTF non pris est à moins de `X` points au-delà de l'extrême de C2, `X ∈ {10, 20}`.
- **Automatisation** : **partielle**. Le modèle B complet (lecture des PD arrays « respected / disrespected », « treat it as a one minute chart ») reste discrétionnaire.

### Q21 — Modèle C « 9-10 h »
- **Défaut** : module séparé, testé à part sur ES (et NQ en comparaison) ; il ne fait pas partie de la stratégie de référence.
- **Automatisation** : 100 % sauf le choix du swing du MSS (fractal `n` comme Q8).

### Q22 — Confluences (sweeps nommés, SMT)
- **Défaut** : non utilisées comme filtres ; enregistrées comme **étiquettes** sur chaque trade (sweep de l'extrême de C2, du London low/high 02:00-05:00, du lunch 12:00-13:00, de la veille), pour mesurer leur effet.
- **SMT** (ES/NQ) : non retenu (V0 seulement) ; possible plus tard si les données ES sont disponibles.
- **Automatisation** : 100 % pour les étiquettes.

---

## Ce qui ne sera pas automatisé

- Le « jugement » de sélection (« be selective and choose which one to skip » [Tea-SeT3-OU @ 0:32:00](https://www.youtube.com/watch?v=Tea-SeT3-OU&t=1920s)) : remplacé par les seuils ci-dessus.
- Les prediction plays et le renforcement de position [6jM0S5_Um9M @ 0:21:26](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1286s), [6jM0S5_Um9M @ 0:23:06](https://www.youtube.com/watch?v=6jM0S5_Um9M&t=1386s).
- La lecture « wicks do the damage, bodies tell the story » [oSqLOXBP7NY @ 0:06:27](https://www.youtube.com/watch?v=oSqLOXBP7NY&t=387s) au-delà de la règle de C3.
- Ce qu'il réserve à son groupe privé : « an exact area where you put your entry, stop-loss, take profit » [3LrXQDS187Y @ 0:39:58](https://www.youtube.com/watch?v=3LrXQDS187Y&t=2398s).

## Décisions à valider

Les valeurs par défaut ci-dessus forment la **version de référence** que je coderai en Phase 3-4 :

> FVG 15 min (puis 1 h) · C3 `c < h(C2)` · W1 ≤ 4 min + W2 = C4 · IFVG ou CISD en 1 min (fractal 2) ·
> marché à la clôture · objectif au bord proche du gap · stop à 1:1 (TP-first), rejet si plus serré que le swing LTF ·
> distance mini 8 pts · 1 trade/jour · 8:30-16:00 ET · pas de BE · sortie forcée à la clôture de C5.

Points où ton avis compte le plus : **Q1** (objectif), **Q2** (stop), **Q6** (anticipation pendant C3 ou attente de C4),
**Q12** (sessions), **Q18** (tes coûts réels).
