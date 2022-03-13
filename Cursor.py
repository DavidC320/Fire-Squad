import pygame

class CursorControl(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        image = pygame.image.load(r"GFX\aim.png")
        image_size = image.get_size()
        self.image = pygame.transform.scale(image, (int(image_size[0] / 35), int(image_size[1] / 35)))  # this is taken from A2
        # original Dimensions (2048, 2048)
        self.rect = self.image.get_rect(center=((self.x, self.y)))

    def cursor_move(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = self.image.get_rect(center=((self.x, self.y)))

    def update(self, pos):
        self.cursor_move(pos)