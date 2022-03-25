# created on 3/17/2022
import pygame
from Settings import wn_height, wn_width

class BaseUpgrades:
    def __init__(self, spawn_x, level):
        self.x = spawn_x
        self.y = wn_height + 24

        # Image
        color = "White"
        self.image_size = [24, 24]
        self.upgrade_image = pygame.Surface((self.image_size[0], self.image_size[1]))
        self.upgrade_image.fill(color)

        # display
        self.image_size = self.upgrade_image.get_size()
        self.rect = self.upgrade_image.get_rect(center=(self.x, self.y))

        self.state = "Spawn"
        '''
        Spawn = The UI is moving from the top screen to the middle
        Idle = Moving up and down from the center of the screen
        Hovering = Resized to be bigger when the cursor is over it
        Selected + =
        Selected - =
        '''
        self.move_up = True
        self.changed = False

    def spawn_movement(self):
        if self.y >= 320:
            spawn_speed -= 5
            self.y -= spawn_speed
        else:
            self.state = "Idle"

    def idle_movement(self):
        """
        screen width is 600 so 300 is the center of iscolation
        maybe the iscolation will look good with a 20 pixel ofset so 40 pixel up and down
        300 + 20 = 320 then 300 - 20 = 280
        """
        if self.move_up:
            if self.y >=  280:
                self.y -= 5
            else:
                self.move_up = False
        else:
            if self.y <=  320:
                self.y += 5
            else:
                self.move_up = True

    def select_fun(self, is_selected):
        if is_selected:
            None
        else:
            None

class HealthUpgrade(BaseUpgrades):
    def __init__(self, spawn_x, level):
        self.level = level
        ###################################### display ######################################
        # icon

        # text
        self.title_text = "Health"
        self.discription = "Increase the amout of damage you can reseive from your advisaries"
        # price, will be used in comparison between the player wallet.
        self.price = None
        ###################################### display ######################################
