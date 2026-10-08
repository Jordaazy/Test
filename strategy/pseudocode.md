# Phase 3 — Formalisation : pseudo-code

Spécification commune à l'indicateur Pine, à la `strategy()` Pine et au backtest Python, pour que les trois
produisent **les mêmes signaux**. Les règles viennent de `regles.md` ; les valeurs de `parametres.json`
(paramètres notés `P.nom`) ; les choix non sourcés renvoient aux questions de `questions.md` (Qn).

---

## 1. Conventions

- Horloge : **heure de New York (ET)**. Une bougie est datée par son **ouverture** et close à `t_open + durée`.
- `tick = 0.25` (NQ). `s_f` = sens du FVG (+1 haussier, −1 baissier) ; `dir = −s_f` = sens du trade (+1 long, −1 short).
- Les bougies **HTF** (15 min, 1 h, 4 h) sont **construites à partir des bougies LTF** (agrégation sur la grille d'horloge),
  pas lues via un autre flux : Pine et Python voient ainsi exactement les mêmes OHLC.
- Toute décision est prise à la **clôture d'une bougie LTF**. Pas de lookahead : une bougie HTF n'est connue qu'une fois
  sa dernière bougie LTF clôturée.
- **Journée de trading** = date de `t + 6 h` (une journée CME commence à 18:00 ET).

Raccourcis pour un setup (C1, C2, C3 [, C4]) :

```
near(C3)  = (s_f>0) ? l(C3) : h(C3)          # bord proche du gap (côté prix)
far(C1)   = (s_f>0) ? h(C1) : l(C1)          # bord lointain
G         = s_f * (near − far)               # taille du gap (> 0 si FVG)
ext2      = (s_f>0) ? h(C2) : l(C2)          # extrême de C2 côté « continuation »
ext3      = (s_f>0) ? h(C3) : l(C3)          # extrême de C3 du même côté
tp_level  = near − s_f * P.tp_profondeur * G  # Q1
```

## 2. État

```
htf_bar      : bougie HTF en cours {t_open, t_close, o, h, l, c}
htf_hist[]   : bougies HTF clôturées (on garde les 3 dernières + ATR14)
ltf_hist[]   : bougies LTF (fenêtre glissante, ≥ 3 bougies HTF)
setups[]     : setups actifs (voir §3)
position     : null | {dir, entry, sl, tp, R, setup_id, t_entry, be_done}
pending      : null | ordre limite {dir, prix, sl, tp, setup_id, expire_at}
trades_today : compteur, remis à 0 au changement de journée de trading
```

Un **setup** :

```
{ id, s_f, dir, C1, C2, C3 (en cours puis figée), C4 (en cours),
  etat ∈ {FORMATION, ARME, EXPIRE, CONSOMME, INVALIDE, DECLENCHE},
  struct_start : index LTF de début de la fenêtre de structure  (P.fenetre_structure_debut)
  t_close_C3, t_close_C4, t_close_C5 }
```

## 3. Boucle principale (à chaque clôture de bougie LTF `k`, heure `t = t_close(k)`)

```
0.  executer_marche(k)                        # §6.1 : ordre au marché décidé en k−1 → rempli à o(k) ± slippage
1.  remplir_limite(k)                         # §6.4 : ordre limite en attente touché ?
2.  gerer_position(k)                         # §7 : SL / TP / BE / sortie forcée, y compris sur la bougie du remplissage
3.  maj_htf(k)                                # agrège k dans htf_bar
4.  SI t == htf_bar.t_close :                 # la bougie HTF vient de clôturer
        cloturer_htf()                        # §4
5.  POUR chaque setup s en FORMATION :        # C3 en cours  → fenêtre W1
        SI non gap_en_formation(s) : s.etat = INVALIDE ; continuer
        SI P.w1_actif ET (s.t_close_C3 − t) ≤ P.w1_minutes_avant_cloture[HTF]
           ET G(s) ≥ P.gap_min_points                          # gap provisoire (near = extrême de C3 jusqu'ici)
           ET (P.c3_regle n'exige pas "sweep" OU s_f*(ext3 − ext2) > 0)       # sweep déjà fait si exigé
           ET s_f*(c_k − ext2(s)) < 0                         # C3 « clôturerait » dans C2 si elle clôturait maintenant
           ET s_f*(ext2(s) − c_k) ≥ P.w1_distance_c2_frac * range(C2)      # Q7
           ET signal_ltf(s, k) :
              tenter_entree(s, k)
6.  POUR chaque setup s ARME :                # C4 en cours  → fenêtre W2
        SI P.consommer_si_gap_touche ET prix_a_atteint(tp_level(s), depuis t_close_C3) :
              s.etat = CONSOMME ; continuer
        SI P.w2_actif
           ET (non P.w2_flip_requis OU flip(s, k))             # §5.5
           ET signal_ltf(s, k) :
              tenter_entree(s, k)
```

Quand plusieurs setups donnent un signal sur la même bougie, le plus ancien est pris (Q23).

## 4. Clôture d'une bougie HTF

```
cloturer_htf():
    B = htf_bar ; htf_hist.push(B)

    # a) les setups dont C3 vient de clôturer
    POUR s en FORMATION avec s.C3 == B :
        SI fvg_valide(s) ET regle_C3(s) ET displacement_ok(s.C2) :
             s.etat = ARME                    # C4 commence maintenant
        SINON :
             s.etat = INVALIDE                # une position anticipée garde son stop (règle A.5.8)

    # b) les setups dont C4 vient de clôturer
    POUR s ARME avec s.C4 == B : s.etat = EXPIRE        # plus d'entrée après C4 (A.7.1)

    # c) nouveau candidat : B devient C2, la bougie qui s'ouvre devient C3
    SI len(htf_hist) ≥ 2 :
        C1, C2 = htf_hist[-2], htf_hist[-1]
        POUR s_f dans {+1, −1} :
            créer setup {s_f, dir=−s_f, C1, C2, C3=bougie qui s'ouvre, etat=FORMATION}
            # il sera invalidé dès que C3 touche la mèche de C1 (gap_en_formation faux)
```

Fonctions HTF (`regles.md` A.2) :

```
gap_en_formation(s) :  s_f>0 → l(C3 jusqu'ici) > h(C1)      |   s_f<0 → h(C3 jusqu'ici) < l(C1)
fvg_valide(s)       :  gap_en_formation(s) ET G(s) ≥ P.gap_min_points
regle_C3(s)         :  s_f*(c(C3) − ext2) < 0                                   # « fails to close above C2 »
                       ET (P.c3_regle n'exige pas "sweep" OU s_f*(ext3 − ext2) > 0)
                       ET (P.c3_regle n'exige pas "wick" OU meche_C3 ≥ P.c3_wick_min * range(C3))
                       où meche_C3 = s_f>0 ? h(C3) − max(o,c)(C3) : min(o,c)(C3) − l(C3)
displacement_ok(C2) :  (P.c2_displacement_atr_k == 0 OU |c−o|(C2) ≥ k * ATR14_HTF)
                       ET (|c−o|(C2) / range(C2) ≥ P.c2_body_ratio_min)
```

## 5. Signaux LTF (`regles.md` A.4)

Toutes les fonctions ne regardent que les bougies LTF d'index `≥ s.struct_start` (début de C3 par défaut).
Elles sont écrites pour `dir = +1` (long) ; pour un short, on inverse haut/bas et le sens des inégalités.
Chacune renvoie `(signal: bool, zone_limite: prix, invalidation: prix)`.

### 5.1 Swings (fractals)

```
swing_high(i) : h(i) > h(j) pour tout j ∈ [i−n, i+n], j ≠ i       (n = P.fractal_n)
swing_low(i)  : l(i) < l(j) pour tout j ∈ [i−n, i+n], j ≠ i
Un swing d'index i n'est CONNU qu'à partir de la bougie i+n (pas de lookahead).
```

### 5.2 IFVG (« 180 »)

```
FVG_LTF baissier d'index (i−2, i−1, i) : h(i) < l(i−2) ; zone [h(i), l(i−2)] ; taille ≥ P.ifvg_min_points
ifvg_long(s, k) :
    F = dernier FVG_LTF baissier formé depuis struct_start et pas encore inversé
    signal       = c(k) > haut(F) ET c(k−1) ≤ haut(F)            # 1re clôture au-dessus = inversion
    zone_limite  = haut(F)                                       # retest de la zone inversée
    invalidation = min(l) sur [struct_start, k]
```

### 5.3 CISD / breaker (version 2026)

```
cisd_long(s, k) :
    H1 = dernier swing high connu, d'index iH ≥ struct_start
    L1 = dernier swing low connu d'index iL1 ∈ [struct_start, iH)
    L2 = min(l) sur (iH, k−1]                                    # « lower low », pas besoin d'être un fractal
    signal       = L2 < L1 ET c(k) > h(iH) ET c(k−1) ≤ h(iH)     # « higher high » en clôture
    j            = dernière bougie haussière (c > o) d'index ∈ [iL1, iH], sinon iH   # l'OB baissier « raté » = breaker
    zone_limite  = h(j)
    invalidation = L2
```

### 5.4 Variantes optionnelles

```
cisd_open_long(s, k) :                               # version 2025, par l'opening price
    m     = argmin(l) sur [struct_start, k−1]        # bougie du sweep
    serie = plus longue suite de bougies baissières consécutives se terminant en m (ou juste avant m)
    niv   = o(première bougie de serie)
    signal = c(k) > niv ET c(k−1) ≤ niv ; zone_limite = niv ; invalidation = l(m)

ob_long(s, k) :                                      # « break and retest » (mai 2026)
    H1 (iH), L1 (iL1 < iH), L2 = swing low connu d'index iL2 > iH avec l(iL2) > L1   # higher low
    signal = c(k) > h(iH) ET c(k−1) ≤ h(iH)
    j = dernière bougie baissière d'index ∈ [iH, iL2] ; zone_limite = h(j) ; invalidation = l(iL2)
```

`signal_ltf(s, k)` = OU logique des modèles listés dans `P.modeles` ; s'il y en a plusieurs, on retient celui dont
l'invalidation est la plus proche du prix (risque le plus faible).

### 5.5 Flip (option W2)

```
flip(s, k) : (dir>0 : l(C4 jusqu'ici) < o(C4) ET c(k) > o(C4))      # manipulation puis repasse au-dessus de l'open
             (dir<0 : h(C4 jusqu'ici) > o(C4) ET c(k) < o(C4))
```

## 6. Entrée (`regles.md` A.0, A.5)

### 6.1 Filtres globaux

```
tenter_entree(s, k) :
    SI position ≠ null OU pending ≠ null              : rien        # une seule exposition à la fois
    SI trades_today ≥ P.max_trades_par_jour           : rien        # Q11
    SI heure(t) ∉ P.session_et                        : rien        # Q12
    (sig, zone, inv) = signal_ltf(s, k)
    e = (P.type_ordre == "marche_cloture") ? c(k) : zone            # prix de référence pour le calcul
    SI HTF == 60 ET P.grand_range_points_1h ≠ null ET range(C3) > P.grand_range_points_1h :   # Q15
         e = (h(C3) + l(C3)) / 2 ; type forcé = limite
    (sl, tp, ok) = calcul_stops(s, e, inv)
    SI non ok : rien
    SI dir*(tp − e) < P.distance_tp_min_points[HTF]   : rien        # Q5
    SI type == marché : ordre transmis → rempli à o(k+1) ± slippage par executer_marche(k+1) ;
                        sl/tp recalculés à 1:1 sur le prix réel ; si le 1:1 n'est plus possible (R ≤ 0
                        après un écart d'ouverture) → ordre annulé
    SINON            : pending = {dir, prix=e, sl, tp, s.id, expire_at = s.t_close_C4}
    s.etat = DECLENCHE ; trades_today += 1 (au remplissage)
```

### 6.2 Stop et objectif (Q2)

```
calcul_stops(s, e, inv) :
    b  = P.stop_buffer_ticks * tick
    tp = tp_level(s)
    SELON P.stop_mode :
      TP_FIRST   : R = dir*(tp − e) ; sl = e − dir*R
                   ok = R > 0 ET dir*(inv − sl) ≥ b        # le stop doit être au-delà de l'invalidation LTF
      STRUCTURE  : sl = inv − dir*b ; R = dir*(e − sl) ; tp = e + dir*R
                   ok = R > 0 ET dir*(tp − near(C3)) ≥ 0    # 1R doit atteindre le gap
      C3_EXTREME : sl = ext3(C3 jusqu'ici) + s_f*b ; R = dir*(e − sl) ; tp = e + dir*R
                   ok = R > 0
    renvoyer (sl, tp, ok)
```

### 6.3 R:R

`P.rr = 1` n'est **pas** optimisé : c'est une règle explicite du modèle (A.0.3).

### 6.4 Ordre limite

```
remplir_limite(k) :
    SI pending ET t ≤ pending.expire_at :
        SI dir>0 ET l(k) ≤ prix − P.limite_trade_through_ticks*tick : ouvrir au prix limite
        SI dir<0 ET h(k) ≥ prix + P.limite_trade_through_ticks*tick : ouvrir au prix limite
    SI pending ET t > pending.expire_at : annuler
```

## 7. Gestion de position

```
gerer_position(k) :
    SI position == null : rien
    touche_sl = dir>0 ? l(k) ≤ sl : h(k) ≥ sl
    touche_tp = dir>0 ? h(k) ≥ tp + through : l(k) ≤ tp − through
    SI touche_sl : sortir à sl ∓ slippage                       # si SL et TP dans la même bougie : SL d'abord (pessimiste)
    # bougie de remplissage d'un ordre LIMITE : seul le SL est testé (l'ordre intra-bougie est inconnu)
    SINON SI touche_tp : sortir à tp
    SINON :
        SI P.be_a_R ≠ null ET non be_done ET dir*(extrême favorable(k) − entry) ≥ P.be_a_R * R :
             sl = entry ; be_done = vrai                        # Q14
        SI P.sortie_forcee == "cloture_C5" ET t == setup.t_close_C5 : sortir à c(k) ∓ slippage
        (idem "cloture_C4")
```

Coût d'un trade : `P.commission_aller_retour_usd` + slippage. Le résultat est exprimé en **R** (gain/perte ÷ risque initial)
et en dollars (NQ : 20 $/point).

---

## 8. Modèle C — bougie 9h-10h (module séparé, ES)

```
à 10:00 ET : biais = signe(c − o) de la bougie 1 h 09:00-10:00 ; SI 0 → pas de trade
de 10:00 à 11:00, en 1 min, pour biais = +1 :
    MSS contre le biais : clôture sous le dernier swing low connu formé après 10:00
    jambe = du dernier swing high avant le MSS jusqu'au plus bas après le MSS
    PDA   = FVG baissiers 1 min de la jambe ∪ OB baissier (dernière bougie haussière avant la jambe)
    entrée long = 1re clôture au-dessus du plus haut des bords supérieurs des PDA, MSS non tenu
    SL = plus bas de la jambe − b ; TP = 1:1 ; 1 trade par jour
(miroir pour biais = −1)
```

## 9. Modèle B — continuation (automatisation partielle)

```
sur chaque bougie HTF clôturée B :
    cible_haut = swing high HTF non pris le plus proche au-dessus ; cible_bas = idem en dessous
    score(+1) = [dist(cible_haut) ≤ p*ATR] + [dernier FVG HTF haussier respecté] + [dernier FVG HTF baissier inversé]
              + [B haussière ET corps(B) ≥ k*ATR]
    projection = +1 si score(+1) ≥ seuil ET score(−1) < seuil (miroir pour −1)
pendant la bougie suivante : tout passage sous son open = fake-out ;
    entrée = signal_ltf dans le sens de la projection, après un passage sous l'open ;
    objectif = la cible ; stop = 1:1 (ou structure)
```

« Respecté / disrespected » et « treat it as a one minute chart » relèvent du jugement : ce score n'en est qu'une approximation.

---

## 10. Ce qui est automatisable

| Élément | Automatisation | Commentaire |
|---|---|---|
| Construction de C1-C4 sur 15 min / 1 h / 4 h | **100 %** | agrégation sur l'horloge ET (Q16 pour le 4 h) |
| FVG haussier / baissier, gap unfilled | **100 %** | définition explicite |
| Règle C3 (`c(C3)` dans C2) | **100 %** | variantes Q3 |
| Displacement de C2 | **100 % avec seuil choisi** | lui ne chiffre pas (Q4) |
| Fenêtres de timing W1 / W2 | **100 %** | minutes explicites pour 15 min et 1 h |
| « Loin » de l'extrême de C2 | **100 % avec seuil choisi** | Q7 |
| IFVG, CISD/breaker, OB, CISD par opening price | **100 % avec définition choisie** | sa lecture visuelle des swings est remplacée par des fractals (Q8) |
| Objectif dans le gap, 1:1, distance mini | **100 %** | profondeur contradictoire (Q1) |
| Stop | **100 % par mode** | trois modes testés (Q2) |
| 1 trade / jour, sessions, sortie forcée | **100 %** | |
| Break-even | **100 % avec seuil choisi** | déclencheur réel discrétionnaire (Q14) |
| Grands ranges 1 h (50 %) | **100 %**, définition **ambiguë** | sur quelle bougie tirer le Fibonacci ? (Q15) |
| Confluences (sweeps nommés, SMT) | **100 % en étiquettes** | pas de filtre par défaut (Q22) |
| Modèle C (9-10 h) | **100 %** | swing du MSS à fixer |
| Modèle B (continuation) | **partiel** | score approximatif des 3 critères |
| Sélection au jugé, prediction plays, renforcement | **non** | exclus |
| Zones « enseignées dans le groupe privé » | **non** | inconnues |

## 11. Notes d'implémentation

**Pine v6** (indicateur puis `strategy()`) :
- graphique en 1 min ; bougies HTF reconstruites avec `timeframe.change("15")` et des accumulateurs `o/h/l/c`
  (pas de `request.security` pour la logique, afin de rester identique au Python) ;
- `strategy()` : `process_orders_on_close = false` → un ordre au marché envoyé à la clôture de `k` est rempli à
  l'ouverture de `k+1`, comme en Python ; `strategy.exit(stop=sl, limit=tp)` ;
- profondeur d'historique limitée sur TradingView (1 min) : la `strategy()` Pine sert à vérifier visuellement les
  signaux, pas à valider l'edge.

**Python** (Databento, Phase 4) :
- OHLCV 1 min (ou 1 s pour départager SL/TP dans la même minute) ; contrat continu NQ avec roll au volume ;
- même pseudo-code, moteur événementiel bougie par bougie ; tests unitaires sur des scénarios construits à la main
  (un par règle de `regles.md`) ;
- statistiques et protocole anti-surapprentissage (in-sample / out-of-sample, walk-forward, grilles de robustesse sur
  les plages `test`) : Phase 4.
