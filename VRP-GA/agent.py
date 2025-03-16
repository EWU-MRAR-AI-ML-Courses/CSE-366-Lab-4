import random
import math

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

class RouteGASolver:
    """
    Solves a single route optimization problem using a genetic algorithm.
    The candidate solution is a permutation of the delivery points assigned to a vehicle.
    The complete route is assumed to be: depot -> candidate permutation -> depot.
    """
    def __init__(self, depot, route_points, population_size=100, mutation_rate=0.01):
        self.depot = depot
        self.route_points = route_points[:]  # list of delivery points for this vehicle
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = []
        self.fitness_values = []
        self.best_solution = None
        self.best_fitness = 0
        self.generation = 0
        self.initialize_population()
        self.evaluate_population()  # Evaluate initial population so best_solution is set
    
    def initialize_population(self):
        base = self.route_points[:]
        for _ in range(self.population_size):
            candidate = base[:]
            random.shuffle(candidate)
            self.population.append(candidate)
    
    def total_distance(self, route):
        """Compute total route distance: depot -> route -> depot."""
        d = distance(self.depot, route[0])
        for i in range(len(route) - 1):
            d += distance(route[i], route[i+1])
        d += distance(route[-1], self.depot)
        return d
    
    def fitness(self, route):
        """Define fitness as the inverse of the route distance."""
        d = self.total_distance(route)
        return 1.0 / (d + 1e-6)
    
    def evaluate_population(self):
        self.fitness_values = []
        for candidate in self.population:
            fit = self.fitness(candidate)
            self.fitness_values.append(fit)
        self.best_fitness = max(self.fitness_values)
        best_index = self.fitness_values.index(self.best_fitness)
        self.best_solution = self.population[best_index]
    
    def select_parent(self):
        """Tournament selection."""
        tournament_size = 5
        selected = random.sample(list(zip(self.population, self.fitness_values)), tournament_size)
        selected.sort(key=lambda x: x[1], reverse=True)
        return selected[0][0]
    
    def crossover(self, parent1, parent2):
        """Order crossover (OX)"""
        size = len(parent1)
        child = [None] * size
        a, b = sorted(random.sample(range(size), 2))
        child[a:b+1] = parent1[a:b+1]
        pos = (b + 1) % size
        for gene in parent2:
            if gene not in child:
                child[pos] = gene
                pos = (pos + 1) % size
        return child
    
    def mutate(self, candidate):
        """Swap mutation"""
        for i in range(len(candidate)):
            if random.random() < self.mutation_rate:
                j = random.randint(0, len(candidate) - 1)
                candidate[i], candidate[j] = candidate[j], candidate[i]
        return candidate
    
    def next_generation(self):
        new_population = []
        self.evaluate_population()
        # Elitism: preserve the best candidate
        new_population.append(self.best_solution[:])
        while len(new_population) < self.population_size:
            parent1 = self.select_parent()
            parent2 = self.select_parent()
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child)
        self.population = new_population
        self.generation += 1
    
    def run_generation(self):
        self.next_generation()
        self.evaluate_population()

class VRPAgentGenetic:
    """
    Solves the VRP by partitioning the delivery points among a fixed number of vehicles
    and creating one RouteGASolver per vehicle.
    """
    def __init__(self, depot, deliveries, num_vehicles, population_size=100, mutation_rate=0.01):
        self.depot = depot
        self.deliveries = deliveries[:]
        self.num_vehicles = num_vehicles
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.partitions = self.partition_deliveries()
        self.solvers = []
        for part in self.partitions:
            solver = RouteGASolver(depot, part, population_size, mutation_rate)
            self.solvers.append(solver)
    
    def partition_deliveries(self):
        """Sort deliveries by angle from the depot and assign them round-robin."""
        points_with_angle = []
        for point in self.deliveries:
            dx = point[0] - self.depot[0]
            dy = point[1] - self.depot[1]
            angle = math.atan2(dy, dx)
            points_with_angle.append((point, angle))
        points_with_angle.sort(key=lambda x: x[1])
        partitions = [[] for _ in range(self.num_vehicles)]
        for i, (point, angle) in enumerate(points_with_angle):
            partitions[i % self.num_vehicles].append(point)
        return partitions
    
    def run_generation(self):
        for solver in self.solvers:
            solver.run_generation()
    
    def get_best_routes(self):
        routes = []
        for solver in self.solvers:
            best = solver.best_solution
            # Complete route: depot -> best solution -> depot
            route = [self.depot] + best + [self.depot]
            routes.append(route)
        return routes
    
    def get_generation_info(self):
        info = []
        for solver in self.solvers:
            avg_fit = sum(solver.fitness_values) / len(solver.fitness_values)
            info.append({
                "generation": solver.generation,
                "max_fitness": solver.best_fitness,
                "avg_fitness": avg_fit
            })
        return info
