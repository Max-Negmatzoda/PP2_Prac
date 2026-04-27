import pygame
import time
import random
import json
from connect import connect


# Load configuration file; fallback to defaults if file missing or corrupted
def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except:
        return {"snake_color":[0,255,0], "grid":True, "sound":False}


# Persist configuration to disk
def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f)


# Ensure player exists in DB and return primary key
def get_player_id(username):
    conn = connect()
    cur = conn.cursor()

    # Insert player only if not exists
    cur.execute("""
        INSERT INTO players (username)
        VALUES (%s)
        ON CONFLICT (username) DO NOTHING
    """,(username,))
    conn.commit()

    # Fetch player id
    cur.execute("SELECT id FROM players WHERE username=%s",(username,))
    pid = cur.fetchone()[0]

    cur.close()
    conn.close()
    return pid


# Save game session result
def save_result(username, score, level):
    conn = connect()
    cur = conn.cursor()

    pid = get_player_id(username)

    cur.execute("""
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s,%s,%s)
    """,(pid,score,level))

    conn.commit()
    cur.close()
    conn.close()


# Get max score for current user
def get_best(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT MAX(g.score)
        FROM game_sessions g
        JOIN players p ON p.id=g.player_id
        WHERE p.username=%s
    """,(username,))

    res = cur.fetchone()[0]

    cur.close()
    conn.close()
    return res if res else 0


# Get global leaderboard
def get_top10():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, g.score, g.level_reached
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        ORDER BY g.score DESC
        LIMIT 10
    """)

    data = cur.fetchall()

    cur.close()
    conn.close()
    return data


pygame.init()

window_x = 720
window_y = 480

game_window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption("Snake")

fps = pygame.time.Clock()


# Color definitions (RGB)
black = pygame.Color(0,0,0)        # background
white = pygame.Color(255,255,255)  # normal food
orange = pygame.Color(255,165,0)   # bonus food

poison_color = pygame.Color(0,200,0)   # poison
shield_color = pygame.Color(0,100,255) # shield
speed_color  = pygame.Color(255,0,0)   # speed boost
slow_color   = pygame.Color(255,255,0) # slow

wall_color = pygame.Color(120,120,120)

font = pygame.font.Font(None,30)


# Apply user settings
settings = load_settings()
snake_color = pygame.Color(*settings["snake_color"])
grid_enabled = settings["grid"]


# Render text utility
def draw_text(text,x,y):
    img = font.render(text,True,white)
    game_window.blit(img,(x,y))


# Game over screen with explicit state parameters (no globals)
def game_over_screen(score, level):
    save_result(username,score,level)

    while True:
        game_window.fill(black)

        draw_text("GAME OVER",250,150)
        draw_text(f"Score: {score}",250,200)
        draw_text("ESC to exit",250,260)

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

        pygame.display.update()


# Main menu state selector
def main_menu():
    while True:
        game_window.fill(black)

        draw_text("1 - Play",300,150)
        draw_text("2 - Leaderboard",300,200)
        draw_text("3 - Settings",300,250)
        draw_text("ESC - Quit",300,300)

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    return "play"
                elif e.key == pygame.K_2:
                    return "leaderboard"
                elif e.key == pygame.K_3:
                    return "settings"
                elif e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        pygame.display.update()


# Leaderboard rendering loop
def leaderboard_screen():
    data = get_top10()

    while True:
        game_window.fill(black)

        draw_text("TOP 10",300,60)

        y=120
        for i,row in enumerate(data):
            draw_text(f"{i+1}. {row[0]} {row[1]} lvl:{row[2]}",200,y)
            y+=30

        draw_text("ESC - Back",250,420)

        for e in pygame.event.get():
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE:
                return

        pygame.display.update()


