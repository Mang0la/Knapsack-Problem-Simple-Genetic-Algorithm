#Importing the required libraries
from random import random
from random import choices, choice, randint, randrange
from functools import partial


class Chromosome:
    def __init__(this, value, weight):
        this.value = value
        this.weight = weight


#defining all of the functions

def generate_chromosome(length):
    return choices( [ 0, 1 ], k = length )


def generate_population(size, chromosome_length):
    return [generate_chromosome(chromosome_length) for _ in range(size)]


def fitness(chromosome, alleles, weight_limit):
    if len(chromosome) != len(alleles):
        raise ValueError("Chromosome and Things must be of same length")

    weight = 0
    value = 0
    for i, allele in enumerate(alleles):
        if chromosome[i] == 1:
            weight += int(allele.weight)
            value += int(allele.value)

            if weight > weight_limit:
                return 0

    return value


def roulette_selection(population, fitness_func):

    return choices(population=population,
                   weights=[fitness_func(chromosome) for chromosome in population],
                   k=2)


def tournament_selection(population, fitness_func):

    parents = []

    for i in range(0, 2):
        c1 = choice(population)
        c2 = choice(population)
        k = 0.75
        r = random()

        if r < k:
            if fitness_func(c1) > fitness_func(c2):
                parents.append(c1)
            else:
                parents.append(c2)

        else:
            if fitness_func(c1) > fitness_func(c2):
                parents.append(c2)
            else:
                parents.append(c1)

    return parents[0], parents[1]


def single_point_crossover(a, b):
    if len(a) != len(b):
        raise ValueError("Chromosomes a and b need to be of the same length")

    length = len(a)
    if length < 2:
        return a,b

    p = randint(1,length-1)
    return a[:p] + b[p:] , b[:p] + a[p:]


def double_point_crossover (a, b):
    if len(a) != len(b):
        raise ValueError("Chromosomes a and b need to be of the same length")

    length = len(a)

    if length < 2:
        return a, b

    point1 = randint(1, length - 1)
    point2 = randint(1, length - 1)

    if point1 < point2:
        return a[:point1] + b[point1:point2] + a[point2:], b[:point1] + a[point1:point2] + b[point2:]
    else:
        return a[:point2] + b[point2:point1] + a[point1:], b[:point2] + a[point2:point1] + b[point1:]


def pairwise_exchange(chromosome, rate):

    mod_chromosome = list(chromosome)
    if random() <= rate:
        allele1 = randrange(len(mod_chromosome))
        allele2 = randrange(len(mod_chromosome))

        temp = mod_chromosome[allele1]
        mod_chromosome[allele1] = mod_chromosome[allele2]
        mod_chromosome[allele2] = temp

    return mod_chromosome


def cycle_of_three(chromosome, rate):

    mod_chromosome = list(chromosome)
    if random() <= rate:
        allele1 = randrange(len(mod_chromosome))
        allele2 = randrange(len(mod_chromosome))
        allele3 = randrange(len(mod_chromosome))

        temp = mod_chromosome[allele1]
        mod_chromosome[allele1] = mod_chromosome[allele2]
        mod_chromosome[allele2] = mod_chromosome[allele3]
        mod_chromosome[allele3] = temp

    return mod_chromosome


def run_evolution(
        populate_func,
        fitness_func,
        selection_func,
        crossover_func,
        mutation_func,
        mutation_rate,
        fit_freq_print,
        generation_limit
):

    while True:
        population = populate_func()
        fitness_vals = [fitness_func(chromosome) for chromosome in population]

        if not all(x == 0 for x in fitness_vals):
            break

    for i in range(generation_limit):

        #Elitism
        #sorts the population in ascending order
        population = sorted(population,
                            key= lambda chromosome: fitness_func(chromosome),
                            reverse= True)

        #chooses the first two in the population in ascending order to the next generation
        next_generation = population[:2]

        for j in range(int(len(population)/2)-1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a, mutation_rate)
            offspring_b = mutation_func(offspring_b, mutation_rate)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

        fitness_vals = [fitness_func(chromosome) for chromosome in population]

        if i % fit_freq_print == 0:
            print(f"Generation {i}: {max(fitness_vals)}")

    population = sorted(population,
                        key=lambda chromosome: fitness_func(chromosome),
                        reverse=True)

    return population, i


#Importing data sets
def data_read():
    filename = input('Enter a filename:')
    max_weight = 0
    weights = []
    values = []

    try:
        with open (filename, 'r') as fileH:
            max_weight = int(fileH.readline())
            weights = [int(x) for x in fileH.readline().split(" ")]
            values = [int(x) for x in fileH.readline().split(" ")]

        for i in range(len(weights)):
            item_weight = weights[i]
            item_value = values[i]
            alleles.append(Chromosome(item_value, item_weight))

        return max_weight

    except FileNotFoundError:
        print("[Errno 2] No such file or directory: '%s'" %( filename ))


if __name__ == "__main__":

    # Thing = namedtuple('Thing',['value','weight'])
    alleles = []
    weight_limit = data_read()


    inp_selection_func = input("roulette_selection (r) or tournament_selection (t)\n")
    inp_crossover_func = input("single_point_crossover (s) or double_point_crossover (d)\n")
    inp_mutation_func = input("pairwise_exchange (p) or cycle_of_three (c)\n")
    mutation_rate = float(input("What do you want the mutation rate (Recommend 0.05)\n"))
    fit_freq_print = int(input("After how many generations do you want to see the best fitness value?\n"))

    if inp_selection_func == "r":
        selection_func = roulette_selection
    else:
        selection_func = tournament_selection

    if inp_crossover_func == "s":
        crossover_func = single_point_crossover
    else:
        crossover_func = double_point_crossover

    if inp_mutation_func == "p":
        mutation_func = pairwise_exchange
    else:
        mutation_func = cycle_of_three

    population, generations = run_evolution(
        populate_func=partial(generate_population, size = 5*len(alleles), chromosome_length = len(alleles)),
        fitness_func=partial(fitness, alleles = alleles, weight_limit = weight_limit),
        selection_func=selection_func,
        crossover_func=crossover_func,
        mutation_func=mutation_func,
        mutation_rate=mutation_rate,
        fit_freq_print=fit_freq_print,
        generation_limit=1000
    )

    print(f"\nNumber of generations: {generations}")
    print(f"Best solution: {population[0]}")
    print(f"Value: {fitness(population[0], alleles, weight_limit)}")