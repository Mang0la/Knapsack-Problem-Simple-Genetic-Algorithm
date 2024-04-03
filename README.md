# 22SP CS-4623 Evolutionary Computation Software Project
The Knapsack Problem is a problem where a set of _n_ items can be placed into a knapsack with a capacity of _C_. Each item _i_ has their own value _v_ and weight that takes up a capacity _c_. The objective of the algorithm is to maxmize the value _v_ within the knapsack without surpassing capacity _C_. This is to emulate the "survival of the fittest" evolutionary process.

**Overview**
- Chromosomes are represented as a binary string to indicate whether an item was accepted into the knapsack or not.
- There is a fitness function to determine the chromosomes' fitness value, which is done before operating on a population
- A population is selected through two choices: roulette or tournament.
  - Roulette will calculate the total fitness and group individuals by their relative fitness. A random number between 0 and 1 is generated and used to select the individuals that contain the random number based on the probability distribution 
  - Tournament pits two random individuals together and chooses a random number between 0 and 1. If the number is belowe 0.75 then the fitter individual is chosen, otherwise, the less fit one is chosen.
- From there, single-point or double-point is used to cross over individuals from differing populations to share chromosomal data.
- Lastly, mutations have a 5% chance of occurring within a population.
- The selection, crossover, and mutation process will repeat for 1000 cycles before stopping and presents the user with the results.
- Simulated Annealing only utilizes mutation functions within a population and chooses the more fit individual, with a chance of choosing the less fit individual.
- Foolish Hill Climbing is similar to Simulated Annealing but will never choose the less fit individual.
All of these choices are dictated from user input prompted within the console, including the probability of a mutation from the user.
