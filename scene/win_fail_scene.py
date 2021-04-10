import pygame
from pygame.constants import QUIT

from scene import SceneResult


class WinFailScene:
    def __init__(self,state):
        if state == SceneResult.Win:
            self.image = pygame.image.load("resource1/img/victory1.png")
        if state == SceneResult.Fail:
            self.image = pygame.image.load("resource1/img/defeat.png")

    def run(self,surface):
        clock = pygame.time.Clock()
        exit = False
        while not exit:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit = True

            surface.blit(self.image,(200,80))
            clock.tick(20)
            pygame.display.update()