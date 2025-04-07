import pygame

class Canvas:
    def __init__(self, width, height, pixel_size):
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        
        self.grid = [[(255, 255, 255) for _ in range(width)] for _ in range(height)]
        self.drawing = False
        self.color = (0, 0, 0)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.drawing = True
            self.paint(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.drawing = False
        elif event.type == pygame.MOUSEMOTION and self.drawing:
            self.paint(event.pos)
            
    def paint(self, pos):
        x, y = pos
        col = x // self.pixel_size
        row = y // self.pixel_size
        
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = self.color
        
    def update(self):
        pass
    
    def draw(self, surface):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    x * self.pixel_size,
                    y * self.pixel_size,
                    self.pixel_size,
                    self.pixel_size,
                )
                pygame.draw.rect(surface, self.grid[y][x], rect)
                pygame.draw.rect(surface, (200, 200, 200), rect, 1)
                