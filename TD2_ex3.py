import random
import math

random.seed(42)
I = float("inf")

d = [
    [0, 14, 15, I, I, I, I, 17],
    [14, 0, 13, 14, 20, I, I, 21],
    [15, 13, 0, 11, 21, 17, 9, 9],
    [I, 14, 11, 0, 11, 10, 8, 20],
    [I, 20, 21, 11, 0, 15, 18, I],
    [I, I, 17, 10, 15, 0, 9, I],
    [I, I, 9, 8, 18, 9, 0, 13],
    [17, 21, 9, 20, I, I, 13, 0]
]

initiale = [1, 2, 3, 4, 5, 6, 7, 8]


def cout(s):
    total = 0
    for i in range(len(s)):
        a = s[i] - 1
        b = s[(i + 1) % len(s)] - 1
        total += d[a][b]
    return total


def echanger(s, i, j):
    v = s.copy()
    v[i], v[j] = v[j], v[i]
    return v


def tabou():
    s = initiale.copy()
    meilleur = s.copy()
    liste_tabou = []

    for k in range(30):
        voisins = []

        for i in range(1, 8):
            for j in range(i + 1, 8):
                v = echanger(s, i, j)

                if cout(v) != I:
                    if (i, j) not in liste_tabou or cout(v) < cout(meilleur):
                        voisins.append((cout(v), v, (i, j)))

        if not voisins:
            break

        _, s, mouvement = min(voisins, key=lambda x: x[0])

        liste_tabou.append(mouvement)
        if len(liste_tabou) > 3:
            liste_tabou.pop(0)

        if cout(s) < cout(meilleur):
            meilleur = s.copy()

    return meilleur


def recuit():
    s = initiale.copy()
    meilleur = s.copy()
    T = 20

    for k in range(5):
        voisins = []

        for i in range(1, 8):
            for j in range(i + 1, 8):
                v = echanger(s, i, j)
                if cout(v) != I:
                    voisins.append(v)

        if not voisins:
            break

        v = random.choice(voisins)
        delta = cout(v) - cout(s)

        if delta <= 0 or random.random() < math.exp(-delta / T):
            s = v

        if cout(s) < cout(meilleur):
            meilleur = s.copy()

        print("Itération", k + 1, "T =", round(T, 2),
              "Coût =", cout(s))

        T = T * 0.7

    return meilleur


def genetique():
    population = [initiale.copy()]

    while len(population) < 20:
        villes = list(range(2, 9))
        random.shuffle(villes)
        s = [1] + villes

        if cout(s) != I:
            population.append(s)

    for k in range(100):
        population.sort(key=cout)
        parents = population[:10]
        nouvelle = parents.copy()

        while len(nouvelle) < 20:
            p1, p2 = random.sample(parents, 2)

            enfant = p1[:4]
            for ville in p2:
                if ville not in enfant:
                    enfant.append(ville)
            
            if random.random() < 0.2:
                i, j = random.sample(range(1, 8), 2)
                enfant = echanger(enfant, i, j)

            if cout(enfant) != I:
                nouvelle.append(enfant)
            else:
                nouvelle.append(p1.copy())

        population = nouvelle

    return min(population, key=cout)

print("Solution initiale :", initiale + [1])
print("Coût initial :", cout(initiale))

s1 = tabou()
print("\nRecherche taboue :", s1 + [1])
print("Coût :", cout(s1))

print("\nRecuit simulé :")
s2 = recuit()
print("Meilleure solution :", s2 + [1])
print("Coût :", cout(s2))

s3 = genetique()
print("\nAlgorithme génétique :", s3 + [1])
print("Coût :", cout(s3))
