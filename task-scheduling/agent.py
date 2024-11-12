import numpy as np

class Agent:
    def __init__(self, id, efficiency):
        self.id = id  # Unique identifier for each robot
        self.efficiency = efficiency  # Efficiency factor of the robot
        self.tasks = []  # List of tasks assigned to this robot

    def assign_task(self, task_duration, task_priority):
        """
        Assign a task to the robot and calculate effective task time
        considering robot efficiency and task priority.
        """
        effective_time = task_duration / self.efficiency * task_priority
        self.tasks.append(effective_time)

    def total_time(self):
        """Calculate the total time required by this robot to complete all tasks."""
        return sum(self.tasks)

    def reset_tasks(self):
        """Clear the tasks assigned to the agent."""
        self.tasks = []
