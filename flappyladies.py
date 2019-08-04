# -*- coding: utf-8 -*-
import pygame
import random

# Initialize all imported pygame modules
pygame.init()

# Initialize a window for display
screen = pygame.display.set_mode([700, 497])
pygame.display.set_caption("FlapPyLadies")

# Clock object to help track time
clock = pygame.time.Clock()

# Load new image from a file
img_player = pygame.image.load('img/player.png')
img_upper_barrier = pygame.image.load('img/img_upper_barrier.png')
img_lower_barrier = pygame.image.load('img/img_lower_barrier.png')
img_game_over = pygame.image.load('img/game_over.png')
img_background = pygame.image.load('img/bg.jpg')
img_start = pygame.image.load('img/start.png')
# Create a new Sound object from a file
jump = pygame.mixer.Sound('sounds/jump.wav')
jump.set_volume(0.1)
collision = pygame.mixer.Sound('sounds/explode.wav')
collision.set_volume(0.1)

# Window status
close = False
# Player initial position
x_player = 350
y_player = 250
height_player = 0
# Barrier dimension
width_barrier = 70
height_barrier = random.randint(0, 350)
distance_barrier = 150
# Barrier position and speed
x_barrier = 700
pos_upper_barrier = 0
pos_lower_barrier = 450
speed_barrier = 4
# Score
points = 0
# Play again
game_over = False
# Background
img_size = 1320
img_initial_pos = 0


# Function to draw the player on screen
def player(player_area):
    # Draw one image onto another (source, dest)
    screen.blit(img_player, player_area)
# def player(player_area):
    # Draw a rectangle (surface, color, rect)
    # pygame.draw.rect(screen, [0, 0, 0], player_area)


# Function to draw the barriers on screen
def barriers():
    screen.blit(img_upper_barrier, [x_barrier, height_barrier - 500])
    screen.blit(img_lower_barrier, [x_barrier, height_barrier + distance_barrier])
# def barriers(upper_barrier, lower_barrier):
    # pygame.draw.rect(screen, [0, 255, 0], upper_barrier)
    # pygame.draw.rect(screen, [0, 255, 0], lower_barrier)


# Function to draw the points on screen
def score(points):
    # Create a new Font object from a file
    point_font = pygame.font.Font('fonts/geo.ttf', 55)
    # render(text, antialias (smooth edges), color)
    text = point_font.render(str(points), True, [255, 255, 255])
    # Draw text on screen
    screen.blit(text, (350, 20))


# Function to draw the intro on screen
def intro_screen():
    screen.blit(img_start, (0, 0))
    pygame.display.update()
    pygame.time.wait(2000)


# Function to draw the intro on screen
def game_over_screen():
    screen.blit(img_game_over, (0, 0))
    font = pygame.font.Font('fonts/geo.ttf', 40)
    text = font.render(str(points), True, [238, 37, 79])
    screen.blit(text, (410, 79))
    pygame.display.flip()


intro_screen()

# # # GAME LOOP # # #
while not close:

    # # # Player event recognition (keyboard) # # #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close = True
        # Hit a key (key down event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            jump.play()
            height_player = -10
        # Release a key (key up event)
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            height_player = 5

    # # # Scrolling background # # #
    # screen.fill([255, 255, 255])
    screen.blit(img_background, (img_initial_pos, 0))
    screen.blit(img_background, (img_initial_pos + img_size, 0))
    # Background speed
    img_initial_pos -= 2
    # Scrolling loop
    if img_initial_pos * -1 == img_size:
        img_initial_pos = 0

    # # # Player # # #
    # Object for storing rectangular coordinates: Rect(left, top, width, height)
    player_area = pygame.Rect(x_player, y_player, 45, 45)
    # Draw the player on screen
    player(player_area)
    # Increase +1 in y player position (player movement)
    y_player += height_player

    # # # Barriers # # #
    upper_barrier = pygame.Rect(x_barrier, 0, width_barrier, height_barrier)
    lower_barrier = pygame.Rect(x_barrier, (height_barrier + distance_barrier), width_barrier, height_barrier + 500)
    # Draw the first barriers on screen
    barriers()
    # barriers(upper_barrier, lower_barrier)
    # Decrease x barrier position (barrier movement)
    x_barrier -= speed_barrier
    # Draw the next barriers on screen
    if x_barrier < -60:
        x_barrier = 700
        height_barrier = random.randint(0, 350)

    # # # Score # # #
    # Draw the points
    score(points)
    # Points counter
    if x_player == x_barrier + width_barrier:
        points += 1

    # # # Collision # # #
    if (y_player > pos_lower_barrier or y_player < pos_upper_barrier
            or player_area.colliderect(upper_barrier) or player_area.colliderect(lower_barrier)):
        collision.play()
        height_player = 0
        speed_barrier = 0
        game_over = True

    # Update the full display Surface (background) to the screen
    pygame.display.flip()
    # Update the clock (frames per second)
    clock.tick(60)

    # # # Play again # # #
    while game_over:
        pygame.time.wait(300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
                game_over = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                x_player = 350
                y_player = 250
                height_player = 0
                x_barrier = 700
                height_barrier = random.randint(0, 350)
                speed_barrier = 4
                points = 0
                game_over = False
        game_over_screen()

pygame.quit()
