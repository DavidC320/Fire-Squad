# created on 3/17/2022
from msilib.schema import Upgrade
from matplotlib.pyplot import text
from numpy import can_cast, imag
import pygame
from Settings import wn_height, wn_width

class BaseUpgrades(pygame.sprite.Sprite):
    def __init__(self, display_screen):
        super().__init__()

        self.display = display_screen
        # image
        self.upgrade_image = pygame.image.load("GFX\\gui\\gameGui\\Upgrade\\Upgrade.png").convert_alpha()
        self.image_size = self.upgrade_image.get_size()

        self.size_change = 2
        self.size_cap = 11

    def spawn_movement(self):
        if self.y >= 320:
            spawn_speed = 5
            self.y -= spawn_speed
        else:
            self.state = "idle"

    def idle_movement(self):
        """
        screen width is 600 so 300 is the center of iscolation
        maybe the iscolation will look good with a 20 pixel ofset so 40 pixel up and down
        300 + 20 = 320 then 300 - 20 = 280
        im going to add 20 more to make this look better
        """
        if self.move_up:
            if self.y >=  260:
                self.y -= 1.5
            else:
                self.move_up = False
        else:
            if self.y <=  340:
                self.y += 1.5
            else: 
                self.move_up = True

    def select_fun(self, is_selected):  # image smooth scale fix from L1
        """
        The fix is to keep a copy of original image and using that as the something but I guess it is used as a double check for the master image"""
        if is_selected and not self.reverting:
            self.changed = True
            if self.times_changed < self.size_cap:
                self.times_changed += 1
                self.image_size = self.image.get_size()
                self.image = pygame.transform.smoothscale(self.upgrade_image, (int(self.image_size[0] + self.size_change),int(self.image_size[1] + self.size_change*2)))
        else:
            if self.changed:
                if self.times_changed > -1:
                    self.reverting = True
                    self.times_changed -= 1
                    self.image_size = self.image.get_size()
                    self.image = pygame.transform.smoothscale(self.upgrade_image, (int(self.image_size[0] - self.size_change),int(self.image_size[1] - self.size_change*2)))
                else:
                    self.reverting = False
                    self.changed = False

    def despawn(self):
        if self.changed:
                if self.times_changed > -1:
                    self.times_changed -= 1
                    self.image_size = self.image.get_size()
                    self.image = pygame.transform.smoothscale(self.upgrade_image, (int(self.image_size[0] - self.size_change),int(self.image_size[1] - self.size_change*2)))
                else:
                    self.changed = False
        self.image_size = self.image.get_size()
        if self.y <= wn_height + self.image_size[1]:
            self.y += 5
        else:
            self.kill()

    def icon_location(self):
        midtop_pos = self.rect.midtop
        distance = self.y - midtop_pos[1]
        location = distance * 0.38
        return location

    def text_write(self, text, color, pos, font_num):
        self.font = pygame.font.Font(None, 40)
        
        if font_num == 1:
            screen_text = self.font.render(text, True, color)

        screen_text_rect = screen_text.get_rect(center=(pos))

        self.display.blit(screen_text, screen_text_rect)


class HealthUpgrade(BaseUpgrades):
    def __init__(self, spawn_x, dificulty, player_data, display_screen):
        BaseUpgrades.__init__(self, display_screen)
        pygame.sprite.Sprite.__init__(self)

        self.x = spawn_x
        self.y = wn_height + 24
        self.times_changed = 0  # records how many times the image has been changed. This will be used to increase and decrease the size.
        

        self.player_data = player_data
        self.level = player_data.health_lv
        self.rounds = player_data.total_rounds()
        ###################################### display ######################################
        # display
        self.image = self.upgrade_image.convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # icon
        self.icon_copy = pygame.image.load("GFX\\gui\\gameGui\\Upgrade\\Health.png").convert_alpha()
        self.icon = pygame.image.load("GFX\\gui\\gameGui\\Upgrade\\Health.png").convert_alpha()

        # text
        self.title_text = "Health"

        # price, will be used in comparison between the player wallet.
        if dificulty > 0:
            self.price = (1000 * self.level + (200 * int(0.5 * self.rounds))) * dificulty
        else:
            self.price = 1000 * self.level + (200 * int(0.5 * self.rounds))

        self.credits = self.player_data.credits
        ###################################### display ######################################

        self.state = "spawn"
        self.reverting = False
        self.move_up = True
        self.changed = False


    def activation(self):
        if not self.state == "despawn":
            if self.price > self.player_data.credits:  # checks if the player can purchase an item and changes the border acordenly
                None
            else:
                self.player_data.credits -= self.price
                self.player_data.health += 1
                self.player_data.health_lv += 1
                self.state = "despawn"

    def update(self, destroy):
        if destroy:
            self.state = "despawn"

        if self.state == "spawn":
            self.spawn_movement()

        elif self.state == "idle":
            self.idle_movement()

        elif self.state == "despawn":
            self.despawn()

        else:
            print("despawned")
            self.despawn()
        
        self.text_write(self.title_text, "Grey", (self.x, self.y+25), 1)
        self.text_write(str(self.price), "Grey", (self.x, self.y+55), 1)

        location = self.icon_location()
        
        self.icon_rect = self.icon.get_rect(center=(self.x, self.y - location))  # this is really difficult to think of too keep this centerd on the target location
        # Here is the problem, if I was to just use a midtop offset then the icon would be placed incorectly when the upgrade is scaled up. If I used the center then it would even be even more incorect when the upgrade scale.
        # Here is my idea. I can use the midtop and center to create the position for the icon, center - mitop = value betweenn midtop and center then value / or * another value = to y location. completed.
        self.display.blit(self.icon, self.icon_rect)

        self.rect = self.image.get_rect(center=(self.x, self.y))

