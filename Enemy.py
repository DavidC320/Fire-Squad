import pygame
import math
from random import randrange
from ToolBoxOfGarbage import point_getter
from Settings import wn_width, wn_height, z_max, rangers


class Enemy(pygame.sprite.Sprite):
    def __init__(self, ship_type, z_value, spawn_pos, speed, spawn_time):
        super().__init__()
        # init settings
        self.ship_type = ship_type
        self.speed = speed
        self.z = z_value  # 0.05

        # other variables
        self.z_speed = .001 * self.speed
        self.state = "chasing"
        self.health = 1

        ############################## spawn location ##############################
        self.x = spawn_pos[0]
        self.y = spawn_pos[1]

        ################################ ship image ################################

        ################################ ship types ################################

        if self.ship_type == "chaser":
            self.ship_image = pygame.image.load("GFX\\enemy\\Chaser.png").convert_alpha()
            # color = (255, 0, 0)  # red
            targ_x = wn_width/2
            targ_y = wn_height/2
            self.z_max = z_max
            # varables
            self.damage = 1
            self.score_points = 150

        if self.ship_type == "launcher":
            self.ship_image = pygame.image.load("GFX\\enemy\\Launcher.png").convert_alpha()
            # color = (255, 255, 0)  # taken from D1 // yellow
            targ_x = randrange(0, wn_width)
            targ_y = randrange(129, wn_height-74)
            self.z_max = 1
            # varables
            self.damage = 1
            self.score_points = 250
            self.speed = speed / 2
            self.spawn_time = spawn_time
            self.can_fire = False
            self.last_fire = None

        if self.ship_type == "shooter":
            self.ship_image = pygame.image.load("GFX\\enemy\\Shooter.png").convert_alpha()
            # color = (0, 255, 0)  # green
            targ_x = randrange(0, wn_width)
            targ_y = randrange(129, wn_height-74)
            self.z_max = 1
            # varables
            self.damage = 1
            self.score_points = 250
            self.speed = speed / 2
            self.spawn_time = spawn_time
            self.can_fire = False
            self.last_fire = None
            
        
        ############################### Projectiles ###############################

        if self.ship_type == "bullet":
            color = "Yellow"
            self.image_size = [24, 24]
            self.ship_image = pygame.Surface((self.image_size[0], self.image_size[1]))
            self.ship_image.fill(color)

            targ_x = wn_width/2
            targ_y = wn_height/2
            self.z_max = z_max
            #varables
            self.damage = 1
            hypo = math.hypot(targ_x - self.x, targ_y - self.y)
            print(hypo/100)
            self.speed = speed / (hypo/150)
            print(self.speed)
            self.z_speed = .003 * speed

        if self.ship_type == "missle":
            color = "Green"
            self.image_size = [24, 24]
            self.ship_image = pygame.Surface((self.image_size[0], self.image_size[1]))
            self.ship_image.fill(color)

            targ_x = randrange(0, wn_width)
            targ_y = randrange(129, wn_height-74)
            self.z_max = z_max
            #varables
            self.damage = 1
            self.score_points = 100
            hypo = math.hypot(targ_x - self.x, targ_y - self.y)
            print(hypo/100)
            self.speed = speed / (hypo/150)
            print(self.speed)
            self.z_speed = .0015 * speed

        ############################ unused ship types ############################

        if self.ship_type == "morpher":
            color = (196, 196, 196)  # taken from googles color picker // light grey
        if self.ship_type == "holder":
            color = (138, 43, 226)  # taken from D2 // blue violet

        self.image_size = self.ship_image.get_size()
        self.image = pygame.transform.scale(self.ship_image, (self.image_size[0] * self.z, self.image_size[1] * self.z))
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Block of variables from B3
        # Target location
        self.tar_x = targ_x  # B3 equivalent - mx
        self.tar_y = targ_y  # B3 equivalent - my
        # Previous location
        self.pre_x = self.x  # B3 equivalent - pmx
        self.pre_y = self.x  # B3 equivalent - pmy
        # Directional value
        self.dir_x = 0  # B3 equivalent - dx
        self.dir_y = 0  # B3 equivalent - dx

        # Movement
        self.moving = False

    def enemy_movement_cont(self, move_lock):
        locks = move_lock
        keys = pygame.key.get_pressed()
        up = (keys[pygame.K_UP] or keys[pygame.K_w])
        down = (keys[pygame.K_DOWN] or keys[pygame.K_s])
        left = (keys[pygame.K_LEFT] or keys[pygame.K_a])
        right = (keys[pygame.K_RIGHT] or keys[pygame.K_d])

        if not locks[1] and up:
            self.y += self.speed
            if self.ship_type != "chaser":
                self.tar_y += self.speed

        if not locks[3] and down:
            self.y -= self.speed
            if self.ship_type != "chaser":
                self.tar_y -= self.speed

        if not locks[0] and left:
            self.x += self.speed
            if self.ship_type != "chaser":
                self.tar_x += self.speed

        if not locks[2] and right:
            self.x -= self.speed
            if self.ship_type != "chaser":
                self.tar_x -= self.speed

        if up or down or left or right:
            self.moving = True
            # print('yeah')
        else:
            self.moving = False
            # print('no')

        # print(f"{self.spawn_x} {self.spawn_y}")

    # This is taken from B3
    def enemy_movement(self):
        pos = [self.x, self.y]
        # print((pos))
        target_pos = [self.tar_x, self.tar_y]
        # print(target_pos)
        speed = self.speed

        if self.moving:
            speed = speed / 4
            # print('woo')

        pos_check = (target_pos[0] - self.speed < pos[0] < target_pos[0] + self.speed) and (
                target_pos[1] - self.speed < pos[1] < target_pos[1] + self.speed)

        self.pre_x = self.x
        self.pre_y = self.y

        if pos_check:
            if self.ship_type == "chaser":
                self.tar_x = wn_width/2
                self.tar_y = wn_height/2
            elif self.ship_type in rangers:
                self.tar_x = randrange(0, wn_width)
                self.tar_y = randrange(129, wn_height-74)


        if not pos_check:
            radians = math.atan2(self.tar_y - self.pre_y, self.tar_x - self.pre_x)

            self.dir_x = math.cos(radians) * speed
            self.dir_y = math.sin(radians) * speed

            self.pre_x, self.pre_y = self.tar_x, self.tar_y
            # print('Targeting')
            self.x += self.dir_x
            self.y += self.dir_y
            # print('moving')

        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def z_movement(self):  # controls the z value and size of the ship
        if self.z < self.z_max:
            self.z += self.z_speed
        else:
            if self.ship_type in rangers:
                self.can_fire = True
        self.image = pygame.transform.scale(self.ship_image, (self.image_size[0] * self.z, self.image_size[1] * self.z))

    def enemy_run(self, current_time):
        if current_time - self.spawn_time > 20000:
            self.kill()

    def update(self, list_in, current_time):
        self.z_movement()
        self.enemy_movement_cont(list_in)
        self.enemy_movement()

        if self.ship_type in rangers:
            self.enemy_run(current_time)
