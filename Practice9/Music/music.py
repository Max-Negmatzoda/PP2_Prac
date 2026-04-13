import pygame

pygame.init()
pygame.display.set_caption('Music Player')

# Screen setup
screen_size = screen_width, screen_height = 600, 150
screen = pygame.display.set_mode(screen_size)

# Initialize mixer (audio system)
pygame.mixer.init()

# Path to audio files
path = './music/'

# Playlist
songList = [
    'light-rain.mp3',
    'LIONEL_RICHIE_HELLO!.mp3',
    'Lonely_But_Not_Alone.mp3',
    'One_Day_Imagine_Dragons.mp3'
]

# Current song index and name
crrnt_song_index = 0
crrnt_song = songList[crrnt_song_index]

# Load and play first song
pygame.mixer.music.load(path + crrnt_song)
pygame.mixer.music.play()

# Button text (controls)
btn_font = pygame.font.Font(None, 32)
btn = btn_font.render('C(Pause)    V(Unpause)    B(Prev)    N(Next)', True, 'royalblue')

# Song name display
song_name_font = pygame.font.Font(None, 32)
song_name = song_name_font.render(crrnt_song.split('.')[0], True, 'black')


def next_song():
    """Switch to next song in playlist (loop if end reached)"""
    global crrnt_song, crrnt_song_index, song_name

    crrnt_song_index += 1
    if crrnt_song_index >= len(songList):
        crrnt_song_index = 0  # loop back to first song

    crrnt_song = songList[crrnt_song_index]

    # Update displayed song name
    song_name = song_name_font.render(crrnt_song.split('.')[0], True, 'black')

    # Load and play new song
    pygame.mixer.music.load(path + crrnt_song)
    pygame.mixer.music.play()


def prev_song():
    """Switch to previous song in playlist (loop if beginning reached)"""
    global crrnt_song, crrnt_song_index, song_name

    crrnt_song_index -= 1
    if crrnt_song_index < 0:
        crrnt_song_index = len(songList) - 1  # go to last song

    crrnt_song = songList[crrnt_song_index]

    # Update displayed song name
    song_name = song_name_font.render(crrnt_song.split('.')[0], True, 'black')

    # Load and play new song
    pygame.mixer.music.load(path + crrnt_song)
    pygame.mixer.music.play()


run = True
while run:
    # Clear screen
    screen.fill('white')

    # Draw UI text
    screen.blit(btn, (75, screen_height - 40))
    screen.blit(song_name, (15, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Keyboard controls
        if event.type == pygame.KEYDOWN:

            # Pause music
            if event.key == pygame.K_c:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()

            # Unpause music
            if event.key == pygame.K_v:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.unpause()

            # Next track
            if event.key == pygame.K_n:
                next_song()

            # Previous track
            if event.key == pygame.K_b:
                prev_song()

    # Update display
    pygame.display.flip()

pygame.quit()