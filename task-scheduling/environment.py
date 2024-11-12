import pygame
import numpy as np

class Environment:
    def __init__(self, num_tasks, num_robots):
        self.num_tasks = num_tasks
        self.num_robots = num_robots
        self.task_durations = np.random.randint(1, 11, size=num_tasks)
        self.task_priorities = np.random.randint(1, 6, size=num_tasks)
        self.robot_efficiencies = np.random.uniform(0.5, 1.5, size=num_robots)

    def generate_assignments(self):
        """
        Randomly assign tasks to robots for initial population in the genetic algorithm.
        """
        return [np.random.randint(0, self.num_robots, size=self.num_tasks) for _ in range(50)]

    def draw_grid(self, screen, font, task_assignments):
        """
        Draw a grid representing the task assignments on the Pygame screen.
        Each row is a robot, each column is a task, colors are based on task durations, and annotations
        show task priorities and durations inside the grid.
        """
        screen.fill((255, 255, 255))  # Background color
        
        color_map = [(0, 0, 255 - i * 25) for i in range(10)]  # Color gradient for durations
        
        # Set spacing and margins
        cell_size = 60
        margin_left = 150
        margin_top = 100

        # Display task names on the top (X-axis labels)
        for col in range(self.num_tasks):
            task_text = font.render(f"Task {col + 1}", True, (0, 0, 0))
            screen.blit(task_text, (margin_left + col * cell_size + cell_size // 3, margin_top - 30))

        # Draw each robot row with tasks assigned
        for row in range(self.num_robots):
            # Display robot efficiency on the left of each row
            efficiency_text = font.render(f"Efficiency: {self.robot_efficiencies[row]:.2f}", True, (0, 0, 0))
            screen.blit(efficiency_text, (10, margin_top + row * cell_size + cell_size // 3))

            for col in range(self.num_tasks):
                # Determine if this task is assigned to the current robot
                assigned_robot = task_assignments[col]
                
                # Set color based on task duration
                color = color_map[self.task_durations[col] - 1] if assigned_robot == row else (200, 200, 200)
                
                # Draw the cell
                cell_rect = pygame.Rect(
                    margin_left + col * cell_size,
                    margin_top + row * cell_size,
                    cell_size,
                    cell_size
                )
                pygame.draw.rect(screen, color, cell_rect)
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)  # Draw cell border

                # Display task priority and duration within the cell
                priority_text = font.render(f"P{self.task_priorities[col]}", True, (255, 255, 255) if assigned_robot == row else (0, 0, 0))
                duration_text = font.render(f"{self.task_durations[col]}h", True, (255, 255, 255) if assigned_robot == row else (0, 0, 0))
                screen.blit(priority_text, (cell_rect.x + 5, cell_rect.y + 5))
                screen.blit(duration_text, (cell_rect.x + 5, cell_rect.y + 25))
