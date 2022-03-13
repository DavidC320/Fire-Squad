# restart date 1/19/2022
# version 1.0.4
# David Cruz
# credit in credits.txt in the info folder
from decimal import ROUND_DOWN, Rounded
import math
import pygame
from random import randrange, choices, random

pygame.init()
wn_width = 800
wn_height = 600
z_max = 10
screen = pygame.display.set_mode((wn_width, wn_height))
pygame.display.set_caption('Shooting thing')
clock = pygame.time.Clock()


class StarParticleController(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # posistion
        self.spawn_x = wn_width / 2
        self.spawn_y = wn_height / 2

        # Image
        self.image = pygame.Surface((24, 24))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(self.spawn_x, self.spawn_y))
        self.speed = 4
        self.lock_config = [False, False, False, False]

    def star_spawn_movement(self):
        keys = pygame.key.get_pressed()
        
        # upward movement
        if self.rect.y <= wn_height - 16 and (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.spawn_y += self.speed
            self.lock_config[1] = False
        elif self.rect.y >= wn_height - 16:
            self.lock_config[1] = True
    
        # downward movement
        if self.rect.y >= -8 and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.spawn_y -= self.speed
            self.lock_config[3] = False
        elif self.rect.y <= -8:
            self.lock_config[3] = True
    
        # leftward movment
        if self.rect.x <= wn_width - 16 and (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.spawn_x += self.speed
            self.lock_config[0] = False
        elif self.rect.x >= wn_width - 16:
            self.lock_config[0] = True
    
        # rightward movement
        if self.rect.x >= -8 and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.spawn_x -= self.speed
            self.lock_config[2] = False
        elif self.rect.x <= -8:
            self.lock_config[2] = True
    
        self.rect = self.image.get_rect(center=(self.spawn_x, self.spawn_y))
        #print(f"{self.spawn_x} {self.spawn_y}")

    def update(self):
        self.star_spawn_movement()
        # print(self.lock_config)


class Particle(pygame.sprite.Sprite):
    def __init__(self, origin_pos, z_value, targ_pos, speed, style, damage):
        super().__init__()

        # variables
        self.speed = speed
        self.damage = damage
        self.z = z_value

        # origin posistion
        self.spawn_x = origin_pos[0]
        self.spawn_y = origin_pos[1]

        # actual posistion
        self.x = self.spawn_x
        self.y = self.spawn_y

        # target posistion // taken from D5
        if style == "star":
            targ_pos = self.point(origin_pos[0],origin_pos[1], 10000)
        self.targ_x = targ_pos[0]
        self.targ_y = targ_pos[1]

        # image
        self.image_size = [12, 12]
        self.image = pygame.Surface(self.image_size)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def point(self, h, k, r):  # code taken from D5
        """This creates a random point somewhere on the circonferance of a circle"""
        # h and k are the center of the circle so the origin point
        # r is radius
        theta = random() * 2 * math.pi
        return h + math.cos(theta) * r, k + math.sin(theta) * r

    def z_movment(self):
        if self.z < z_max:
            self.z += .001 * self.speed
        else:
            self.kill()
        self.image = pygame.transform.scale(self.image, (self.image_size[0] * self.z, self.image_size[1] * self.z))

    def particle_cont(self, move_lock):
        locks = move_lock

        # gets key inputs 
        keys = pygame.key.get_pressed()
        up = (keys[pygame.K_UP] or keys[pygame.K_w])
        down = (keys[pygame.K_DOWN] or keys[pygame.K_s])
        left = (keys[pygame.K_LEFT] or keys[pygame.K_a])
        right = (keys[pygame.K_RIGHT] or keys[pygame.K_d])

        if not locks[1] and up:
            self.y += self.speed
            self.targ_y += self.speed

        if not locks[3] and down:
            self.y -= self.speed
            self.targ_y -= self.speed

        if not locks[0] and left:
            self.x += self.speed
            self.targ_x += self.speed

        if not locks[2] and right:
            self.x -= self.speed
            self.targ_x -= self.speed
        
        if up or down or left or right:
            self.moving = True
        else:
            self.moving = False
        
    def particle_movement(self):
        pos = [(self.x), (self.y)]
        # print((pos))
        target_pos = [self.targ_x, self.targ_y]
        # print(target_pos)
        speed = self.speed
        
        if self.moving:
                speed = speed/4
                # print('wooh')

        pos_check = (pos[0] > target_pos[0] - self.speed and pos[0] < target_pos[0] + self.speed) and (pos[1] > target_pos[1] - self.speed and pos[1] < target_pos[1] + self.speed)

        self.pre_x = self.x
        self.pre_y = self.y

        if pos_check:
            self.distance = 0
            self.tar_x = randrange(0, wn_width)
            self.tar_y = randrange(0, wn_height)

        if not pos_check:
            radians = math.atan2(self.targ_y - self.pre_y, self.targ_x - self.pre_x)
            self.distance = math.hypot(self.targ_x - self.pre_x, self.targ_y - self.pre_y)

            self.dir_x = math.cos(radians) * speed
            self.dir_y = math.sin(radians) * speed

            self.pre_x, self.pre_y = self.targ_x, self.targ_y
            # print('Targeting')
            self.x += self.dir_x
            self.y += self.dir_y
            # print('moving'

        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def update(self, locks):
        self.z_movment()
        self.particle_cont(locks)
        self.particle_movement()


class CursorControl(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        image = pygame.image.load(r"../../GFX/aim.png")
        image_size = image.get_size()
        self.image = pygame.transform.scale(image, (image_size[0] / 35, image_size[1] / 35))  # this is taken from A2
        # original Dimensions (2048, 2048)
        self.rect = self.image.get_rect(center=((self.x, self.y)))

    def cursor_move(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = self.image.get_rect(center=((self.x, self.y)))

    def update(self, pos):
        self.cursor_move(pos)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, ship_type):
        super().__init__()

        self.ship_type = ship_type

        # Location
        self.x = wn_width/2
        self.y = wn_height/2
        self.z = 0.05

        # Image
        self.image_size = [50, 24]
        self.image = pygame.Surface((self.image_size[0], self.image_size[1]))  # (width, height)
        color = (0, 0, 0)
        if self.ship_type == "chaser":
            color = (255, 0, 0)  # red
        if self.ship_type == "shooter":
            color = (255, 255, 0)  # taken from D1 // yellow
        if self.ship_type == "launcher":
            color = (0, 255, 0)  # green
        if self.ship_type == "morpher":
            color = (196, 196, 196)  # taken from googles color picker // light grey
        if self.ship_type == "holder":
            color = (138,43,226)  # taken from D2 // blue violet
        self.image = pygame.transform.scale(self.image, (self.image_size[0] * self.z, self.image_size[1] * self.z))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        

        # Block of varables from B3
        # Target location
        self.tar_x = randrange(0, wn_width)  # B3 eqivelent - mx
        self.tar_y = randrange(0, wn_height)  # B3 eqivelent - my
        # Previous location
        self.pre_x = self.x  # B3 eqivelent - pmx
        self.pre_y = self.x  # B3 eqivelent - pmy
        # Directional value
        self.dir_x = 0  # B3 eqivelent - dx
        self.dir_y = 0  # B3 eqivelent - dx
        self.distance = 0
        
        # Movement 
        self.moving = False
        self.speed = 10

    def enemy_movement_cont(self, move_lock):
        locks = move_lock
        keys = pygame.key.get_pressed()
        up = (keys[pygame.K_UP] or keys[pygame.K_w])
        down = (keys[pygame.K_DOWN] or keys[pygame.K_s])
        left = (keys[pygame.K_LEFT] or keys[pygame.K_a])
        right = (keys[pygame.K_RIGHT] or keys[pygame.K_d])

        if not locks[1] and up:
            self.y += self.speed
            self.tar_y += self.speed

        if not locks[3] and down:
            self.y -= self.speed
            self.tar_y -= self.speed

        if not locks[0] and left:
            self.x += self.speed
            self.tar_x += self.speed

        if not locks[2] and right:
            self.x -= self.speed
            self.tar_x -= self.speed
        
        if up or down or left or right:
            self.moving = True
            #print('yeah')
        else:
            self.moving = False
            # print('no')

        # print(f"{self.spawn_x} {self.spawn_y}")

# This is taken from B3
    def enemy_movement(self):
        pos = [(self.x), (self.y)]
        # print((pos))
        target_pos = [self.tar_x, self.tar_y]
        # print(target_pos)
        speed = self.speed
        
        if self.moving:
                speed = speed/4
                # print('wooh')

        pos_check = (pos[0] > target_pos[0] - self.speed and pos[0] < target_pos[0] + self.speed) and (pos[1] > target_pos[1] - self.speed and pos[1] < target_pos[1] + self.speed)

        self.pre_x = self.x
        self.pre_y = self.y

        if pos_check:
            self.distance = 0
            self.tar_x = randrange(0, wn_width)
            self.tar_y = randrange(0, wn_height)

        if not pos_check:
            radians = math.atan2(self.tar_y - self.pre_y, self.tar_x - self.pre_x)
            self.distance = math.hypot(self.tar_x - self.pre_x, self.tar_y - self.pre_y)

            self.dir_x = math.cos(radians) * speed
            self.dir_y = math.sin(radians) * speed

            self.pre_x, self.pre_y = self.tar_x, self.tar_y
            # print('Targeting')
            self.x += self.dir_x
            self.y += self.dir_y
            # print('moving')

        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def z_movment(self):
        if self.z < z_max:
            self.z += .001 * self.speed
        else:
            self.z = .05
        self.image = pygame.transform.scale(self.image, (self.image_size[0] * self.z, self.image_size[1] * self.z))
           
    def update(self, list_in):
        self.z_movment()
        self.enemy_movement_cont(list_in)
        self.enemy_movement()

def enemy_collide(health):
    if len(enemy_group) > 0:
        for enemies in enemy_group:  # This is taken from B1
            # this is taken from B2
            if pygame.mouse.get_pressed()[0] and enemies.rect.colliderect(cursor.sprite.rect):
                enemies.kill()
            if enemies.z > z_max * .8:
                if enemies.z >= z_max:
                    health -=1
                return True, health
            else:
                return False, health
    else:
        return False, health


# Images
game_ship_gui = pygame.image.load("../../GFX/gui/gameGui/ShipBackGround0.2.png")

# Groups
# spcae controller
star_point = StarParticleController()
space_cont = pygame.sprite.GroupSingle()
space_cont.add(star_point)

star_group = pygame.sprite.Group()

# enemies
enemy_name = ['chaser', "shooter", "launcher", "morpher", "holder"]
enemy_weight = [24, 24, 24, 24, 4] 
enemy_group = pygame.sprite.Group()
for action in range(1):
    enemy_type = choices(enemy_name, enemy_weight, k=1)  # taken from D3
    enemy = Enemy(*enemy_type)  # taken from D4 // * symbol gets rib of the []
    enemy_group.add(enemy)

# mouse controller
pointer = CursorControl()
cursor = pygame.sprite.GroupSingle()
cursor.add(pointer)

# Variables
playing = True
game = True

warning = False
health = 10

# timer
star_particle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(star_particle_timer, 1500)

# code taken from C1
font = pygame.font.Font(None, 50)
warning_surface = font.render('WARNING!', True, 'Yellow')
warning_rect = warning_surface.get_rect(center=(wn_width/2, wn_height/1.2))

# Bugfixes
mouse_position = (wn_width / 2, wn_height / 2) # in case the mouse is not in the game window

# Game
while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            exit()
        if events.type == pygame.MOUSEMOTION:  # This is taken from A1
            mouse_position = pygame.mouse.get_pos()
            # print(mouse_position)
        if game:
            if events.type == star_particle_timer:
                star = Particle((star_point.spawn_x, star_point.spawn_y), 1, (0, 0), 5, "star", 0)
                star_group.add(star)

    # Checks
    check_info = enemy_collide(health)
    warning = check_info[0]
    health = check_info[1]
    if health < 1:
        enemy_group.empty()
        star_group.empty()
        print("game over")

    # Draw
    screen.fill((30, 30, 30))

    space_cont.draw(screen)
    space_cont.update()

    star_group.draw(screen)
    star_group.update(space_cont.sprite.lock_config)

    enemy_group.draw(screen)
    enemy_group.update(space_cont.sprite.lock_config)

    cursor.draw(screen)
    cursor.update(mouse_position)

    screen.blit(game_ship_gui, (0, 0))

    if warning:
        # code taken from C1
        screen.blit(warning_surface, warning_rect)

    pygame.display.update()
    clock.tick(60)
