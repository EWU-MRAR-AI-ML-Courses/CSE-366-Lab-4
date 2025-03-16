# Vehicle Routing Problem (VRP): Detailed Algorithmic Solutions and Approach

## 1. Introduction

The Vehicle Routing Problem (VRP) is a fundamental optimization challenge in logistics and transportation. It involves determining the optimal set of routes for a fleet of vehicles to serve a set of customers (or delivery points) while minimizing the total travel cost (often measured in distance or time) and adhering to constraints such as vehicle capacity and route duration. This document details two algorithmic solutions to the VRP using local search techniques:

- **Simulated Annealing (SA) Approach**
- **Genetic Algorithm (GA) Approach**

Both approaches are implemented with a real-time visualization using Pygame, allowing users to observe the optimization process and monitor performance metrics such as temperature, fitness scores, and generation count.

## 2. Problem Statement

In VRP, the objective is to design optimal routes that:
- Start and end at a central depot.
- Visit each customer (or delivery point) exactly once.
- Minimize the overall travel distance (or time).
- Optionally, consider additional constraints (like vehicle capacity, delivery time windows, etc.).

For our implementations, the problem is simplified to focus on route optimization for a fixed number of vehicles with a set of delivery points randomly generated within a given area.

## 3. Proposed Approaches

### 3.1 Simulated Annealing Approach

#### Overview

Simulated Annealing (SA) is a probabilistic technique inspired by the annealing process in metallurgy. It iteratively refines a candidate solution by exploring neighboring solutions and accepts worse solutions with a probability that decreases over time (as the "temperature" cools). This mechanism helps the algorithm escape local optima in search of a global optimum.

#### Key Components

- **Initial Solution:**  
  A starting route is constructed by assigning delivery points to vehicles using an angle-based round-robin method. Each route is defined as:  
  **Route = Depot → (Assigned Delivery Points) → Depot**

- **Neighborhood Generation:**  
  A neighboring solution is produced by swapping two randomly selected delivery points in the route (excluding the depot).

- **Acceptance Criteria:**  
  If the new route has a shorter total distance (i.e., lower cost), it is accepted. If not, it may still be accepted with a probability based on the difference in cost and the current temperature (using the Metropolis criterion).

- **Cooling Schedule:**  
  The temperature is gradually reduced using a cooling factor (e.g., 0.995 per iteration) until it falls below a predefined threshold.

#### Implementation Details

- **Algorithm Pseudocode:**

  1. **Initialize** temperature \(T_0\) and generate an initial solution.
  2. **Repeat** until the temperature is low:
     - Generate a neighboring solution by swapping two delivery points.
     - Compute the change in route distance (\(\Delta\)).
     - If \(\Delta < 0\) (better solution), accept it.
     - Otherwise, accept the worse solution with probability \(e^{-\Delta / T}\).
     - Reduce the temperature: \(T \leftarrow T \times \text{cooling\_rate}\).
  3. **Output** the best route found.

- **Visualization:**  
  The SA process is shown in the top area of the Pygame window with live updates of the current route and the temperature.

### 3.2 Genetic Algorithm Approach

#### Overview

Genetic Algorithms (GA) are inspired by the process of natural selection. In GA, a population of candidate solutions evolves over generations through selection, crossover, and mutation. The fitness function evaluates how good each candidate is, guiding the evolution toward better solutions.

#### Key Components

- **Individual Representation:**  
  Each individual (or chromosome) represents a potential solution—a permutation of delivery points assigned to a vehicle. The complete route is defined as:  
  **Route = Depot → (Permutation of Delivery Points) → Depot**

- **Initial Population:**  
  A population of candidate solutions is generated randomly by shuffling the delivery points.

- **Fitness Function:**  
  The fitness of a solution is defined as the inverse of the total route distance.  
  **Fitness = \( \frac{1}{\text{Total Distance} + \epsilon} \)**  
  This ensures that shorter routes yield higher fitness values.

