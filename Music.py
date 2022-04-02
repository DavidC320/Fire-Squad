import pygame
from pygame import mixer
from random import randint
pygame.mixer.init()

class MusicCont(): 
    def __init__(self):
        # list based off of j1
        self.gameMusic = (
            "Playlist\\game\\71075.mid",
            "Playlist\\game\\celes2.mid",
            "Playlist\\game\\Born-To-Be-Alive-1.mid",
            "Playlist\\game\\Strange-Kind-Of-Woman.mid", 
            ################# 4.0.0 #################
            "Playlist\\game\\Absolute - Dream Odyssey.mid",
            "Playlist\\game\\Bad_Religion_-_A_Walk.mid",
            "Playlist\\game\\Human3gm.mid",
            ################# 4.0.6 #################
            "Playlist\\game\\chatanoogachoo.mid",
            "Playlist\\game\\ss9th11.mid"
            )
        self.menuMusic = "Playlist\\title\\Lemon & Einar K - Anticipation (Original Mix).mid"
        self.gameoverMusic = (
            "Playlist\\gameover\\73561_08.mid.mid",
            ################# 4.0.0 #################
            "Playlist\\gameover\\La-Cathedrale-Engloutie.mid",
            "Playlist\\gameover\\Never-Gonna-Give-You-Up-3.mid",
            "Playlist\\gameover\\Skies of Arcadia - Tension Theme.mid",
            "Playlist\\gameover\\zeal.mid",
            ################# 4.0.6 #################
            "Playlist\\gameover\\Notorious BIG - Notorious Thugs.mid"
        )
        self.bossMusic = (
            "Playlist\\Boss\\amunet-prime.mp3",
            "Playlist\\Boss\\Berlin_-_The_Metro.mid",
            "Playlist\\Boss\\Demoiselle_Dner_-_09_-_YM_I_Y.mp3",
            "Playlist\\Boss\\GILLESPIE.Night in Tunisia.mid",
            "Playlist\\Boss\\HEAVY.MID",
            "Playlist\\Boss\\Komiku_-_35_-_The_True_Last_Boss.mp3",
            "Playlist\\Boss\\kylie_minogue-confide_in_me.mid",
            "Playlist\\Boss\\pink-most_girls.mid"

        )

    def gameMusic_player(self):
        music_pic = randint(0, len(self.gameMusic) - 1)
        music = self.gameMusic[music_pic]
        mixer.music.stop()
        mixer.music.load(music)
        mixer.music.play(-1)
        pygame.mixer.music.set_volume(1)  # code taken from j2

    def bossMusic_player(self):
        music_pic = randint(0, len(self.bossMusic) - 1)
        music = self.bossMusic[music_pic]
        mixer.music.stop()
        mixer.music.load(music)
        mixer.music.play(-1)
        pygame.mixer.music.set_volume(1)

    def menuMusic_player(self):
        mixer.music.stop()
        mixer.music.load(self.menuMusic)
        mixer.music.play(-1)
        pygame.mixer.music.set_volume(.5)

    def gameoverMusic_player(self):
        music_pic = randint(0, len(self.gameoverMusic) - 1)
        music = self.gameoverMusic[music_pic]
        mixer.music.stop()
        mixer.music.load(music)
        mixer.music.play(-1)
        pygame.mixer.music.set_volume(1.5)

    def stopMusic_player(self):
        mixer.music.stop()
