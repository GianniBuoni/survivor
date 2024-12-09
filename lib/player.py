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
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")
        self.rect.center = self.hitbox_rect.center

    def animate(self, dt):
        # get state
        if self.direction.x != 0:
            self.state = "right" if self.direction.x > 0 else "left"
        if self.direction.y != 0:
            self.state = "down" if self.direction.y > 0 else "up"

        # change frames
        self.frame_index = self.frame_index + (5 * dt) if self.direction else 0
        state_frames = self.frames[self.state]
        self.image = state_frames[int(self.frame_index % len(state_frames))]


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
        self.animate(dt)
        self.move(dt)
