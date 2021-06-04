import pygame
import random
# can be used define local constants for keystrokes, mouse movents and display attributes
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# set up screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# define a player object by extending pygame.sprite.Sprite


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        # keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # spawn enemy off the screen
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        # spawn enemies with random speeds
        self.speed = random.randint(5, 20)
    # enemy moves automatically towards the left side of the screen

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# cloud object


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# setup for sounds
pygame.mixer.init()
# initialise game
pygame.init()

# create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# create a custom event for adding a new enemy
# events are defined as integers by pygame, so we need to give a unique identifier for our custom event
# the last event pygame reserves is called USEREVENT
ADDENEMY = pygame.USEREVENT + 1
# ADDENEMY event is fired every 250ms
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# instantiate player
player = Player()

# create groups to hold enemy sprites and all sprites
# enemies group is used for collision detection and position updates
# clouds is used for position updates
# all_sprites group is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# load and play background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("Electric.mp3")
pygame.mixer.music.play(loops=-1)

move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")
# setup clock for a decent framerate
clock = pygame.time.Clock()
# set up game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # escape loop
            if event.key == K_ESCAPE:
                running = False
        # escape loop
        elif event.type == QUIT:
            running = False
        # add a new enemy
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        # add a new cloud
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # get set of kets pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # update player sprite based on user keypresses
    player.update(pressed_keys)
    # update enemy position
    enemies.update()
    clouds.update()

    screen.fill((135, 206, 250))

    # draw all sprites
    # blit stands for Block Transfer
    # blit() takes 2 args: the surface to draw, the location
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.mixer.music.stop()
pygame.mixer.quit()
