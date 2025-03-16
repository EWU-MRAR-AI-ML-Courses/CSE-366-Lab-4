import random

class VRPEnvironment:
    def __init__(self, width, height, num_deliveries=15):
        self.width = width
        self.height = height
        self.num_deliveries = num_deliveries
        # Depot is at the center
        self.depot = (width // 2, height // 2)
        self.deliveries = self.generate_deliveries()
    
    def generate_deliveries(self):
        points = []
        margin = 50
        for _ in range(self.num_deliveries):
            x = random.randint(margin, self.width - margin)
            y = random.randint(margin, self.height - margin)
            points.append((x, y))
        return points
