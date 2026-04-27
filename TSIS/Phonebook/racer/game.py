import pygame, random, sys, os, time, json
from pygame.locals import *

# ---------------------------------------------------------------------------
# Window & display constants
# ---------------------------------------------------------------------------
WINDOWWIDTH  = 800
WINDOWHEIGHT = 600

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
TEXTCOLOR      = (255, 255, 255)
BACKGROUNDCOLOR = (0,   0,   0)
YELLOW  = (255, 215,   0)
RED     = (220,  50,  50)
BROWN   = (139,  90,  43)
BLUE    = ( 50, 120, 220)
GREEN   = ( 50, 200,  80)
GRAY    = (160, 160, 160)
ORANGE  = (255, 140,   0)
CYAN    = (  0, 220, 220)
PURPLE  = (160,  50, 220)
DARK_GRAY = (40,  40,  40)
LIGHT_GRAY = (200, 200, 200)

# ---------------------------------------------------------------------------
# Frame rate
# ---------------------------------------------------------------------------
FPS = 40

# ---------------------------------------------------------------------------
# Enemy / coin / obstacle spawn rates and sizes
# ---------------------------------------------------------------------------
BADDIEMINSIZE  = 10
BADDIEMAXSIZE  = 40
BADDIEMINSPEED = 8
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6

PLAYERMOVERATE = 5

COINSIZE      = 10
COINSPEED     = 8
ADDNEWCOINS   = 7

ROAD_EVENT_RATE     = 180
ROAD_EVENT_DURATION = 120
OBSTACLE_RATE       = 90
HAZARD_RATE         = 60
POWERUP_RATE        = 200
POWERUP_TIMEOUT     = 300
NITRO_DURATION      = 3 * FPS   # 3 seconds

# ---------------------------------------------------------------------------
# Hazard / event / obstacle / power-up type constants
# ---------------------------------------------------------------------------
HAZARD_OIL  = 'oil'
HAZARD_SLOW = 'slow'
HAZARD_NONE = 'none'

EVENT_BARRIER   = 'barrier'
EVENT_SPEEDBUMP = 'speedbump'
EVENT_NITRO     = 'nitro'

OBSTACLE_BARRIER = 'barrier'
OBSTACLE_OIL     = 'oil'
OBSTACLE_POTHOLE = 'pothole'

PU_NITRO  = 'nitro'
PU_SHIELD = 'shield'
PU_REPAIR = 'repair'

# ---------------------------------------------------------------------------
# File paths
# ---------------------------------------------------------------------------
DATA_DIR         = './Practice10&11/racer/data'
LEADERBOARD_FILE = os.path.join(DATA_DIR, 'leaderboard.json')
SETTINGS_FILE    = os.path.join(DATA_DIR, 'settings.json')
SAVE_FILE        = os.path.join(DATA_DIR, 'save.dat')
COINS_FILE       = os.path.join(DATA_DIR, 'coins_count.dat')

# ---------------------------------------------------------------------------
# Road lanes (x-range inside the track)
# ---------------------------------------------------------------------------
LANE_LEFT  = (150, 260)
LANE_MID   = (260, 370)
LANE_RIGHT = (370, 480)
LANES = [LANE_LEFT, LANE_MID, LANE_RIGHT]

# ---------------------------------------------------------------------------
# Car color tints available in Settings
# ---------------------------------------------------------------------------
CAR_COLORS = {
    'Default': None,
    'Red':    RED,
    'Blue':   BLUE,
    'Green':  GREEN,
    'Yellow': YELLOW,
}
CAR_COLOR_KEYS = list(CAR_COLORS.keys())

# ---------------------------------------------------------------------------
# Difficulty presets
# ---------------------------------------------------------------------------
DIFFICULTIES = ['Easy', 'Normal', 'Hard']
DIFFICULTY_SPEED_MULT = {'Easy': 0.7, 'Normal': 1.0, 'Hard': 1.4}


# ===========================================================================
# Settings helpers
# ===========================================================================

def defaultSettings():
    """Return factory-default settings dictionary."""
    return {
        'sound':      True,
        'car_color':  'Default',
        'difficulty': 'Normal',
    }


def loadSettings():
    """Load settings.json; fall back to defaults if file is absent or corrupt."""
    if not os.path.exists(SETTINGS_FILE):
        return defaultSettings()
    try:
        with open(SETTINGS_FILE, 'r') as f:
            data = json.load(f)
        # Fill in any missing keys with defaults
        defaults = defaultSettings()
        for key, val in defaults.items():
            data.setdefault(key, val)
        return data
    except Exception:
        return defaultSettings()


def saveSettings(settings):
    """Persist settings dictionary to settings.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)


# ===========================================================================
# Leaderboard helpers
# ===========================================================================

def loadLeaderboard():
    """Load top-10 list from JSON; return empty list if file is missing."""
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return []


def saveLeaderboard(lb):
    """Write leaderboard list to JSON file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(lb, f, indent=2)


