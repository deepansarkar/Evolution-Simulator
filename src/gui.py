import pygame

class GUI:
    """
    Manages rendering of the simulation's organisms, food, and UI elements.
    """

    def __init__(self, width=1400, height=1000):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height

        # Background surface for static grid
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255, 255, 255))  # white background

        # Grid surface (1000x1000 for simulation environment)
        self.grid_surface = pygame.Surface((1000, 1000))
        self.grid_surface.fill((230, 230, 230))  # light grey grid background

        # Draw grid lines once for optimization
        for x in range(0, 1001, 100):
            pygame.draw.line(self.grid_surface, (200, 200, 200), (x, 0), (x, 1000))
            pygame.draw.line(self.grid_surface, (200, 200, 200), (0, x), (1000, x))

    def draw(self, organisms, food_positions, food_available, step_count, num_organisms, num_food):
        """
        Render all simulation elements on screen each frame.

        Args:
            organisms (list): list of Organism objects.
            food_positions (np.ndarray): array of food positions.
            food_available (np.ndarray): availability mask for food.
            step_count (int): current simulation step.
            num_organisms (int): number of living organisms.
            num_food (int): number of available food items.
        """
        # Clear only the dynamic parts by blitting static background and grid
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.grid_surface, (0, 0))

        # Draw each organism (blue circles scaled by size attribute)
        for org in organisms:
            pygame.draw.circle(self.screen, (0, 0, 255), (int(org.pos_x), int(org.pos_y)), int(org.size))

        # Draw food items as small green dots if available
        for idx, pos in enumerate(food_positions):
            if food_available[idx]:
                pygame.draw.circle(self.screen, (0, 255, 0), (int(pos[0]), int(pos[1])), 3)

        # Display counters on top right
        font = pygame.font.SysFont('Arial', 18)
        step_surf = font.render(f"Step: {step_count}", True, (0, 0, 0))
        org_surf = font.render(f"Organisms: {num_organisms}", True, (0, 0, 0))
        food_surf = font.render(f"Food: {num_food}", True, (0, 0, 0))

        self.screen.blit(step_surf, (1100, 20))
        self.screen.blit(org_surf, (1100, 50))
        self.screen.blit(food_surf, (1100, 80))

        # Refresh display with new drawings
        pygame.display.flip()
