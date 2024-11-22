import pygame
from random import randint

from lib.player import Player
from lib.sprites import *
from settings import *

class Game():
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Survivor")
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # sprites
        self.player = Player((WINDOW_WIDTH / 2 , WINDOW_HEIGHT / 2), self.all_sprites, self.collision_sprites)

        for i in range(6):
            x, y = randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
            w, h = randint(50, 100), randint(60, 100)
            CollissionSprite((x, y), (w, h), (self.all_sprites, self.collision_sprites))

    def run(self):
        while self.running:

            # dt in ms
            dt = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill("black")
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
        pygame.quit()
