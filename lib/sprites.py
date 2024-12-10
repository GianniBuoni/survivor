# pyright: reportOptionalMemberAccess = false

import pygame
from os.path import join
from math import atan2, degrees

from settings import WINDOW_WIDTH, WINDOW_HEIGHT

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups) -> None:
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups) -> None:
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups) -> None:
        # player connection
        self.player = player
        self.distance = 140
        self.player_direction = pygame.Vector2(1,0)

        # sprite setup
        super().__init__(groups)
        self.gun_surface = pygame.image.load(join("images", "gun", "gun.png")).convert_alpha()
        self.image = self.gun_surface
        self.rect = self.image.get_frect(
            center = self.player.rect.center + self.player_direction * self.distance
        )

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        playr_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 )
        self.player_direction = (mouse_pos - playr_pos).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surface, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surface, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surface, pos, direction, groups) -> None:
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center = pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000

        # movement
        self.direction = direction
        self.speed = 1200

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites) -> None:
        super().__init__(groups)
        self.player = player

        # image
        self.frames, self.frame_idx = frames, 0
        self.image = self.frames[self.frame_idx]
        self.animation_speed = 6

        # rect
        self.rect = self.image.get_frect(center = pos)
        self.hitbox = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites

        # movement
        self.direction = pygame.Vector2()
        self.speed = 350
