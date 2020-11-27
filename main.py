import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()
pygame.mixer.init()

# creating a screen
screen = pygame.display.set_mode((800, 600))  # width , height or x , y axis

# background
background = pygame.image.load("background.png")

# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# caption and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('space-invaders (1).png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("ufo.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 4
bulletY_change = 30
bullet_state = "ready"  # ready ----> cant see the bullet on screen

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# life
life_left = 3
font1 = pygame.font.Font('freesansbold.ttf', 32)

text1X = 30
text1Y = 45

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_life(x, y):
    life = font1.render("life :" + str(life_left), True, (255, 255, 255))
    screen.blit(life, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):  # blit means drawing
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):  # blit means drawing
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


def is_collision_player(enemy_x, enemy_y, player_x, player_y):
    distance = math.sqrt((math.pow(enemy_x - player_x + 2, 2)) + (math.pow(enemy_y - player_y + 2, 2)))
    if distance < 25:
        return True
    else:
        return False


running = True
while running:
    # Rgb values background of the window
    screen.fill((255, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke is pressed check weather its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_DOWN:
                playerY_change = 5
            if event.key == pygame.K_UP:
                playerY_change = -5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX  # get the current x coordinate of the spaceship
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # checking for boundaries of spaceship
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 538:
        playerY = 538

    #  enemy spaceship movement
    for i in range(num_of_enemies):

        # game over
        if life_left == 0:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            playerX = 2000

            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # collision bullet to enemy
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
        # collision enemy to player
        collision_player = is_collision_player(enemyX[i], enemyY[i], playerX, playerY)
        if collision_player:
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            life_left -= 1
            playerX = 370
            playerY = 480

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    show_life(text1X, text1Y)
    pygame.display.update()
