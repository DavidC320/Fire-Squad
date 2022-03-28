# created on 3/17/2022
from numpy import can_cast, imag
import pygame
from Settings import wn_height, wn_width

class BaseUpgrades(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.size_change = 1.5
        self.size_cap = 90

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
        """
        if self.move_up:
            if self.y >=  280:
                self.y -= 2.5
            else:
                self.move_up = False
        else:
            if self.y <=  320:
                self.y += 2.5
            else:
                self.move_up = True

    def select_fun(self, is_selected):
        if is_selected:
            self.changed = True
            if self.times_changed <= self.size_cap:
                self.times_changed += 1
                self.image_size = self.image.get_size()
                self.upgrade_image = pygame.transform.scale(self.image, (int(self.image_size[0] * self.size_change),int(self.image_size[1] * self.size_change)))
        else:
            if self.changed:
                if self.times_changed == 0:
                    self.times_changed -= 1
                    self.image_size = self.image.get_size
                    self.upgrade_image = pygame.transform.scale(self.image, (int(self.image_size[0] / self.size_change),int(self.image_size[1] / self.size_change)))

    def despawn(self):
        if self.y <= wn_height + self.image_size[1]:
            self.y += 5
        else:
            self.kill()


class HealthUpgrade(BaseUpgrades):
    def __init__(self, spawn_x, dificulty, player_data):
        BaseUpgrades.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        self.x = spawn_x
        self.y = wn_height + 24
        self.times_changed = 0  # records how many times the image has been changed. This will be used to increase and decrease the size.
        

        self.player_data = player_data
        self.level = player_data.health_lv
        self.rounds = player_data.total_rounds()
        ###################################### display ######################################

        color = "white"
        self.image_size = [200, 200]
        self.upgrade_image = pygame.Surface((self.image_size[0], self.image_size[1]))
        self.upgrade_image.fill(color)

        # display
        self.image = self.upgrade_image
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # icon

        # text
        self.title_text = "Health"
        self.discription = "Increase the amout of damage you can reseive from your advisaries"

        # price, will be used in comparison between the player wallet.
        if dificulty > 0:
            self.price = (1000 * self.level + (200 * int(0.5 * self.rounds))) * dificulty
        else:
            self.price = 1000 * self.level + (200 * int(0.5 * self.rounds))

        self.credits = self.player_data.credits

        if self.price > self.credits:  # checks if the player can purchase an item and changes the border acordenly
            self.can_buy = False
        else:
            self.can_buy = True
        ###################################### display ######################################

        self.state = "spawn"
        self.move_up = True
        self.changed = False


    def activation(self):
        self.player_data.credits -= self.price
        self.player_data.health += 1
        self.state = "despawn"

    def update(self, hovering, clicked, destroy):
        print(self.state)
        print(self.y)
        if destroy:
            self.state = "despawn"

        if self.state == "spawn":
            print(1)
            self.spawn_movement()

        elif self.state == "idle":
            print(2)
            is_hovering = hovering
            self.idle_movement()
            if is_hovering:
                self.select_fun()
                if clicked:
                    if self.can_buy:
                        self.activation
                    else:
                        None # play a sound

        elif self.state == "despawn":  # despawn
            print("despawned")
            self.despawn()

        else:
            print("despawned")
            self.despawn()

        self.rect = self.image.get_rect(center=(self.x, self.y))
