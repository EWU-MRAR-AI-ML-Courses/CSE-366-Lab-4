import pygame
import math
from agent import VRPAgentGenetic
from environment import VRPEnvironment

pygame.init()

# Window settings
sim_width = 600          # Left area width (for GA process and path simulation)
panel_width = 400        # Right panel width
height = 800
total_width = sim_width + panel_width

screen = pygame.display.set_mode((total_width, height))
pygame.display.set_caption("VRP Genetic Algorithm Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)

# Create VRP environment and GA agent
env = VRPEnvironment(sim_width, height, num_deliveries=20)
num_vehicles = 3
population_size = 100
mutation_rate = 0.02
agent = VRPAgentGenetic(env.depot, env.deliveries, num_vehicles, population_size, mutation_rate)

# GA simulation control variables
simulate = False       # Flag to start GA simulation (run generations)
vehicle_simulation_started = False  # Flag to start vehicle movement
generation = 0
max_generations = 200  # Run GA for a fixed number of generations

# Buttons
button_rect = pygame.Rect(10, 10, 150, 40)      # "Solve VRP" button (top area)
button_color = (0, 128, 255)
button_sim_rect = pygame.Rect(10, 410, 150, 40)   # "Start Simulation" button (bottom area)

# Layout: left side divided into top and bottom areas
top_area_height = 400
bottom_area_height = height - top_area_height

# Vehicle class for final path simulation
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
        end = self.route[self.current_index+1]
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
            if self.current_index >= len(self.route)-1:
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

# Vehicle colors: Vehicle 1: white, Vehicle 2: blue, Vehicle 3: green
vehicle_colors = [(255,255,255), (0,0,255), (0,255,0)]
vehicles = []

# Base explanation text for the right panel with additional fitness details.
base_explanation = [
    "Vehicle Routing Problem (VRP)",
    "--------------------------------",
    "Description:",
    "Optimize routes for a fleet of vehicles",
    "delivering goods. Depot (red) is central,",
    "deliveries are white.",
    "",
    "Genetic Algorithm (GA) Simulation",
    "----------------------------------",
    "Top: GA Process Visualization",
    "Bottom: Vehicle Simulation",
    "",
    "Instructions:",
    "- Click 'Solve VRP' (top) to run GA optimization.",
    f"- GA runs for {max_generations} generations.",
    "- After GA, click 'Start Simulation' (bottom)",
    "  to animate vehicles.",
    "",
    "Fitness Function Calculation:",
    "  - Total Distance = depot -> first delivery -> ...",
    "    -> last delivery -> depot",
    "  - Fitness = 1 / (Total Distance + 1e-6)",
    "    (Higher fitness means a shorter route.)",
    "",
    "GA Metrics:",
    "Generation, Max Fitness, Avg Fitness",
]

# Helper functions for coordinate transformation
def compute_scale_offsets(area_width, area_height, env_width, env_height):
    scale = min(area_width / env_width, area_height / env_height)
    offset_x = (area_width - (env_width * scale)) / 2
    return scale, offset_x

def transform_point(point, offset_y, area_width, area_height):
    scale, offset_x = compute_scale_offsets(area_width, area_height, env.width, env.height)
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
            # "Solve VRP" button in top area
            if event.button == 1 and button_rect.collidepoint(event.pos) and not simulate:
                simulate = True
                generation = 0
                vehicles = []
            # "Start Simulation" button in bottom area (after GA finishes)
            if event.button == 1 and button_sim_rect.collidepoint(event.pos) and vehicles and not vehicle_simulation_started:
                vehicle_simulation_started = True

    # Run GA simulation if active and generation count is below threshold
    if simulate and generation < max_generations:
        agent.run_generation()
        generation += 1
    elif simulate and generation >= max_generations:
        simulate = False
        # GA finished: create vehicles from best routes
        best_routes = agent.get_best_routes()
        vehicles = [Vehicle(route, speed=2.0) for route in best_routes]

    # Update vehicles if simulation has started
    if vehicles and vehicle_simulation_started:
        for vehicle in vehicles:
            vehicle.update()
    
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw divider between left area and right panel
    pygame.draw.line(screen, (100, 100, 100), (sim_width, 0), (sim_width, height), 2)
    
    # --- Draw Top Area (GA Process Visualization) ---
    top_area_rect = pygame.Rect(0, 0, sim_width, top_area_height)
    pygame.draw.rect(screen, (30, 30, 30), top_area_rect)
    # Draw depot (red) and deliveries (white) in top area
    depot_top = transform_point(env.depot, 0, sim_width, top_area_height)
    pygame.draw.circle(screen, (255, 0, 0), depot_top, 8)
    for point in env.deliveries:
        pt = transform_point(point, 0, sim_width, top_area_height)
        pygame.draw.circle(screen, (255, 255, 255), pt, 5)
    # Draw GA best routes in top area
    best_routes = agent.get_best_routes()
    for i, route in enumerate(best_routes):
        color = vehicle_colors[i % len(vehicle_colors)]
        for j in range(len(route) - 1):
            p1 = transform_point(route[j], 0, sim_width, top_area_height)
            p2 = transform_point(route[j+1], 0, sim_width, top_area_height)
            pygame.draw.line(screen, color, p1, p2, 2)
    # Draw "Solve VRP" button in top area if GA hasn't started
    if not simulate and not vehicles:
        pygame.draw.rect(screen, button_color, button_rect)
        button_text = font.render("Solve VRP", True, (255, 255, 255))
        screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))
    
    # --- Draw Bottom Area (Vehicle Simulation) ---
    bottom_area_rect = pygame.Rect(0, top_area_height, sim_width, bottom_area_height)
    pygame.draw.rect(screen, (20, 20, 20), bottom_area_rect)
    depot_bottom = transform_point(env.depot, top_area_height, sim_width, bottom_area_height)
    pygame.draw.circle(screen, (255, 0, 0), depot_bottom, 8)
    for point in env.deliveries:
        pt = transform_point(point, top_area_height, sim_width, bottom_area_height)
        pygame.draw.circle(screen, (255, 255, 255), pt, 5)
    if vehicles:
        for i, vehicle in enumerate(vehicles):
            color = vehicle_colors[i % len(vehicle_colors)]
            for j in range(len(vehicle.route) - 1):
                p1 = transform_point(vehicle.route[j], top_area_height, sim_width, bottom_area_height)
                p2 = transform_point(vehicle.route[j+1], top_area_height, sim_width, bottom_area_height)
                pygame.draw.line(screen, color, p1, p2, 2)
        for i, vehicle in enumerate(vehicles):
            color = vehicle_colors[i % len(vehicle_colors)]
            pos = transform_point(vehicle.position, top_area_height, sim_width, bottom_area_height)
            pygame.draw.circle(screen, color, pos, 6)
        if not vehicle_simulation_started:
            pygame.draw.rect(screen, button_color, button_sim_rect)
            sim_button_text = font.render("Start Simulation", True, (255, 255, 255))
            screen.blit(sim_button_text, (button_sim_rect.x + 10, button_sim_rect.y + 10))
    
    # --- Draw Right Panel (GA Parameters, Explanations, and Problem Description) ---
    panel_rect = pygame.Rect(sim_width, 0, panel_width, height)
    pygame.draw.rect(screen, (50, 50, 50), panel_rect)
    explanation_lines = base_explanation[:]
    # Add GA metrics for each vehicle solver
    ga_info = []
    for i, solver in enumerate(agent.solvers):
        avg_fit = sum(solver.fitness_values) / len(solver.fitness_values)
        ga_info.append(f"Vehicle {i+1}: Gen {solver.generation}  Max Fit: {solver.best_fitness:.4f}  Avg Fit: {avg_fit:.4f}")
    explanation_lines.extend(["", "GA Metrics:"] + ga_info)
    y_offset = 10
    for line in explanation_lines:
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (sim_width + 10, y_offset))
        y_offset += 20
    
    pygame.display.flip()

pygame.quit()
