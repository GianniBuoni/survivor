# pyright: reportOptionalMemberAccess= false

import pygame
from os.path import join
from pytmx.util_pygame import load_pygame

from lib.groups import AllSprites
from lib.player import Player
from lib.sprites import *
from settings import *

class Game():
    def __init__(self):
        # initialize
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Survivor")
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        # sprites
        self.map_setup()

    def map_setup(self):
        map = load_pygame(join("data", "maps", "world.tmx"))

        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprite(
                (x * TILE_SIZE , y * TILE_SIZE),
                image,
                self.all_sprites
            )

        for obj in map.get_layer_by_name("Collisions"):
            CollisionSprite(
                (obj.x, obj.y),
                pygame.Surface((obj.width, obj.height)),
                self.collision_sprites
            )

        for obj in map.get_layer_by_name("Objects"):
            CollisionSprite(
                (obj.x, obj.y),
                obj.image,
                (self.all_sprites, self.collision_sprites)
            )

        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player(
                    (obj.x, obj.y),
                    self.all_sprites,
                    self.collision_sprites
                )

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
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        pygame.quit()
