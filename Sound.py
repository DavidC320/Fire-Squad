import pygame
from pygame import mixer
pygame.mixer.init()

class SoundCont(): 
    def __init__(self):  # based off of K3
        self.bullet = 'SFX\\146730__leszek-szary__shoot.wav'
        self.missle = 'SFX\\39031__wildweasel__dsglaun.wav'
        self.fire = 'SFX\\512469__michael-grinnell__laser-shot.wav'
        self.hit = 'SFX\\530486__rickplayer__metal-impact.mp3'
        self.warning = 'SFX\\365641__furbyguy__8-bit-alarm.wav'

    def bullet_sfx(self):
        bullet = mixer.Sound(self.bullet)
        bullet.play()

    def missle_sfx(self):
        missle = mixer.Sound(self.missle)
        missle.play()

    def fire_sfx(self):
        fire = mixer.Sound(self.fire)
        fire.set_volume(.25)
        fire.play()

    def hit_sfx(self):
        hit = mixer.Sound(self.hit)
        hit.play()

    def warning_sfx(self):
        warning = mixer.Sound(self.warning)
        warning.play()
