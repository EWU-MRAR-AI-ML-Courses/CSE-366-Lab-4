import math
import random

class VRPAgentSimulatedAnnealing:
    def __init__(self, depot, deliveries, num_vehicles, 
                 initial_temp=10000, cooling_rate=0.995, min_temp=1e-8):
        """
        depot: tuple (x, y) for the depot location.
        deliveries: list of tuples [(x, y), ...] for delivery locations.
        num_vehicles: number of vehicles (routes) to compute.
        initial_temp, cooling_rate, min_temp: parameters for simulated annealing.
        """
        self.depot = depot
        self.deliveries = deliveries
        self.num_vehicles = num_vehicles
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp

    def compute_initial_routes(self):
        """
        Partitions deliveries and builds initial routes for each vehicle.
        Uses angle sorting and round-robin assignment.
        Each route starts and ends at the depot.
        """
        # Compute angle for each delivery relative to the depot
        points_with_angle = []
        for point in self.deliveries:
            dx = point[0] - self.depot[0]
            dy = point[1] - self.depot[1]
            angle = math.atan2(dy, dx)
            points_with_angle.append((point, angle))
        points_with_angle.sort(key=lambda x: x[1])
        
        # Partition deliveries among vehicles round-robin
        partitions = [[] for _ in range(self.num_vehicles)]
        for i, (point, angle) in enumerate(points_with_angle):
            partitions[i % self.num_vehicles].append(point)
        
        routes = []
        for part in partitions:
            # If partition is empty, route is depot->depot
            if not part:
                routes.append([self.depot, self.depot])
                continue
            # Initial route: depot -> deliveries (in partition order) -> depot
            route = [self.depot] + part + [self.depot]
            routes.append(route)
        return routes

class SAOptimizer:
    def __init__(self, route, initial_temp=10000, cooling_rate=0.995, min_temp=1e-8):
        """
        Initializes the simulated annealing optimizer for one route.
        route: initial route (list of points; depot is fixed at start and end).
        initial_temp, cooling_rate, min_temp: SA parameters.
        """
        self.route = route[:]              # current solution
        self.best_route = route[:]         # best found solution
        self.current_distance = self.total_distance(self.route)
        self.best_distance = self.current_distance
        self.temperature = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.iteration = 0

    def total_distance(self, route):
        """Return the total Euclidean distance of a route."""
        total = 0
        for i in range(len(route) - 1):
            total += math.hypot(route[i+1][0] - route[i][0],
                                route[i+1][1] - route[i][1])
        return total

    def update(self):
        """
        Performs one iteration of simulated annealing:
         - Generates a neighboring solution by swapping two delivery points (excluding the depot).
         - Accepts the neighbor if it improves the route or with a probability
           that decreases with temperature.
         - Updates the current temperature and iteration count.
        """
        if self.temperature <= self.min_temp:
            return  # finished
        # Create neighbor by swapping two indices (excluding first and last)
        new_route = self.route[:]
        i, j = random.sample(range(1, len(new_route) - 1), 2)
        new_route[i], new_route[j] = new_route[j], new_route[i]
        new_distance = self.total_distance(new_route)
        delta = new_distance - self.current_distance
        if delta < 0 or random.random() < math.exp(-delta / self.temperature):
            self.route = new_route
            self.current_distance = new_distance
            if new_distance < self.best_distance:
                self.best_distance = new_distance
                self.best_route = new_route[:]
        self.temperature *= self.cooling_rate
        self.iteration += 1

    def is_finished(self):
        """Return True if the optimizer has cooled below the threshold."""
        return self.temperature <= self.min_temp

    def get_state(self):
        """Return current state information for display."""
        return {
            "iteration": self.iteration,
            "temperature": self.temperature,
            "current_distance": self.current_distance,
            "best_distance": self.best_distance,
        }
