# -*- coding: utf-8 -*-
import pygame
import random

# Inicialização do pygame
pygame.init()

# Tamanho e nome da janela
tela = pygame.display.set_mode([700,497])
pygame.display.set_caption("FlapPyLadies")

# Frame por segundo
clock = pygame.time.Clock()

# Carrega imagens e efeitos sonoros
img_jogador = pygame.image.load('img/player.png')
img_obstaculo1 = pygame.image.load('img/img_obstaculo1.png')
img_obstaculo2 = pygame.image.load('img/img_obstaculo2.png')
img_fimDoJogo = pygame.image.load('img/gameover.png')
img_fundo1 = pygame.image.load('img/bg.jpg')
img_fundo2 = pygame.image.load('img/bg.jpg')
img_inicio = pygame.image.load('img/start.png')
img_logo = pygame.image.load('img/logoPython.png')
pulo = pygame.mixer.Sound('sounds/jump.wav')
colisao = pygame.mixer.Sound('sounds/explode.wav')
pulo.set_volume(0.1)
colisao.set_volume(0.1)

# Funçoes para desenhar objetos na tela
def jogador(area_jogador):
    #pygame.draw.rect(tela, [0,0,0], area_jogador)
    tela.blit(img_jogador, area_jogador)

#def obstaculos(obstaculo1, obstaculo2):
def obstaculos():
    #pygame.draw.rect(tela, [0,255,0], obstaculo1)
    #pygame.draw.rect(tela, [0,255,0], obstaculo2)
    tela.blit(img_obstaculo1, [x_obstaculo, altura_obstaculo - 500])
    tela.blit(img_obstaculo2, [x_obstaculo, altura_obstaculo + espaco])

def pontuacao(pontos):
    font = pygame.font.Font('fonts/geo.ttf', 55)
    text = font.render(str(pontos), True, [255,255,255])
    tela.blit(text, [350,20])

# Funçao para exibir a introduçao
def intro():
    tela.fill([255, 255, 255])
    tela.blit(img_logo, [40, 300])
    tela.blit(img_inicio, [170, 50])
    pygame.display.update()
    pygame.time.wait(2000)

# # # VARIAVEIS # # #
# Janela esta aberta ou fechada
fechada = False
# Jogador
x_jogador = 350 # Posiçao inicial
y_jogador = 250
# Velocidade inicial do jogador
velocidade_jogador = 0
# Obstaculo
x_obstaculo = 700 #localizaçao
largura_obstaculo = 70
altura_obstaculo = random.randint(0, 350)
espaco = 150
velocidade_obstaculo = 4
cima_obstaculo = 0
baixo_obstaculo = 450
# Pontuaçao
pontos = 0
# Jogar novamente
gameover = False
# Imagem de fundo
Img = 1320
posImg = 0

intro()

# # # Loop do jogo # # #
while not fechada:
    
    #Inicio FOR
    # Reconhece eventos do jogador (mouse e teclado)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fechada = True
            # Apertar uma tecla
        if event.type == pygame.KEYDOWN:
            # Aperta Tecla "espaço"
            if event.key == pygame.K_SPACE:
                pulo.play()
                velocidade_jogador = -10
            # Solta Tecla "espaço"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                velocidade_jogador = 5

    # # # BACKGROUND # # #
    #tela.fill([255,255,255])
    tela.blit(img_fundo1, (posImg, 0))
    tela.blit(img_fundo2, (posImg + Img, 0))
    posImg -= 2 # Velocidade
    if posImg * -1 == Img: #Recomeçar
        posImg = 0

    # # # JOGADOR # # #
    # Cria jogador (retangulo para colisao)
    area_jogador = pygame.Rect(x_jogador, y_jogador, 45, 45)
    # Desenha jogador
    jogador(area_jogador)
    # Aumenta +1 a posiçao y do jogador
    y_jogador += velocidade_jogador

    # # # OBSTACULO # # #
    # Cria obstaculo
    obstaculo1 = pygame.Rect(x_obstaculo, 0, largura_obstaculo, altura_obstaculo)
    obstaculo2 = pygame.Rect(x_obstaculo, (altura_obstaculo + espaco), largura_obstaculo, altura_obstaculo + 500)
    # Desenha obstaculo
    #obstaculos(obstaculo1, obstaculo2)
    obstaculos()
    # Decrementa a posição x do obstaculo 
    x_obstaculo -= velocidade_obstaculo
    # Cria mais obstaculos
    if x_obstaculo < -60:
        x_obstaculo = 700
        altura_obstaculo = random.randint(0, 350)

    # # # PONTUAÇÃO # # #
    # Desenha pontos
    pontuacao(pontos)
    # Conta pontos
    if x_jogador == x_obstaculo + largura_obstaculo:
        pontos += 1

    # # # COLISAO # # #
    if (y_jogador > baixo_obstaculo or y_jogador < cima_obstaculo):
        colisao.play()
        velocidade_jogador = 0
        velocidade_obstaculo = 0
        gameover = True

    if area_jogador.colliderect(obstaculo1) or area_jogador.colliderect(obstaculo2):
        colisao.play()
        velocidade_jogador = 0
        velocidade_obstaculo = 0
        gameover = True

    # Atualiza o fundo
    pygame.display.flip()
    clock.tick(60)

    # # # JOGAR NOVAMENTE # # #
    while gameover:
        pygame.time.wait(300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fechada = True
                gameover = False
            # Apertar uma tecla
            if event.type == pygame.KEYDOWN:
                # Aperta Tecla "espaço"
                if event.key == pygame.K_SPACE:
                    # Jogador
                    x_jogador = 350 # Posiçao inicial
                    y_jogador = 250
                    # Velocidade inicial do jogador
                    velocidade_jogador = 0
                    # Obstaculo
                    x_obstaculo = 700 #localizaçao
                    altura_obstaculo = random.randint(0, 350)
                    velocidade_obstaculo = 4
                    # Pontuaçao
                    pontos = 0
                    # Jogar novamente
                    gameover = False

        # Imagem game over
        tela.fill([255,255,255])
        tela.blit(img_fimDoJogo, (175,20))
        font = pygame.font.Font('fonts/geo.ttf', 40)
        text = font.render(str(pontos), True, [238,37,79])
        tela.blit(text, [410,43])
        pygame.display.flip()

pygame.quit()
