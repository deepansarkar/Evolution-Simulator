import numpy as np

class Organism:
    """
    Class representing each organism in the simulation.
    """

    def __init__(self, pos_x, pos_y, speed, size, sensory_range, energy, health, min_repro_energy, energy_transfer_ratio):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed
        self.size = size
        self.sensory_range = sensory_range
        self.energy = energy
        self.health = health
        self.min_repro_energy = min_repro_energy
        self.energy_transfer_ratio = energy_transfer_ratio

    def step(self, food_positions, food_energies, food_available):
        """
        Perform one simulation step: move toward food, consume energy,
        possibly reproduce or die.

        Args:
            food_positions (np.ndarray): Array of food coordinates shape (N, 2).
            food_energies (np.ndarray): Corresponding energy of foods shape (N,).
            food_available (np.ndarray): Boolean mask whether food is still available (shape N,).

        Returns:
            str: "alive" or "dead" depending on energy and health.
            dict: offspring info if reproduction occurs, else None.
        """
        # Only consider available food items for detection
        available_food_positions = food_positions[food_available]

        # Defensive check: If no food available, wander randomly
        if len(available_food_positions) == 0:
            self._random_move()
        else:
            # Calculate squared distances to available food
            dists_sq = np.sum((available_food_positions - np.array([self.pos_x, self.pos_y]))**2, axis=1)
            sensory_range_sq = self.sensory_range ** 2
            in_range_mask = dists_sq < sensory_range_sq

            if np.any(in_range_mask):
                # Get nearest food index within range
                nearest_index = np.argmin(dists_sq[in_range_mask])
                indices_in_range = np.where(in_range_mask)[0]
                nearest_food_pos = available_food_positions[indices_in_range[nearest_index]]

                # Move toward the nearest food
                self._move_towards(nearest_food_pos)
            else:
                # No food in sensory range, random wandering
                self._random_move()

        # Clamp position within grid limits (0 to 1000)
        self.pos_x = max(0, min(1000, self.pos_x))
        self.pos_y = max(0, min(1000, self.pos_y))

        # Energy cost calculation (movement + size cost)
        movement_cost = 0.1 * self.speed + 0.01 * self.size
        self.energy -= movement_cost

        # Health degradation if energy low
        if self.energy < 10:
            self.health -= 1

        offspring = None
        # Check for reproduction
        if self.energy > self.min_repro_energy:
            offspring_energy = self.energy * self.energy_transfer_ratio
            self.energy *= (1 - self.energy_transfer_ratio)

            # Create offspring traits (mutated)
            offspring = self._reproduce(offspring_energy)

        # Death conditions
        if self.health <= 0 or self.energy <= 0:
            return "dead", None
        else:
            return "alive", offspring

    def _move_towards(self, target_pos):
        """
        Move organism toward target position.

        Args:
            target_pos (np.ndarray): Array with x, y target coordinates.
        """
        direction = target_pos - np.array([self.pos_x, self.pos_y])
        norm = np.linalg.norm(direction)

        if norm > 0:
            direction = direction / norm
            move_dist = min(self.speed, norm)
            self.pos_x += direction[0] * move_dist
            self.pos_y += direction[1] * move_dist

    def _random_move(self):
        """
        Move organism randomly in one cardinal direction scaled by speed.
        """
        step_choices = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
        random_step = step_choices[np.random.randint(0, 4)] * self.speed
        self.pos_x += random_step[0]
        self.pos_y += random_step[1]

    def _reproduce(self, offspring_energy):
        """
        Produce offspring with mutated traits.

        Args:
            offspring_energy (float): energy to give to offspring.

        Returns:
            dict: offspring traits and energy.
        """
        # Gaussian mutation parameters
        mutation_rate = 0.02  # 2%
        mutated_speed = max(0.1, self.speed + np.random.normal(0, mutation_rate * self.speed))
        mutated_size = max(1, self.size + np.random.normal(0, mutation_rate * self.size))
        mutated_sensory_range = max(1, self.sensory_range + np.random.normal(0, mutation_rate * self.sensory_range))
        mutated_health = 90  # reset health for offspring

        # Calculate offspring's minimum reproduction energy based on size
        offspring_min_repro_energy = (mutated_size ** 2) * 35 * 0.5

        offspring_energy_transfer_ratio = 0.5  # fixed

        offspring_traits = {
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            "speed": mutated_speed,
            "size": mutated_size,
            "sensory_range": mutated_sensory_range,
            "energy": offspring_energy,
            "health": mutated_health,
            "min_repro_energy": offspring_min_repro_energy,
            "energy_transfer_ratio": offspring_energy_transfer_ratio
        }

        return offspring_traits
