import pygame
import math

# Base colors
WHITE = (255, 255, 255)
PREVIEW = (190, 190, 190)


# Create rectangle from two points
def rect_from_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    left = min(x1, x2)
    top = min(y1, y2)
    w = abs(x2 - x1)
    h = abs(y2 - y1)
    return pygame.Rect(left, top, w, h)


# Right triangle (simple L-shape)
def right_tri(surface, color, p1, p2, width):
    x1, y1 = p1
    x2, y2 = p2
    pygame.draw.polygon(surface, color, [(x1, y1), (x2, y2), (x1, y2)], width)


# Equilateral triangle using perpendicular vector
def equi_tri(surface, color, p1, p2, width):
    x1, y1 = p1
    x2, y2 = p2

    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    if length == 0:
        return

    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    height = (math.sqrt(3) / 2) * length

    # perpendicular unit vector
    nx = -dy / length
    ny = dx / length

    top = (mid_x + nx * height, mid_y + ny * height)

    pygame.draw.polygon(surface, color, [p1, p2, top], width)


# Diamond (rhombus)
def diamond(surface, color, p1, p2, width):
    x1, y1 = p1
    x2, y2 = p2

    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2

    pts = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
    pygame.draw.polygon(surface, color, pts, width)


# Flood fill using stack
def fill(surface, start_pos, target_color, fill_color):
    if target_color == fill_color:
        return

    w, h = surface.get_size()
    stack = [start_pos]

    while stack:
        x, y = stack.pop()

        if x < 0 or y < 0 or x >= w or y >= h:
            continue

        if surface.get_at((x, y))[:3] != target_color:
            continue

        surface.set_at((x, y), fill_color)

        stack += [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]


# Draw preview (temporary overlay)
def preview(surface, mode, p1, p2, size, offset):
    if not p1 or not p2:
        return

    # shift because of toolbar
    s = (p1[0], p1[1] + offset)
    e = (p2[0], p2[1] + offset)

    x1, y1 = s
    x2, y2 = e

    if mode == "line":
        pygame.draw.line(surface, PREVIEW, s, e, size)

    elif mode == "rect":
        pygame.draw.rect(surface, PREVIEW, rect_from_points(s, e), size)

    elif mode == "square":
        side = max(abs(x2 - x1), abs(y2 - y1))
        sx = x1 if x2 >= x1 else x1 - side
        sy = y1 if y2 >= y1 else y1 - side
        pygame.draw.rect(surface, PREVIEW, (sx, sy, side, side), size)

    elif mode == "circle":
        r = int(math.hypot(x2 - x1, y2 - y1))
        pygame.draw.circle(surface, PREVIEW, s, r, size)

    elif mode == "right_triangle":
        right_tri(surface, PREVIEW, s, e, size)

    elif mode == "equilateral_triangle":
        equi_tri(surface, PREVIEW, s, e, size)

    elif mode == "rhombus":
        diamond(surface, PREVIEW, s, e, size)
    elif mode == "erase_rect":
        pygame.draw.rect(surface, (220,220,220), rect_from_points(s,e), 2)