import pygame

class CollissionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups) -> None:
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.fill("blue")
        self.rect = self.image.get_frect(center = pos)