# Settings modification loop
def settings_screen(settings):
    global snake_color, grid_enabled

    while True:
        game_window.fill(black)

        draw_text(f"1 Grid: {settings['grid']}",200,150)
        draw_text(f"2 Sound: {settings['sound']}",200,200)
        draw_text("3 Random snake color",200,250)
        draw_text("S Save",200,300)
        draw_text("ESC Back",200,350)

        for e in pygame.event.get():
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_1:
                    settings["grid"]=not settings["grid"]
                    grid_enabled=settings["grid"]

                elif e.key==pygame.K_2:
                    settings["sound"]=not settings["sound"]

                elif e.key==pygame.K_3:
                    settings["snake_color"]=[
                        random.randint(0,255),
                        random.randint(0,255),
                        random.randint(0,255)
                    ]
                    snake_color=pygame.Color(*settings["snake_color"])

                elif e.key==pygame.K_s:
                    save_settings(settings)

                elif e.key==pygame.K_ESCAPE:
                    return

        pygame.display.update()


# Username input (blocking loop)
username=""
typing=True

while typing:
    game_window.fill(black)

    draw_text("Enter username:",250,200)
    draw_text(username,250,250)

    for e in pygame.event.get():
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_RETURN and username:
                typing=False
            elif e.key==pygame.K_BACKSPACE:
                username=username[:-1]
            else:
                username+=e.unicode

    pygame.display.update()

best_score=get_best(username)


