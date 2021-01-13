# Collective memory and spatial sorting in animal groups - Boids behaviour
Auteurs: [F. Beroujon](https://github.com/Flosilver), [F. Cormée](https://github.com/Florian-Cormee), [H. Duarté](https://github.com/Bacmel)

Tuteur: N. Bredèche

---

## Context

Pour un devoir de master en informatique, notre groupe à repris l'étude sur le comportement de particules en essaim. Contrairement à l'étude d'origine, nous travaillons dans un environnement 2D. L'objectif principal était de retrouver un comportement de mémoire  dans le groupe représenté par un cycle d'hystérésis lorsque le rayon d'orientation des particules évoluent au cours d'une même simulation.

La simulation que nous utilisons est tiré du travil de [Christoph Smithmyer](https://gitlab.com/chrismit3s/boids) que nous avons grandement modifié pour correspondre au travail demandé.

---
## Comment ça marche?

### Prérequis

Python3.8 est requis et lancez la commande suivante:

> `python3.8 -m pip install requirements.txt`

### Lancer une simulation

Vérifiez les arguments de la simulation pour découvrir le champ des possibles avec la commande:

> `python3.8 src/sim.py --help`

Attention, vous devrez au moins définir au moins un type de perception. Si vous ne le faite pas, un message d'erreur vous indiquera de le faire.

Un script bash (`run.sh`) est également disponible et pré-rempli. Lancez le avec:

> `source src/run.sh`