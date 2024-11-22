import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups) -> None:
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups) -> None:
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)