# Generate position avoiding forbidden list
def get_free_position(forbidden):
    while True:
        pos=[random.randrange(1,(window_x//10))*10,
             random.randrange(1,(window_y//10))*10]
        if pos not in forbidden:
            return pos


# Generate obstacles dynamically by level
def generate_obstacles(level):
    obs=[]
    if level<3:
        return obs

    count=level+2

    while len(obs)<count:
        start=get_free_position(obs)
        length=random.randint(2,5)
        horizontal=random.choice([True,False])

        for i in range(length):
            block=[
                start[0]+(i*10 if horizontal else 0),
                start[1]+(i*10 if not horizontal else 0)
            ]
            if block not in obs:
                obs.append(block)

    return obs


# Main gameplay loop
def run_game():

    snake_pos=[100,50]
    snake_body=[[100,50],[90,50],[80,50]]

    direction='RIGHT'
    change_to=direction

    score=0
    level=1
    speed=15
    obstacles=[]

    fruit_pos=get_free_position(snake_body)

    t_fruit_pos=[0,0]
    t_active=False
    t_timer=5
    t_duration=5
    t_cooldown=8

    powerup=None
    powerup_pos=[0,0]
    powerup_spawn_time=0
    spawn_timer=8

    active_effect=None
    effect_start=0
    effect_duration=8000

    shield_active=False

    timer_event=pygame.USEREVENT+1
    pygame.time.set_timer(timer_event,1000)

    while True:

        for event in pygame.event.get():

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    change_to='UP'
                elif event.key==pygame.K_DOWN:
                    change_to='DOWN'
                elif event.key==pygame.K_LEFT:
                    change_to='LEFT'
                elif event.key==pygame.K_RIGHT:
                    change_to='RIGHT'

            elif event.type==timer_event:

                # Handle timed bonus food lifecycle
                if t_active:
                    t_timer-=1
                    if t_timer<=0:
                        t_active=False
                        t_timer=t_cooldown
                else:
                    t_timer-=1
                    if t_timer<=0:
                        t_active=True
                        t_timer=t_duration
                        t_fruit_pos=get_free_position(snake_body+obstacles)

                # Spawn power-ups
                if powerup is None:
                    spawn_timer-=1
                    if spawn_timer<=0:
                        powerup=random.choice(['poison','shield','speed','slow'])
                        powerup_pos=get_free_position(snake_body+obstacles)
                        powerup_spawn_time=pygame.time.get_ticks()
                        spawn_timer=8

        # Remove expired power-up from map
        if powerup:
            if pygame.time.get_ticks()-powerup_spawn_time>=8000:
                powerup=None

        # Direction validation
        if change_to=='UP' and direction!='DOWN':
            direction='UP'
        if change_to=='DOWN' and direction!='UP':
            direction='DOWN'
        if change_to=='LEFT' and direction!='RIGHT':
            direction='LEFT'
        if change_to=='RIGHT' and direction!='LEFT':
            direction='RIGHT'

        # Movement update
        if direction=='UP':
            snake_pos[1]-=10
        if direction=='DOWN':
            snake_pos[1]+=10
        if direction=='LEFT':
            snake_pos[0]-=10
        if direction=='RIGHT':
            snake_pos[0]+=10

        snake_body.insert(0,list(snake_pos))

        # Normal food collision
        if snake_pos==fruit_pos:
            score+=10
            fruit_pos=get_free_position(snake_body+obstacles)
        else:
            snake_body.pop()

        # Bonus food collision
        if t_active and snake_pos==t_fruit_pos:
            score+=25
            snake_body.append(snake_body[-1])
            t_active=False
            t_timer=t_cooldown

        # Power-up collision
        if powerup and snake_pos==powerup_pos:

            if powerup=='poison':
                for _ in range(2):
                    if len(snake_body)>1:
                        snake_body.pop()
                if len(snake_body)<=1:
                    game_over_screen(score,level)

            elif powerup=='shield':
                shield_active=True

            elif powerup=='speed':
                active_effect='speed'
                effect_start=pygame.time.get_ticks()
                speed+=5

            elif powerup=='slow':
                active_effect='slow'
                effect_start=pygame.time.get_ticks()
                speed=max(5,speed-5)

            powerup=None
            spawn_timer=8

        # Effect expiration logic
        if active_effect:
            if pygame.time.get_ticks()-effect_start>=effect_duration:
                if active_effect=='speed':
                    speed-=5
                elif active_effect=='slow':
                    speed+=5
                active_effect=None

        game_window.fill(black)

        # Optional grid rendering
        if grid_enabled:
            for x in range(0,window_x,10):
                pygame.draw.line(game_window,(50,50,50),(x,0),(x,window_y))
            for y in range(0,window_y,10):
                pygame.draw.line(game_window,(50,50,50),(0,y),(window_x,y))

        # Render snake
        for pos in snake_body:
            pygame.draw.rect(game_window,snake_color,pygame.Rect(pos[0],pos[1],10,10))

        # Render normal food
        pygame.draw.rect(game_window,white,pygame.Rect(fruit_pos[0],fruit_pos[1],10,10))

        # Render bonus food
        if t_active:
            pygame.draw.rect(game_window,orange,pygame.Rect(t_fruit_pos[0],t_fruit_pos[1],10,10))

        # Render power-up
        if powerup:
            color={'poison':poison_color,'shield':shield_color,'speed':speed_color,'slow':slow_color}[powerup]
            pygame.draw.rect(game_window,color,pygame.Rect(powerup_pos[0],powerup_pos[1],10,10))

        # Render obstacles
        for block in obstacles:
            pygame.draw.rect(game_window,wall_color,pygame.Rect(block[0],block[1],10,10))

        # Boundary collision
        if snake_pos[0]<0 or snake_pos[0]>=window_x or snake_pos[1]<0 or snake_pos[1]>=window_y:
            if shield_active:
                shield_active=False
            else:
                game_over_screen(score,level)

        # Self collision
        for block in snake_body[1:]:
            if snake_pos==block:
                if shield_active:
                    shield_active=False
                else:
                    game_over_screen(score,level)

        # Obstacle collision
        for block in obstacles:
            if snake_pos==block:
                if shield_active:
                    shield_active=False
                else:
                    game_over_screen(score,level)

        # Level progression logic
        if score>=level*20:
            level+=1
            speed+=2
            obstacles=generate_obstacles(level)

        # HUD rendering
        draw_text(f"Score: {score}",10,10)
        draw_text(f"Best: {best_score}",10,40)
        draw_text(f"Level: {level}",600,10)

        if shield_active:
            draw_text("Shield ACTIVE",550,40)

        pygame.display.update()
        fps.tick(speed)


# Main application loop (state machine)
while True:
    action=main_menu()

    if action=="play":
        run_game()
    elif action=="leaderboard":
        leaderboard_screen()
    elif action=="settings":
        settings_screen(settings)