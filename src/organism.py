import numpy as np
import random

TRAIT_MUTATION_RATE = 0.02

class Organism:
    """
    Organism represents an individual with traits and biological behaviors.
    """
    def __init__(self, pos_x, pos_y, speed, size, energy, health, sensory_range,
                 min_reproduction_energy, energy_transfer_ratio):
        """
        Initialize organism with traits and reproduction parameters.
        """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed
        self.size = size
        self.max_energy = size ** 2 * 35
        self.energy = self.max_energy * energy
        self.health = health
        self.sensory_range = sensory_range
        self.min_reproduction_energy = min_reproduction_energy
        self.energy_transfer_ratio = energy_transfer_ratio

        # For zig-zag movement toggle
        self.zigzag_toggle = True

    def perceive(self, food_sources):
        """
        Return nearby foods within sensory range.
        """
        visible = []
        for food in food_sources:
            if abs(food.pos_x - self.pos_x) < self.sensory_range and abs(food.pos_y - self.pos_y) < self.sensory_range:
                visible.append(food)
        return visible

    def move_toward(self, target_x, target_y, grid_size, zigzag=False):
        """
        Move toward target coordinates.
        If zigzag=True, alternate horizontal and vertical moves each step for zigzag pattern.
        """
        dx = target_x - self.pos_x
        dy = target_y - self.pos_y

        if not zigzag:
            # Direct movement towards target
            if dx != 0:
                self.pos_x += max(-self.speed, min(self.speed, dx // abs(dx)))
            if dy != 0:
                self.pos_y += max(-self.speed, min(self.speed, dy // abs(dy)))
        else:
            # Zigzag alternate movement
            if self.zigzag_toggle:
                # Move horizontally if possible
                if dx != 0:
                    self.pos_x += max(-self.speed, min(self.speed, dx // abs(dx)))
                else:
                    if dy != 0:
                        self.pos_y += max(-self.speed, min(self.speed, dy // abs(dy)))
            else:
                # Move vertically if possible
                if dy != 0:
                    self.pos_y += max(-self.speed, min(self.speed, dy // abs(dy)))
                else:
                    if dx != 0:
                        self.pos_x += max(-self.speed, min(self.speed, dx // abs(dx)))
            # Toggle flag for next step
            self.zigzag_toggle = not self.zigzag_toggle

        # Boundaries check
        self.pos_x = max(0, min(grid_size - 1, self.pos_x))
        self.pos_y = max(0, min(grid_size - 1, self.pos_y))

    def random_move(self, grid_size, zigzag=False):
        """
        Make random movement either normally or zigzag alternation.
        """
        if not zigzag:
            # Choose random cardinal direction
            move_dir = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.pos_x += move_dir[0] * self.speed
            self.pos_y += move_dir[1] * self.speed
        else:
            # Zigzag random movement: alternate horizontal/vertical steps randomly each move
            if self.zigzag_toggle:
                # Horizontal move randomly right or left
                move_dir = random.choice([(1, 0), (-1, 0)])
                self.pos_x += move_dir[0] * self.speed
            else:
                # Vertical move randomly up or down
                move_dir = random.choice([(0, 1), (0, -1)])
                self.pos_y += move_dir[1] * self.speed
            self.zigzag_toggle = not self.zigzag_toggle

        # Boundaries check
        self.pos_x = max(0, min(grid_size - 1, self.pos_x))
        self.pos_y = max(0, min(grid_size - 1, self.pos_y))

    def eat(self, food, food_list):
        """
        Consume food: increase energy then remove food from environment.
        """
        self.energy = min(self.energy + food.energy, self.max_energy)
        food_list.remove(food)

    def reproduce(self, population):
        """
        Create offspring if sufficient energy.
        Offspring inherits mutated traits.
        """
        if self.energy >= self.min_reproduction_energy and random.random() < 0.08:
            child_energy = self.energy * self.energy_transfer_ratio
            child_traits = [
                self.pos_x,
                self.pos_y,
                max(0.1, self.speed + random.gauss(0, TRAIT_MUTATION_RATE * self.speed)),
                max(0.1, self.size + random.gauss(0, TRAIT_MUTATION_RATE * self.size)),
                child_energy,
                self.health,
                max(5, self.sensory_range + random.gauss(0, TRAIT_MUTATION_RATE * self.sensory_range)),
                self.min_reproduction_energy,
                self.energy_transfer_ratio
            ]
            self.energy -= child_energy  # Deduct transferred energy from parent
            population.append(Organism(*child_traits))

    def energy_update(self):
        """
        Costs energy proportional to speed and size; health decreases if energy is low.
        """
        cost = self.speed * self.size * 0.05 + 0.012 * self.size ** 2
        self.energy -= cost
        if self.energy < 30:
            self.health -= (30 - self.energy) * 0.08

    def step(self, food_list, population, grid_size, zigzag_move=False):
        """
        One behavior step combining perception, movement, eating, reproduction, and energy update.
        """
        visible_food = self.perceive(food_list)
        if self.energy < self.min_reproduction_energy and visible_food:
            # Move toward nearest food, possibly zigzag
            nearest = min(visible_food, key=lambda f: ((f.pos_x - self.pos_x)**2 + (f.pos_y - self.pos_y)**2)**0.5)
            self.move_toward(nearest.pos_x, nearest.pos_y, grid_size, zigzag=zigzag_move)
            # Check adjacent food to eat
            for food in food_list:
                if abs(food.pos_x - self.pos_x) <= 1 and abs(food.pos_y - self.pos_y) <= 1:
                    self.eat(food, food_list)
                    break
            else:
                self.energy_update()
        else:
            # Reproduce if enough energy, else random move and energy update
            if self.energy >= self.min_reproduction_energy:
                self.reproduce(population)
            else:
                self.random_move(grid_size, zigzag=zigzag_move)
                self.energy_update()

        # Check survival condition
        return self.health >= 5 and self.energy >= 0
