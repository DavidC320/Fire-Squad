import pygame
from Settings import wn_width, wn_height
from Particles import Particle
from Music import MusicCont
# taken from H2


class Menu:
    def __init__(self, surface, clock):
        # init defining
        self.display_surface = surface
        self.clock = clock
        # timer
        # star stuff
        self.star_val = 100
        self.star_particle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.star_particle_timer, self.star_val)


        # star group
        self.starParticles = pygame.sprite.Group()

        # key info
        self.up_key, self.down_key, self.start_key, self.back_key = False, False, False, False
        self.startGame, self.startOptions, self.startCredits = False, False, False

        # msuic player
        self.m = MusicCont()

        # other variables
        self.wn_halfX = wn_width/2
        self.wn_halfY = wn_height/2

        # running check
        self.run_display = True

        # curser
        self.curser_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 180

        # font
        self.font_name = 'freesansbold.ttf'

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, "White")
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display_surface.blit(text_surface, text_rect)

    def draw_curser(self):
        self.draw_text('*', 20, self.curser_rect.x, self.curser_rect.y)

    def blit_screen(self):
        pygame.display.update()
        self.clock.tick(60)
        self.reset_keys()

    def reset_keys(self):  # code taken from H1
        self.up_key, self.down_key, self.start_key, self.back_key = False, False, False, False

    def check_events(self):
        # print('buh')
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                exit()
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_RETURN:
                    self.start_key = True
                elif events.key == pygame.K_BACKSPACE:
                    self.back_key = True
                elif events.key == pygame.K_DOWN or events.key == pygame.K_s:
                    self.down_key = True
                elif events.key == pygame.K_UP or events.key == pygame.K_w:
                    self.up_key = True
            if events.type == self.star_particle_timer:
                    star = Particle((self.wn_halfX, self.wn_halfY), .50, (0, 0), 6, "star", 0, pygame.time.get_ticks())
                    self.starParticles.add(star)
                    star = Particle((self.wn_halfX, self.wn_halfY), .50, (0, 0), 6, "star", 0, pygame.time.get_ticks())
                    self.starParticles.add(star)



class MainMenu(Menu):
    def __init__(self, surface, clock, class_ob):
        Menu.__init__(self, surface, clock)
        self.data_ob = class_ob

        # title image
        self.title_surf = pygame.image.load("GFX\gui\FireSquad.png").convert_alpha()
        self.title_rect = self.title_surf.get_rect(midtop=(wn_width/2, 50))

        # default state
        self.state = "Start"

        # button information
        self.startX, self.startY = self.wn_halfX, self.wn_halfY - 40
        self.optionsX, self.optionsY = self.wn_halfX, self.wn_halfY
        self.creditsX, self.creditsY = self.wn_halfX, self.wn_halfY + 40
        self.curser_rect.center = (self.startX + self.offset, self.startY)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            # checks
            self.check_events()
            self.check_input()

            # draws
            self.display_surface.fill("Black")

            # stars
            self.starParticles.draw(self.display_surface)
            self.starParticles.update((True, True, True, True), pygame.time.get_ticks())

            # text
            self.display_surface.blit(self.title_surf, self.title_rect)
            self.draw_text("Start Game", 50, self.startX, self.startY)
            self.draw_text("Options", 50, self.optionsX, self.optionsY)
            self.draw_text("Credits", 50, self.creditsX, self.creditsY)

            self.draw_curser()

            self.blit_screen()

    def move_cursor(self):  # menu selection thing
        if self.down_key:
            if self.state == "Start":
                self.curser_rect.center = (self.optionsX + self.offset, self.optionsY + 15 )
                self.state = 'Options'
            elif self.state == "Options":
                self.curser_rect.center = (self.creditsX + self.offset, self.creditsY + 15 )
                self.state = 'Credits'
            elif self.state == "Credits":
                self.curser_rect.center = (self.startX + self.offset, self.startY + 15 )
                self.state = 'Start'
        elif self.up_key:
            if self.state == "Start":
                self.curser_rect.center = (self.creditsX + self.offset, self.creditsY + 15 )
                self.state = 'Credits'
            elif self.state == "Options":
                self.curser_rect.center = (self.startX + self.offset, self.startY + 15 )
                self.state = 'Start'
            elif self.state == "Credits":
                self.curser_rect.center = (self.optionsX + self.offset, self.optionsY + 15 )
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.start_key:
            if self.state == 'Start':
                self.data_ob.start = True

            elif self.state == 'Options':
                print('this is not implemented, you have been sent to start menu')
                self.data_ob.start = True

            elif self.state == 'Credits':
                print('this is not implemented, you have been sent to start menu')
                self.data_ob.start = True
            self.run_display = False


