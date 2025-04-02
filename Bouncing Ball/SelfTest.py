import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Self Test")

clock = pygame.time.Clock()
running = True

# Ball setup
ball_pos = [400, 300]
ball_radius = 20
ball_color = (0, 0, 255)
ball_velocity = [5, 5]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # Bounce off the walls
    if ball_pos[0] - ball_radius < 0 or ball_pos[0] + ball_radius > 800:
        ball_velocity[0] *= -1
    if ball_pos[1] - ball_radius < 0 or ball_pos[1] + ball_radius > 600:
        ball_velocity[1] *= -1

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the ball
    pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)
    
    

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
