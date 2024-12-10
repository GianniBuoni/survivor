# pyright: reportOptionalMemberAccess=false

import pygame
from os import walk, path

from lib.entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, collision_group) -> None:
        # load images before super
        self.load_images()
        self.state = "down"

        super().__init__(self.all_frames[self.state], pos, groups, collision_group)

    def load_images(self):
        self.all_frames = { "left": [], "down": [], "up": [], "right": [], }
        dirparent = path.join("images", "player")

        for dirpath, _, filenames in walk(dirparent):
            if filenames:
                state = dirpath.replace(f"{dirparent}/", "")
                for file in sorted(filenames, key = lambda x: int(x.split(".")[0])):
                    file_path = path.join(dirpath, file)
                    surface = pygame.image.load(file_path).convert_alpha()
                    self.all_frames[state].append(surface)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def change_state(self):
        # get state
        if self.direction.x != 0:
            self.state = "right" if self.direction.x > 0 else "left"
        if self.direction.y != 0:
            self.state = "down" if self.direction.y > 0 else "up"

        # change frames
        self.frames = self.all_frames[self.state]

    def update(self, dt):
        self.input()
        self.change_state()
        self.animate(dt)
        self.move(dt)
