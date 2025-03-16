import pygame
import math
from agent import VRPAgentSimulatedAnnealing, SAOptimizer
from environment import VRPEnvironment

# Set overall window dimensions to 800x800 for the left area and 400x for the right panel.
sim_width = 600          # Left side width (for SA process and path simulation)
panel_width = 400        # Right panel width (increased to 400)
height = 950             # Total height
total_width = sim_width + panel_width

pygame.init()
screen = pygame.display.set_mode((total_width, height))
pygame.display.set_caption("VRP: SA Process (Top) & Path Simulation (Bottom)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)

# Create the VRP environment (dimensions for drawing: use sim_width x height for left area)
env = VRPEnvironment(sim_width, height, num_deliveries=15)

# Global variables
routes = None           
optimizers = []         
vehicles = []           
optimization_running = False  
vehicle_simulation_started = False  # Flag for starting vehicle simulation

# Button for SA optimization in the top area
button_rect = pygame.Rect(10, 10, 150, 40)
button_color = (0, 128, 255)

# Layout: Split left side into two areas
top_area_height = 400                   # Top area (SA process)
bottom_area_height = height - top_area_height  # Bottom area (vehicle simulation)

# Button for starting vehicle simulation (appears in bottom area after SA finishes)
button_sim_rect = pygame.Rect(10, top_area_height + 10, 150, 40)

# A simple Vehicle class for final path simulation
class Vehicle:
    def __init__(self, route, speed=2.0):
        self.route = route
        self.speed = speed
        self.current_index = 0  
        self.position = route[0]
        self.finished = False
        self.segment_progress = 0.0

    def update(self):
        if self.finished:
            return
        if self.current_index >= len(self.route) - 1:
            self.finished = True
            return
        start = self.route[self.current_index]
        end = self.route[self.current_index + 1]
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        seg_length = math.hypot(dx, dy)
        if seg_length == 0:
            self.current_index += 1
            self.segment_progress = 0.0
            return
        self.segment_progress += self.speed
        if self.segment_progress >= seg_length:
            self.current_index += 1
            self.segment_progress = 0.0
            if self.current_index >= len(self.route) - 1:
                self.position = end
                self.finished = True
                return
            start = self.route[self.current_index]
            end = self.route[self.current_index+1]
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            seg_length = math.hypot(dx, dy)
        t = self.segment_progress / seg_length
        new_x = start[0] + dx * t
        new_y = start[1] + dy * t
        self.position = (new_x, new_y)
    
    def get_distance_travelled(self):
        dist = 0
        for i in range(self.current_index):
            start = self.route[i]
            end = self.route[i+1]
            dist += math.hypot(end[0]-start[0], end[1]-start[1])
        dist += self.segment_progress
        return dist
    
    def total_route_distance(self):
        total = 0
        for i in range(len(self.route)-1):
            start = self.route[i]
            end = self.route[i+1]
            total += math.hypot(end[0]-start[0], end[1]-start[1])
        return total

# Updated vehicle colors:
# Vehicle 1: White, Vehicle 2: Blue, Vehicle 3: Green
vehicle_colors = [(255, 255, 255), (0, 0, 255), (0, 255, 0)]

# Base explanation text for the right-side panel with added problem description.
base_explanation = [
    "Vehicle Routing Problem (VRP)",
    "--------------------------------",
    "Description:",
    "Determine optimal routes for a fleet of",
    "vehicles delivering goods to various",
    "locations. Each vehicle starts and ends",
    "at a central depot (red). Delivery points",
    "are shown in white.",
    "",
    "VRP Simulation with Simulated Annealing (SA)",
    "",
    "Top: SA Process Visualization",
    "Bottom: Path Simulation (Vehicles)",
    "",
    "Instructions:",
    "- Click 'Solve VRP' in the top area",
    "  to begin SA optimization.",
    "- After SA finishes, click",
    "  'Start Simulation' in the bottom area",
    "  to animate vehicles.",
    "",
    "SA Heuristic:",
    "1. Partition deliveries by angle (round-robin).",
    "2. Initial route: depot -> deliveries -> depot.",
    "3. SA refines the route by swapping orders,",
    "   accepting worse solutions based on temp.",
    "",
    "Dynamic SA Parameters:",
]

# Compute uniform scaling to fit the environment into each sub-window.
scale = min(sim_width / env.width, top_area_height / env.height)
offset_x = (sim_width - (env.width * scale)) / 2
top_offset_y = 0
bottom_offset_y = top_area_height

def transform_point(point, offset_y):
    x, y = point
    new_x = offset_x + x * scale
    new_y = offset_y + y * scale
    return (int(new_x), int(new_y))

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # If "Solve VRP" button in top area is clicked (and SA hasn't started)
            if event.button == 1 and button_rect.collidepoint(event.pos) and not optimization_running:
                num_vehicles = 3
                agent = VRPAgentSimulatedAnnealing(env.depot, env.deliveries, num_vehicles)
                routes = agent.compute_initial_routes()
                optimizers = [SAOptimizer(route) for route in routes]
                optimization_running = True
                vehicles = []
                vehicle_simulation_started = False
            # If "Start Simulation" button in bottom area is clicked (after SA finishes)
            if event.button == 1 and button_sim_rect.collidepoint(event.pos) and (not optimization_running) and vehicles and (not vehicle_simulation_started):
                vehicle_simulation_started = True

    # Update SA process if running
    if optimization_running:
        for optimizer in optimizers:
            if not optimizer.is_finished():
                optimizer.update()
        if all(optimizer.is_finished() for optimizer in optimizers):
            optimization_running = False
            vehicles = [Vehicle(optimizer.best_route, speed=2.0) for optimizer in optimizers]
    # Update vehicles only if SA is finished and simulation has started
    if not optimization_running and vehicles and vehicle_simulation_started:
        for vehicle in vehicles:
            vehicle.update()
    
    # Clear screen and draw divider between left area and right panel
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (100, 100, 100), (sim_width, 0), (sim_width, height), 2)
    
    # --- Draw Top Area (SA Process Visualization) ---
    top_area_rect = pygame.Rect(0, 0, sim_width, top_area_height)
    pygame.draw.rect(screen, (30, 30, 30), top_area_rect)
    # Draw depot and deliveries in top area
    depot_top = transform_point(env.depot, top_offset_y)
    pygame.draw.circle(screen, (255, 0, 0), depot_top, 8)
    for point in env.deliveries:
        pt = transform_point(point, top_offset_y)
        pygame.draw.circle(screen, (255, 255, 255), pt, 5)
    # Draw SA route (current while optimizing; best when finished)
    if optimization_running:
        for i, optimizer in enumerate(optimizers):
            color = vehicle_colors[i % len(vehicle_colors)]
            route = optimizer.route
            for j in range(len(route) - 1):
                p1 = transform_point(route[j], top_offset_y)
                p2 = transform_point(route[j+1], top_offset_y)
                pygame.draw.line(screen, color, p1, p2, 2)
    else:
        if optimizers:
            for i, optimizer in enumerate(optimizers):
                color = vehicle_colors[i % len(vehicle_colors)]
                route = optimizer.best_route
                for j in range(len(route) - 1):
                    p1 = transform_point(route[j], top_offset_y)
                    p2 = transform_point(route[j+1], top_offset_y)
                    pygame.draw.line(screen, color, p1, p2, 2)
    # Draw "Solve VRP" button in top area if SA hasn't started
    if not optimization_running and not vehicles:
        pygame.draw.rect(screen, button_color, button_rect)
        button_text = font.render("Solve VRP", True, (255, 255, 255))
        screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))
    
    # --- Draw Bottom Area (Path Simulation) ---
    bottom_area_rect = pygame.Rect(0, top_area_height, sim_width, bottom_area_height)
    pygame.draw.rect(screen, (20, 20, 20), bottom_area_rect)
    # Draw depot and deliveries in bottom area
    depot_bottom = transform_point(env.depot, bottom_offset_y)
    pygame.draw.circle(screen, (255, 0, 0), depot_bottom, 8)
    for point in env.deliveries:
        pt = transform_point(point, bottom_offset_y)
        pygame.draw.circle(screen, (255, 255, 255), pt, 5)
    # Draw final optimized routes and vehicles if available
    if vehicles:
        for i, vehicle in enumerate(vehicles):
            color = vehicle_colors[i % len(vehicle_colors)]
            for j in range(len(vehicle.route) - 1):
                p1 = transform_point(vehicle.route[j], bottom_offset_y)
                p2 = transform_point(vehicle.route[j+1], bottom_offset_y)
                pygame.draw.line(screen, color, p1, p2, 2)
        for i, vehicle in enumerate(vehicles):
            color = vehicle_colors[i % len(vehicle_colors)]
            pos = transform_point(vehicle.position, bottom_offset_y)
            pygame.draw.circle(screen, color, pos, 6)
        # If simulation hasn't started, show the "Start Simulation" button
        if not vehicle_simulation_started:
            pygame.draw.rect(screen, button_color, button_sim_rect)
            sim_button_text = font.render("Start Simulation", True, (255, 255, 255))
            screen.blit(sim_button_text, (button_sim_rect.x + 10, button_sim_rect.y + 10))
    
    # --- Draw Right Panel (SA Parameters, Explanations, and Problem Description) ---
    panel_rect = pygame.Rect(sim_width, 0, panel_width, height)
    pygame.draw.rect(screen, (50, 50, 50), panel_rect)
    explanation_lines = base_explanation[:]
    if optimization_running:
        for idx, optimizer in enumerate(optimizers):
            state = optimizer.get_state()
            info = (f"Vehicle {idx+1}:",
                    f" Iter: {state['iteration']}",
                    f" Temp: {state['temperature']:.2f}",
                    f" Curr D: {state['current_distance']:.1f}",
                    f" Best D: {state['best_distance']:.1f}")
            explanation_lines.append("")
            explanation_lines.extend(info)
    elif vehicles:
        for idx, optimizer in enumerate(optimizers):
            state = optimizer.get_state()
            info = (f"Vehicle {idx+1} (Final):",
                    f" Iter: {state['iteration']}",
                    f" Best D: {state['best_distance']:.1f}")
            explanation_lines.append("")
            explanation_lines.extend(info)
    line_height = 20
    for i, line in enumerate(explanation_lines):
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (sim_width + 10, 10 + i * line_height))
    
    pygame.display.flip()

pygame.quit()
