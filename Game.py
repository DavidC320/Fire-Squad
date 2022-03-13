import pygame
from random import choices, randint
from Cursor import CursorControl
from SpaceCont import SpaceController
from Particles import Particle
from Enemy import Enemy
from Music import MusicCont
from Sound import SoundCont
from Settings import enemy_name, enemy_weight, wn_width, wn_height, z_max, rangers, projectiles

class GamePlay:
    def __init__(self, surface, clock):

        # init setting
        self.display_surface = surface
        self.running, self.playing = True, True
        self.clock = clock

        ########################## Timers #################################

        # timers
        # Star timer
        self.star_val = 0
        self.star_particle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.star_particle_timer, self.star_val)
        
        # Enemy timer
        self.enemyTimerValue = 0
        self.enemy_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer, self.enemyTimerValue)

        # Round timer
        self.round_length = 60000
        self.round_start_time = 0

        # Down time timer
        self.down_time_length = 2000
        self.down_time_start_time = 0  # The time when down time starts

        # Firerate timer
        self.firerate = 500  # defualt firerate, not too slow, not too fast
        self.button_press_time = 0

        ###################### Game Variables #############################

        # Difficulty stuff
        self.enemySpeed = None
        self.playerSpeed = None
        self.playerHealth = None

        # Player stuff
        self.credits = 0
        self.score = 0
        self.warning = False
        self.can_fire = True
        self.player_size = pygame.Rect((wn_width/2)-(527/2), 129 ,527, 356)  # code from k1 and k2

        # player firing atributes
        self.damage = 1

        # Round stuff
        self.in_round = False
        self.rounds = 0


        ###################### Display things #############################

        # Player ship
        self.game_ship_gui = pygame.image.load("GFX\\gui\\gameGui\\ShipBackGround0.2.png")
        
        # Player aim
        self.pointer = CursorControl()
        self.cursor = pygame.sprite.GroupSingle()
        self.cursor.add(self.pointer)
        self.mouse_position = (0, 0)

        # Space Controller
        self.space = SpaceController()

        # Particle group
        self.starParticles = pygame.sprite.Group()

        # Player bullet group
        self.playerBulletGroup = pygame.sprite.Group()

        # Enemy group
        self.enemyGroup = pygame.sprite.Group()  # Enemy bullets also go here
        self.test_group = list()

        # Music controller
        self.music_player = MusicCont()
        # Sound controller
        self.sound_player = SoundCont()

        # Fonts // code taken from C1
        self.font = pygame.font.Font(None, 50)
        self.score_font = pygame.font.Font(None, 35)

        # Text
        # Warning text
        self.warning_surface = self.font.render('WARNING!', True, 'Yellow')
        self.warning_rect = self.warning_surface.get_rect(center=(wn_width / 2, wn_height / 1.2))
        
    def play(self):
        self.down_time_start_time = pygame.time.get_ticks()
        self.running = True
        while self.running:
            self.check_events()

            ###################### Display things #############################

            # Display stuff
            self.display_surface.fill((0, 11, 26))

            # Space
            self.space.update(self.playerSpeed)

            # Stars
            self.starParticles.draw(self.display_surface)
            self.starParticles.update(self.space.lock_config, pygame.time.get_ticks())

            # Enemies
            if self.in_round:
                self.enemyGroup.draw(self.display_surface)
                self.enemyGroup.update(self.space.lock_config, self.current_time)

            # Cursor
            self.cursor.update(self.mouse_position)
            self.cursor.draw(self.display_surface)

            # Player Ship
            self.display_surface.blit(self.game_ship_gui, (0, 0))

            # health text
            if self.playerHealth > 0:
                self.health_surface = self.font.render(f'Health: {self.playerHealth}', True, 'Red')
                self.health_rect = self.health_surface.get_rect(center=(wn_width / 2, wn_height / 1.06))
                self.display_surface.blit(self.health_surface, self.health_rect)

            # player rect display
            pygame.draw.rect(self.display_surface, "Red", self.player_size, 2)
            
            # Score text
            self.score_surface = self.font.render(f'Score:', True, 'Black')
            self.score_rect = self.health_surface.get_rect(center=(wn_width * .15, wn_height * .06))
            self.display_surface.blit(self.score_surface, self.score_rect)

            self.score_surface = self.score_font.render(f'{self.score}', True, 'Black')
            self.score_rect = self.health_surface.get_rect(center=(wn_width * .15, wn_height * .15))
            self.display_surface.blit(self.score_surface, self.score_rect)

            # rounds
            self.round_surface = self.font.render(f"rounds: {self.rounds}", True, "Black")
            self.round_rect = self.round_surface.get_rect(midtop=(wn_width/2, 10))
            self.display_surface.blit(self.round_surface, self.round_rect)

            if self.in_round:
                self.round_surface = self.font.render(f"time: {int((self.current_time - self.round_start_time)/1000)}", True, "Black")
                self.round_rect = self.round_surface.get_rect(midtop=(wn_width/2, 60))
                self.display_surface.blit(self.round_surface, self.round_rect)
            else:
                self.round_surface = self.font.render(f"Break", True, "Black")
                self.round_rect = self.round_surface.get_rect(midtop=(wn_width/2, 60))
                self.display_surface.blit(self.round_surface, self.round_rect)

            # Warning text
            if self.warning:
                # code taken from C1
                self.display_surface.blit(self.warning_surface, self.warning_rect)

            pygame.display.update()
            self.clock.tick(60)
        return False

    def check_events(self):

        self.current_time = pygame.time.get_ticks()  # gets the current time

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                exit()
            if events.type == pygame.MOUSEMOTION:  # This is taken from A1
                self.mouse_position = pygame.mouse.get_pos()

            if self.playing:

                ############################### Timers ###############################

                if events.type == self.star_particle_timer:
                    star = Particle((self.space.spawn_x, self.space.spawn_y), .50, (0, 0), self.playerSpeed, "star", 0, pygame.time.get_ticks())
                    self.starParticles.add(star)

                if self.in_round:
                    if events.type == self.enemy_timer:
                        if len(self.enemyGroup) <= 199:
                            enemy_type = choices(enemy_name, weights=enemy_weight, k=1)  # taken from D3
                            enemy = Enemy(*enemy_type, 0.05, (self.space.spawn_x, self.space.spawn_y), self.enemySpeed, self.current_time)
                            # taken from D4 // * symbol gets rid of the []
                            self.enemyGroup.add(enemy)
                            self.reorganize_group()
                            # print(self.test_group)
                        self.ranger_fire()

                elif len(self.enemyGroup) >= 1:
                    self.enemyGroup.empty()

                if self.current_time - self.button_press_time > self.firerate:
                    self.can_fire = True

                if self.current_time - self.down_time_start_time > self.down_time_length:
                    if not self.in_round:
                        self.round_start_time = pygame.time.get_ticks()
                        self.in_round = True
                        self.music_player.gameMusic_player()

                if self.in_round:
                    if self.current_time - self.round_start_time > self.round_length:
                        self.rounds += 1
                        self.down_time_start_time = pygame.time.get_ticks()
                        self.in_round = False

                ########################### miscilanious ###########################

                if self.in_round:
                    if pygame.mouse.get_pressed()[0]:
                        if self.can_fire:
                            self.sound_player.fire_sfx()

                        for enemy in self.enemyGroup:
                            if enemy.ship_type != "bullet":
                                if self.can_fire:
                                    self.button_press_time = pygame.time.get_ticks()
                                    if enemy.rect.colliderect(self.cursor.sprite.rect):
                                        enemy.health -= self.damage
                                        if enemy.health <= 0:
                                            self.score += enemy.score_points
                                            enemy.kill()
                        self.can_fire = False  # turns off firing until the ship auto reloads

                    self.enemy_collide_with_player()

                if self.playerHealth <= 0:
                    self.enemyGroup.empty()
                    self.starParticles.empty()
                    self.running = False

    def enemy_collide_with_player(self):
        if len(self.enemyGroup) > 0:
            for enemy in self.enemyGroup:
                if enemy.ship_type in projectiles:  # Projectile collide check
                    if enemy.rect.colliderect(self.player_size):
                        if enemy.z > z_max * .8:
                            if enemy.z >= z_max:
                                self.sound_player.hit_sfx()
                                self.playerHealth -= enemy.damage
                                enemy.kill()
                            self.warning = True
                    else:
                        if enemy.z >= z_max:
                            enemy.kill()
                        self.warning = False
                elif enemy.ship_type in enemy_name:  # Enemy collide check
                    if enemy.z > z_max * .8:
                        if enemy.z >= z_max:
                            self.sound_player.hit_sfx()
                            self.playerHealth -= enemy.damage
                            enemy.kill()
                        self.warning = True

                else:
                    self.warning = False

        else:
            self.warning = False
    


    def ranger_fire(self):
        # checks of the enemy is a ranger (shooters and launchers). if thefy are then see if they can fire. if so, activate a the enemies fire timer and check every cycle
        # if the timer has been reached and shoot
        if len(self.enemyGroup) >= 1:
            for enemy_ship in self.enemyGroup:
                ship_type = enemy_ship.ship_type
                if ship_type in rangers:
                    state = enemy_ship.can_fire
                    if state:
                        if self.current_time - enemy_ship.last_fire > 2500:
                            fire_chance = randint(0, 3)
                            if fire_chance == 0:
                                if ship_type == "shooter":
                                    self.sound_player.bullet_sfx()
                                    spawn_posi = (enemy_ship.x, enemy_ship.y)
                                    enemy = Enemy("bullet", 1, spawn_posi, self.enemySpeed, self.current_time)
                                    self.enemyGroup.add(enemy)
                                    self.reorganize_group()

                                elif ship_type == "launcher":
                                    self.sound_player.missle_sfx()
                                    spawn_posi = (enemy_ship.x, enemy_ship.y)
                                    enemy = Enemy("missle", 1, spawn_posi, self.enemySpeed, self.current_time)
                                    self.enemyGroup.add(enemy)
                                    self.reorganize_group()
                            enemy_ship.last_fire = self.current_time
                    else:
                        enemy_ship.last_fire = self.current_time


    def reorganize_group(self):  # this is a very import ant funttion
        reorganize = []
        if len(self.enemyGroup) >= 1:  # checks if there are any sprites in the group. if not then just ignore the rest
            for enemy in self.enemyGroup:
                info = [enemy, enemy.z]
                reorganize.append(info)
                """
                This takes the enemy sprite out of the group alon with extracting the enemies z data to be used to
                reorganize it later down"""
            self.enemyGroup.empty()  # this needs to be empty so there is no duplicates.
            # code from F1-3
            reorganize = sorted(reorganize, key=lambda k: float(k[1]))  # major thanks to G1-2
            # reorganize.sort(reverse=True, key=lambda k: float(k[1])) // I thought I needed this but no.
            for enemy in reorganize:  # Final, reading all the sprites back in after reorganization.
                self.enemyGroup.add(enemy[0])
        """
        For those who think this is worthless code and I could have done it a different way... no, no I could not.
        I needed a system to constantly check where an enemy is on the z coordinate and have pygame render it according
        to that. 'You could have used Ordered updates.' I couldn't due to ordered updates being based off of what was 
        added first and not a value."""

    def difficulty_set(self, difficulty):
        if difficulty == 0:
            self.enemySpeed = 4
            self.playerSpeed = 3
            self.playerHealth = 5
            star_val = 500
            enemy_timer_value = 200
        elif difficulty == 1:
            self.enemySpeed = 4
            self.playerSpeed = 5 
            self.playerHealth = 4
            star_val = 400
            enemy_timer_value = 400
        elif difficulty == 2:
            self.enemySpeed = 9
            self.playerSpeed = 7
            self.playerHealth = 3
            star_val = 200
            enemy_timer_value = 500
        elif difficulty == 3:
            self.enemySpeed = 7
            self.playerSpeed = 5
            self.playerHealth = 2
            star_val = 400
            enemy_timer_value = 400
        elif difficulty == 4:
            self.enemySpeed = 7
            self.playerSpeed = 3
            self.playerHealth = 1
            star_val = 200 
            enemy_timer_value = 400
        else:
            self.enemySpeed = 0
            self.playerSpeed = 4
            self.playerHealth = 20
            star_val = 600
            enemy_timer_value = 200

        #print(f"{self.enemySpeed}\n{self.playerSpeed}\n{self.playerHealth}")

        # sets the timer
        pygame.time.set_timer(self.enemy_timer, enemy_timer_value)
        pygame.time.set_timer(self.star_particle_timer, star_val)

    def restart(self):
        self.space.spawn_x = wn_width/2
        self.space.spawn_y = wn_height/2
        self.button_press_time = 0
        self.down_time_start_time = 0
        self.round_start_time = 0
        self.in_round = False
        self.rounds = 0
        self.credits = 0
        self.score = 0
        self.warning = False
        self.can_fire = True
