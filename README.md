
# Local Search

This repository presents three problem solutions using local search techniques:
1. **Vehicle Routing Problem (VRP) – Simulated Annealing:**  
   Optimizes routes for a fleet of vehicles delivering goods by iteratively refining a solution using simulated annealing.
2. **Vehicle Routing Problem (VRP) – Genetic Algorithm:**  
   Uses a genetic algorithm to evolve optimal routes for vehicles, visualizing fitness and route evolution over generations.
3. **Task Scheduling Optimization:**  
   Implements a Genetic Algorithm to optimize task assignments for multiple robots in a dynamic production environment to minimize total production time, balance workload, and prioritize critical tasks.

---

## Objective

The goal of these projects is to explore different local search methods (Simulated Annealing and Genetic Algorithms) to solve complex optimization problems. Specifically, the objectives are:

- **VRP Solutions:**  
  - Determine optimal routes for a fleet of vehicles (starting and ending at a central depot) that visit all delivery points.
  - Minimize the total distance traveled (or total production time in a task scheduling context) while balancing the workload.
  
- **Task Scheduling Optimization:**  
  - Minimize total production time.
  - Balance task assignments among robots.
  - Prioritize high-priority tasks to meet production goals.

---

## Features

- **Dynamic Environment:**  
  Simulates delivery points and tasks with varying durations, priorities, and robot efficiencies.
  
- **Local Search Optimization:**  
  - **Simulated Annealing:** Gradually cools the solution space to escape local minima in VRP.
  - **Genetic Algorithm:** Evolves candidate solutions over generations for VRP and task scheduling.
  
- **Visualization:**  
  Uses Pygame to provide a real-time graphical representation:
  - For VRP (SA and GA): Displays evolving routes, best solutions per generation, and dynamic fitness metrics.
  - For Task Scheduling: Visualizes the task assignment grid, robot efficiencies, and task priorities.
  
- **Real-Time Metrics:**  
  The right-side panel displays detailed metrics such as generation count, maximum and average fitness values, and explanations of fitness calculations.

---

## Assignment Details

### Background

- **VRP:**  
  The Vehicle Routing Problem involves determining the most efficient routes for vehicles starting and ending at a central depot while visiting a set of delivery points. Constraints (e.g., vehicle capacity, time windows) may also be considered.

- **Task Scheduling:**  
  Each task is defined by a duration and priority, and each robot has an efficiency factor. The objective is to assign tasks such that total production time is minimized, workload is balanced, and critical tasks are prioritized.

### Data Preparation

For the task scheduling problem, mock data can be generated as follows:

```python
import numpy as np

# Generate mock data for task scheduling
task_durations = np.random.randint(1, 11, size=10)       # Task durations (1 to 10 hours)
task_priorities = np.random.randint(1, 6, size=10)         # Task priorities (1 to 5)
robot_efficiencies = np.random.uniform(0.5, 1.5, size=5)   # Robot efficiencies (0.5x to 1.5x)
```

---

## Genetic Algorithm Implementation (for Task Scheduling and VRP)

### Individual Representation

Each individual represents a possible solution:
- **For Task Scheduling:**  
  An array where each element corresponds to a task and contains the ID of the assigned robot.
  
- **For VRP (GA):**  
  A permutation of delivery points assigned to a vehicle (the complete route is: depot → deliveries → depot).

### Fitness Function

**VRP Example:**

```python
def fitness(route):
    # Calculate the total distance (depot -> route -> depot)
    total_distance = distance(depot, route[0]) + \
                     sum(distance(route[i], route[i+1]) for i in range(len(route)-1)) + \
                     distance(route[-1], depot)
    return 1 / (total_distance + 1e-6)  # Higher fitness for shorter routes
```

**Task Scheduling Example:**

```python
def fitness(individual):
    robot_times = np.zeros(len(robot_efficiencies))
    for task_idx, robot_idx in enumerate(individual):
        duration = task_durations[task_idx]
        priority = task_priorities[task_idx]
        efficiency = robot_efficiencies[robot_idx]
        effective_time = (duration / efficiency) * priority  # Time weighted by priority and efficiency
        robot_times[robot_idx] += effective_time
    T_total = np.max(robot_times)
    B = np.std(robot_times)
    F = T_total + B  # Fitness to minimize
    return F
```

*Objective:* Minimize the fitness value (or maximize its inverse for VRP).

### Selection, Crossover, and Mutation

- **Selection:**  
  Selects the fittest individuals (e.g., using tournament selection or sorting).

- **Crossover:**  
  Combines parts of two parent solutions (e.g., single-point or order crossover for VRP).

- **Mutation:**  
  Introduces random changes to maintain diversity (e.g., swap mutation).

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Set Up a Virtual Environment (Optional but Recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
   If no `requirements.txt` is provided, install manually:
   ```bash
   pip install pygame numpy
   ```

---

## Usage

Run the main script to start the visualization:

```bash
python run.py
```

A Pygame window will open, displaying:
- **Top Area (Left):**  
  The GA or SA process visualization (routes evolving, fitness metrics updating).
- **Bottom Area (Left):**  
  The final optimized routes with animated vehicles (for VRP solutions).
- **Right Panel:**  
  Detailed problem description, instructions, and real-time GA metrics (generation, max fitness, average fitness) along with fitness calculation details.

### Controls

- **Start GA/SA Simulation:**  
  Click the "Solve VRP" button in the top area to start the optimization.
  
- **Start Vehicle Simulation:**  
  After the GA/SA process completes, click the "Start Simulation" button in the bottom area to animate the vehicles.
  
- **Exit:**  
  Close the Pygame window to exit the application.

---

## Project Structure

- **run.py:**  
  The main script that initializes the environment, runs the optimization algorithm (GA and SA for VRP, and task scheduling), and handles the visualization.
- **agent.py:**  
  Contains the algorithm implementations (both Genetic Algorithm and Simulated Annealing for VRP, as well as task scheduling optimization methods).
- **environment.py:**  
  Defines the environment for tasks, deliveries, and robots. It generates the depot, tasks, and delivery points.
- **README.md:**  
  This file, providing an overview of the project, objectives, and usage instructions.

---

## Customization

You can modify various parameters in the code to tailor the simulation:

- **Number of Tasks/Deliveries:**  
  Adjust the values in the environment.
  
- **Number of Robots/Vehicles:**  
  Modify the corresponding parameters to change available resources.
  
- **Genetic Algorithm Parameters:**
  - `population_size`
  - `mutation_rate`
  - `n_generations` (or `max_generations`)
  - `generation_delay` (if you add delays for visualization)

- **Optimization Method:**  
  Switch between Simulated Annealing and Genetic Algorithm solutions by running the respective module.

---

This repository demonstrates multiple local search solutions, showcasing how different algorithms can be applied to solve optimization problems in real-time with visualization.

Happy coding and optimizing!
