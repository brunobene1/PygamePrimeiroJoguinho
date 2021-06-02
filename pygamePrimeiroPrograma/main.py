

import pygame
import random
import math
from pygame import mixer



# cntrl + alt + L ----> identação automática!
mainClock = pygame.time.Clock()

# inicializando
pygame.init()

# criando a tela
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("Background.png")
mixer.music.load("MusElevador.wav")
mixer.music.play(-1)

# titulo e icone
pygame.display.set_caption("Ovni2d2")
icon = pygame.image.load("Player.png")
pygame.display.set_icon(icon)

# Player
playerIMG = pygame.image.load("Player.png")
playerX = 400
playerY = 480
playerX_change = 0

# Inimigo
inimigoIMG = []
inimigoX = []
inimigoY = []
inimigoX_change = []
inimigoY_change = []
num_of_enemies = 20
velInimigo = 6

for i in range(num_of_enemies):
    inimigoIMG.append(pygame.image.load("Inimigo.png"))
    inimigoX.append(random.randint(0, 769))
    inimigoY.append(random.randint(50, 150))
    inimigoX_change.append(velInimigo)
    inimigoY_change.append(20)

# Bala
# ready - pode atirar
# fire - esta no cenario
balaIMG = pygame.image.load("Bala.png")
balaX = 0
balaY = 480
balaY_change = 4
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

#Game over
over_font = pygame.font.Font("freesansbold.ttf", 32)

def game_over_text():
    over_text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def showScore(x, y):
    score = over_font.render(str(score_value) + " / 100", True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    # Blit - desenhar na tela
    screen.blit(playerIMG, (x, y))


def inimigo(x, y, i):
    screen.blit(inimigoIMG[i], (x, y))


def fireBullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(balaIMG, (x + 16, y + 10))


def isColission(inimigoX, inimigoY, balaX, balaY):
    dist = math.sqrt((math.pow(inimigoX - balaX, 2)) + (math.pow(inimigoY - balaY, 2)))
    if dist < 27:
        return True
    else:
        return False


#MENU ----------------------------



# Game Loop
running = True
while running:
    # (R, G, B) - 0 até 255
    screen.fill((0, 0, 0))

    # background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Manager de Input do teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_sound = mixer.Sound("Bruh.wav")
                bullet_sound.play()
                balaX = playerX
                fireBullet(balaX, balaY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX < 0:
        playerX = 800
    if playerX > 800:
        playerX = 0

    # inimigos
    for i in range(num_of_enemies):
        #GameOver
        if inimigoY[i] > 440 or score_value >= 100:
            for j in range (num_of_enemies):
                inimigoY[j] = 2000
            game_over_text()
            break

        inimigoX[i] += inimigoX_change[i]
        if inimigoX[i] < 0:
            inimigoX_change[i] = velInimigo
            inimigoY[i] += inimigoY_change[i]
        if inimigoX[i] > 770:
            inimigoX_change[i] = -velInimigo
            inimigoY[i] += inimigoY_change[i]

        # colisao
        collision = isColission(inimigoX[i], inimigoY[i], balaX, balaY)
        if collision:
            collision_sound = mixer.Sound("peido.wav")
            collision_sound.play()
            balaY = 480
            bullet_state = "ready"
            score_value += 1
            inimigoX[i] = random.randint(0, 769)
            inimigoY[i] = random.randint(50, 150)

        inimigo(inimigoX[i], inimigoY[i], i)

    # movimento da bala

    if balaY < 0:
        balaY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fireBullet(balaX, balaY)
        balaY -= balaY_change

    # Desenhar o player depois do screen.fill
    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
    mainClock.tick(60)