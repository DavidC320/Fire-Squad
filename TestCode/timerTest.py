# from clear code
import pygame, sys

pygame.init()
screen = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()


current_time = 0

button_press_time = 0
start_time = pygame.time.get_ticks()
set_round = True
round_start = 0


beggining_time = 300
round_time = 1000

can_fire = True
level = 100
firerate = 600

# 600 firerate
round = 0

while True:
    keys = pygame.key.get_pressed()  # code taken from I1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  # code taken from I2
            if event.key == pygame.K_LEFT:
                print("ye")
                if firerate < 1000:
                    firerate += level
                    print(firerate)
            if event.key == pygame.K_RIGHT:
                print("ye")
                if firerate > 0:
                    firerate -= level 
                    print(firerate)
    """if keys[pygame.K_UP]:
        print("ye")
        if firerate < 1000:
            firerate += level
            print(firerate)
    if keys[pygame.K_DOWN]:
        print("ye")
        if firerate > 0:
            firerate -= level 
            print(firerate)"""
    if keys[pygame.K_SPACE]:
        if can_fire:
            button_press_time = pygame.time.get_ticks()
            screen.fill((255, 255, 255))
            print("pow")
            can_fire = False
    

    current_time = pygame.time.get_ticks()

    if current_time - button_press_time > firerate:
        screen.fill((0, 0, 0))
        can_fire = True
        
    if current_time - start_time > round_time:
        if set_round:
            round_start = pygame.time.get_ticks()
            print("downtime over")
            set_round = False

    if current_time - round_start > round_time:
        if not set_round:
            round += 1
            print(f"rounds: {round}: now in down time")
            start_time = pygame.time.get_ticks()
            set_round = True



    #print(f"current time: {current_time} button press time: {button_press_time}")
    pygame.display.flip()
    clock.tick(60)
