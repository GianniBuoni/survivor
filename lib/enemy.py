# pyright: reportOptionalMemberAccess = false

import pygame
from lib.entity import Entity

class Enemy(Entity):
    def __init__(self, frames, pos, groups, player, collision_group) -> None:
        super().__init__(frames, pos, groups, collision_group)
        self.player = player

    def follow_player(self):
        # change direction
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        new_vector = (player_pos - enemy_pos)
        if new_vector == pygame.Vector2(0,0):
            self.direction = pygame.Vector2()
        else:
            self.direction = new_vector.normalize()

    def update(self, dt):
        self.follow_player()
        self.move(dt)
        self.animate(dt)