def addToLeaderboard(lb, name, score, distance):
    """Insert new entry, sort by score descending, keep only top 10."""
    lb.append({'name': name, 'score': score, 'distance': distance})
    lb.sort(key=lambda x: x['score'], reverse=True)
    return lb[:10]


# ===========================================================================
# Utility / drawing helpers
# ===========================================================================

def terminate():
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    """Block until the player presses any key (ESC quits)."""
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


def drawText(text, font, surface, x, y, color=TEXTCOLOR):
    """Render text at (x, y) top-left position."""
    obj  = font.render(text, 1, color)
    rect = obj.get_rect()
    rect.topleft = (x, y)
    surface.blit(obj, rect)


def drawTextCentered(text, font, surface, cx, y, color=TEXTCOLOR):
    """Render text horizontally centered around cx."""
    obj  = font.render(text, 1, color)
    rect = obj.get_rect(center=(cx, y))
    surface.blit(obj, rect)


def drawButton(surface, font, label, rect, hovered=False, color=DARK_GRAY, hover_color=GRAY):
    """Draw a simple rectangular button; returns True if mouse is over it."""
    bg = hover_color if hovered else color
    pygame.draw.rect(surface, bg, rect, border_radius=8)
    pygame.draw.rect(surface, LIGHT_GRAY, rect, 2, border_radius=8)
    obj = font.render(label, 1, TEXTCOLOR)
    surface.blit(obj, obj.get_rect(center=rect.center))
    return hovered


def isHovered(rect):
    """Check if the mouse cursor is currently inside rect."""
    mx, my = pygame.mouse.get_pos()
    return rect.collidepoint(mx, my)


# ===========================================================================
# Game-object collision helpers
# ===========================================================================

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False


def playerHasHitCoin(playerRect, coins):
    for coin in coins:
        if playerRect.colliderect(coin['rect']):
            return True
    return False


def getHazardUnderPlayer(playerRect, hazards):
    for h in hazards:
        if playerRect.colliderect(h['rect']):
            return h['type']
    return HAZARD_NONE


def getRoadEventUnderPlayer(playerRect, events):
    for e in events:
        if playerRect.colliderect(e['rect']):
            return e['type']
    return None


def playerHitObstacle(playerRect, obstacles):
    for o in obstacles:
        if playerRect.colliderect(o['rect']):
            return True
    return False


def isSafeSpawn(newRect, playerRect, margin=60):
    """Return True if newRect doesn't overlap an expanded playerRect."""
    expanded = playerRect.inflate(margin, margin)
    return not expanded.colliderect(newRect)


# ===========================================================================
# Road-element draw helpers
# ===========================================================================

def drawHazard(surface, hazard):
    r = hazard['rect']
    if hazard['type'] == HAZARD_OIL:
        pygame.draw.ellipse(surface, (25, 18, 8), r)
        rainbow = [(120, 0, 180), (0, 80, 200), (0, 160, 60), (180, 160, 0)]
        strip_w = r.width // len(rainbow)
        for i, color in enumerate(rainbow):
            s = pygame.Surface((strip_w, r.height), pygame.SRCALPHA)
            s.fill((*color, 110))
            surface.blit(s, (r.x + i * strip_w, r.y))
        pygame.draw.ellipse(surface, (100, 80, 40), r, 2)
    elif hazard['type'] == HAZARD_SLOW:
        s = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
        s.fill((50, 100, 220, 90))
        surface.blit(s, (r.x, r.y))
        pygame.draw.rect(surface, BLUE, r, 2)


def drawRoadEvent(surface, event):
    r = event['rect']
    if event['type'] == EVENT_BARRIER:
        pygame.draw.rect(surface, RED, r)
        for i in range(0, r.width, 10):
            pygame.draw.rect(surface, (255, 255, 255), (r.x + i, r.y, 5, r.height))
    elif event['type'] == EVENT_SPEEDBUMP:
        pygame.draw.rect(surface, BROWN, r)
        pygame.draw.rect(surface, (200, 160, 80), r, 2)
    elif event['type'] == EVENT_NITRO:
        s = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
        s.fill((50, 220, 80, 100))
        surface.blit(s, (r.x, r.y))
        pygame.draw.rect(surface, GREEN, r, 3)


def drawObstacle(surface, obs):
    r = obs['rect']
    if obs['type'] == OBSTACLE_BARRIER:
        pygame.draw.rect(surface, GRAY, r)
        pygame.draw.rect(surface, RED, r, 2)
    elif obs['type'] == OBSTACLE_OIL:
        pygame.draw.ellipse(surface, (20, 15, 5), r)
        pygame.draw.ellipse(surface, (60, 45, 15), r, 2)
    elif obs['type'] == OBSTACLE_POTHOLE:
        pygame.draw.ellipse(surface, (40, 30, 20), r)
        pygame.draw.ellipse(surface, (90, 70, 50), r, 2)