class DamageUpgrade(BaseUpgrades):
    def __init__(self, spawn_x, dificulty, player_data, display_screen):
        BaseUpgrades.__init__(self, display_screen)
        pygame.sprite.Sprite.__init__(self)

        self.x = spawn_x
        self.y = wn_height + 24
        self.times_changed = 0  # records how many times the image has been changed. This will be used to increase and decrease the size.
        

        self.player_data = player_data
        self.level = player_data.damage_lv
        self.rounds = player_data.total_rounds()
        ###################################### display ######################################
        # display
        self.image = self.upgrade_image.convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # icon
        self.icon_copy = pygame.image.load("GFX\\gui\\gameGui\\Upgrade\\Damage.png").convert_alpha()
        self.icon = pygame.image.load("GFX\\gui\\gameGui\\Upgrade\\Damage.png").convert_alpha()

        # text
        self.title_text = "Damage"

        # price, will be used in comparison between the player wallet.
        if dificulty > 0:
            self.price = (1000 * self.level + (200 * int(0.5 * self.rounds))) * dificulty
        else:
            self.price = 1000 * self.level + (200 * int(0.5 * self.rounds))

        self.credits = self.player_data.credits
        ###################################### display ######################################

        self.state = "spawn"
        self.reverting = False
        self.move_up = True
        self.changed = False


    def activation(self):
        if not self.state == "despawn":
            if self.price > self.player_data.credits:  # checks if the player can purchase an item and changes the border acordenly
                None
            else:
                self.player_data.credits -= self.price
                self.player_data.damage += 1
                self.player_data.damage_lv += 1
                self.state = "despawn"

    def update(self, destroy):
        if destroy:
            self.state = "despawn"

        if self.state == "spawn":
            self.spawn_movement()

        elif self.state == "idle":
            self.idle_movement()

        elif self.state == "despawn":
            self.despawn()

        else:
            print("despawned")
            self.despawn()
        
        self.text_write(self.title_text, "grey", (self.x, self.y+25), 1)
        self.text_write(str(self.price), "grey", (self.x, self.y+55), 1)

        location = self.icon_location()
        
        self.icon_rect = self.icon.get_rect(center=(self.x, self.y - location))

        self.display.blit(self.icon, self.icon_rect)

        self.rect = self.image.get_rect(center=(self.x, self.y))

class FirerateUpgrade(BaseUpgrades):
    def __init__(self, spawn_x, dificulty, player_data, display_screen):
        BaseUpgrades.__init__(self, display_screen)
        pygame.sprite.Sprite.__init__(self)

        self.x = spawn_x
        self.y = wn_height + 24
        self.times_changed = 0  # records how many times the image has been changed. This will be used to increase and decrease the size.
        

        self.player_data = player_data
        self.level = player_data.damage_lv
        self.rounds = player_data.total_rounds()
        ###################################### display ######################################
        # display
        self.image = self.upgrade_image.convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # icon
        self.icon_copy = pygame.image.load("GFX\\gui\\gameGui\\Upgrade\\Firerate.png").convert_alpha()
        self.icon = pygame.image.load("GFX\\gui\\gameGui\\Upgrade\\Firerate.png").convert_alpha()

        # text
        self.title_text = "Firerate"

        # price, will be used in comparison between the player wallet.
        if dificulty > 0:
            self.price = (2000 * self.level + (200 * int(0.5 * self.rounds))) * dificulty
        else:
            self.price = 2000 * self.level + (200 * int(0.5 * self.rounds))

        self.credits = self.player_data.credits
        ###################################### display ######################################

        if self.player_data.firerate_lv <= 5:
            self.can_buy = True
        else:
            self.can_buy = False

        self.state = "spawn"
        self.reverting = False
        self.move_up = True
        self.changed = False


    def activation(self):
        if not self.state == "despawn" or self.can_buy:
            if self.price > self.player_data.credits:  # checks if the player can purchase an item and changes the border acordenly
                None
            else:
                self.player_data.credits -= self.price
                self.player_data.damage_lv += 1
                self.state = "despawn"

    def update(self, destroy):
        if destroy:
            self.state = "despawn"

        if self.state == "spawn":
            self.spawn_movement()

        elif self.state == "idle":
            self.idle_movement()

        elif self.state == "despawn":
            self.despawn()

        else:
            print("despawned")
            self.despawn()
        
        self.text_write(self.title_text, "grey", (self.x, self.y+25), 1)
        self.text_write(str(self.price), "grey", (self.x, self.y+55), 1)

        location = self.icon_location()
        
        self.icon_rect = self.icon.get_rect(center=(self.x, self.y - location))

        self.display.blit(self.icon, self.icon_rect)

        self.rect = self.image.get_rect(center=(self.x, self.y))