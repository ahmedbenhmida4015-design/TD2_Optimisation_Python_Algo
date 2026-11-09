import random
capacites = [20, 15, 35, 40, 15, 15, 10]
demandes = [80, 90, 65, 70]
genes = [
    ["1100", "0110", "0011"],
    ["1100", "0110", "0011"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"]
]

population = []
for i in range(42):
    chromosome = []
    for j in range(7):
        gene = random.choice(genes[j])
        chromosome.append(gene)
    population.append(chromosome)

for generation in range(100):
    scores = []
    for chromosome in population:
        reserves = []
        for i in range(4):
            maintenance = 0
            for j in range(7):
                if chromosome[j][i] == "1":
                    maintenance = maintenance + capacites[j]
            reserve = 150 - maintenance - demandes[i]
            reserves.append(reserve)
        performance = min(reserves)
        if performance < 0:
            performance = 0
        scores.append([performance, chromosome])
    scores.sort(reverse=True)
    nouvelle_population = []

    nouvelle_population.append(scores[0][1])
    nouvelle_population.append(scores[1][1])

    while len(nouvelle_population) < 42:
        parent1 = random.choice(scores[:21])[1]
        parent2 = random.choice(scores[:21])[1]
        point = random.randint(1, 6)
        enfant1 = parent1[:point] + parent2[point:]
        enfant2 = parent2[:point] + parent1[point:]

        for i in range(7):
            if random.random() < 0.1:
                enfant1[i] = random.choice(genes[i])

        for i in range(7):
            if random.random() < 0.1:
                enfant2[i] = random.choice(genes[i])
        nouvelle_population.append(enfant1)

        if len(nouvelle_population) < 42:

            nouvelle_population.append(enfant2)

    population = nouvelle_population
    print("Generation :", generation + 1)
    print("Meilleure performance :", scores[0][0]) 
    scores = []

for chromosome in population:
    reserves = []
    for i in range(4):
        maintenance = 0
        for j in range(7):
            if chromosome[j][i] == "1":
                maintenance = maintenance + capacites[j]
        reserve = 150 - maintenance - demandes[i]
        reserves.append(reserve)
    performance = min(reserves)

    if performance < 0:
        performance = 0
    scores.append([performance, chromosome])

scores.sort(reverse=True)
print("\n===== RESULTAT FINAL =====")
print("Meilleur chromosome :")
for i in range(7):
    print("Centrale", i + 1, ":", scores[0][1][i])
print("Performance :", scores[0][0])