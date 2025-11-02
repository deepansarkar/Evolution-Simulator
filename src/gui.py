import pygame
import matplotlib.pyplot as plt
import io
import PIL.Image

def draw_grid_and_organisms(screen, bg, foods, population, ORG_COLOR, FOOD_COLOR):
    """
    Draw background, food items as small green dots, and organisms as blue circles.
    """
    screen.blit(bg, (0, 0))
    for food in foods:
        pygame.draw.circle(screen, FOOD_COLOR, (int(food.pos_x), int(food.pos_y)), 3)
    for org in population:
        pygame.draw.circle(screen, ORG_COLOR, (int(org.pos_x), int(org.pos_y)), max(3, int(org.size)))

def draw_histograms(screen, population, grid_size):
    """
    Draws larger histograms for speed, size, max energy on the right panel.
    """
    rects = [
        (grid_size + 20, 150, 240, 180),
        (grid_size + 20, 490, 240, 180),
        (grid_size + 20, 730, 240, 180),
    ]
    data = [
        [org.speed for org in population],
        [org.size for org in population],
        [org.max_energy for org in population],
    ]
    titles = ["Speed", "Size", "Max Energy"]

    for n, arr in enumerate(data):
        plt.figure(figsize=(5, 2.5))
        plt.hist(arr, bins=20, color="#6497b1")
        plt.title(titles[n])
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        im = PIL.Image.open(buf)
        mode = im.mode
        size = im.size
        data_bytes = im.tobytes()
        img = pygame.image.fromstring(data_bytes, size, mode)
        screen.blit(img, (rects[n][0], rects[n][1]))
        plt.close()

def draw_counters(screen, step, num_organisms, num_foods, grid_size):
    """
    Display simulation counters: step number, live organisms, and food count.
    """
    font = pygame.font.SysFont(None, 30)
    step_text = f"Step: {step}"
    org_text = f"Organisms: {num_organisms}"
    food_text = f"Food items: {num_foods}"

    x_pos = grid_size + 30
    y_pos = 5
    screen.blit(font.render(step_text, True, (0, 0, 0)), (x_pos, y_pos))
    screen.blit(font.render(org_text, True, (0, 0, 0)), (x_pos, y_pos + 30))
    screen.blit(font.render(food_text, True, (0, 0, 0)), (x_pos, y_pos + 60))
