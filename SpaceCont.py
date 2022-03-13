import pygame
from Settings import wn_width, wn_height


class SpaceController:
    def __init__(self):

        # position
        self.spawn_x = wn_width / 2
        self.spawn_y = wn_height / 2

        # locks
        self.lock_config = [False, False, False, False]

    def star_spawn_movement(self, speed):
        self.speed = speed
        keys = pygame.key.get_pressed()

        # upward movement
        if self.spawn_y <= wn_height and (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.spawn_y += self.speed
            self.lock_config[1] = False
        elif self.spawn_y >= wn_height:
            self.lock_config[1] = True

        # downward movement
        if self.spawn_y >= 0 and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.spawn_y -= self.speed
            self.lock_config[3] = False
        elif self.spawn_x <= 0:
            self.lock_config[3] = True

        # leftward movement
        if self.spawn_x <= wn_width and (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.spawn_x += self.speed
            self.lock_config[0] = False
        elif self.spawn_x >= wn_width:
            self.lock_config[0] = True

        # rightward movement
        if self.spawn_x >= 0 and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.spawn_x -= self.speed
            self.lock_config[2] = False
        elif self.spawn_x <= 0:
            self.lock_config[2] = True
        # print(f"{self.spawn_x} {self.spawn_y}")

    def update(self, speed):
        self.star_spawn_movement(speed)
