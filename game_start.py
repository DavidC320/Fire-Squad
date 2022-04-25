import pygame  
from Settings import wn_height, wn_width
from Game import GamePlay
from Music import MusicCont
from Menu import MainMenu, GameSelectMenu, GameOver
from Player import Player_info
# Version Beta 4.1.3
# David Cruz


class FireSquad:
    def __init__(self):
        # pygame stuff I think
        self.screen = pygame.display.set_mode((wn_width, wn_height))
        self.clock = pygame.time.Clock()

        self.running = True
        self.difficulty = None

        # Player information class
        player_info = Player_info()

        # game state classes
        self.mus = MusicCont()
        self.g = GamePlay(self.screen, self.clock, player_info)  # the actual game
        self.go = GameOver(self.screen, self.clock, self, player_info)
        self.m = MainMenu(self.screen, self.clock, self)
        self.s = GameSelectMenu(self.screen, self.clock, self)

        # game bool controller
        self.playing = False  # this is for when the game itself is running
        self.game = False
        self.start = False
        self.option = False
        self.credits = False

    def start_game(self):
        self.running = True
        self.mus.menuMusic_player()
        while self.running:
            if self.playing:
                if self.game:
                    self.g.difficulty_set(self.difficulty)
                    self.game = self.g.play()
                else:
                    self.go.display_menu()   
                    self.g.restart()
            else:
                if self.start:
                    self.s.display_menu()
                elif self.option:
                    pass
                elif self.credits:
                    pass
                else:  # starting menua
                    self.m.display_menu()

pygame.init()
screen = pygame.display.set_mode((wn_width, wn_height))
pygame.display.set_caption('Fire Squad')

fire_squad = FireSquad()

if __name__ == "__main__":
    fire_squad.start_game()
