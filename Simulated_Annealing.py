#Importing the required libraries
from random import random
from random import choices, choice, randint, randrange
from functools import partial
import math


class Chromosome:
    def __init__(this, value, weight):
        this.value = value
        this.weight = weight


#defining all of the functions

def generate_chromosome(length):
    return choices([0, 1], k=length)


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


def pairwise_exchange(chromosome):
    allele1 = randrange(len(chromosome))
    allele2 = randrange(len(chromosome))

    mod_chromosome = list(chromosome)

    temp = mod_chromosome[allele1]
    mod_chromosome[allele1] = mod_chromosome[allele2]
    mod_chromosome[allele2] = temp

    return mod_chromosome


def cycle_of_three(chromosome):

    allele1 = randrange(len(chromosome))
    allele2 = randrange(len(chromosome))
    allele3 = randrange(len(chromosome))

    mod_chromosome = list(chromosome)

    temp = mod_chromosome[allele1]
    mod_chromosome[allele1] = mod_chromosome[allele2]
    mod_chromosome[allele2] = mod_chromosome[allele3]
    mod_chromosome[allele3] = temp

    return mod_chromosome


def run_evolution(
        populate_func,
        fitness_func,
        mutation_func,
        fit_freq_print,
        generation_limit
):

    while True:
        population = populate_func()
        fitness_vals = [fitness_func(chromosome) for chromosome in population]

        if not all(x == 0 for x in fitness_vals):
            break

    population = sorted(population,
                        key=lambda chromosome: fitness_func(chromosome),
                        reverse=True)

    s = population[0]
    t = 100
    iter = 100

    for i in range(generation_limit):
        for j in range(int(iter)):
            next_generation = []
            for k in range(len(population)):
                next_generation += [mutation_func(population[k])]

            population = next_generation

            s_new = sorted(population,
                           key=lambda chromosome: fitness_func(chromosome),
                           reverse=True)[0]

            if fitness_func(s_new) > fitness_func(s) or (random() < math.e ** ((fitness_func(s_new) - fitness_func(s))/t)):
                s = s_new

        t = 0.99*t
        iter = .99*iter

        if i % fit_freq_print == 0:
            print(f"Generation {i}: {fitness_func(s)}")

    return s


# Importing data sets
def data_read():
    filename = input('Enter a filename:')
    max_weight = 0
    weights = []
    values = []

    try:
        with open(filename, 'r') as fileH:
            max_weight = int(fileH.readline())
            weights = [int(x) for x in fileH.readline().split(" ")]
            values = [int(x) for x in fileH.readline().split(" ")]

        for i in range(len(weights)):
            item_weight = weights[i]
            item_value = values[i]
            alleles.append(Chromosome(item_value, item_weight))

        return max_weight

    except FileNotFoundError:
        print("[Errno 2] No such file or directory: '%s'" % filename)


if __name__ == "__main__":

    # Thing = namedtuple('Thing',['value','weight'])
    alleles = []
    weight_limit = data_read()
    generation_limit = 1000

    inp_mutation_func = input("pairwise_exchange (p) or cycle_of_three (c)\n")
    fit_freq_print = int(input("After how many generations do you want to see the best fitness value?\n"))

    if inp_mutation_func == "p":
        mutation_func = pairwise_exchange
    else:
        mutation_func = cycle_of_three

    solution = run_evolution(
        populate_func=partial(generate_population, size=5*len(alleles), chromosome_length=len(alleles)),
        fitness_func=partial(fitness, alleles=alleles, weight_limit=weight_limit),
        mutation_func=mutation_func,
        fit_freq_print=fit_freq_print,
        generation_limit=generation_limit
    )

    print(f"\nNumber of generations: {generation_limit}")
    print(f"Best solution: {solution}")
    print(f"Value: {fitness(solution, alleles, weight_limit)}")