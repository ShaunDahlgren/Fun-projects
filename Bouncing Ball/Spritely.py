import pygame
import sys
import time
import tkinter as tk
from tkinter import colorchooser

# --- Config ---
CELL_SIZE = 20
GRID_WIDTH = 32
GRID_HEIGHT = 32
TOOLBAR_WIDTH = 150
DEFAULT_DRAW_COLOR = (0, 0, 0)
ERASE_COLOR = (255, 255, 255)
BUTTON_HEIGHT = 40
BUTTON_PADDING = 10
FONT_SIZE = 18

YELLOW_BG = (255, 250, 225)  # Butter Cream

pygame.init()
info = pygame.display.Info()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
pygame.display.set_caption("Spritely - Pixel Art Editor")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, FONT_SIZE)
logo_font = pygame.font.SysFont(None, 48)
tooltip_font = pygame.font.SysFont(None, 16)

# --- Data ---
sprite_size_options = [(8, 8), (16, 16), (32, 32), (64, 64), (128, 128)]
frames = [[[ERASE_COLOR for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]]
current_frame_index = 0
draw_color = DEFAULT_DRAW_COLOR
brush_size = 1
show_grid = True
show_onion_skin = True
zoom_level = 1.0
min_zoom = 0.5
max_zoom = 4.0
active_tool = "draw"

undo_stack = []
redo_stack = []
state = "menu"
playing = False
frame_timer = 0
frame_duration = 100

info = pygame.display.Info()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

def pick_color_action():
    global draw_color
    root = tk.Tk()
    root.withdraw()
    color = colorchooser.askcolor(title="Pick a color")[0]
    root.destroy()
    if color:
        draw_color = tuple(map(int, color))

def update_window_size():
    global screen
    # Do not resize window based on canvas anymore
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

def new_sprite():
    set_state("size_select")

def push_undo():
    grid = frames[current_frame_index]
    undo_stack.append([row[:] for row in grid])
    if len(undo_stack) > 20:
        undo_stack.pop(0)

def undo():
    grid = frames[current_frame_index]
    if undo_stack:
        redo_stack.append([row[:] for row in grid])
        state_grid = undo_stack.pop()
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                grid[y][x] = state_grid[y][x]

def redo():
    grid = frames[current_frame_index]
    if redo_stack:
        undo_stack.append([row[:] for row in grid])
        state_grid = redo_stack.pop()
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                grid[y][x] = state_grid[y][x]

def save_image():
    import json
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    base_name = f"sprite_{timestamp}"
    filename = base_name + ".png"
    meta_name = base_name + ".json"

    sheet_width = GRID_WIDTH * len(frames)
    sheet_height = GRID_HEIGHT
    image = pygame.Surface((sheet_width, sheet_height))

    for idx, frame in enumerate(frames):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                image.set_at((x + idx * GRID_WIDTH, y), frame[y][x])

    pygame.image.save(image, filename)
    print(f"Saved as {filename}")

    metadata = {
        "sprite_name": base_name,
        "frame_width": GRID_WIDTH,
        "frame_height": GRID_HEIGHT,
        "frame_count": len(frames),
        "frames": [
        {"x": i * GRID_WIDTH, "y": 0, "duration": 100, "label": f"frame_{i}"} for i in range(len(frames))
    ]
    }

    with open(meta_name, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"Metadata saved as {meta_name}")
    print(f"Saved as {filename}")

def load_image():
    try:
        loaded = pygame.image.load("my_sprite.png")
        for y in range(min(GRID_HEIGHT, loaded.get_height())):
            for x in range(min(GRID_WIDTH, loaded.get_width())):
                grid[y][x] = loaded.get_at((x, y))[:3]
        print("Loaded my_sprite.png")
    except Exception as e:
        print("Failed to load image:", e)

def draw_grid():
    grid = frames[current_frame_index]
    prev_grid = frames[current_frame_index - 1] if current_frame_index > 0 and show_onion_skin else None
    next_grid = frames[current_frame_index + 1] if current_frame_index < len(frames) - 1 and show_onion_skin else None
    global CELL_SIZE
    zoomed_cell = int(CELL_SIZE * zoom_level)
    canvas_width = GRID_WIDTH * zoomed_cell
    canvas_height = GRID_HEIGHT * zoomed_cell
    canvas_x = TOOLBAR_WIDTH + (WINDOW_WIDTH - TOOLBAR_WIDTH - canvas_width) // 2
    canvas_y = (WINDOW_HEIGHT - canvas_height) // 2

    # Draw canvas background box
    canvas_rect = pygame.Rect(canvas_x - 2, canvas_y - 2, canvas_width + 4, canvas_height + 4)
    pygame.draw.rect(screen, (220, 220, 220), canvas_rect)  # subtle background frame
    pygame.draw.rect(screen, (180, 180, 180), canvas_rect, 2)  # border

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(canvas_x + x * zoomed_cell, canvas_y + y * zoomed_cell, zoomed_cell, zoomed_cell)
            # Onion skin previous frame
            if prev_grid:
                blend_color = prev_grid[y][x]
                surface = pygame.Surface((zoomed_cell, zoomed_cell), pygame.SRCALPHA)
                surface.fill((*blend_color, 100))
                screen.blit(surface, rect.topleft)
            if next_grid:
                blend_color = next_grid[y][x]
                surface = pygame.Surface((zoomed_cell, zoomed_cell), pygame.SRCALPHA)
                surface.fill((*blend_color, 60))
                screen.blit(surface, rect.topleft)
            pygame.draw.rect(screen, grid[y][x], rect)
            if show_grid:
                pygame.draw.rect(screen, (210, 210, 210), rect, 1)  # Light Gray

def apply_brush(mouse_pos, color):
    grid = frames[current_frame_index]
    zoomed_cell = int(CELL_SIZE * zoom_level)
    canvas_width = GRID_WIDTH * CELL_SIZE
    canvas_height = GRID_HEIGHT * CELL_SIZE
    canvas_x = TOOLBAR_WIDTH + (WINDOW_WIDTH - TOOLBAR_WIDTH - canvas_width) // 2
    canvas_y = (WINDOW_HEIGHT - canvas_height) // 2
    x, y = mouse_pos
    grid_x = (x - canvas_x) // zoomed_cell
    grid_y = (y - canvas_y) // zoomed_cell
    half = brush_size // 2
    for dy in range(-half, half + 1):
        for dx in range(-half, half + 1):
            gx = grid_x + dx
            gy = grid_y + dy
            if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                grid[gy][gx] = color

def eyedrop(mouse_pos):
    grid = frames[current_frame_index]
    zoomed_cell = int(CELL_SIZE * zoom_level)
    canvas_width = GRID_WIDTH * CELL_SIZE
    canvas_height = GRID_HEIGHT * CELL_SIZE
    canvas_x = TOOLBAR_WIDTH + (WINDOW_WIDTH - TOOLBAR_WIDTH - canvas_width) // 2
    canvas_y = (WINDOW_HEIGHT - canvas_height) // 2
    x, y = mouse_pos
    grid_x = (x - canvas_x) // zoomed_cell
    grid_y = (y - canvas_y) // zoomed_cell
    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
        return grid[grid_y][grid_x]
    return draw_color

class Button:
    def __init__(self, label, tooltip, y, action, x=None, width=None):
        if x is None:
            x = WINDOW_WIDTH // 2 - 75
        if width is None:
            width = 150
        self.rect = pygame.Rect(x, y, width, BUTTON_HEIGHT)
        self.label = label
        self.tooltip = tooltip
        self.action = action

    def draw(self, mouse_pos):
        color = (100, 160, 255)  # Sky Blue
        if self.rect.collidepoint(mouse_pos):
            color = (140, 180, 255)  # Cornflower
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        text = font.render(self.label, True, (40, 40, 40))  # Dark Charcoal
        screen.blit(text, text.get_rect(center=self.rect.center))

        if self.rect.collidepoint(mouse_pos):
            tooltip = tooltip_font.render(self.tooltip, True, (80, 80, 80))  # Slate Gray
            screen.blit(tooltip, (self.rect.x, self.rect.bottom + 5))

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

def main_menu():
    global state, WINDOW_WIDTH, WINDOW_HEIGHT, screen
    mouse_pos = pygame.mouse.get_pos()
    screen.fill(YELLOW_BG)

    title = logo_font.render("Spritely", True, (60, 40, 0))
    screen.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, 60)))

    for button in menu_buttons:
        button.draw(mouse_pos)

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_EQUALS] or keys[pygame.K_KP_PLUS]:
            zoom_level = min(max_zoom, zoom_level * 1.1)
        elif keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
            zoom_level = max(min_zoom, zoom_level / 1.1)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            WINDOW_WIDTH, WINDOW_HEIGHT = event.size
            screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in menu_buttons:
                    if button.check_click(mouse_pos):
                        button.action()

    pygame.display.flip()

