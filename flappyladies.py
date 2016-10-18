#!/usr/bin/env python
import pygame
import random

pygame.init()  # Initialize the pygame module

img_wallup = pygame.image.load('FlapPyLadies/img/img_wallup.png')
img_walldown = pygame.image.load('FlapPyLadies/img/img_walldown.png')
img_gameover = pygame.image.load('FlapPyLadies/img/gameover.png')
img_bg1 = pygame.image.load('FlapPyLadies/img/bg.jpg')
img_bg2 = pygame.image.load('FlapPyLadies/img/bg.jpg')
img_start = pygame.image.load('FlapPyLadies/img/start.png')
img_logo = pygame.image.load('FlapPyLadies/img/logoPython.png')
jump = pygame.mixer.Sound('FlapPyLadies/sounds/jump.wav')
hit = pygame.mixer.Sound('FlapPyLadies/sounds/explode.wav')
jump.set_volume(0.1)
hit.set_volume(0.1)

screen = pygame.display.set_mode([700, 497])  # Creates a screen
pygame.display.set_caption('FlapPy')  # Sets the screen caption

clock = pygame.time.Clock()


class Player:
    def __init__(self, screen):
        self.x = 350
        self.y = 250
        self.screen = screen
        self.area = pygame.Rect(self.x, self.y, 45, 45)
        self.points = 0

    def Area(self):
        return pygame.Rect(self.x, self.y, 45, 45)

    def draw(self):
        self.screen.blit(pygame.image.load('FlapPyLadies/img/player.png'),
                         pygame.Rect(self.x, self.y, 45, 45))


class Obstacle:
    def __init__(self, screen):
        self. x = 700
        self.width = 70
        self.heigth = random.randint(0, 350)
        self.gap = 150
        self.speed = 4
        self.screen = screen
        self.color = [0, 255, 0]

    def draw(self):
        upper_obst = screen.blit(img_wallup, [self.x, self.heigth - 500])
        lower_obst = screen.blit(img_walldown,
                                 [self.x, self.heigth + self.gap])
        return upper_obst, lower_obst


def intro():
    screen.fill([255, 255, 255])
    screen.blit(img_logo, [40, 300])
    screen.blit(img_start, [170, 50])
    pygame.display.update()
    pygame.time.wait(2000)


def score(points):
    font = pygame.font.Font("FlapPyLadies/fonts/geo.ttf", 55)
    text = font.render(str(points), True, [0, 0, 0])
    screen.blit(text, [350, 20])

player = Player(screen)
obstacle = Obstacle(screen)
close = False
speed = 5
game_over = False
posImg = 0
Img = 1320

intro()
while not close:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                speed -= 10
                jump.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                speed = 5

    #  screen.fill([255, 255, 255])
    screen.blit(img_bg1, (posImg, 0))
    screen.blit(img_bg2, (posImg + Img, 0))
    posImg -= 2
    if posImg * -1 == Img:
        posImg = 0
    player_area = pygame.Rect(player.x, player.y, 45, 45)
    player.draw()
    player.y += speed

    upper_obst, lower_obst = obstacle.draw()
    obstacle.x -= obstacle.speed

    if obstacle.x < -60:
        obstacle = Obstacle(screen)
        obstacle.heigth = random.randint(0, 350)

    score(player.points)

    if player.x == obstacle.x + obstacle.width:
        player.points += 1

    if player.y > 450 or player.y < 0:
        speed = 0
        obstacle.speed = 0
        hit.play()
        game_over = True

    if player.Area().colliderect(
            upper_obst) or player.Area().colliderect(lower_obst):
        speed = 0
        obstacle.speed = 0
        hit.play()
        game_over = True

    pygame.display.flip()
    clock.tick(60)
    while game_over:
        pygame.time.wait(300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.x = 350
                    player.y = 250
                    speed = 0
                    obstacle = Obstacle(screen)
                    obstacle.heigth = random.randint(0, 350)
                    player.points = 0
                    game_over = False
        screen.fill([255, 255, 255])
        screen.blit(img_gameover, (175, 20))
        font = pygame.font.Font('FlapPyLadies/fonts/geo.ttf', 40)
        text = font.render(str(player.points), True, [238, 37, 79])
        screen.blit(text, [410, 43])
        pygame.display.flip()


pygame.quit()
