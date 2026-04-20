import pygame

# create window
screen = pygame.display.set_mode((900, 700))
pygame.display.set_caption('GFG Paint')

# drawing state
draw_on = False   # true when mouse is pressed
last_pos = (0, 0) # last mouse position to make smooth lines

radius = 5        # brush size
eraser_width = 50

# colors
BLACK = (0, 0, 0)   # used as eraser
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# buttons with colors
COLOR_BUTTONS = [
    {"color": RED, "rect": pygame.Rect(10, 10, 50, 50)},
    {"color": WHITE, "rect": pygame.Rect(70, 10, 50, 50)},
    {"color": YELLOW, "rect": pygame.Rect(130, 10, 50, 50)},
    {"color": GREEN, "rect": pygame.Rect(190, 10, 50, 50)},
    {"color": BLUE, "rect": pygame.Rect(250, 10, 50, 50)},
    {"color": PURPLE, "rect": pygame.Rect(310, 10, 50, 50)}
]

# load eraser image
eraser = pygame.image.load('./Practice10&11/paint/data/3672876_education_eraser_erasing_rubber_stationery_icon.png')
eraser_img_resize = pygame.transform.scale(eraser, (eraser_width, eraser_width))

# eraser button position
eraser_rect = pygame.Rect(360, 10, 50, 50)

# draws smooth line between two points
def roundline(canvas, color, start, end, radius=1):
    Xaxis = end[0] - start[0]
    Yaxis = end[1] - start[1]
    dist = max(abs(Xaxis), abs(Yaxis))
    for i in range(dist):
        x = int(start[0] + float(i) / dist * Xaxis)
        y = int(start[1] + float(i) / dist * Yaxis)
        pygame.draw.circle(canvas, color, (x, y), radius)

# current state
color = WHITE
initial_pos = None  # start of figure
final_pos = None    # end of figure
figure = None       # selected figure

try:
    while True:
        e = pygame.event.wait()

        if e.type == pygame.QUIT:
            raise StopIteration

        # change color or eraser
        if e.type == pygame.MOUSEBUTTONDOWN:
            if eraser_rect.collidepoint(e.pos):
                color = BLACK
            for button in COLOR_BUTTONS:
                if button["rect"].collidepoint(e.pos):
                    color = button['color']

        # choose figure with keyboard
        if e.type == pygame.KEYDOWN:
            radius = 0  # disable brush
            if e.key == pygame.K_r:
                initial_pos = pygame.mouse.get_pos()
                figure = 'rect'
            elif e.key == pygame.K_c:
                initial_pos = pygame.mouse.get_pos()
                figure = 'circle'
            elif e.key == pygame.K_s:
                initial_pos = pygame.mouse.get_pos()
                figure = 'sqr'
            elif e.key == pygame.K_t:
                initial_pos = pygame.mouse.get_pos()
                figure = 'r_t'
            elif e.key == pygame.K_e:
                initial_pos = pygame.mouse.get_pos()
                figure = 'e_t'
            elif e.key == pygame.K_w:
                initial_pos = pygame.mouse.get_pos()
                figure = 'rhombus'

        # reset after key release
        if e.type == pygame.KEYUP:
            initial_pos = None
            final_pos = None
            radius = 5

        # save end point
        if e.type == pygame.MOUSEBUTTONUP:
            final_pos = pygame.mouse.get_pos()

        # draw figures
        if final_pos is not None and initial_pos is not None:

            if figure == 'rect':
                pygame.draw.rect(screen, color,
                    (initial_pos,
                     (final_pos[0] - initial_pos[0],
                      final_pos[1] - initial_pos[1])))

            elif figure == 'circle':
                circle_rad = (final_pos[0] - initial_pos[0]) / 2
                circle_pos = (initial_pos[0] + circle_rad,
                              initial_pos[1] + circle_rad)
                pygame.draw.circle(screen, color, circle_pos, int(circle_rad))

            elif figure == 'sqr':
                size = final_pos[0] - initial_pos[0]
                pygame.draw.rect(screen, color, (initial_pos, (size, size)))

            elif figure == 'r_t':
                pygame.draw.polygon(screen, color,
                    (initial_pos, final_pos,
                     (initial_pos[0], final_pos[1])))

            elif figure == 'e_t':
                pygame.draw.polygon(screen, color,
                    (((initial_pos[0] + final_pos[0]) / 2, initial_pos[1]),
                     (initial_pos[0], final_pos[1]),
                     final_pos))

            elif figure == 'rhombus':
                pygame.draw.polygon(screen, color,
                    (((initial_pos[0] + final_pos[0]) / 2, initial_pos[1]),
                     (initial_pos[0], (initial_pos[1] + final_pos[1]) / 2),
                     (final_pos[0], (initial_pos[1] + final_pos[1]) / 2),
                     ((initial_pos[0] + final_pos[0]) / 2, final_pos[1])))

        # free drawing
        if e.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.circle(screen, color, e.pos, radius)
            draw_on = True

        if e.type == pygame.MOUSEBUTTONUP:
            draw_on = False

        if e.type == pygame.MOUSEMOTION:
            if draw_on:
                pygame.draw.circle(screen, color, e.pos, radius)
                roundline(screen, color, e.pos, last_pos, radius)
            last_pos = e.pos

        # draw buttons
        for button in COLOR_BUTTONS:
            pygame.draw.rect(screen, button["color"], button["rect"])

        # draw eraser icon
        screen.blit(eraser_img_resize, (370, 10))

        pygame.display.flip()

except StopIteration:
    pass

pygame.quit()