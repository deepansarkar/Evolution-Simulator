import pygame
import random
from src.organism import Organism
from src.food import FoodManager
from src.gui import draw_grid_and_organisms, draw_histograms, draw_counters

GRID_SIZE = 1000
STEP_SIZE = 30
ORG_COLOR = (70, 130, 180)
FOOD_COLOR = (34, 139, 34)
BG_COLOR = (250, 250, 250)
INITIAL_POPULATION = 20

# Constants for initial organism traits & reproduction parameters (constant for initial population)
INITIAL_SPEED = 3.5
INITIAL_SIZE = 10
INITIAL_SENSORY_RANGE = 40
INITIAL_HEALTH = 90
INITIAL_ENERGY = 0.5
MIN_REPRO_ENERGY = 0.8
ENERGY_TRANSFER_RATIO = 0.5

class EvolutionSimulation:
    STEP_SIZE = STEP_SIZE

    def __init__(self):
        self.population = []
        self.food_manager = FoodManager(GRID_SIZE)
        pygame.init()
        self.pygame = pygame
        self.screen = pygame.display.set_mode((GRID_SIZE + 600, GRID_SIZE))
        self.clock = pygame.time.Clock()
        self.bg = pygame.Surface(self.screen.get_size())
        self.bg.fill(BG_COLOR)

        # Initialize population with constant parameters, including new reproduction params
        for _ in range(INITIAL_POPULATION):
            org = Organism(
                random.randint(0, GRID_SIZE - 1),
                random.randint(0, GRID_SIZE - 1),
                INITIAL_SPEED,
                INITIAL_SIZE,
                INITIAL_ENERGY,
                INITIAL_HEALTH,
                INITIAL_SENSORY_RANGE,
                min_reproduction_energy=MIN_REPRO_ENERGY,
                energy_transfer_ratio=ENERGY_TRANSFER_RATIO
            )
            self.population.append(org)

    def organism_step(self, organism):
        """
        Wrapper calling organism’s self-contained step behavior.
        Here zigzag_move=True enables zig-zag pattern movement.
        """
        return organism.step(
            self.food_manager.foods,
            self.population,
            GRID_SIZE,
            zigzag_move=True
        )

    def draw(self, step_number, num_organisms, num_foods):
        """
        Draw organisms, food, histograms, and counters.
        """
        draw_grid_and_organisms(self.screen, self.bg, self.food_manager.foods, self.population, ORG_COLOR, FOOD_COLOR)
        draw_histograms(self.screen, self.population, GRID_SIZE)
        draw_counters(self.screen, step_number, num_organisms, num_foods, GRID_SIZE)
        pygame.display.flip()

    def run(self):
        running = True
        step = 0
        while running:
            self.clock.tick(self.STEP_SIZE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            new_population = []
            for org in self.population:
                if self.organism_step(org):
                    new_population.append(org)
            self.population = new_population

            if step % 14 == 0:
                self.food_manager.respawn_food()

            self.draw(step, len(self.population), len(self.food_manager.foods))
            step += 1

        pygame.quit()
