# Coûts de transport
couts = [
    [5, 3, 4],   
    [6, 7, 2]    
]


def calcul_cout(solution):
    total = 0

    for i in range(2):
        for j in range(3):
            total += solution[i][j] * couts[i][j]

    return total


def generer_voisins(solution):
    voisins = []
    for i in range(3):
        for j in range(3):

            if i != j:

                if solution[0][i] > 0 and solution[1][j] > 0:

                    voisin = [
                        solution[0].copy(),
                        solution[1].copy()
                    ]
                    voisin[0][i] -= 1
                    voisin[0][j] += 1

                    voisin[1][i] += 1
                    voisin[1][j] -= 1

                    voisins.append(((i, j), voisin))

    return voisins


def recherche_taboue(solution_initiale, nb_iterations=15, taille_tabou=3):

    solution_courante = solution_initiale

    meilleure_solution = [
        solution_initiale[0].copy(),
        solution_initiale[1].copy()
    ]

    meilleur_cout = calcul_cout(meilleure_solution)

    liste_tabou = []

    for iteration in range(nb_iterations):

        voisins = generer_voisins(solution_courante)

        meilleur_voisin = None
        meilleur_voisin_cout = float("inf")
        meilleur_mouvement = None

        for mouvement, voisin in voisins:

            cout = calcul_cout(voisin)
            if mouvement not in liste_tabou or cout < meilleur_cout:

                if cout < meilleur_voisin_cout:
                    meilleur_voisin = voisin
                    meilleur_voisin_cout = cout
                    meilleur_mouvement = mouvement

        if meilleur_voisin is None:
            break

        solution_courante = meilleur_voisin

        # Ajouter le mouvement inverse dans la liste taboue
        inverse = (
            meilleur_mouvement[1],
            meilleur_mouvement[0]
        )

        liste_tabou.append(inverse)

        if len(liste_tabou) > taille_tabou:
            liste_tabou.pop(0)

        if meilleur_voisin_cout < meilleur_cout:

            meilleure_solution = [
                meilleur_voisin[0].copy(),
                meilleur_voisin[1].copy()
            ]

            meilleur_cout = meilleur_voisin_cout

        print(
            "Iteration", iteration + 1,
            "| Solution :", solution_courante,
            "| Cout :", calcul_cout(solution_courante)
        )

    return meilleure_solution,meilleur_cout

solution_initiale = [
    [4, 4, 0],
    [0, 1, 8]   
]

solution, cout = recherche_taboue(solution_initiale)

print("\nMeilleure solution :")

print("D1 :", solution[0])
print("D2 :", solution[1])

print("Cout minimal =", cout)



