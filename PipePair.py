import pygame
from pygame.surface import Surface
from random import randint

import Config


class PipePair:
    def __init__(self):
        self.surface: Surface = self.GetPipeSurface()
        self.pipe_gap: int = Config.PIPE_GAP
        self.center_middle: float = (Config.SCREEN_HEIGHT - 85*2)/2 + self.GetVariation()
        self.bottom_pipe = self.surface.get_rect(midtop=(Config.PIPE_SPAWN_X_POSITION, self.center_middle + self.pipe_gap/2))
        self.top_pipe = self.surface.get_rect(midbottom=(Config.PIPE_SPAWN_X_POSITION, self.center_middle + self.pipe_gap/2))
        self.passed_by_bird = False

    @staticmethod
    def GetPipeSurface():
        pipe_surface: Surface = pygame.image.load(Config.PIPE_GREEN_PATH)
        pipe_surface = pygame.transform.scale2x(pipe_surface)
        return pipe_surface

    @staticmethod
    def GetVariation():
        return randint(-Config.PIPE_HEIGHT_VARIATION/2, Config.PIPE_HEIGHT_VARIATION)

    def Draw(self, screen: Surface):
        screen.blit(self.surface, self.bottom_pipe)
        screen.blit(pygame.transform.flip(self.surface, False, True), self.top_pipe)

    def Move(self):
        self.bottom_pipe = self.surface.get_rect(midtop=(self.bottom_pipe.centerx - Config.PIPE_SPEED, self.center_middle + self.pipe_gap/2))
        self.top_pipe = self.surface.get_rect(midbottom=(self.top_pipe.centerx - Config.PIPE_SPEED, self.center_middle - self.pipe_gap/2))
