import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((1000,700))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# Load game sounds
flap_sound = pygame.mixer.Sound('audio/flap.mp3')
bg_music = pygame.mixer.Sound('audio/bg.mp3')
gameover_music = pygame.mixer.Sound('audio/gameover.mp3')

# Load game assets
sky_surface1 = pygame.image.load("assets/bg.png").convert()
sky_surface2 = pygame.image.load("assets/bg_night.png").convert()
sky_surfaces = [sky_surface1, sky_surface2]

ground_surface = pygame.image.load("assets/base.png").convert()

pipe_surface = pygame.image.load("assets/pipe.png").convert()
inverted_pipe_surface = pygame.image.load("assets/pipe-inverted.png").convert_alpha()

# Load bird assets
bird_upflap_surface = pygame.image.load("assets/bird-upflap.png").convert_alpha()
bird_midflap_surface = pygame.image.load("assets/bird-midflap.png").convert_alpha()
bird_downflap_surface = pygame.image.load("assets/bird-downflap.png").convert_alpha()
bird_frames = [bird_upflap_surface, bird_midflap_surface, bird_downflap_surface]
bird_frame_index = 0
bird_surface = bird_frames[bird_frame_index]
bird_rect = bird_surface.get_rect(center=(100, 350))
bird_y_pos = 350

# Load obstacles assets
obstacles = []

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1800)
pipe_x_pos = 1000

# Set variables
game_active = False
play_gameover_music_bool = True
start_time = 0
highscore = 0
score = 0
gravity = -15

# Create starting obstacles
obstacle_gap = 0
def create_obstacles(obstacle_gap):
    obstacle_gap +=220
    random_number = random.randint(300, 500)
    obstacles.append(pipe_surface.get_rect(topleft=(250+obstacle_gap,random_number)))
    obstacles.append(inverted_pipe_surface.get_rect(bottomleft=(250+obstacle_gap, random_number-200)))
    return obstacle_gap

obstacle_gap = create_obstacles(obstacle_gap)
obstacle_gap = create_obstacles(obstacle_gap)
obstacle_gap = create_obstacles(obstacle_gap)

# Function to display score while game is active
def display_score():
    current_time = int(pygame.time.get_ticks()/2000) - start_time + 1
    score_surface = test_font.render(f'Score : {current_time}', False, 'White')
    score_rect = score_surface.get_rect(midbottom = (500, 50))
    screen.blit(score_surface, score_rect)
    return current_time

# Play sound on gameover
def play_gameover_sound():
    gameover_music.play()

while True:
    # Events
    for event in pygame.event.get():
        # Check for quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Handle events during active gameplay
        if game_active:
            # Flap the bird on spacebar press
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and bird_rect.y>30:
                flap_sound.play()
                gravity = -15

            # Create new obstacles based on the timer
            if event.type == obstacle_timer:
                random_number = random.randint(300, 500)
                obstacles.append(pipe_surface.get_rect(topleft=(pipe_x_pos, random_number)))
                obstacles.append(inverted_pipe_surface.get_rect(bottomleft=(pipe_x_pos, random_number - 200)))
        
        # Handle events when the game is not active
        else:
            # Start the game on spacebar press
            sky_surface = random.choice(sky_surfaces)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_time = int(pygame.time.get_ticks() / 2000)  # Reset start_time
                game_active = True
                bird_rect.y = 350
                gravity = -15
                obstacles.clear()
                obstacle_gap = 0
                obstacle_gap = create_obstacles(obstacle_gap)
                obstacle_gap = create_obstacles(obstacle_gap)
                obstacle_gap = create_obstacles(obstacle_gap)
                bg_music.play(loops=-1)

    # //////////////////////////////////////////////////////////////////

    # Game Logic Section
    play_gameover_music_bool = True
    
    if game_active:
        # Render game elements during active gameplay
        screen.blit(sky_surface, (0, 0))

        # Create obstacles in runtime
        for obstacle in obstacles:
            if obstacle.y > 300:
                screen.blit(pipe_surface, obstacle)
            else:
                screen.blit(inverted_pipe_surface, obstacle)

            obstacle.x -= 2

            # Check for collision with obstacles
            if obstacle.colliderect(bird_rect):
                game_active = False
                if play_gameover_music_bool == True:
                    play_gameover_sound()
                play_gameover_music_bool = False
                obstacles.clear()
                bg_music.stop()

        screen.blit(ground_surface, (0, 600))
        bird_frame_index = (bird_frame_index + 1) % len(bird_frames)
        bird_surface = bird_frames[bird_frame_index]
        bird_rect.y += gravity
        screen.blit(bird_surface, bird_rect)

        gravity += 1

        score = display_score()

        # Check for bird touching the ground
        if bird_rect.midbottom[1] >= 600:
            game_active = False
            if play_gameover_music_bool == True:
                play_gameover_sound()
                play_gameover_music_bool = False
                bg_music.stop()
    else:
         # Render the game over screen
        gameover_bg_surface = pygame.image.load("assets/gameoverbg.png").convert()
        screen.blit(gameover_bg_surface, (0, 0))

        start_message_surface = test_font.render('Press space to start', False, 'White')
        start_message_rect = start_message_surface.get_rect(midbottom=(500, 500))
        screen.blit(start_message_surface, start_message_rect)

        if score == 0:
            # Display the game intro screen
            intro_surface = pygame.image.load("assets/intro.png").convert_alpha()
            intro_rect = intro_surface.get_rect(midtop=(500, 100))
            screen.blit(intro_surface, intro_rect)
        else:    
            # Display the game over screen with score and highscore
            gameover_image_surface = pygame.image.load("assets/gameover.png").convert_alpha()
            gameover_image_rect = gameover_image_surface.get_rect(midbottom=(500,250))
            screen.blit(gameover_image_surface, gameover_image_rect)
            high_score = score
            score_message_surface = test_font.render(f'Your score: {score}', False, 'White')
            score_message_rect = score_message_surface.get_rect(midbottom=(500, 350))

            screen.blit(score_message_surface, score_message_rect)

            if score > highscore:
                highscore = score
            highscore_message_surface = test_font.render(f'Highscore: {highscore}', False, 'White')
            highscore_message_rect = highscore_message_surface.get_rect(midbottom=(500, 400))
            screen.blit(highscore_message_surface, highscore_message_rect)

    # Update the display
    pygame.display.update()
    clock.tick(60)