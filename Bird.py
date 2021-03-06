import pygame
from pygame.surface import Surface

import Config


class Bird:
    def __init__(self) -> None:
        self.bird_surface: Surface = self.GetBirdSurface()
        self.bird_position = self.bird_surface.get_rect(center=(Config.BIRD_X_POSITION, Config.SCREEN_HEIGHT / 2))
        self.movement = 0
        self.score = 0

    @staticmethod
    def GetBirdSurface(bird_image=Config.BIRD_YELLOW_MID_PATH):
        bird_surface: Surface = pygame.image.load(bird_image)
        bird_surface = pygame.transform.scale2x(bird_surface)

        return bird_surface

    def Draw(self, screen: Surface):
        screen.blit(self.bird_surface, self.bird_position)

    def Flap(self):
        self.movement = Config.BIRD_FLAP_STRENGTH
        self.PlaySound(Config.SOUND_WING_PATH)

    def Move(self):
        self.movement -= Config.GRAVITY
        self.bird_position = self.bird_surface.get_rect(
            center=(Config.BIRD_X_POSITION, self.bird_position.centery - self.movement))
        if self.bird_position.top < 0:
            self.movement = 0
            self.bird_position = self.bird_surface.get_rect(
                center=(Config.BIRD_X_POSITION, 0 + self.bird_position.height / 2))

        if self.movement > 2:
            self.bird_surface = self.GetBirdSurface(bird_image=Config.BIRD_YELLOW_DOWN_PATH)
        elif 2 > self.movement > -2:
            self.bird_surface = self.GetBirdSurface(bird_image=Config.BIRD_YELLOW_MID_PATH)
        else:
            self.bird_surface = self.GetBirdSurface(bird_image=Config.BIRD_YELLOW_UP_PATH)

    def FloorTouched(self):
        if self.bird_position.bottom > Config.SCREEN_HEIGHT - 85*2:
            # self.PlaySound(Config.SOUND_HIT_PATH)
            return True
        return False

    @staticmethod
    def PlaySound(sound):
        pygame.mixer.Sound(sound).play()
