import random

class Food:
    """
    Represents a food resource with a position and energy value.
    """
    def __init__(self, pos_x, pos_y, energy):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.energy = energy

class FoodManager:
    """
    Manages food items: initialization and periodic respawning.
    """
    def __init__(self, grid_size, initial_food=500):
        self.foods = []
        self.grid_size = grid_size
        for _ in range(initial_food):
            fx = random.randint(0, grid_size - 1)
            fy = random.randint(0, grid_size - 1)
            fe = random.randint(30, 80)
            self.foods.append(Food(fx, fy, fe))

    def respawn_food(self, rate=40):
        """
        Adds new food items randomly across the grid for resource regeneration.
        """
        for _ in range(rate):
            fx = random.randint(0, self.grid_size - 1)
            fy = random.randint(0, self.grid_size - 1)
            fe = random.randint(15, 90)
            self.foods.append(Food(fx, fy, fe))
