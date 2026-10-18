"""
Exercice 3 - Voyageur de commerce : recherche taboue et recuit simulé.
Les tirets du tableau sont modélisés par l'absence d'arête (None).
Aucune bibliothèque externe n'est nécessaire.
"""
import math
import random
from collections import deque

# Matrice symétrique des distances. Les villes sont numérotées de 1 à 8.
DISTANCES = [
    [0, 14, 15, None, None, None, None, 17],
    [14, 0, 13, 14, 20, None, None, 21],
    [15, 13, 0, 11, 21, 17, 9, 9],
    [None, 14, 11, 0, 11, 10, 8, 20],
    [None, 20, 21, 11, 0, 15, 18, None],
    [None, None, 17, 10, 15, 0, 9, None],
    [None, None, 9, 8, 18, 9, 0, 13],
    [17, 21, 9, 20, None, None, 13, 0],
]
TOUR_INITIAL = [1, 2, 3, 4, 5, 6, 7, 8]


def cout_tour(tour):
    """Retourne la distance du cycle, ou None si une liaison est absente."""
    total = 0
    cycle = tour + [tour[0]]
    for i in range(len(tour)):
        distance = DISTANCES[cycle[i] - 1][cycle[i + 1] - 1]
        if distance is None:
            return None
        total += distance
    return total


def voisins_par_echange(tour):
    """Voisinage : échange de deux villes, en gardant la ville 1 au départ."""
    resultats = []
    for i in range(1, len(tour)):
        for j in range(i + 1, len(tour)):
            voisin = tour.copy()
            voisin[i], voisin[j] = voisin[j], voisin[i]
            cout = cout_tour(voisin)
            if cout is not None:
                mouvement = tuple(sorted((tour[i], tour[j])))
                resultats.append((voisin, cout, mouvement))
    return resultats


def recherche_taboue(iterations=100, tenure=5):
    courant = TOUR_INITIAL.copy()
    cout_courant = cout_tour(courant)
    meilleur = courant.copy()
    cout_meilleur = cout_courant
    tabou = deque(maxlen=tenure)
    historique = []

    for iteration in range(1, iterations + 1):
        candidats = []
        for voisin, cout, mouvement in voisins_par_echange(courant):
            est_tabou = mouvement in tabou
            # Aspiration : une solution meilleure que le meilleur connu est autorisée.
            if not est_tabou or cout < cout_meilleur:
                candidats.append((cout, voisin, mouvement))

        if not candidats:
            # Si tous les mouvements disponibles sont tabous, on libère le plus ancien.
            if tabou:
                tabou.popleft()
                for voisin, cout, mouvement in voisins_par_echange(courant):
                    if mouvement not in tabou or cout < cout_meilleur:
                        candidats.append((cout, voisin, mouvement))
            if not candidats:
                break

        candidats.sort(key=lambda item: item[0])
        cout_courant, courant, mouvement = candidats[0]
        tabou.append(mouvement)

        if cout_courant < cout_meilleur:
            meilleur = courant.copy()
            cout_meilleur = cout_courant

        historique.append((iteration, courant.copy(), cout_courant,
                           meilleur.copy(), cout_meilleur))

    return meilleur, cout_meilleur, historique


def recuit_simule(iterations=5, temperature_initiale=20.0,
                   refroidissement=0.75, seed=42):
    """Recuit simulé sur exactement 5 itérations par défaut."""
    random.seed(seed)
    courant = TOUR_INITIAL.copy()
    cout_courant = cout_tour(courant)
    meilleur = courant.copy()
    cout_meilleur = cout_courant
    historique = []

    for iteration in range(1, iterations + 1):
        temperature = temperature_initiale * (refroidissement ** (iteration - 1))
        candidats = voisins_par_echange(courant)
        if not candidats:
            historique.append((iteration, temperature, None, None,
                               courant.copy(), cout_courant, "aucun voisin valide"))
            continue

        voisin, cout_voisin, _ = random.choice(candidats)
        delta = cout_voisin - cout_courant

        if delta <= 0:
            accepte = True
        else:
            probabilite = math.exp(-delta / temperature)
            accepte = random.random() < probabilite

        decision = "accepté" if accepte else "rejeté"
        if accepte:
            courant = voisin
            cout_courant = cout_voisin

        if cout_courant < cout_meilleur:
            meilleur = courant.copy()
            cout_meilleur = cout_courant

        historique.append((iteration, temperature, voisin.copy(), cout_voisin,
                           courant.copy(), cout_courant, decision))

    return meilleur, cout_meilleur, historique


def afficher_tour(tour):
    return "-".join(map(str, tour + [tour[0]]))


if __name__ == "__main__":
    print("=== Recherche taboue ===")
    print("Circuit initial :", afficher_tour(TOUR_INITIAL))
    print("Coût initial :", cout_tour(TOUR_INITIAL))
    meilleur, cout, historique = recherche_taboue()
    print("Meilleur circuit :", afficher_tour(meilleur))
    print("Distance totale :", cout)
    print("Itérations :", len(historique))

    print("\n=== Recuit simulé (5 itérations) ===")
    meilleur_rs, cout_rs, historique_rs = recuit_simule()
    for ligne in historique_rs:
        iteration, temperature, voisin, cout_voisin, courant, cout_courant, decision = ligne
        if voisin is None:
            print(f"Itération {iteration}: T={temperature:.2f}, {decision}")
        else:
            print(
                f"Itération {iteration}: T={temperature:.2f}, "
                f"voisin={afficher_tour(voisin)} (coût={cout_voisin}), "
                f"décision={decision}, coût courant={cout_courant}"
            )
    print("Meilleur circuit trouvé :", afficher_tour(meilleur_rs))
    print("Distance totale :", cout_rs)