class GameSelectMenu(Menu):
    def __init__(self, surface, clock, class_ob):
        Menu.__init__(self, surface, clock)
        self.data_ob = class_ob

        # default state
        self.state = "easy"
        self.difficulty = 0

        # button information
        self.easyX, self.easyY = self.wn_halfX, self.wn_halfY * 1.1
        self.normalX, self.normalY = self.wn_halfX, self.wn_halfY * 1.3
        self.hardX, self.hardY = self.wn_halfX, self.wn_halfY * 1.5
        self.veryHardX, self.veryHardY = self.wn_halfX, self.wn_halfY * 1.7
        self.deadManX, self.deadManY = self.wn_halfX, self.wn_halfY * 1.9
        self.curser_rect.center = (self.easyX + self.offset, self.easyY)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            # checks
            self.check_events()
            self.check_input()

            # draws
            self.display_surface.fill("Black")

            # stars
            self.starParticles.draw(self.display_surface)
            self.starParticles.update((True, True, True, True), pygame.time.get_ticks())

            # text
            self.draw_text("Difficulty select", 50, self.wn_halfX, self.wn_halfY * .2)
            self.draw_text("Easy", 50, self.easyX, self.easyY)
            self.draw_text("Normal", 50, self.normalX, self.normalY)
            self.draw_text("Hard", 50, self.hardX, self.hardY)
            self.draw_text("Very Hard", 50, self.veryHardX, self.veryHardY)
            self.draw_text("Dead Man", 50, self.deadManX, self.deadManY)

            self.draw_curser()

            self.blit_screen()

    def move_cursor(self):  # menu selection thing
        if self.down_key:
            if self.state == "easy":
                self.curser_rect.center = (self.normalX + self.offset, self.normalY + 15 )
                self.state = 'normal'
            elif self.state == "normal":
                self.curser_rect.center = (self.hardX + self.offset, self.hardY + 15 )
                self.state = 'hard'
            elif self.state == "hard":
                self.curser_rect.center = (self.veryHardX + self.offset, self.veryHardY + 15 )
                self.state = 'very hard'
            elif self.state == "very hard":
                self.curser_rect.center = (self.deadManX + self.offset, self.deadManY + 15 )
                self.state = 'dead man'
            elif self.state == "dead man":
                self.curser_rect.center = (self.easyX + self.offset, self.easyY + 15 )
                self.state = 'easy'
        elif self.up_key:
            if self.state == "easy":
                self.curser_rect.center = (self.deadManX + self.offset, self.deadManY + 15)
                self.state = 'dead man'
            elif self.state == "normal":
                self.curser_rect.center = (self.easyX + self.offset, self.easyY + 15)
                self.state = 'easy'
            elif self.state == "hard":
                self.curser_rect.center = (self.normalX + self.offset, self.normalY + 15)
                self.state = 'normal'
            elif self.state == "very hard":
                self.curser_rect.center = (self.hardX + self.offset, self.hardY + 15)
                self.state = 'hard'
            elif self.state == "dead man":
                self.curser_rect.center = (self.veryHardX + self.offset, self.veryHardY + 15)
                self.state = 'very hard'

    def check_input(self):
        self.move_cursor()
        if self.start_key:
            if self.state == 'easy':
                self.data_ob.difficulty = 0

            elif self.state == 'normal':
                self.data_ob.difficulty = 1

            elif self.state == 'hard':
                self.data_ob.difficulty = 2

            elif self.state == 'very hard':
                self.data_ob.difficulty = 3

            elif self.state == 'dead man':
                self.data_ob.difficulty = 4

            self.run_display = False
            self.data_ob.start = False
            self.data_ob.playing = True
            self.data_ob.game = True


class GameOver(Menu):
    def __init__(self, surface, clock, class_ob, player_data):
        Menu.__init__(self, surface, clock)
        self.player = player_data
        self.data_ob = class_ob

        # default state
        self.state = "restart"

        # button information
        self.restartX, self.restartY = self.wn_halfX, self.wn_halfY - 40
        self.quitX, self.quitY = self.wn_halfX, self.wn_halfY
        self.curser_rect.center = (self.restartX + self.offset, self.restartY)

    def display_menu(self):
        self.run_display = True
        self.m.gameoverMusic_player()
        while self.run_display:
            # checks
            self.check_events()
            self.check_input()

            # draws
            self.display_surface.fill("Black")

            # stars
            self.starParticles.draw(self.display_surface)
            self.starParticles.update((True, True, True, True), pygame.time.get_ticks())

            # text
            self.draw_text("Game over", 50, self.wn_halfX, self.wn_halfY * .2)
            self.draw_text("Restart", 50, self.restartX, self.restartY)
            self.draw_text("Quit", 50, self.quitX, self.quitY)

            self.draw_curser()

            self.blit_screen()

    def move_cursor(self):  # menu selection thing
        if self.down_key:
            if self.state == "restart":
                self.curser_rect.center = (self.quitX + self.offset, self.quitY + 15)
                self.state = 'quit'
            elif self.state == "quit":
                self.curser_rect.center = (self.restartX + self.offset, self.restartY + 15)
                self.state = 'restart'
        elif self.up_key:
            if self.state == "restart":
                self.curser_rect.center = (self.quitX + self.offset, self.quitY + 15)
                self.state = 'quit'
            elif self.state == "quit":
                self.curser_rect.center = (self.restartX + self.offset, self.restartY + 15)
                self.state = 'restart'

    def check_input(self):
        self.move_cursor()
        if self.start_key:
            if self.state == 'restart':
                self.data_ob.game = True

            elif self.state == 'quit':
                self.data_ob.playing = False
            self.run_display = False
            name = self.player.name
            score = self.player.score
            dif = self.player.score

