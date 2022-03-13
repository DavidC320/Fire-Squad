from shutil import move
from ToolBoxOfGarbage import point_getter
import pygame
import math
from random import random, randrange
from Settings import z_max, wn_width, wn_height


class Particle(pygame.sprite.Sprite):
    def __init__(self, origin_pos, z_value, target_pos, speed, style, damage, spawn_time):
        super().__init__()

        self.spawn_time = spawn_time

        # variables
        self.speed = speed * 0.90
        self.damage = damage
        self.z = z_value

        # origin position
        self.spawn_x = origin_pos[0]
        self.spawn_y = origin_pos[1]

        # actual position
        self.x = self.spawn_x
        self.y = self.spawn_y

        # target position // taken from D5
        self.style = style
        if style == "star":
            target_pos = point_getter.point(origin_pos[0], origin_pos[1], 10000)
        self.target_x = target_pos[0]
        self.target_y = target_pos[1]

        # image
        self.image_size = [12, 12]
        self.image = pygame.Surface(self.image_size)
        self.image.fill((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (int(self.image_size[0] * self.z), int(self.image_size[1] * self.z)))
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.moving = False


    def z_movement(self):
        if self.z < z_max:
            self.z += .001 * self.speed
        else:
            self.kill()
        self.image = pygame.transform.scale(self.image, (int(self.image_size[0] * self.z), int(self.image_size[1] * self.z)))

    def particle_cont(self, move_lock):
        locks = move_lock

        # gets key inputs
        keys = pygame.key.get_pressed()
        up = (keys[pygame.K_UP] or keys[pygame.K_w])
        down = (keys[pygame.K_DOWN] or keys[pygame.K_s])
        left = (keys[pygame.K_LEFT] or keys[pygame.K_a])
        right = (keys[pygame.K_RIGHT] or keys[pygame.K_d])
        locks = move_lock
        """if self.style == "star":
            locks = (True, True, True, True)"""

        if not locks[1] and up:
            self.y += self.speed
            self.target_y += self.speed

        if not locks[3] and down:
            self.y -= self.speed
            self.target_y -= self.speed

        if not locks[0] and left:
            self.x += self.speed
            self.target_x += self.speed

        if not locks[2] and right:
            self.x -= self.speed
            self.target_x -= self.speed

        if up or down or left or right:
            self.moving = True
        else:
            self.moving = False

    def particle_movement(self):
        pos = [(self.x), (self.y)]
        # print((pos))
        target_pos = [self.target_x, self.target_y]
        # print(target_pos)
        speed = self.speed

        if self.moving and self.style != "star":
            speed = speed / 4
            # print('wooh')

        pos_check = (target_pos[0] - self.speed < pos[0] < target_pos[0] + self.speed) and (
                target_pos[1] - self.speed < pos[1] < target_pos[1] + self.speed)

        self.pre_x = self.x
        self.pre_y = self.y

        if pos_check:
            self.target_x = randrange(0, wn_width)
            self.target_y = randrange(0, wn_height)

        if not pos_check:
            radians = math.atan2(self.target_y - self.pre_y, self.target_x - self.pre_x)

            self.dir_x = math.cos(radians) * speed
            self.dir_y = math.sin(radians) * speed

            self.pre_x, self.pre_y = self.target_x, self.target_y
            # print('Targeting')
            self.x += self.dir_x
            self.y += self.dir_y
            # print('moving'

        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def update(self, locks, current_time):
        self.z_movement()
        self.particle_cont(locks)
        self.particle_movement()

        if current_time - self.spawn_time > 10000:  # kill particle
            self.kill()
