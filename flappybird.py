import pygame
from pygame.surface import Surface
from pygame.tests.time_test import Clock


import Config
import sys

from World import World
from Bird import Bird
from PipePair import PipePair


def DrawPipes(pipes: list[PipePair], screen: Surface):
    for pipe in pipes:
        pipe.Draw(screen)


def MovePipes(pipes: list[PipePair]):
    for pipe in pipes:
        pipe.Move()


def BirdPipeCollided(bird: Bird, pipes: list[PipePair]):
    for pipe in pipes:
        if pipe.bottom_pipe.colliderect(bird.bird_position) or pipe.top_pipe.colliderect(bird.bird_position) or \
                bird.FloorTouched():
            return True
    return False


def main():
    pygame.init()

    screen: Surface = pygame.display.set_mode(Config.SCREEN_RES)
    clock: Clock = pygame.time.Clock()
    world: World = World()
    bird: Bird = Bird()
    game_active = False

    SPAWNPIPE: int = pygame.USEREVENT + 2
    spawnpipe_interval: int = Config.PIPE_SPAWNING_SPEED
    pygame.time.set_timer(SPAWNPIPE, spawnpipe_interval)
    pipe_list: list = []

    game_over = False

    while True:
        world.DrawBackground(screen)
        world.DrawFloor(screen)

        if len(pipe_list) > 3:
            pipe_list = pipe_list[1:]

        for event in pygame.event.get():
            if event.type == SPAWNPIPE and game_active:
                pipe_list.append(PipePair())
            elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN) and not game_over:
                flap = True in pygame.mouse.get_pressed(3) or event.key == pygame.K_SPACE
                if flap and not game_active:
                    game_active = True
                if flap and game_active:
                    bird.Flap()
                    print(pipe_list)

        if game_active:
            bird.Move()
            world.Move()
            MovePipes(pipe_list)

            if bird.FloorTouched():
                game_active = False
                game_over = True

        DrawPipes(pipe_list, screen)
        bird.Draw(screen)

        if BirdPipeCollided(bird, pipe_list):
            game_active = False
            game_over = True


        pygame.display.update()
        clock.tick(Config.GAME_FPS)


if __name__ == '__main__':
    main()
