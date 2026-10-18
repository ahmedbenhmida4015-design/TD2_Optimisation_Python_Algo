# TD n°2 — Optimisation combinatoire en Python

**Faculté des Sciences de Sfax — Travaux dirigés n°2**

Ce dépôt contient les solutions demandées pour les exercices 2 et 3. Le code utilise uniquement Python standard : aucune bibliothèque externe n'est nécessaire.

## Contenu du projet

```text
TD2_Optimisation_Python/
├── README.md
├── exercice2/
│   └── exercice2_tabou.py
└── exercice3/
    └── exercice3_tabou_recuit.py
```

## Prérequis et lancement

- Python 3.9 ou plus récent recommandé.
- Télécharger/cloner le dépôt, puis ouvrir un terminal dans le dossier du projet.

### Exercice 2 — Recherche taboue (transport)

```bash
python exercice2/exercice2_tabou.py
```

Données reprises du sujet :

| Dépôt | M1 | M2 | M3 | Capacité |
|---|---:|---:|---:|---:|
| D1 | 5 | 3 | 4 | 8 |
| D2 | 6 | 7 | 2 | 9 |
| Demande | 4 | 5 | 8 | 17 |

Le programme représente une solution par `x = (x1, x2, x3)`, où `xj` est la quantité livrée par D1 au magasin Mj. D2 livre le complément de chaque demande. Ainsi, la somme des livraisons de D1 vaut 8, chaque demande est satisfaite, et D2 livre au total 9 containers.

Le voisinage déplace un container de D1 d'un magasin vers un autre, sans violer les capacités ni les demandes. La liste taboue évite de refaire immédiatement un mouvement inverse. Le critère d'aspiration autorise un mouvement tabou s'il améliore la meilleure solution globale connue.

**Solution optimale pour ces données :**

| Dépôt | M1 | M2 | M3 | Total |
|---|---:|---:|---:|---:|
| D1 | 3 | 5 | 0 | 8 |
| D2 | 1 | 0 | 8 | 9 |
| Total livré | 4 | 5 | 8 | 17 |

Coût : `3×5 + 5×3 + 1×6 + 8×2 = 52`.

Le coût 55 est optimal : D1 est moins cher que D2 pour M1 et M2, tandis que D2 est moins cher pour M3. Il est donc optimal d'affecter les 5 unités de M2 et les 3 unités restantes de D1 à M1 ; D2 fournit l'unité restante de M1 et les 8 unités de M3.

### Exercice 3 — Voyageur de commerce

```bash
python exercice3/exercice3_tabou_recuit.py
```

Le tableau du sujet est traité comme un graphe non complet et non orienté : une valeur numérique est une distance disponible ; un tiret signifie que la liaison n'existe pas. Un circuit n'est accepté que si toutes ses liaisons existent.

#### 1. Recherche taboue

- Circuit initial imposé : `1-2-3-4-5-6-7-8-1`.
- Distance initiale : `14 + 13 + 11 + 11 + 15 + 9 + 13 + 17 = 103`.
- Voisinage : échanger deux villes sans déplacer la ville 1 de sa position initiale.
- Les circuits contenant une liaison absente sont exclus.
- Une liste taboue de mouvements et un critère d'aspiration sont utilisés.

Le programme affiche le meilleur circuit trouvé et sa distance. Comme il s'agit d'une métaheuristique, le résultat dépend des paramètres et du voisinage ; il ne faut pas confondre une solution trouvée par la recherche avec une preuve générale d'optimalité.

#### 2. Recuit simulé — exactement 5 itérations

- Température initiale empirique : `T₀ = 20`.
- Facteur de refroidissement : `α = 0,75`.
- Température à l'itération `k` : `Tₖ = T₀ × α^(k−1)`.
- Un voisin valide est choisi aléatoirement à chaque itération.
- Si le voisin améliore le coût, il est accepté. Sinon, il est accepté avec la probabilité `exp(-Δ/T)`, où `Δ` est l'augmentation du coût.
- Les températures des cinq itérations sont donc 20 ; 15 ; 11,25 ; 8,4375 ; 6,328125.

Le programme affiche la température, le voisin proposé, sa distance, la décision d'acceptation et le meilleur circuit obtenu.

## Reproductibilité

Les graines aléatoires sont fixées (`seed=42`) pour que les exécutions donnent les mêmes résultats avec la même version de Python et le même environnement.