def drawPowerUp(surface, pu):
    """Draw a collectible power-up as a labeled circle (N / S / R)."""
    r  = pu['rect']
    cx, cy = r.centerx, r.centery
    color_map = {PU_NITRO: ORANGE, PU_SHIELD: CYAN, PU_REPAIR: PURPLE}
    label_map = {PU_NITRO: 'N',    PU_SHIELD: 'S',   PU_REPAIR: 'R'}
    color  = color_map[pu['type']]
    letter = label_map[pu['type']]
    pygame.draw.circle(surface, color, (cx, cy), 18)
    pygame.draw.circle(surface, TEXTCOLOR, (cx, cy), 18, 2)
    small_font = pygame.font.Font(None, 26)
    lbl = small_font.render(letter, 1, TEXTCOLOR)
    surface.blit(lbl, lbl.get_rect(center=(cx, cy)))


def drawActivePowerUp(surface, font, active_pu, active_pu_timer):
    """Show active power-up name and remaining seconds in the top-right corner."""
    if active_pu == PU_NITRO:
        secs  = max(0, active_pu_timer // FPS)
        label = 'NITRO: %ds' % secs
        drawText(label, font, surface, 550, 0, ORANGE)
    elif active_pu == PU_SHIELD:
        drawText('SHIELD active', font, surface, 550, 0, CYAN)


def applyCarTint(base_image, color_name):
    """Return a copy of base_image tinted with the chosen color, or original if Default."""
    if color_name == 'Default' or color_name not in CAR_COLORS:
        return base_image
    tint = CAR_COLORS[color_name]
    tinted = base_image.copy()
    tint_surf = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
    tint_surf.fill((*tint, 120))   # semi-transparent tint overlay
    tinted.blit(tint_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return tinted


# ===========================================================================
# Screen: ask username
# ===========================================================================

def askUsername(surface, font):
    """Text-input screen: player types their name before the game starts."""
    name = ''
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_RETURN and len(name) > 0:
                    return name
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                elif event.key == K_ESCAPE:
                    terminate()
                elif len(name) < 14 and event.unicode.isprintable():
                    name += event.unicode
        surface.fill(BACKGROUNDCOLOR)
        drawTextCentered('Enter your name:', font, surface, WINDOWWIDTH // 2, 220)
        drawTextCentered(name + '_', font, surface, WINDOWWIDTH // 2, 260, YELLOW)
        drawTextCentered('Press ENTER to confirm', font, surface, WINDOWWIDTH // 2, 290)
        pygame.display.update()


# ===========================================================================
# Screen: Main Menu
# ===========================================================================

def showMainMenu(surface, font, big_font):
    """
    Display the main menu with four buttons.
    Returns the chosen action string: 'play', 'leaderboard', 'settings', 'quit'.
    """
    btn_w, btn_h = 220, 50
    cx = WINDOWWIDTH // 2

    buttons = {
        'play':        pygame.Rect(cx - btn_w // 2, 200, btn_w, btn_h),
        'leaderboard': pygame.Rect(cx - btn_w // 2, 270, btn_w, btn_h),
        'settings':    pygame.Rect(cx - btn_w // 2, 340, btn_w, btn_h),
        'quit':        pygame.Rect(cx - btn_w // 2, 410, btn_w, btn_h),
    }
    labels = {
        'play':        'Play',
        'leaderboard': 'Leaderboard',
        'settings':    'Settings',
        'quit':        'Quit',
    }

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                terminate()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for action, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        return action

        surface.fill(BACKGROUNDCOLOR)
        drawTextCentered('CAR RACER', big_font, surface, cx, 110, YELLOW)
        drawTextCentered('Use arrow keys / WASD to drive', font, surface, cx, 160)

        for action, rect in buttons.items():
            drawButton(surface, font, labels[action], rect, hovered=isHovered(rect))

        pygame.display.update()


# ===========================================================================
# Screen: Settings
# ===========================================================================

def showSettings(surface, font, big_font, settings):
    """
    Settings screen: toggle sound, pick car color, choose difficulty.
    Saves and returns updated settings when the player hits Back.
    """
    cx    = WINDOWWIDTH // 2
    btn_w = 180
    btn_h = 44

    # Navigation buttons
    back_rect  = pygame.Rect(cx - 100, 500, 200, 50)
    reset_rect = pygame.Rect(cx + 120, 500, 180, 50)

    # Sound toggle button
    sound_rect = pygame.Rect(cx, 150, 160, 44)

    # Car color arrow buttons
    color_left  = pygame.Rect(cx - 130, 240, 44, 44)
    color_right = pygame.Rect(cx + 90,  240, 44, 44)

    # Difficulty arrow buttons
    diff_left  = pygame.Rect(cx - 130, 330, 44, 44)
    diff_right = pygame.Rect(cx + 90,  330, 44, 44)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                saveSettings(settings)
                return settings
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                # Toggle sound on / off
                if sound_rect.collidepoint(mx, my):
                    settings['sound'] = not settings['sound']

                # Cycle car color
                elif color_left.collidepoint(mx, my):
                    idx = CAR_COLOR_KEYS.index(settings['car_color'])
                    settings['car_color'] = CAR_COLOR_KEYS[(idx - 1) % len(CAR_COLOR_KEYS)]
                elif color_right.collidepoint(mx, my):
                    idx = CAR_COLOR_KEYS.index(settings['car_color'])
                    settings['car_color'] = CAR_COLOR_KEYS[(idx + 1) % len(CAR_COLOR_KEYS)]

                # Cycle difficulty
                elif diff_left.collidepoint(mx, my):
                    idx = DIFFICULTIES.index(settings['difficulty'])
                    settings['difficulty'] = DIFFICULTIES[(idx - 1) % len(DIFFICULTIES)]
                elif diff_right.collidepoint(mx, my):
                    idx = DIFFICULTIES.index(settings['difficulty'])
                    settings['difficulty'] = DIFFICULTIES[(idx + 1) % len(DIFFICULTIES)]

                # Back — save and return
                elif back_rect.collidepoint(mx, my):
                    saveSettings(settings)
                    return settings

                # Reset to defaults
                elif reset_rect.collidepoint(mx, my):
                    settings = defaultSettings()

        # Draw screen
        surface.fill(BACKGROUNDCOLOR)
        drawTextCentered('SETTINGS', big_font, surface, cx, 70, YELLOW)

        # Sound row
        drawText('Sound:', font, surface, cx - 180, 162)
        sound_label = 'ON' if settings['sound'] else 'OFF'
        sound_color = GREEN if settings['sound'] else RED
        drawButton(surface, font, sound_label, sound_rect, hovered=isHovered(sound_rect), color=sound_color, hover_color=sound_color)

        # Car color row
        drawText('Car Color:', font, surface, cx - 180, 252)
        drawButton(surface, font, '<', color_left,  hovered=isHovered(color_left))
        drawButton(surface, font, '>', color_right, hovered=isHovered(color_right))
        # Color preview swatch
        swatch_color = CAR_COLORS[settings['car_color']] or GRAY
        pygame.draw.rect(surface, swatch_color, pygame.Rect(cx - 85, 242, 170, 44), border_radius=6)
        pygame.draw.rect(surface, LIGHT_GRAY,   pygame.Rect(cx - 85, 242, 170, 44), 2, border_radius=6)
        drawTextCentered(settings['car_color'], font, surface, cx, 264)

        # Difficulty row
        drawText('Difficulty:', font, surface, cx - 180, 342)
        drawButton(surface, font, '<', diff_left,  hovered=isHovered(diff_left))
        drawButton(surface, font, '>', diff_right, hovered=isHovered(diff_right))
        diff_color = {
            'Easy': GREEN, 'Normal': YELLOW, 'Hard': RED
        }[settings['difficulty']]
        pygame.draw.rect(surface, DARK_GRAY, pygame.Rect(cx - 85, 332, 170, 44), border_radius=6)
        pygame.draw.rect(surface, LIGHT_GRAY, pygame.Rect(cx - 85, 332, 170, 44), 2, border_radius=6)
        drawTextCentered(settings['difficulty'], font, surface, cx, 354, diff_color)

        # Back / Reset buttons
        drawButton(surface, font, 'Back', back_rect,   hovered=isHovered(back_rect))
        drawButton(surface, font, 'Reset Defaults', reset_rect, hovered=isHovered(reset_rect))

        pygame.display.update()


# ===========================================================================
# Screen: Leaderboard
# ===========================================================================

def showLeaderboard(surface, font, big_font, lb):
    """
    Display the top-10 leaderboard with a Back button.
    Returns when the player clicks Back or presses ESC.
    """
    cx        = WINDOWWIDTH // 2
    back_rect = pygame.Rect(cx - 90, 530, 180, 46)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if back_rect.collidepoint(event.pos):
                    return

        surface.fill(BACKGROUNDCOLOR)
        drawTextCentered('TOP 10 LEADERBOARD', big_font, surface, cx, 40, YELLOW)

        # Column headers
        headers = 'Rank  Name            Score    Distance'
        drawText(headers, font, surface, 100, 80)
        pygame.draw.line(surface, GRAY, (100, 102), (700, 102), 1)

        if not lb:
            drawTextCentered('No records yet — go race!', font, surface, cx, 280, GRAY)
        else:
            for i, entry in enumerate(lb):
                y    = 112 + i * 30
                rank = str(i + 1).ljust(6)
                name = entry['name'][:14].ljust(16)
                sc   = str(entry['score']).ljust(9)
                dist = str(entry['distance']) + 'm'
                row_color = YELLOW if i == 0 else TEXTCOLOR
                drawText('%s%s%s%s' % (rank, name, sc, dist), font, surface, 100, y, row_color)

        drawButton(surface, font, 'Back', back_rect, hovered=isHovered(back_rect))
        pygame.display.update()


# ===========================================================================
# Screen: Game Over
# ===========================================================================

def showGameOver(surface, font, big_font, total_score, distance, coin_count, lives_left):
    """
    Game-over screen showing final stats and two buttons:
    - Retry  → returns 'retry'
    - Main Menu → returns 'menu'
    """
    cx         = WINDOWWIDTH // 2
    retry_rect = pygame.Rect(cx - 210, 420, 180, 50)
    menu_rect  = pygame.Rect(cx + 30,  420, 180, 50)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return 'menu'
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if retry_rect.collidepoint(event.pos):
                    return 'retry'
                if menu_rect.collidepoint(event.pos):
                    return 'menu'

        surface.fill(BACKGROUNDCOLOR)
        drawTextCentered('GAME OVER', big_font, surface, cx, 100, RED)

        # Final stats block
        stats = [
            ('Score',    str(total_score)),
            ('Distance', str(distance) + ' m'),
            ('Coins',    str(coin_count)),
            ('Lives left', str(lives_left)),
        ]
        for row, (label, value) in enumerate(stats):
            y = 210 + row * 46
            drawTextCentered('%s:  %s' % (label, value), font, surface, cx, y, YELLOW)

        drawButton(surface, font, 'Retry',     retry_rect, hovered=isHovered(retry_rect))
        drawButton(surface, font, 'Main Menu', menu_rect,  hovered=isHovered(menu_rect))

        pygame.display.update()


# ===========================================================================
# Pygame initialisation
# ===========================================================================

pygame.init()
mainClock = pygame.time.Clock()

windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Car Racer')
pygame.mouse.set_visible(True)   # cursor visible for menu buttons

font     = pygame.font.Font(None, 30)
big_font = pygame.font.Font(None, 58)

# ---------------------------------------------------------------------------
# Load sounds
# ---------------------------------------------------------------------------
gameOverSound = pygame.mixer.Sound('./Practice10&11/racer/music/crash.wav')
pygame.mixer.music.load('./Practice10&11/racer/music/car.wav')
laugh = pygame.mixer.Sound('./Practice10&11/racer/music/laugh.wav')

# ---------------------------------------------------------------------------
# Load images
# ---------------------------------------------------------------------------
playerImageBase = pygame.image.load('./Practice10&11/racer/image/car1.png')
car3 = pygame.image.load('./Practice10&11/racer/image/car3.png')
car4 = pygame.image.load('./Practice10&11/racer/image/car4.png')

baddieImage  = pygame.image.load('./Practice10&11/racer/image/car2.png')
enemy_pool   = [car3, car4, baddieImage]

wallLeft  = pygame.image.load('./Practice10&11/racer/image/left.png')
wallRight = pygame.image.load('./Practice10&11/racer/image/right.png')

coinImage  = pygame.image.load('./Practice10&11/racer/image/653278_coin_bitcoin_cash_currency_dollar_icon.png')
coinImage2 = pygame.image.load('./Practice10&11/racer/image/5310117_coin_dollar_money_icon.png')
coinImage3 = pygame.image.load('./Practice10&11/racer/image/3319620_coin_dollar_money_shine_icon.png')
coin_pool  = [coinImage, coinImage2, coinImage3]

# ---------------------------------------------------------------------------
# Ensure data directory and persistent files exist
# ---------------------------------------------------------------------------
os.makedirs(DATA_DIR, exist_ok=True)

if not os.path.exists(COINS_FILE):
    open(COINS_FILE, 'w').write('0')
if not os.path.exists(SAVE_FILE):
    open(SAVE_FILE, 'w').write('0')

topScore  = int(open(SAVE_FILE).read().strip() or '0')
most_coin = int(open(COINS_FILE).read().strip() or '0')

# ---------------------------------------------------------------------------
# Ask for player name (once per session)
# ---------------------------------------------------------------------------
player_name = askUsername(windowSurface, font)

# Load leaderboard and settings from disk
leaderboard = loadLeaderboard()
settings    = loadSettings()

# ===========================================================================
# Main application loop — handles menus and game restarts
# ===========================================================================

lives = 3   # player starts with 3 lives

while True:

    # -----------------------------------------------------------------------
    # Main Menu
    # -----------------------------------------------------------------------
    action = showMainMenu(windowSurface, font, big_font)

    if action == 'quit':
        terminate()

    elif action == 'leaderboard':
        showLeaderboard(windowSurface, font, big_font, leaderboard)
        continue   # return to main menu

    elif action == 'settings':
        settings = showSettings(windowSurface, font, big_font, settings)
        # Apply sound preference immediately
        if not settings['sound']:
            pygame.mixer.music.stop()
        continue   # return to main menu

    elif action == 'play':
        lives = 3  # reset lives for a fresh game session

    # -----------------------------------------------------------------------
    # Build player image respecting current car-color setting
    # -----------------------------------------------------------------------
    playerImage = applyCarTint(playerImageBase, settings['car_color'])
    playerRect  = playerImage.get_rect()

    # Speed multiplier from difficulty setting
    speed_mult = DIFFICULTY_SPEED_MULT[settings['difficulty']]

    # -----------------------------------------------------------------------
    # Lives loop — each iteration is one "life"
    # -----------------------------------------------------------------------
    while lives > 0:

        # Reset per-life state
        baddies       = []
        coins         = []
        lane_hazards  = []
        road_events   = []
        road_obstacles= []
        power_ups     = []

        coinAddCounter   = 0
        baddieAddCounter = 0
        hazard_counter   = 0
        event_counter    = 0
        obstacle_counter = 0
        powerup_counter  = 0

        score      = 0
        distance   = 0
        coin_count = 0
        total_score = 0

        active_pu      = None
        active_pu_timer = 0
        shield_active  = False
        nitro_timer    = 0

        playerRect.topleft = (WINDOWWIDTH // 2, WINDOWHEIGHT - 50)

        moveLeft = moveRight = moveUp = moveDown = False
        reverseCheat = slowCheat = False

        # Start background music if sound is enabled
        if settings['sound']:
            pygame.mixer.music.play(-1, 0.0)

        pygame.mouse.set_visible(False)   # hide cursor during gameplay

        # -------------------------------------------------------------------
        # Inner game loop — runs each frame while the player is alive
        # -------------------------------------------------------------------
        while True:
            score    += 1
            distance  = score // 10

            # ---- Event handling ------------------------------------------
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == ord('z'):  reverseCheat = True
                    if event.key == ord('x'):  slowCheat    = True
                    if event.key in (K_LEFT,  ord('a')): moveLeft  = True;  moveRight = False
                    if event.key in (K_RIGHT, ord('d')): moveRight = True;  moveLeft  = False
                    if event.key in (K_UP,    ord('w')): moveUp    = True;  moveDown  = False
                    if event.key in (K_DOWN,  ord('s')): moveDown  = True;  moveUp    = False
                if event.type == KEYUP:
                    if event.key == ord('z'): reverseCheat = False; score = 0
                    if event.key == ord('x'): slowCheat    = False; score = 0
                    if event.key == K_ESCAPE: terminate()
                    if event.key in (K_LEFT,  ord('a')): moveLeft  = False
                    if event.key in (K_RIGHT, ord('d')): moveRight = False
                    if event.key in (K_UP,    ord('w')): moveUp    = False
                    if event.key in (K_DOWN,  ord('s')): moveDown  = False

            # ---- Advance counters only when no cheat is active ------------
            if not reverseCheat and not slowCheat:
                baddieAddCounter += 1
                coinAddCounter   += 1
                hazard_counter   += 1
                event_counter    += 1
                obstacle_counter += 1
                powerup_counter  += 1

            # ---- Tick active nitro power-up timer -------------------------
            if active_pu == PU_NITRO:
                active_pu_timer -= 1
                if active_pu_timer <= 0:
                    active_pu = None   # nitro expired

            # ---- Spawn coin -----------------------------------------------
            if coinAddCounter == ADDNEWCOINS + 10:
                coinAddCounter = 0
                choice  = random.choice(coin_pool)
                coinX   = random.randint(140, 485)
                coinRect = pygame.Rect(coinX, -COINSIZE, 30, 30)
                if isSafeSpawn(coinRect, playerRect):
                    coins.append({
                        'rect':    coinRect,
                        'speed':   COINSPEED * speed_mult,
                        'surface': pygame.transform.scale(choice, (30, 30)),
                        'choice':  choice,
                    })

            # ---- Spawn enemy car + side walls -----------------------------
            if baddieAddCounter == ADDNEWBADDIERATE:
                baddieAddCounter = 0
                baddieX   = random.randint(140, 485)
                baddieRect = pygame.Rect(baddieX, -30, 23, 47)
                if isSafeSpawn(baddieRect, playerRect):
                    baddies.append({
                        'rect':    baddieRect,
                        'speed':   random.randint(BADDIEMINSPEED, BADDIEMAXSPEED) * speed_mult,
                        'surface': pygame.transform.scale(random.choice(enemy_pool), (23, 47)),
                    })
                # Side walls scroll with the same speed multiplier
                wall_speed = random.randint(BADDIEMINSPEED, BADDIEMAXSPEED) * speed_mult
                baddies.append({
                    'rect':    pygame.Rect(0, 0, 126, 600),
                    'speed':   wall_speed,
                    'surface': pygame.transform.scale(wallLeft, (126, 599)),
                })
                baddies.append({
                    'rect':    pygame.Rect(497, 0, 303, 600),
                    'speed':   wall_speed,
                    'surface': pygame.transform.scale(wallRight, (303, 599)),
                })

            # ---- Spawn lane hazard ----------------------------------------
            if hazard_counter >= HAZARD_RATE:
                hazard_counter = 0
                lane = random.choice(LANES)
                hx   = random.randint(lane[0], lane[1] - 30)
                hType = random.choice([HAZARD_OIL, HAZARD_SLOW])
                hRect = pygame.Rect(hx, -40, 80, 40) if hType == HAZARD_OIL else pygame.Rect(hx, -30, 50, 30)
                if isSafeSpawn(hRect, playerRect):
                    lane_hazards.append({'rect': hRect, 'type': hType, 'speed': BADDIEMINSPEED * speed_mult})

            # ---- Spawn road event -----------------------------------------
            if event_counter >= ROAD_EVENT_RATE:
                event_counter = 0
                eType = random.choice([EVENT_BARRIER, EVENT_SPEEDBUMP, EVENT_NITRO])
                eX    = random.randint(150, 440)
                eRect = pygame.Rect(eX, -20, 100, 18)
                if isSafeSpawn(eRect, playerRect):
                    road_events.append({'rect': eRect, 'type': eType, 'speed': BADDIEMINSPEED * speed_mult, 'timer': ROAD_EVENT_DURATION})

            # ---- Spawn static road obstacle --------------------------------
            if obstacle_counter >= OBSTACLE_RATE:
                obstacle_counter = 0
                oType = random.choice([OBSTACLE_BARRIER, OBSTACLE_OIL, OBSTACLE_POTHOLE])
                oX    = random.randint(150, 460)
                dims  = {'barrier': (60, 18), 'oil': (55, 22), 'pothole': (40, 24)}[oType]
                oRect = pygame.Rect(oX, -20, *dims)
                if isSafeSpawn(oRect, playerRect):
                    road_obstacles.append({'rect': oRect, 'type': oType, 'speed': BADDIEMINSPEED * speed_mult})

            # ---- Spawn collectible power-up --------------------------------
            if powerup_counter >= POWERUP_RATE:
                powerup_counter = 0
                puType = random.choice([PU_NITRO, PU_SHIELD, PU_REPAIR])
                puX    = random.randint(155, 465)
                puRect = pygame.Rect(puX, -36, 36, 36)
                if isSafeSpawn(puRect, playerRect):
                    power_ups.append({'rect': puRect, 'type': puType, 'speed': BADDIEMINSPEED * speed_mult, 'timeout': POWERUP_TIMEOUT})

            # ---- Determine current movement speed -------------------------
            current_speed = PLAYERMOVERATE
            hazard_type   = getHazardUnderPlayer(playerRect, lane_hazards)
            event_type    = getRoadEventUnderPlayer(playerRect, road_events)

            if active_pu == PU_NITRO:
                current_speed = int(PLAYERMOVERATE * 1.8)
            elif nitro_timer > 0:
                current_speed = int(PLAYERMOVERATE * 1.8)
                nitro_timer  -= 1
            elif hazard_type == HAZARD_OIL:
                current_speed = max(1, int(PLAYERMOVERATE * 0.5))
            elif hazard_type == HAZARD_SLOW:
                current_speed = max(1, int(PLAYERMOVERATE * 0.6))

            if event_type == EVENT_NITRO and nitro_timer == 0 and active_pu != PU_NITRO:
                nitro_timer = 80
            elif event_type == EVENT_SPEEDBUMP:
                current_speed = max(1, int(current_speed * 0.4))

            # ---- Move player ----------------------------------------------
            if moveLeft  and playerRect.left   > 0:            playerRect.move_ip(-current_speed, 0)
            if moveRight and playerRect.right  < WINDOWWIDTH:  playerRect.move_ip( current_speed, 0)
            if moveUp    and playerRect.top    > 0:            playerRect.move_ip(0, -current_speed)
            if moveDown  and playerRect.bottom < WINDOWHEIGHT: playerRect.move_ip(0,  current_speed)

            # ---- Scroll and cull coins ------------------------------------
            scroll_dir = -5 if reverseCheat else (1 if slowCheat else 1)
            coin_spd   = -5 if reverseCheat else (1 if slowCheat else None)
            for coin in coins:
                coin['rect'].move_ip(0, coin_spd if coin_spd else coin['speed'])
            coins = [c for c in coins if c['rect'].top <= WINDOWHEIGHT]

            # ---- Scroll and cull enemies ----------------------------------
            for b in baddies:
                b['rect'].move_ip(0, -5 if reverseCheat else (1 if slowCheat else b['speed']))
            baddies = [b for b in baddies if b['rect'].top <= WINDOWHEIGHT]

            # ---- Scroll and cull hazards ----------------------------------
            for h in lane_hazards:
                h['rect'].move_ip(0, h['speed'])
            lane_hazards = [h for h in lane_hazards if h['rect'].top <= WINDOWHEIGHT]

            # ---- Scroll, tick timer, and cull road events -----------------
            for e in road_events:
                e['rect'].move_ip(0, e['speed'])
                e['timer'] -= 1
            road_events = [e for e in road_events if e['rect'].top <= WINDOWHEIGHT and e['timer'] > 0]

            # ---- Scroll and cull static obstacles -------------------------
            for o in road_obstacles:
                o['rect'].move_ip(0, o['speed'])
            road_obstacles = [o for o in road_obstacles if o['rect'].top <= WINDOWHEIGHT]

            # ---- Scroll, timeout, and cull power-ups ----------------------
            for pu in power_ups:
                pu['rect'].move_ip(0, pu['speed'])
                pu['timeout'] -= 1
            power_ups = [pu for pu in power_ups if pu['rect'].top <= WINDOWHEIGHT and pu['timeout'] > 0]

            # ---- Draw everything ------------------------------------------
            windowSurface.fill(BACKGROUNDCOLOR)

            for h in lane_hazards:   drawHazard(windowSurface, h)
            for e in road_events:    drawRoadEvent(windowSurface, e)
            for o in road_obstacles: drawObstacle(windowSurface, o)
            for pu in power_ups:     drawPowerUp(windowSurface, pu)

            # Combined score: base time + coins * 10 + distance + power-up bonus
            powerup_bonus = coin_count * 2 if active_pu else 0
            total_score   = score + coin_count * 10 + distance + powerup_bonus

            # HUD
            drawText('Score: %s'      % total_score, font, windowSurface, 128, 0)
            drawText('Top Score: %s'  % topScore,    font, windowSurface, 128, 20)
            drawText('Lives: %s'      % lives,       font, windowSurface, 128, 40)
            drawText('Coins: %s'      % coin_count,  font, windowSurface, 350, 20)
            drawText('Best Coins: %s' % most_coin,   font, windowSurface, 350, 40)
            drawText('Dist: %sm'      % distance,    font, windowSurface, 350, 60)
            drawText(settings['difficulty'], font, windowSurface, 680, 0, {
                'Easy': GREEN, 'Normal': YELLOW, 'Hard': RED
            }[settings['difficulty']])

            drawActivePowerUp(windowSurface, font, active_pu, active_pu_timer)

            # Player car with optional shield border
            windowSurface.blit(playerImage, playerRect)
            if shield_active:
                pygame.draw.rect(windowSurface, CYAN, playerRect, 3)

            for coin in coins:  windowSurface.blit(coin['surface'], coin['rect'])
            for b in baddies:   windowSurface.blit(b['surface'],    b['rect'])

            pygame.display.update()

            # ---- Collect coins --------------------------------------------
            for coin in coins[:]:
                if playerRect.colliderect(coin['rect']):
                    coin_count += coin_pool.index(coin['choice']) + 1
                    coins.remove(coin)

            # ---- Collect power-ups (only one active at a time) -----------
            for pu in power_ups[:]:
                if playerRect.colliderect(pu['rect']) and active_pu is None:
                    active_pu = pu['type']
                    if pu['type'] == PU_NITRO:
                        active_pu_timer = NITRO_DURATION
                        shield_active   = False
                    elif pu['type'] == PU_SHIELD:
                        active_pu_timer = 9999
                        shield_active   = True
                    elif pu['type'] == PU_REPAIR:
                        lives    = min(lives + 1, 5)
                        active_pu = None   # repair is instant
                        shield_active = False
                    power_ups.remove(pu)

            # ---- Enemy collision ------------------------------------------
            if playerHasHitBaddie(playerRect, baddies):
                if shield_active:
                    # Shield absorbs the hit — no life lost
                    shield_active   = False
                    active_pu       = None
                    active_pu_timer = 0
                else:
                    if coin_count > most_coin:
                        open(COINS_FILE, 'w').write(str(coin_count))
                        most_coin = coin_count
                    if total_score > topScore:
                        open(SAVE_FILE, 'w').write(str(total_score))
                        topScore = total_score
                    break   # end this life

            # ---- Static obstacle collision --------------------------------
            elif playerHitObstacle(playerRect, road_obstacles):
                if shield_active:
                    shield_active   = False
                    active_pu       = None
                    active_pu_timer = 0
                else:
                    if coin_count > most_coin:
                        open(COINS_FILE, 'w').write(str(coin_count))
                        most_coin = coin_count
                    if total_score > topScore:
                        open(SAVE_FILE, 'w').write(str(total_score))
                        topScore = total_score
                    break

            # ---- Moving barrier collision ---------------------------------
            else:
                hit_barrier = False
                for e in road_events:
                    if e['type'] == EVENT_BARRIER and playerRect.colliderect(e['rect']):
                        if shield_active:
                            shield_active   = False
                            active_pu       = None
                            active_pu_timer = 0
                        else:
                            if total_score > topScore:
                                open(SAVE_FILE, 'w').write(str(total_score))
                                topScore = total_score
                            hit_barrier = True
                        break
                if hit_barrier:
                    break

            # ---- Difficulty scaling: speed up when enough coins collected -
            N = 1
            if coin_count >= N * 6:
                N += 1
                delta = 0.1 * speed_mult
                for obj in baddies + coins + lane_hazards + road_events + road_obstacles + power_ups:
                    obj['speed'] += delta

            mainClock.tick(FPS)

        # --- End of inner game loop (player hit something) -----------------
        pygame.mixer.music.stop()
        lives -= 1

        if settings['sound']:
            gameOverSound.play()
        time.sleep(1)

        # Save round result to leaderboard
        leaderboard = addToLeaderboard(leaderboard, player_name, total_score, distance)
        saveLeaderboard(leaderboard)

        pygame.mouse.set_visible(True)

        if lives <= 0:
            # All lives spent — show game-over screen with laugh sound
            if settings['sound']:
                laugh.play()

            go_action = showGameOver(windowSurface, font, big_font, total_score, distance, coin_count, lives)

            if settings['sound']:
                gameOverSound.stop()

            if go_action == 'retry':
                lives = 3   # restart with fresh lives, skip menu
                break        # exit lives-loop to re-enter it with fresh lives
            else:
                break        # back to outer while → main menu

    # lives loop ended — continue outer while to show main menu again