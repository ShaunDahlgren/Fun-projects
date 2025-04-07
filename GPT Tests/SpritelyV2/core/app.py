import pygame 
from core.canvas import Canvas

class App:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Spritely V2")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.canvas = Canvas(50, 50, 10)
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
            
        pygame.quit()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            self.canvas.handle_event(event)
            
    def update(self):
        self.canvas.update()
        
    def draw(self):
        self.screen.fill((30, 30, 30))
        self.canvas.draw(self.screen)
        pygame.display.flip()
        