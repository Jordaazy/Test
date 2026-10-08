# Scripts TradingView (Pine v6)

| Fichier | Rôle |
|---|---|
| `amas_ufvg_indicator.pine` | **Indicateur** : gap armé, fenêtres W1 (orange) / W2 (bleu), signaux avec entrée / SL / TP proposés, sorties d'une position virtuelle, tableau d'état, alertes. Aucune exécution. |
| `amas_ufvg_strategy.pine` | **strategy()** : mêmes signaux, ordres réels du testeur TradingView (1 contrat, 2,25 $ par côté, 1 tick de slippage). |
| `core.pine` | Logique commune (ne pas charger seule). |
| `build.py` | Régénère les deux scripts depuis `core.pine` : `python3 pine/build.py`. |

## Installation

1. TradingView → **Pine Editor** (en bas) → **Open** → **New blank indicator**.
2. Efface le contenu, colle `amas_ufvg_indicator.pine`, **Save**, puis **Add to chart**.
3. Pareil pour `amas_ufvg_strategy.pine` (**New blank strategy**). Résultats dans l'onglet **Strategy Tester**.
4. Graphique : **NQ1!** (ou MNQ1!), en **1 minute** pour un FVG 15 min (5 min pour un FVG 1 h, 15 min pour un FVG 4 h).

Les réglages par défaut sont ceux de la version de référence (`strategy/parametres.json`).

## Ce qui est identique au backtest Python

Même construction des bougies HTF, même FVG, même règle C3, mêmes fenêtres W1/W2, mêmes modèles d'entrée
(IFVG, CISD/breaker, OB), mêmes modes de stop, même session (heure de New York), plafond journalier et
sortie forcée.

## Différences connues (petites)

- **Prix d'entrée de référence** : Pine calcule SL/TP sur la **clôture** de la bougie du signal ; Python les
  recalcule sur l'**ouverture suivante + 1 tick**. Les niveaux diffèrent de quelques ticks.
- **CISD par opening price** (variante 2025) : seulement en Python.
- **Pause de séance** : un setup dont C4 tomberait après la pause de 17:00 ET est annulé à la reprise en Pine,
  ignoré d'emblée en Python (sans effet avec la session par défaut 08:30-16:00).
- **Historique** : TradingView ne garde que quelques semaines à quelques mois de données 1 min selon
  l'abonnement ; le Strategy Tester sert à **vérifier visuellement** les signaux, pas à valider l'edge
  (c'est le rôle du backtest Python sur 21 mois).

## Vérifier la concordance avec Python

`results/trades_reference_15m.csv` liste chaque trade du backtest (heure de signal, sens, entrée, SL, TP).
Sur une même journée, l'indicateur doit afficher un signal à la même minute et dans le même sens.

## Si TradingView affiche une erreur de compilation

Ces scripts n'ont pas pu être compilés dans l'environnement de développement (pas d'accès à TradingView).
Copie le message d'erreur exact (avec le numéro de ligne) : la correction est en général d'une ligne.
