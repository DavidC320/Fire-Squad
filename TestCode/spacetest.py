import pygame


class StarParticleController(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.spawn_x = 400
        self.spawn_y = 300

        self.image = pygame.Surface((24, 24))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(self.spawn_x, self.spawn_y))
        self.speed = 10

    def star_spawn_movement(self):
        keys = pygame.key.get_pressed()
        if self.rect.y <= 580 and keys[pygame.K_UP] or keys[pygame.K_w]:
            self.spawn_y += self.speed

        if self.rect.y >= -10 and keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.spawn_y -= self.speed

        if self.rect.x <= 780 and keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.spawn_x += self.speed

        if self.rect.x >= -10 and keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.spawn_x -= self.speed

        self.rect = self.image.get_rect(center=(self.spawn_x, self.spawn_y))
        print(f'{self.spawn_x} {self.spawn_y}')

    def update(self):
        self.star_spawn_movement()


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Shooting thing')
clock = pygame.time.Clock()

# groups
star = StarParticleController()
star_group = pygame.sprite.Group()
star_group.add(star)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # drawing
    screen.fill((30, 30, 30))
    star_group.draw(screen)
    star_group.update()

    pygame.display.update()
    clock.tick(60)
