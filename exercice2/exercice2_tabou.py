"""
Exercice 2 - Problème de transport résolu par recherche taboue.
Aucune bibliothèque externe n'est nécessaire.
"""
import random
from collections import deque

# Coût unitaire de transport : lignes = dépôts D1, D2 ; colonnes = M1, M2, M3
COUTS = ((5, 3, 4),
         (6, 7, 2))
CAPACITES = (8, 9)
DEMANDES = (4, 5, 8)


def cout_total(x):
    """x[j] = quantité envoyée de D1 vers Mj ; D2 complète la demande."""
    d1 = list(x)
    d2 = [DEMANDES[j] - d1[j] for j in range(3)]
    return sum(COUTS[0][j] * d1[j] + COUTS[1][j] * d2[j]
               for j in range(3))


def est_faisable(x):
    return (
        len(x) == 3
        and sum(x) == CAPACITES[0]
        and all(0 <= x[j] <= DEMANDES[j] for j in range(3))
        and all(DEMANDES[j] - x[j] >= 0 for j in range(3))
        and sum(DEMANDES[j] - x[j] for j in range(3)) == CAPACITES[1]
    )


def voisins(x):
    """Déplace un container de la destination i vers la destination j pour D1.
    Les demandes et les capacités restent respectées.
    """
    resultat = []
    for i in range(3):
        if x[i] == 0:
            continue
        for j in range(3):
            if i == j or x[j] >= DEMANDES[j]:
                continue
            y = list(x)
            y[i] -= 1
            y[j] += 1
            if est_faisable(y):
                resultat.append((tuple(y), (i, j)))
    return resultat


def recherche_taboue(iterations=100, tenure=5, seed=42):
    random.seed(seed)
    courant = (4, 3, 1)  # Répartition initiale de D1, somme = 8
    meilleur = courant
    cout_meilleur = cout_total(meilleur)
    liste_taboue = deque(maxlen=tenure)
    historique = []

    for k in range(1, iterations + 1):
        candidats = []
        for solution, mouvement in voisins(courant):
            # Le mouvement inverse est interdit pendant la tenure.
            mouvement_inverse = (mouvement[1], mouvement[0])
            est_tabou = mouvement_inverse in liste_taboue
            cout = cout_total(solution)
            # Critère d'aspiration : autoriser si cela améliore le meilleur global.
            if not est_tabou or cout < cout_meilleur:
                candidats.append((cout, solution, mouvement))

        if not candidats:
            break

        candidats.sort(key=lambda element: element[0])
        cout_courant, courant, mouvement = candidats[0]
        liste_taboue.append(mouvement)
        if cout_courant < cout_meilleur:
            meilleur, cout_meilleur = courant, cout_courant
        historique.append((k, courant, cout_courant, meilleur, cout_meilleur))

    return meilleur, cout_meilleur, historique


def afficher_solution(x, cout):
    d1 = list(x)
    d2 = [DEMANDES[j] - d1[j] for j in range(3)]
    print("Répartition optimale trouvée (en containers) :")
    print("             M1   M2   M3   Total expédié")
    print(f"Dépôt D1 :  {d1[0]:>2}   {d1[1]:>2}   {d1[2]:>2}       {sum(d1)}")
    print(f"Dépôt D2 :  {d2[0]:>2}   {d2[1]:>2}   {d2[2]:>2}       {sum(d2)}")
    print(f"Demandes :   {DEMANDES[0]:>2}   {DEMANDES[1]:>2}   {DEMANDES[2]:>2}")
    print(f"Coût total de transport : {cout}")


if __name__ == "__main__":
    solution, cout, historique = recherche_taboue()
    afficher_solution(solution, cout)
    print(f"Nombre d'itérations effectuées : {len(historique)}")