- **Genetic Operations:**
  - **Selection:**  
    Use tournament selection to choose parents based on fitness.
  - **Crossover:**  
    Apply order crossover (OX) to combine parent solutions and generate offspring.
  - **Mutation:**  
    Use swap mutation to introduce random changes and maintain genetic diversity.

- **Elitism:**  
  The best solution from each generation is carried over to the next generation to preserve high-quality solutions.

#### Implementation Details

- **Algorithm Pseudocode:**

  1. **Initialize** a population of candidate solutions.
  2. **Evaluate** fitness for each individual.
  3. **Repeat** for a fixed number of generations:
     - Select parent pairs using tournament selection.
     - Generate offspring via crossover and apply mutation.
     - Replace the population (with elitism to preserve the best solution).
     - Update generation count and record fitness metrics.
  4. **Output** the best route for each vehicle.

- **Visualization:**  
  The GA process is displayed in the top area of the Pygame window with real-time updates of the generation count, maximum fitness, and average fitness for each vehicle. Once the GA completes, the best routes are animated as moving vehicles in the bottom area.

## 4. Implementation and Visualization

The project is divided into three primary modules:

- **agent.py:**  
  Contains the implementations for the VRP solvers:
  - The `RouteGASolver` class for the Genetic Algorithm.
  - The `VRPAgentGenetic` class that partitions delivery points and creates a GA solver for each vehicle.
  - (Similarly, a separate module for SA is available if needed.)

- **environment.py:**  
  Generates the simulation environment with a depot (centered) and a set of randomly placed delivery points.

- **run.py:**  
  Implements the visualization using Pygame:
  - **Left Side:** Divided into two areas:
    - **Top Area:** Shows the evolving solution from the GA or SA process with dynamic fitness and generation metrics.
    - **Bottom Area:** Displays the final routes with animated vehicle movement.
  - **Right Panel:** Provides a detailed description of the VRP, instructions, and real-time algorithm metrics.  
    The panel also explains the fitness function calculation:
    - **Total Distance:** The sum of distances from the depot to the first delivery, between consecutive deliveries, and from the last delivery back to the depot.
    - **Fitness Calculation:** \( \text{Fitness} = \frac{1}{\text{Total Distance} + \epsilon} \), where \(\epsilon\) is a small constant to avoid division by zero.

## 5. Experimental Setup

- **Environment:**  
  The depot is set at the center of the simulation window. Delivery points are generated within defined margins.

- **Parameters:**
  - **Simulated Annealing:**  
    - Initial Temperature: e.g., 10,000  
    - Cooling Rate: e.g., 0.995  
    - Minimum Temperature: e.g., \(1 \times 10^{-8}\)
  - **Genetic Algorithm:**  
    - Population Size: e.g., 100  
    - Mutation Rate: e.g., 0.02  
    - Number of Generations: e.g., 200

- **Vehicles:**  
  The number of vehicles is fixed (e.g., 3) and each vehicle's route is optimized separately.

## 6. Results and Observations

- **Simulated Annealing:**  
  The SA approach provides a gradual refinement of the solution. The temperature decreases over time, reducing the likelihood of accepting worse solutions and converging to a local optimum.

- **Genetic Algorithm:**  
  The GA approach evolves a population of solutions, with metrics such as generation count, maximum fitness, and average fitness displayed in the right panel. The GA converges over a fixed number of generations, and the best routes are visualized and animated.

- **Visualization:**  
  Both approaches use a two-part layout (process visualization on the top and final path simulation on the bottom) and a detailed right panel. This allows users to observe the evolution of the solution and understand how algorithm parameters impact the optimization process.

## 7. Conclusion

The VRP is a challenging and practical optimization problem. By applying local search methods like Simulated Annealing and Genetic Algorithms, we can effectively approximate high-quality solutions. The detailed visualization provided in this project helps illustrate the inner workings of these algorithms, including how solutions evolve over time and how fitness is calculated and improved.

This document has described the algorithmic details and the overall approach used to solve the VRP. Future work could involve incorporating additional constraints (e.g., vehicle capacity, time windows) and comparing the performance of various local search methods on larger and more complex instances.

