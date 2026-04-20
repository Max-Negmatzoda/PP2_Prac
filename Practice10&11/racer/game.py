import pygame, random, sys, os, time
from pygame.locals import *

# window settings
WINDOWWIDTH = 800
WINDOWHEIGHT = 600

# colors
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)

# fps
FPS = 40

# enemy settings
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 8
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6

# player speed
PLAYERMOVERATE = 5

# lives
count = 3

# coin settings
COINSIZE = 10
COINSPEED = 8
ADDNEWCOINS = 7
most_coin = 0  # best coins

# quit game
def terminate():
    pygame.quit()
    sys.exit()

# wait for player input
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # exit with ESC
                    terminate()
                return

# check collision with enemies
def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

# check collision with coins
def playerHasHitCoin(playerRect, coins):
    for coin in coins:
        if playerRect.colliderect(coin['rect']):
            return True
    return False

# draw text on screen
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# init pygame
pygame.init()
mainClock = pygame.time.Clock()

# create window
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('car race')
pygame.mouse.set_visible(False)

# font
font = pygame.font.Font(None, 30)

# sounds
gameOverSound = pygame.mixer.Sound('./Practice10&11/racer/music/crash.wav')
pygame.mixer.music.load('./Practice10&11/racer/music/car.wav')
laugh = pygame.mixer.Sound('./Practice10&11/racer/music/laugh.wav')

# images
playerImage = pygame.image.load('./Practice10&11/racer/image/car1.png')
car3 = pygame.image.load('./Practice10&11/racer/image/car3.png')
car4 = pygame.image.load('./Practice10&11/racer/image/car4.png')

# player rect
playerRect = playerImage.get_rect()

# enemy images
baddieImage = pygame.image.load('./Practice10&11/racer/image/car2.png')
sample = [car3, car4, baddieImage]

# walls
wallLeft = pygame.image.load('./Practice10&11/racer/image/left.png')
wallRight = pygame.image.load('./Practice10&11/racer/image/right.png')

# coin images
coinImage = pygame.image.load('./Practice10&11/racer/image/653278_coin_bitcoin_cash_currency_dollar_icon.png')
coinImage2 = pygame.image.load('./Practice10&11/racer/image/5310117_coin_dollar_money_icon.png')
coinImage3 = pygame.image.load('./Practice10&11/racer/image/3319620_coin_dollar_money_shine_icon.png')

# coin list
sample_coin_list = [coinImage, coinImage2, coinImage3]

# start screen
drawText('Press any key to start the game.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
drawText('And Enjoy', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3) + 30)
pygame.display.update()
waitForPlayerToPressKey()

zero = 0

# create coin save file if not exists
if not os.path.exists('./Practice10&11/racer/data/coins_count.dat'):
    f = open('./Practice10&11/racer/data/coins_count.dat', 'w')
    f.write((str(zero)))
    f.close()

    v = open('data/coins_count.dat')
    most_coin = int(v.readline())
    v.close()

# create score save file
if not os.path.exists("./Practice10&11/racer/data/save.dat"):
    f = open("./Practice10&11/racer/data/save.dat", 'w')
    f.write(str(zero))
    f.close()

# read top score
v = open("./Practice10&11/racer/data/save.dat", 'r')
topScore = int(v.readline())
v.close()

# main loop (lives)
while (count > 0):

    # enemy list
    baddies = []

    # coin list
    coins = []
    coinAddCounter = 0
    coin_count = 0

    # score
    score = 0

    # player start position
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)

    # movement flags
    moveLeft = moveRight = moveUp = moveDown = False

    # cheat flags
    reverseCheat = slowCheat = False

    # spawn counter
    baddieAddCounter = 0

    pygame.mixer.music.play(-1, 0.0)

    # game loop
    while True:
        score += 1  # increase score

        # events
        for event in pygame.event.get():

            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True

                # movement keys
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                # stop movement
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

        # spawn enemies and coins
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
            coinAddCounter += 1

        # add coin
        if coinAddCounter == ADDNEWCOINS + 10:
            coinAddCounter = 0
            coinSize = 10
            choice = random.choice(sample_coin_list)
            newCoin = {
                'rect': pygame.Rect(random.randint(140, 485), 0 - coinSize, 30, 30),
                'speed': COINSPEED,
                'surface': pygame.transform.scale(choice, (30, 30)),
                'choice': choice
            }
            coins.append(newCoin)

        # add enemy + walls
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = 30
            newBaddie = {
                'rect': pygame.Rect(random.randint(140, 485), 0 - baddieSize, 23, 47),
                'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                'surface': pygame.transform.scale(random.choice(sample), (23, 47)),
            }
            baddies.append(newBaddie)

            # side walls
            sideLeft = {
                'rect': pygame.Rect(0, 0, 126, 600),
                'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                'surface': pygame.transform.scale(wallLeft, (126, 599)),
            }
            baddies.append(sideLeft)

            sideRight = {
                'rect': pygame.Rect(497, 0, 303, 600),
                'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                'surface': pygame.transform.scale(wallRight, (303, 599)),
            }
            baddies.append(sideRight)

        # move player
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # move coins
        for coin in coins:
            if not reverseCheat and not slowCheat:
                coin['rect'].move_ip(0, coin['speed'])
            elif reverseCheat:
                coin['rect'].move_ip(0, -5)
            elif slowCheat:
                coin['rect'].move_ip(0, 1)

        # remove coins outside screen
        for coin in coins[:]:
            if coin['rect'].top > WINDOWHEIGHT:
                coins.remove(coin)

        # move enemies
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # remove enemies outside screen
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # draw background
        windowSurface.fill(BACKGROUNDCOLOR)

        # draw UI
        drawText('Score: %s' % (score), font, windowSurface, 128, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 128, 20)
        drawText('Rest Life: %s' % (count), font, windowSurface, 128, 40)

        drawText('Coins: %s' %(coin_count), font, windowSurface, 350, 20)
        drawText('Most Coins %s' % (most_coin), font, windowSurface, 350, 40)

        # draw player
        windowSurface.blit(playerImage, playerRect)

        # draw coins
        for coin in coins:
            windowSurface.blit(coin['surface'], coin['rect'])

        # draw enemies
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # collect coins
        if playerHasHitCoin(playerRect, coins):
            for coin in coins:
                if playerRect.colliderect(coin['rect']):
                    coin_count += sample_coin_list.index(coin['choice']) + 1
                    coins.remove(coin)

        # collision with enemy
        if playerHasHitBaddie(playerRect, baddies):

            # update coin record
            if coin_count > most_coin:
                fi = open('./Practice10&11/racer/data/coins_count.dat', 'w')
                fi.write(str(coin_count))
                fi.close()
                most_coin = coin_count

            # update score record
            if score > topScore:
                g = open("data/save.dat", 'w')
                g.write(str(score))
                g.close()
                topScore = score
            break

        # difficulty scaling
        N = 1
        if coin_count >= N * 6:
            N += 1
            for coin in coins:
                coin['speed'] += 0.1
            for b in baddies:
                b['speed'] += 0.1

        mainClock.tick(FPS)

    # game over logic
    pygame.mixer.music.stop()
    count = count - 1
    gameOverSound.play()
    time.sleep(1)

    if (count == 0):
        laugh.play()
        drawText('Game over', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
        pygame.display.update()
        time.sleep(2)
        waitForPlayerToPressKey()
        count = 3
        gameOverSound.stop()