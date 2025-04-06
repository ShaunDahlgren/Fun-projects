import pygame
import sys
import time


pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Test window")
clock = pygame.time.Clock()

ballX = screen_width // 2  # Start in the middle of the screen
ballY = screen_height // 2  # Start in the middle of the screen
ballSpeedX = 5
ballSpeedY = 5
ballRadius = 50
countdown = 10

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    screen.fill((0, 0, 0))  # Fill the screen with black
    pygame.draw.circle(screen, (255, 0, 0), (ballX, ballY), ballRadius)  # Draw a red circle at the center of the screen
    ballX += ballSpeedX
    ballY += ballSpeedY
    if(ballX + ballRadius >= screen_width or ballX - ballRadius <= 0):
        ballSpeedX *= -1
        countdown -= 1
    if(ballY + ballRadius >= screen_height or ballY - ballRadius <= 0):
        ballSpeedY *= -1
        countdown -= 1
    if countdown <= 0:
        print("Game Over")
        running = False
        sys.exit()
    clock.tick(60)  # Limit the frame rate to 60 FPS
    pygame.display.flip()  # Update the display