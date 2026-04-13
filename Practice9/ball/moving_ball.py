import pygame
import sys

pygame.init()

# Window dimensions
WIDTH, HEIGHT = 600, 600

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

# Frame rate controller
clock = pygame.time.Clock()

# Ball initial position (center of screen)
x, y = WIDTH // 2, HEIGHT // 2

# Ball properties
radius = 25          # Radius of the ball
step = 20            # Movement step (pixels per key press)

# Border settings
border_thickness = 10  # Thickness of the frame
offset = 20            # Vertical offset (moves frame slightly вниз)

while True:
    for event in pygame.event.get():

        # Handle window close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle keyboard input
        if event.type == pygame.KEYDOWN:

            # Move up (check upper boundary with offset)
            if event.key == pygame.K_UP:
                if y - step - radius >= border_thickness + offset:
                    y -= step

            # Move down (check lower boundary)
            if event.key == pygame.K_DOWN:
                if y + step + radius <= HEIGHT - border_thickness:
                    y += step

            # Move left (check left boundary)
            if event.key == pygame.K_LEFT:
                if x - step - radius >= border_thickness:
                    x -= step

            # Move right (check right boundary)
            if event.key == pygame.K_RIGHT:
                if x + step + radius <= WIDTH - border_thickness:
                    x += step

    # Clear screen with white background
    screen.fill((255, 255, 255))

    # Draw rectangular border (frame) with vertical offset
    pygame.draw.rect(
        screen,
        (0, 0, 0),
        (0, offset, WIDTH, HEIGHT - offset),
        border_thickness
    )

    # Draw the ball
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)

    # Update display
    pygame.display.flip()

    # Limit FPS to 60
    clock.tick(60)
