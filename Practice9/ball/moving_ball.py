import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()

# шар
x, y = WIDTH // 2, HEIGHT // 2
radius = 25
step = 20

# рамка
border_thickness = 10
offset = 20  # 🔥 смещение вниз

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if y - step - radius >= border_thickness + offset:
                    y -= step

            if event.key == pygame.K_DOWN:
                if y + step + radius <= HEIGHT - border_thickness:
                    y += step

            if event.key == pygame.K_LEFT:
                if x - step - radius >= border_thickness:
                    x -= step

            if event.key == pygame.K_RIGHT:
                if x + step + radius <= WIDTH - border_thickness:
                    x += step

    screen.fill((255, 255, 255))

    # 🔥 смещённая рамка
    pygame.draw.rect(
        screen,
        (0, 0, 0),
        (0, offset, WIDTH, HEIGHT - offset),
        border_thickness
    )

    # шар
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)

    pygame.display.flip()
    clock.tick(60)