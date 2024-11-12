import pygame
from agent import Agent
from environment import Environment
import numpy as np
import random

# Initialize Pygame
pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800  # Increased height to accommodate updates below the grid
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Task Assignment Visualization")
font = pygame.font.Font(None, 24)

# Environment setup
num_tasks = 10
num_robots = 5
environment = Environment(num_tasks, num_robots)
task_assignments = environment.generate_assignments()

# Initialize agents
agents = [Agent(id=i, efficiency=environment.robot_efficiencies[i]) for i in range(num_robots)]

# Genetic Algorithm parameters
population_size = 50
mutation_rate = 0.1
n_generations = 10
generation_delay = 1000  # Delay (milliseconds) between each generation for visualization

# Updates list to display below the grid
updates = []
max_updates = 5  # Max number of updates to display at once

# Genetic Algorithm functions
def fitness(individual):
    robot_times = np.zeros(num_robots)
    for task, robot in enumerate(individual):
        duration = environment.task_durations[task]
        priority = environment.task_priorities[task]
        robot_times[robot] += duration / agents[robot].efficiency * priority
    total_time = np.max(robot_times)
    workload_balance = np.std(robot_times)
    return total_time + workload_balance

def selection(population):
    return sorted(population, key=fitness)[:population_size // 2]

def crossover(parent1, parent2):
    point = random.randint(1, num_tasks - 1)
    return np.concatenate([parent1[:point], parent2[point:]])

def mutate(individual):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, num_robots - 1)
    return individual

# Initialize population
population = environment.generate_assignments()

# Visualization loop
running = True
best_solution = None
best_fitness = float('inf')
generation_count = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Genetic Algorithm step-by-step per generation
    selected = selection(population)
    next_generation = []
    while len(next_generation) < population_size:
        parent1, parent2 = random.sample(selected, 2)
        child = crossover(parent1, parent2)
        next_generation.append(mutate(child))
    
    # Update population with next generation
    population = next_generation

    # Find the best solution in the current generation
    current_best = min(population, key=fitness)
    current_fitness = fitness(current_best)
    if current_fitness < best_fitness:
        best_fitness = current_fitness
        best_solution = current_best

    # Draw current generation's best solution on the grid
    environment.draw_grid(screen, font, current_best)

    # Display generation and fitness info on the right panel
    generation_text = font.render(f"Generation: {generation_count + 1}", True, (0, 0, 0))
    fitness_text = font.render(f"Best Fitness: {best_fitness:.2f}", True, (0, 0, 0))
    screen.blit(generation_text, (SCREEN_WIDTH - 200, 50))
    screen.blit(fitness_text, (SCREEN_WIDTH - 200, 80))

    # Add update for the current generation to the updates list
    update_text = f"Generation {generation_count + 1}: Best Fitness = {best_fitness:.2f}"
    updates.append(update_text)
    if len(updates) > max_updates:
        updates.pop(0)  # Remove the oldest update if we exceed the display limit

    # Display the list of updates below the grid
    update_start_y = 650  # Starting Y position below the grid
    for i, update in enumerate(updates):
        update_surface = font.render(update, True, (0, 0, 0))
        screen.blit(update_surface, (50, update_start_y + i * 25))

    pygame.display.flip()
    pygame.time.delay(generation_delay)

    generation_count += 1
    if generation_count >= n_generations:
        break

# Keep window open after completion
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
