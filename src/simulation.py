import pygame
import numpy as np
from src.organism import Organism
from src.food import FoodManager
from src.gui import GUI

class EvolutionSimulation:
    """
    Main class that runs the simulation loop, updating organisms, food,
    and GUI rendering.
    """

    def __init__(self):
        # Initialize organisms list
        self.organisms = []
        initial_population = 120
        for _ in range(initial_population):
            # Randomize initial organism start positions
            pos_x = np.random.uniform(0, 1000)
            pos_y = np.random.uniform(0, 1000)
            # Traits based on initial project parameters
            speed = 3.5
            size = 10
            sensory_range = 40
            energy = 150
            health = 90
            min_repro_energy = (size ** 2) * 35 * 0.5
            energy_transfer_ratio = 0.5

            org = Organism(pos_x, pos_y, speed, size, sensory_range,
                           energy, health, min_repro_energy, energy_transfer_ratio)
            self.organisms.append(org)

        # Initialize food manager
        self.food_manager = FoodManager(max_food=500, respawn_rate=40, grid_size=1000)

        # Initialize GUI
        self.gui = GUI(width=1400, height=1000)

        # Control simulation frame rate
        self.clock = pygame.time.Clock()
        self.fps = 30

        self.step_count = 0

    def run(self):
        running = True
        while running:
            # Handle events (quit, etc.)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Prepare food data arrays for organism updates
            food_positions = self.food_manager.food_positions
            food_energies = self.food_manager.food_energies
            food_available = self.food_manager.food_available

            new_organisms = []

            # Update each organism - let organisms move, consume, reproduce or die
            survivors = 0
            for org in self.organisms:
                # Organism step function returns alive/dead status and offspring traits if any
                status, offspring_traits = org.step(food_positions, food_energies, food_available)
                if status == "alive":
                    # Organism tries to consume food at its position
                    energy_gained = self.food_manager.consume_food(np.array([org.pos_x, org.pos_y]))
                    org.energy += energy_gained
                    survivors += 1
                    new_organisms.append(org)

                    # If offspring present, create Organism instance and add to new list
                    if offspring_traits is not None:
                        offspring = Organism(**offspring_traits)
                        new_organisms.append(offspring)
                # Dead organisms are discarded

            # Update population list to survivors plus offspring
            self.organisms = new_organisms

            # Respawn food periodically (e.g. every 14 steps)
            if self.step_count % 14 == 0:
                self.food_manager.respawn_food()

            # Update GUI display with current state
            self.gui.draw(self.organisms,
                          self.food_manager.food_positions,
                          self.food_manager.food_available,
                          self.step_count, survivors, np.sum(self.food_manager.food_available))

            self.step_count += 1

            # Cap frame rate to reduce excessive CPU load
            self.clock.tick(self.fps)

        pygame.quit()

if __name__ == '__main__':
    sim = EvolutionSimulation()
    sim.run()
