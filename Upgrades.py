# created on 3/17/2022
import pygame

class BaseUpgrades:
    def __init__(self):
        None
        # Image
        color = "White"
        self.image_size = [24, 24]
        self.upgrade_image = pygame.Surface((self.image_size[0], self.image_size[1]))
        self.upgrade_image.fill(color)

        # display
        self.image_size = self.upgrade_image.get_size()
        self.rect = self.upgrade_image.get_rect(center=(self.x, self.y))