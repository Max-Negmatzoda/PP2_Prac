import pygame
import datetime
import sys
from tools import *

def main():
    pygame.init()

    WIDTH, HEIGHT = 900, 600
    BAR = 80  # top toolbar height

    # RGB color system: (Red, Green, Blue)
    # Each value is from 0 to 255
    BLACK = (0, 0, 0)        # no light → black
    WHITE = (255, 255, 255)  # full light → white
    RED   = (255, 0, 0)      # red channel only
    GREEN = (0, 255, 0)      # green channel only
    BLUE  = (0, 0, 255)      # blue channel only
    YELLOW = (255,255,0)     # red + green
    CYAN   = (0,255,255)     # green + blue
    MAGENTA= (255,0,255)     # red + blue
    ORANGE = (255,165,0)     # warm orange tone
    PURPLE = (128,0,128)     # darker magenta
    GRAY   = (128,128,128)   # equal RGB = gray
    BG     = (150,150,150)   # UI background

    COLORS = [
        BLACK, WHITE, RED, GREEN, BLUE,
        YELLOW, CYAN, MAGENTA, ORANGE, PURPLE, GRAY
    ]

    # Brush thickness levels (pixels)
    BRUSH = [2, 5, 10]

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint App")
    clock = pygame.time.Clock()

    # Drawing surface (canvas)
    canvas = pygame.Surface((WIDTH, HEIGHT - BAR))
    canvas.fill(WHITE)

    # Undo/redo system
    undo_stack = []
    redo_stack = []

    tool = "draw"       # current tool
    color = BLACK       # current color
    size_id = 1         # brush index

    start = None        # start point of drawing
    end = None          # end point
    drawing = False     # drawing flag

    # Text tool variables
    typing = False
    text_data = ""
    text_pos = (0,0)

    font = pygame.font.SysFont(None, 28)
    small_font = pygame.font.SysFont(None, 18)

    # Tool panel (label + internal key)
    tools = [
        ("Draw","draw"),
        ("Line","line"),
        ("Rect","rect"),
        ("Square","square"),
        ("Circle","circle"),
        ("R-Tri","right_triangle"),
        ("E-Tri","equilateral_triangle"),
        ("Rhomb","rhombus"),
        ("Erase","eraser"),
        ("BoxErase","erase_rect"),
        ("Bucket","bucket"),
        ("Text","text")
    ]

    # Draw toolbar UI
    def draw_ui():
        pygame.draw.rect(screen,(210,210,210),(0,0,WIDTH,BAR))

        # Tool buttons
        for i,(label,key) in enumerate(tools):
            r = pygame.Rect(5+i*75,5,70,25)
            col = (100,180,100) if tool==key else (120,120,120)
            pygame.draw.rect(screen,col,r)
            pygame.draw.rect(screen,BLACK,r,2)

            txt = small_font.render(label,True,BLACK)
            screen.blit(txt,txt.get_rect(center=r.center))

        # Brush sizes
        for i in range(3):
            r = pygame.Rect(5+i*45,40,40,25)
            col = (100,180,100) if size_id==i else (120,120,120)
            pygame.draw.rect(screen,col,r)

        # Color palette
        for i,c in enumerate(COLORS):
            r = pygame.Rect(150+i*35,40,30,25)
            pygame.draw.rect(screen,c,r)

    running = True

    while running:
        mx,my = pygame.mouse.get_pos()
        cy = my - BAR  # convert to canvas coords

        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.KEYDOWN:

                # Save canvas (Ctrl+S)
                if e.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    name = datetime.datetime.now().strftime("img_%H%M%S.png")
                    pygame.image.save(canvas,name)

                # Undo (Ctrl+Z)
                elif e.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if undo_stack:
                        redo_stack.append(canvas.copy())
                        canvas.blit(undo_stack.pop(),(0,0))

                # Redo (Ctrl+Y)
                elif e.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if redo_stack:
                        undo_stack.append(canvas.copy())
                        canvas.blit(redo_stack.pop(),(0,0))

                # Text input mode
                elif typing:
                    if e.key == pygame.K_RETURN:
                        img = font.render(text_data,True,color)
                        canvas.blit(img,text_pos)
                        text_data=""
                        typing=False

                    elif e.key == pygame.K_ESCAPE:
                        # Cancel text input completely
                        typing = False
                        text_data = ""

                    elif e.key == pygame.K_BACKSPACE:
                        text_data=text_data[:-1]

                    else:
                        text_data+=e.unicode

            elif e.type == pygame.MOUSEBUTTONDOWN:
                x,y = e.pos

                # Click on toolbar
                if y < BAR:

                    # Tool selection
                    for i,(_,key) in enumerate(tools):
                        r = pygame.Rect(5+i*75,5,70,25)
                        if r.collidepoint(x,y):
                            tool = key

                    # Brush size selection
                    for i in range(3):
                        r = pygame.Rect(5+i*45,40,40,25)
                        if r.collidepoint(x,y):
                            size_id = i

                    # Color selection
                    for i,c in enumerate(COLORS):
                        r = pygame.Rect(150+i*35,40,30,25)
                        if r.collidepoint(x,y):
                            color = c

                    continue

                # Save state for undo
                undo_stack.append(canvas.copy())
                redo_stack.clear()

                # Bucket fill tool
                if tool == "bucket":
                    target = canvas.get_at((x,cy))[:3]
                    fill(canvas,(x,cy),target,color)
                    continue

                # Text tool activation
                if tool == "text":
                    typing=True
                    text_data=""
                    text_pos=(x,cy)
                    continue

                drawing=True
                start=(x,cy)
                end=start

            elif e.type == pygame.MOUSEMOTION:
                if drawing:
                    end=(mx,cy)

                    # Freehand drawing
                    if tool=="draw":
                        pygame.draw.line(canvas,color,start,end,BRUSH[size_id])
                        start=end

                    # Soft eraser (white brush)
                    elif tool=="eraser":
                        pygame.draw.line(canvas,WHITE,start,end,BRUSH[size_id])
                        start=end

            elif e.type == pygame.MOUSEBUTTONUP:
                if drawing and start and end:

                    # Straight line
                    if tool=="line":
                        pygame.draw.line(canvas,color,start,end,BRUSH[size_id])

                    # Rectangle
                    elif tool=="rect":
                        pygame.draw.rect(canvas,color,rect_from_points(start,end),BRUSH[size_id])

                    # Square
                    elif tool=="square":
                        dx=end[0]-start[0]
                        dy=end[1]-start[1]
                        s=max(abs(dx),abs(dy))
                        pygame.draw.rect(canvas,color,(start[0],start[1],s,s),BRUSH[size_id])

                    # Circle
                    elif tool=="circle":
                        r=int(((end[0]-start[0])**2+(end[1]-start[1])**2)**0.5)
                        pygame.draw.circle(canvas,color,start,r,BRUSH[size_id])

                    # Shapes
                    elif tool=="right_triangle":
                        right_tri(canvas,color,start,end,BRUSH[size_id])

                    elif tool=="equilateral_triangle":
                        equi_tri(canvas,color,start,end,BRUSH[size_id])

                    elif tool=="rhombus":
                        diamond(canvas,color,start,end,BRUSH[size_id])

                    # Hard erase (rectangle selection)
                    elif tool=="erase_rect":
                        rect = rect_from_points(start,end)
                        pygame.draw.rect(canvas,WHITE,rect)

                drawing=False
                start=None
                end=None

        screen.fill(BG)
        screen.blit(canvas,(0,BAR))

        # Preview layer (ghost drawing)
        if drawing and start and end:
            temp = screen.copy()
            preview(temp,tool,start,end,BRUSH[size_id],BAR)
            screen.blit(temp,(0,0))

        draw_ui()

        # Render text preview
        if typing:
            img = font.render(text_data,True,color)
            screen.blit(img,(text_pos[0],text_pos[1]+BAR))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__=="__main__":
    main()