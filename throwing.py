from pygame import *
import math
from pygame import event

#           R    G    B
WHITE = (255, 255, 255)
GREEN = (78, 255, 87)
YELLOW = (241, 255, 0)
BLUE = (80, 255, 239)
PURPLE = (203, 0, 255)
RED = (237, 28, 36)
Xaxis = 800
Yaxis = 600
mildirect = 0
SCREEN = display.set_mode((Xaxis, Yaxis))
FONT = "fonts/space_invaders.ttf"
IMG_NAMES = ["ship", "mystery",
             "enemy1_1", "enemy1_2",
             "enemy2_1", "enemy2_2",
             "enemy3_1", "enemy3_2",
             "explosionblue", "explosiongreen", "explosionpurple",
             "laser", "enemylaser"]
IMAGES = {name: image.load("images/{}.png".format(name)).convert_alpha()
          for name in IMG_NAMES}

import random


class Coin(sprite.Sprite):
    gravity = 9.81

    def __init__(self, xpos, ypos, speed=55):
        sprite.Sprite.__init__(self)
        self.images = []
        self.row = 0
        self.load_images()
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = xpos - 15
        self.rect.y = ypos - 15

        self.move_timer = time.get_ticks()
        self.rot_timer = time.get_ticks()

        self.moveTime = 10
        self.rotationTime = 100
        newXaxis = Xaxis / Xaxis

        place = xpos / newXaxis
        if place == 1:
            mildirect = 120
        elif place == 0:
            mildirect = 90
        elif place == -1:
            mildirect = 45
        self.angle = mildirect
        self.speed = speed
        self.vx = self.speed * math.cos(math.radians(self.angle))
        self.vy = self.speed * math.sin(math.radians(self.angle))

        self.spawn_time = time.get_ticks()
        self.lifetime = 10000

    def update(self, keys, currentTime):

        if currentTime - self.move_timer > self.moveTime:
            dt = self.moveTime / 100.0

            self.rect.x += self.vx * dt

            self.vy -= self.gravity * dt
            self.rect.y -= self.vy * dt

            self.move_timer += self.moveTime

        if currentTime - self.rot_timer > self.rotationTime:
            # rotate through images
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            self.rot_timer += self.rotationTime

        game.screen.blit(self.image, self.rect)

        if currentTime - self.spawn_time > self.lifetime:
            self.kill()

    def load_images(self):
        self.images = [transform.scale(
            image.load("images/coin-{}.png".format(idx)),
            (30, 30))
            for idx in range(6)]


class Text(object):
    def __init__(self, textFont, size, message, color, xpos, ypos):
        self.font = font.Font(textFont, size)
        self.surface = self.font.render(message, True, color)
        self.rect = self.surface.get_rect(topleft=(xpos, ypos))

    def draw(self, surface):
        surface.blit(self.surface, self.rect)


class Throw(object):
    def __init__(self):
        mixer.pre_init(44100, -16, 1, 512)
        init()
        self.screen = SCREEN
        self.background = image.load('images/background.jpg').convert()
        self.screen.blit(self.background, (0, 0))
        self.startGame = True

        self.clock = time.Clock()
        self.timer = time.get_ticks()

        self.coins = sprite.Group()
        self.coins.add(Coin(400, 300))

        self.allSprites = sprite.Group(self.coins)

        self.keys = key.get_pressed()

    def check_input(self, ev):

        # proceed events
        for event in ev:

            # handle MOUSEBUTTONUP
            if event.type == MOUSEBUTTONUP:
                pos = mouse.get_pos()
                self.coins.add(Coin(*pos))
                self.allSprites.add(self.coins)

    def main(self):
        while True:
            currentTime = time.get_ticks()
            ev = event.get()
            self.check_input(ev)
            self.screen.blit(self.background, (0, 0))
            self.allSprites.update(self.keys, currentTime)

            info = Text(FONT, 20, str(currentTime), GREEN, 85, 5)
            info.draw(self.screen)

            display.update()
            self.clock.tick(100)


if __name__ == '__main__':
    game = Throw()
    score = game.main()
    print(score)
