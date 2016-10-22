# -*- coding: utf-8 -*-

import pygame
import random

# Inicialização do pygame
pygame.init()

# Tamanho e nome da janela
screen = pygame.display.set_mode([700,497])
pygame.display.set_caption("FlapPyLadies")

# Frame por segundo
clock = pygame.time.Clock()

# Carrega imagens e efeitos sonoros
img_player = pygame.image.load('img/player.png')
img_wallup = pygame.image.load('img/img_wallup.png')
img_walldown = pygame.image.load('img/img_walldown.png')
img_gameover = pygame.image.load('img/gameover.png')
img_bg1 = pygame.image.load('img/bg.jpg')
img_bg2 = pygame.image.load('img/bg.jpg')
img_start = pygame.image.load('img/start.png')
img_logo = pygame.image.load('img/logoPython.png')
jump = pygame.mixer.Sound('sounds/jump.wav')
hit = pygame.mixer.Sound('sounds/explode.wav')
jump.set_volume(0.1)
hit.set_volume(0.1)

# Funçoes para desenhar objetos na tela
def player(player_area):
    #pygame.draw.rect(screen, [0,0,0], player_area)
    screen.blit(img_player, player_area)

#def wall(wallup, walldown):
def wall():
    #pygame.draw.rect(screen, [0,255,0], wallup)
    #pygame.draw.rect(screen, [0,255,0], walldown)
    screen.blit(img_wallup, [wall_locx, wall_alt - 500])
    screen.blit(img_walldown, [wall_locx, wall_alt + dist])

def score(points):
    font = pygame.font.Font('fonts/geo.ttf', 55)
    text = font.render(str(points), True, [255,255,255])
    screen.blit(text, [350,20])

# Funçao para exibir a introduçao
def intro():
    screen.fill([255, 255, 255])
    screen.blit(img_logo, [40, 300])
    screen.blit(img_start, [170, 50])
    pygame.display.update()
    pygame.time.wait(2000)

# # # VARIAVEIS # # #
# Janela esta aberta ou fechada
close = False
# Jogador
playerx = 350 # Posiçao inicial
playery = 250
# Velocidade inicial do jogador
speed = 5
# Obstaculo
wall_locx = 700 #localizaçao
wall_larg = 70 # tamanho
wall_alt = random.randint(0, 350)
dist = 150
speedwall = 4
up = 0
down = 450
# Pontuaçao
points = 0
# Jogar novamente
gameover = False
# Imagem de fundo
Img = 1320
posImg = 0

intro()

# # # Loop do jogo # # #
while not close:

    #Inicio FOR
    # Reconhece eventos do jogador (mouse e teclado)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close = True
            # Apertar uma tecla
        if event.type == pygame.KEYDOWN:
            # Aperta Tecla "espaço"
            if event.key == pygame.K_SPACE:
                jump.play()
                speed = -10
            # Solta Tecla "espaço"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                speed = 5

    # # # BACKGROUND # # #
    #screen.fill([255,255,255])
    screen.blit(img_bg1, (posImg, 0))
    screen.blit(img_bg2, (posImg + Img, 0))
    posImg -= 2 # Velocidade
    if posImg * -1 == Img: #Recomeçar
        posImg = 0

    # # # JOGADOR # # #
    # Cria jogador (retangulo para colisao)
    player_area = pygame.Rect(playerx, playery, 45, 45)
    # Desenha jogador
    player(player_area)
    # Incrementa a posiçao y do jogador
    playery += speed

    # # # OBSTACULO # # #
    # Cria obstaculo
    wallup = pygame.Rect(wall_locx, 0, wall_larg, wall_alt)
    walldown = pygame.Rect(wall_locx, (wall_alt + dist), wall_larg, wall_alt + 500)
    # Desenha obstaculo
    #wall(wallup, walldown)
    wall()
    # Decrementa a posição x do obstaculo
    wall_locx -= speedwall
        # Cria mais obstaculos
    if wall_locx < -60:
        wall_locx = 700
        wall_alt = random.randint(0, 350)

    # # # PONTUAÇÃO # # #
    # Desenha pontos
    score(points)
    # Conta pontos
    if playerx == wall_locx + wall_larg:
        points += 1

    # # # COLISAO # # #
    if (playery > down or playery < up):
        hit.play()
        speed = 0
        speedwall = 0
        gameover = True

    if player_area.colliderect(wallup) or player_area.colliderect(walldown):
        hit.play()
        speed = 0
        speedwall = 0
        gameover = True

    # Atualiza o fundo
    pygame.display.flip()
    clock.tick(60)

    # # # JOGAR NOVAMENTE # # #
    while gameover:
        pygame.time.wait(300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
                gameover = False
            # Apertar uma tecla
            if event.type == pygame.KEYDOWN:
                # Aperta Tecla "espaço"
                if event.key == pygame.K_SPACE:
                    # Jogador
                    playerx = 350 # Posiçao inicial
                    playery = 250
                    # Velocidade inicial do jogador
                    speed = 0
                    # Obstaculo
                    wall_locx = 700 #localizaçao
                    wall_alt = random.randint(0, 350)
                    speedwall = 4
                    # Pontuaçao
                    points = 0
                    # Jogar novamente
                    gameover = False

        # Imagem game over
        screen.fill([255,255,255])
        screen.blit(img_gameover, (175,20))
        font = pygame.font.Font('fonts/geo.ttf', 40)
        text = font.render(str(points), True, [238,37,79])
        screen.blit(text, [410,43])
        pygame.display.flip()

pygame.quit()
