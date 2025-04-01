import pygame
import sys

# Config
CELL_SIZE = 20
GRID_WIDTH = 32
GRID_HEIGHT = 32
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
DRAW_COLOR = (0, 0, 0)
ERASE_COLOR = (255, 255, 255)

# Init
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Simple Pixel Art Editor")
clock = pygame.time.Clock()

# Grid storage
grid = [[ERASE_COLOR for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, grid[y][x], rect)
            pygame.draw.rect(screen, (220, 220, 220), rect, 1)  # grid lines

def save_image():
    image = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            image.set_at((x, y), grid[y][x])
    pygame.image.save(image, "my_sprite.png")
    print("Sprite saved as my_sprite.png")

# Main loop
running = True
while running:
    screen.fill(ERASE_COLOR)  # White background
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.mouse.get_pressed()[0]:  # Left click = draw
            x, y = pygame.mouse.get_pos()
            grid_x = x // CELL_SIZE
            grid_y = y // CELL_SIZE
            if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                grid[grid_y][grid_x] = DRAW_COLOR

        if pygame.mouse.get_pressed()[2]:  # Right click = erase
            x, y = pygame.mouse.get_pos()
            grid_x = x // CELL_SIZE
            grid_y = y // CELL_SIZE
            if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                grid[grid_y][grid_x] = ERASE_COLOR

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_image()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
