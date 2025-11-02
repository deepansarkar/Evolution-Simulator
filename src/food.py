import numpy as np

class FoodManager:
    """
    Manages food entries: their positions, energies and respawn logic.
    """

    def __init__(self, max_food=500, respawn_rate=40, grid_size=1000):
        self.grid_size = grid_size
        self.max_food = max_food
        self.respawn_rate = respawn_rate

        # Initialize food properties
        self.food_positions = np.random.uniform(0, grid_size, size=(max_food, 2))
        self.food_energies = np.full(max_food, 10)  # All food items have energy 10
        self.food_available = np.ones(max_food, dtype=bool)  # Food availability mask

    def respawn_food(self):
        """
        Respawn food depleted by organisms up to the respawn_rate.
        Runs periodically every fixed simulation steps.
        """
        # Indices of eaten (not available) food
        eaten_indices = np.where(self.food_available == False)[0]
        if len(eaten_indices) == 0:
            return

        # Respawn only as many as respawn_rate
        to_respawn = min(len(eaten_indices), self.respawn_rate)
        new_positions = np.random.uniform(0, self.grid_size, size=(to_respawn, 2))

        # Update food positions and energies for respawned items
        self.food_positions[eaten_indices[:to_respawn]] = new_positions
        self.food_energies[eaten_indices[:to_respawn]] = 10
        self.food_available[eaten_indices[:to_respawn]] = True

    def consume_food(self, organism_pos, consume_radius=5):
        """
        Let organism consume all food within consume_radius.

        Args:
            organism_pos (np.ndarray or list): [x, y] position of organism.
            consume_radius (float): radius within which food can be eaten.

        Returns:
            float: total energy gained by organism via consumption.
        """
        dists_sq = np.sum((self.food_positions - organism_pos) ** 2, axis=1)
        radius_sq = consume_radius ** 2
        consumable_mask = (dists_sq < radius_sq) & (self.food_available)

        if np.any(consumable_mask):
            indices = np.where(consumable_mask)[0]
            total_energy = np.sum(self.food_energies[indices])
            self.food_available[indices] = False  # Mark food eaten
            return total_energy
        else:
            return 0
