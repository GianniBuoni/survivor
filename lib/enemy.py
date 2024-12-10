# pyright: reportOptionalMemberAccess = false

import pygame
from lib.entity import Entity

class Enemy(Entity):
    def __init__(self, frames, pos, groups, player, collision_group) -> None:
        super().__init__(frames, pos, groups, collision_group)
        self.player = player
        self.death_time = 0
        self.death_duration = 400

        # TO DO: override speed based on a difficulty setting
        self.speed = 100

    def follow_player(self):
        # change direction
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        new_vector = (player_pos - enemy_pos)
        if new_vector == pygame.Vector2(0,0):
            self.direction = pygame.Vector2()
        else:
            self.direction = new_vector.normalize()

    def destroy(self):
        # start death timer
        self.death_time = pygame.time.get_ticks()

        # change surface
        surface = pygame.mask.from_surface(self.frames[0]).to_surface()
        surface.set_colorkey("black")
        self.image = surface

    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()

    def update(self, dt):
        if self.death_time == 0:
            self.follow_player()
            self.move(dt)
            self.animate(dt)
        else:
            self.death_timer()
