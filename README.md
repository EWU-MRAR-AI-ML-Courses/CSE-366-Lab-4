# Task Scheduling Visualization with Genetic Algorithm

This project implements a Genetic Algorithm (GA) to optimize the assignment of multiple robots to a set of tasks in a dynamic production environment. It aims to minimize the total production time, balance the workload among robots, and prioritize critical tasks effectively. The project includes a detailed visualization using Pygame to illustrate the final task assignments, robot efficiencies, and task priorities.

# Objective
The goal of this project is to develop and implement a Genetic Algorithm to optimize task assignments in a production environment. The primary objectives are:

* Minimize Total Production Time: Reduce the maximum time taken by any robot to complete its assigned tasks.
* Balance Workload: Ensure an even distribution of tasks among robots to prevent bottlenecks.
Prioritize Critical Tasks: Assign higher priority tasks appropriately to meet production goals.

# Features
* Dynamic Production Environment: Simulates tasks with varying durations and priorities, and robots with different efficiency factors.
* Genetic Algorithm Optimization: Implements GA components including individual representation, fitness function, selection, crossover, and mutation.
* Visualization: Provides a real-time graphical representation of task assignments using Pygame, highlighting robot efficiencies, task durations, and priorities.
* Real-Time Updates: Displays generation count and best fitness scores, updating after each generation of the GA.
# Assignment Details
## Background
* Tasks: Each task has a specified duration (in hours) and a priority level.
* Robots: Each robot has a unique efficiency factor influencing how quickly it can complete tasks.
* Dynamic Environment: Tasks and their priorities can change over time, simulating a real-world production scenario.
## Tasks
### Data Preparation
Generate mock data for tasks and robots:

```import numpy as np

# Generate mock data
task_durations = np.random.randint(1, 11, size=10)       # Task durations (1 to 10 hours)
task_priorities = np.random.randint(1, 6, size=10)       # Task priorities (1 to 5)
robot_efficiencies = np.random.uniform(0.5, 1.5, size=5) # Robot efficiencies (0.5x to 1.5x)
```

* Task Durations: Randomly assigned durations between 1 and 10 hours.
* Task Priorities: Random priority levels between 1 (lowest) and 5 (highest).
* Robot Efficiencies: Random efficiency factors between 0.5 (50% efficiency) and 1.5 (150% efficiency).
### GA Implementation
Implement the Genetic Algorithm to optimize task assignments:

```
# Initialize GA parameters

population_size = 50
n_generations = 100
mutation_rate = 0.1 

# Create initial population
population = [np.random.randint(0, len(robot_efficiencies), size=len(task_durations)) for _ in range(population_size)]
```

* Population Size: The number of individuals (possible solutions) in each generation.
* Number of Generations: Total iterations the GA will perform to evolve solutions.
* Mutation Rate: Probability of mutation for each gene in an individual.

### Visualization
Create a grid visualization of the task assignments highlighting key information:

* Grid Representation: Rows represent robots, columns represent tasks.
* Color Coding: Cells are colored based on task durations; assigned tasks are highlighted.
* Annotations: Display task priorities and durations within each cell.
* Robot Efficiencies: Displayed alongside each robot row.
## Genetic Algorithm Components
### Individual Representation
Each individual in the population represents a potential task assignment solution:

* Representation: An array/vector where each element corresponds to a task and contains the ID of the assigned robot.
Example:

```
# Individual representation
I = [r0, r1, r2, ..., rN]
# Where rN is the robot assigned to task N
```
### Fitness Function
The fitness function evaluates how good each individual solution is:

* Total Production Time (T_total): Calculated as the maximum time taken by any robot to complete its assigned tasks.
* Workload Balance (B): The standard deviation of the total times across all robots, promoting balanced task distribution.
* Fitness Function (F): Combines total production time and workload balance, incorporating task priorities to penalize delays in high-priority tasks.

Calculation:

```
def fitness(individual):
    robot_times = np.zeros(len(robot_efficiencies))
    for task_idx, robot_idx in enumerate(individual):
        duration = task_durations[task_idx]
        priority = task_priorities[task_idx]
        efficiency = robot_efficiencies[robot_idx]
        # Effective time considering efficiency and priority
        effective_time = (duration / efficiency) * priority
        robot_times[robot_idx] += effective_time
    T_total = np.max(robot_times)
    B = np.std(robot_times)
    F = T_total + B  # Fitness value to minimize
    return F
```

* Objective: Minimize F to find the optimal task assignment.
### Selection, Crossover, and Mutation
Implement genetic operations to evolve the population:

* Selection: Choose the fittest individuals to be parents for the next generation.
```
def selection(population):
    # Select the top half individuals based on fitness
    sorted_population = sorted(population, key=fitness)
    return sorted_population[:len(population) // 2]
```

* Crossover: Combine pairs of parent individuals to create offspring.
```
def crossover(parent1, parent2):
    # Single-point crossover
    point = np.random.randint(1, len(parent1) - 1)
    child = np.concatenate([parent1[:point], parent2[point:]])
    return child
```
* Mutation: Introduce random changes to offspring to maintain genetic diversity.
```
def mutate(individual):
    for i in range(len(individual)):
        if np.random.rand() < mutation_rate:
            individual[i] = np.random.randint(0, len(robot_efficiencies))
    return individual
```
# Installation
1. Clone the repository:

```
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

2. Set up a virtual environment (optional but recommended):

```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install the required dependencies:

```
pip install -r requirements.txt
```
If a requirements.txt file is not provided, install dependencies manually:
```
pip install pygame numpy
```
## Usage
Run the main script to start the visualization:
```
python run.py
```
A Pygame window will open, displaying the task assignment grid and updates on the genetic algorithm's progress.

### Controls
* Exit: Close the Pygame window by clicking the close button to exit the application.

## Project Structure
* run.py: The main script that initializes the environment, runs the genetic algorithm, and handles the visualization.
* agent.py: Contains the Agent class, representing a robot agent with an efficiency factor and methods for task management.
* environment.py: Defines the Environment class that sets up tasks and robots, and provides methods for generating initial assignments and drawing the visualization grid.

# Customization
You can modify various parameters in run.py to customize the simulation according to your needs:

* Number of Tasks: Adjust num_tasks to change the total number of tasks in the simulation.
* Number of Robots: Change num_robots to modify the number of robots available for task assignment.

* Genetic Algorithm Parameters:
*> population_size: The size of the population in each generation.
*> mutation_rate: The probability of mutation for each gene in an individual.
*> n_generations: The total number of generations to run the genetic algorithm.
*> generation_delay: The delay in milliseconds between each generation for visualization purposes.
