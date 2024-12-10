# pyright: reportOptionalMemberAccess = false

import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups, collision_group) -> None:
        super().__init__(groups)

        # image
        self.frames, self.frames_idx = frames, 0
        self.image = self.frames[self.frames_idx]
        self.animation_speed = 5

        # rect
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_group = collision_group

    # move
    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")
        self.rect.center = self.hitbox_rect.center

    # collision
    def collision(self, direction: str):
        for sprite in self.collision_group:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == "horizontal":
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                if direction == "vertical":
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    # animation
    def animate(self, dt):
        self.frames_idx += self.animation_speed * dt if self.direction else 0
        self.image = self.frames[int(self.frames_idx) % len(self.frames)]

    def update(self, dt) -> None:
        raise NotImplemented(f"Child update method not defined. Delta: {dt}")