def sprite_size_select():
    global GRID_WIDTH, GRID_HEIGHT, grid
    screen.fill(YELLOW_BG)
    mouse_pos = pygame.mouse.get_pos()

    title = logo_font.render("Choose Sprite Size", True, (60, 40, 0))
    screen.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, 60)))

    buttons = []
    start_y = 140
    for i, (w, h) in enumerate(sprite_size_options):
        label = f"{w} x {h}"
        tooltip = f"Create a {w}x{h} pixel canvas"
        y_pos = start_y + i * (BUTTON_HEIGHT + 20)

        def make_action(width=w, height=h):
            return lambda: apply_sprite_size(width, height)

        buttons.append(Button(label, tooltip, y_pos, make_action()))

    back_button = Button("Back to Menu", "Return to main menu", y_pos + 60, lambda: set_state("menu"))

    for btn in buttons:
        btn.draw(mouse_pos)
    back_button.draw(mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for btn in buttons:
                    if btn.check_click(mouse_pos):
                        btn.action()
                if back_button.check_click(mouse_pos):
                    back_button.action()

    pygame.display.flip()

def apply_sprite_size(w, h):
    global GRID_WIDTH, GRID_HEIGHT, grid
    GRID_WIDTH = w
    GRID_HEIGHT = h
    grid = [[ERASE_COLOR for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    update_window_size()
    set_state("editor")

menu_buttons = [
    Button("New Sprite", "Start a blank canvas", 150, new_sprite),
    Button("Load Sprite", "Load my_sprite.png", 210, lambda: [load_image(), set_state("editor")]),
    Button("Quit", "Exit the program", 270, lambda: sys.exit()),
]

def set_state(s):
    global state
    state = s

def run_editor():
    global draw_color, active_tool, current_frame_index, frame_timer
    mouse_pos = pygame.mouse.get_pos()
    screen.fill((235, 235, 230))  # Cool Sand

    if playing:
        frame_timer += clock.get_time()
        if frame_timer >= frame_duration:
            frame_timer = 0
            current_frame_index = (current_frame_index + 1) % len(frames)

    # Animation preview
    preview_x = TOOLBAR_WIDTH + 10
    preview_y = WINDOW_HEIGHT - 100
    preview_spacing = 5
    preview_scale = 2
    for idx, frame in enumerate(frames):
        thumb_surf = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                thumb_surf.set_at((x, y), frame[y][x])
        thumb_scaled = pygame.transform.scale(thumb_surf, (GRID_WIDTH * preview_scale, GRID_HEIGHT * preview_scale))
        rect = thumb_scaled.get_rect(topleft=(preview_x + idx * (GRID_WIDTH * preview_scale + preview_spacing), preview_y))
        screen.blit(thumb_scaled, rect)

        if rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            current_frame_index = idx

        if idx == current_frame_index:
            pygame.draw.rect(screen, (255, 0, 0), rect, 2)
        if idx == current_frame_index:
            pygame.draw.rect(screen, (255, 0, 0), rect, 2)

    # Display current frame index
    frame_label = font.render(f"Frame {current_frame_index + 1} / {len(frames)}", True, (40, 40, 40))
    screen.blit(frame_label, frame_label.get_rect(center=(WINDOW_WIDTH // 2, 10)))

    # Display current frame index at top center
    frame_label = font.render(f"Frame {current_frame_index + 1} / {len(frames)}", True, (40, 40, 40))
    screen.blit(frame_label, frame_label.get_rect(center=(WINDOW_WIDTH // 2, 10)))

    draw_grid()

    for button in top_toolbar_buttons:
        button.draw(mouse_pos)
    for button in side_toolbar_buttons:
        button.draw(mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in top_toolbar_buttons:
                    if button.check_click(mouse_pos):
                        button.action()
                        break
            else:
                for button in side_toolbar_buttons:
                    if button.check_click(mouse_pos):
                        button.action()
                        break
                else:
                    if mouse_pos[0] >= TOOLBAR_WIDTH:
                        push_undo()
                        if active_tool == "draw":
                            apply_brush(mouse_pos, draw_color)
                        elif active_tool == "eyedrop":
                            draw_color = eyedrop(mouse_pos)
                            active_tool = "draw"
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # scroll up
                zoom_level = min(max_zoom, zoom_level * 1.1)
            elif event.button == 5:  # scroll down
                zoom_level = max(min_zoom, zoom_level / 1.1)
            elif event.button == 3:
                if mouse_pos[0] >= TOOLBAR_WIDTH:
                    push_undo()
                    apply_brush(mouse_pos, ERASE_COLOR)

        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0] and mouse_pos[0] >= TOOLBAR_WIDTH:
                if active_tool == "draw":
                    apply_brush(mouse_pos, draw_color)

    pygame.display.flip()

top_toolbar_buttons = [
    Button("Color", "Pick a drawing color", 10, lambda: pick_color_action(), x=160, width=100),
    Button("Undo", "Undo last change", 10, undo, x=270, width=80),
    Button("Redo", "Redo last undo", 10, redo, x=360, width=80),
    Button("Save", "Save sprite as PNG", 10, save_image, x=450, width=100),
    Button("Load", "Load sprite from file", 10, load_image, x=560, width=100),
    Button("Grid Toggle", "Show/hide grid lines", 10, lambda: toggle_grid(), x=670, width=130),
    Button("▶ Play", "Preview animation playback", 10, lambda: toggle_play(), x=820, width=120),
    Button("Onion Skin", "Toggle onion skin view", 10, lambda: toggle_onion_skin(), x=950, width=130),
]

side_toolbar_buttons = [
    Button("+ Frame", "Add a new blank frame", 60, lambda: add_frame(), x=10, width=TOOLBAR_WIDTH - 20),
    Button("- Frame", "Delete the current frame", 110, lambda: delete_frame(), x=10, width=TOOLBAR_WIDTH - 20),
    Button("< Prev", "Go to previous frame", 160, lambda: prev_frame(), x=10, width=TOOLBAR_WIDTH - 20),
    Button("Next >", "Go to next frame", 210, lambda: next_frame(), x=10, width=TOOLBAR_WIDTH - 20),
    Button("Brush 1x1", "Set brush to 1x1", 260, lambda: set_brush(1), x=10, width=TOOLBAR_WIDTH - 20),
    Button("Brush 3x3", "Set brush to 3x3", 310, lambda: set_brush(3), x=10, width=TOOLBAR_WIDTH - 20),
    Button("Brush 5x5", "Set brush to 5x5", 360, lambda: set_brush(5), x=10, width=TOOLBAR_WIDTH - 20),
    Button("Eyedropper", "Pick a color from canvas", 410, lambda: set_tool("eyedrop"), x=10, width=TOOLBAR_WIDTH - 20),
]

def set_brush(size):
    global brush_size, active_tool
    brush_size = size
    active_tool = "draw"

def set_tool(tool):
    global active_tool
    active_tool = tool

def add_frame():
    global frames, current_frame_index
    new_frame = [[ERASE_COLOR for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    frames.insert(current_frame_index + 1, new_frame)
    current_frame_index += 1

def delete_frame():
    global frames, current_frame_index
    if len(frames) > 1:
        frames.pop(current_frame_index)
        current_frame_index = max(0, current_frame_index - 1)

def prev_frame():
    global current_frame_index
    if current_frame_index > 0:
        current_frame_index -= 1

def next_frame():
    global current_frame_index
    if current_frame_index < len(frames) - 1:
        current_frame_index += 1

def toggle_play():
    global playing
    playing = not playing

def toggle_onion_skin():
    global show_onion_skin
    show_onion_skin = not show_onion_skin

def toggle_grid():
    global show_grid
    show_grid = not show_grid

while True:
    if state == "menu":
        main_menu()
    elif state == "size_select":
        sprite_size_select()
    elif state == "editor":
        run_editor()
    clock.tick(60)
