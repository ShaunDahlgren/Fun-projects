import pygame
import sys


pygame.init()
font = pygame.font.Font(None, 36)
width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Message Tester")

clock = pygame.time.Clock()
running = True

while running:
    if pygame.event.peek(pygame.QUIT):
        running = False
        sys.exit()
    screen.fill((0, 0, 0))
    message = "I want to go to bed!"
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    clock.tick(60)  # Limit the frame rate to 60 FPS
    
