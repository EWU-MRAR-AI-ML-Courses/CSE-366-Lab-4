import random
import pygame

class VRPEnvironment:
    def __init__(self, width, height, num_deliveries=15):
        """
        Initializes the VRP environment.
         - width, height: dimensions for the simulation area.
         - num_deliveries: number of delivery points to generate.
        """
        self.width = width
        self.height = height
        self.num_deliveries = num_deliveries
        # Depot is set at the center of the simulation area
        self.depot = (width // 2, height // 2)
        self.deliveries = self.generate_deliveries()

    def generate_deliveries(self):
        """Randomly generate delivery points within the screen margins."""
        points = []
        margin = 50
        for _ in range(self.num_deliveries):
            x = random.randint(margin, self.width - margin)
            y = random.randint(margin, self.height - margin)
            points.append((x, y))
        return points

    def draw(self, screen):
        """This method is kept for reference but is not used directly 
           since drawing is handled via transform functions."""
        pass
