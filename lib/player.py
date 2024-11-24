# pyright: reportOptionalMemberAccess=false

import pygame
from os import walk
from os.path import join
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_group) -> None:
        super().__init__(groups)
        self.load_images()
        self.state = "down"
        self.frame_index = 0
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_group = collision_group

    def load_images(self):
        self.frames = { "left": [], "down": [], "up": [], "right": [], }
        dirparent = join("images", "player")

        for dirpath, dirnames, filenames in walk(dirparent):
            if filenames:
                state = dirpath.replace(f"{dirparent}/", "")
                for file in sorted(filenames, key = lambda x: int(x.split(".")[0])):
                    file_path = join(dirpath, file)
                    surface = pygame.image.load(file_path).convert_alpha()
                    self.frames[state].append(surface)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction: str):
        for sprite in self.collision_group:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == "horizontal":
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                if direction == "vertical":
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def update(self, dt):
        self.input()
        self.move(dt)
