import random

import pygame
from pygame.surface import Surface

import Config


class World:
    def __init__(self) -> None:
        self.floor_surface: Surface = self.GetFloorSurface()
        self.background_surface: Surface = self.GetBackgroundSurface()
        self.threshold = Config.SCREEN_WIDTH
        self.background_x_position = 0
        self.floor_x_position = 0

    @staticmethod
    def GetFloorSurface() -> Surface:
        floor_surface: Surface = pygame.image.load(Config.FLOOR_PATH).convert()
        floor_surface = pygame.transform.scale2x(floor_surface)

        return floor_surface

    @staticmethod
    def GetBackgroundSurface() -> Surface:
        background_surface: Surface = pygame.image.load(
            random.choice([Config.BACKGROUND_DAY_PATH, Config.BACKGROUND_NIGHT_PATH])).convert()
        background_surface = pygame.transform.scale2x(background_surface)

        return background_surface

    def DrawBackground(self, screen: Surface) -> None:
        screen.blit(self.background_surface, (self.background_x_position, 0))
        screen.blit(self.background_surface, (506 + self.background_x_position, 0))

    def DrawFloor(self, screen: Surface) -> None:
        floor_y_position = Config.SCREEN_HEIGHT - self.floor_surface.get_height()
        screen.blit(self.floor_surface, (self.floor_x_position, floor_y_position))
        screen.blit(self.floor_surface, (506 + self.floor_x_position, floor_y_position))

    def Move(self):
        self.floor_x_position -= Config.FLOOR_SPEED
        if self.floor_x_position < -506:
            self.floor_x_position += 506

        self.background_x_position -= Config.BACKGROUND_SPEED
        if self.background_x_position < -506:
            self.background_x_position += 506
