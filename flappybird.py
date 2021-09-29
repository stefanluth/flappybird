import pygame
from pygame.surface import Surface
from pygame.tests.time_test import Clock
from pygame.font import Font
from time import sleep

import Config
import sys

from World import World
from Bird import Bird
from PipePair import PipePair


def DrawPipes(pipes: list[PipePair], screen: Surface):
    for pipe in pipes:
        pipe.Draw(screen)


def MovePipes(pipes: list[PipePair], bird: Bird):
    for pipe in pipes:
        pipe.Move()
        if not pipe.passed_by_bird and pipe.bottom_pipe.centerx < bird.bird_position.left:
            pipe.passed_by_bird = True
            bird.score += 1
            bird.PlaySound(Config.SOUND_POINT_PATH)


def BirdCollided(bird: Bird, pipes: list[PipePair]):
    for pipe in pipes:
        if pipe.bottom_pipe.colliderect(bird.bird_position) or \
                pipe.top_pipe.colliderect(bird.bird_position):
            return True
    return False


def DisplayScore(screen: Surface, score: int, game_font: Font):
    score_text = game_font.render(f'{score}', True, (255, 255, 255))
    screen.blit(score_text, (25, 25))


def DisplayHighScore(screen: Surface, high_score: int, game_font: Font):
    high_score_text = game_font.render(f'Highscore: {high_score}', True, (255, 255, 255))
    screen.blit(high_score_text, (25, 25))


def main():
    pygame.init()

    screen: Surface = pygame.display.set_mode(Config.SCREEN_RES)
    pygame.display.set_caption('FlappyBird')
    clock: Clock = pygame.time.Clock()
    world: World = World()
    bird: Bird = Bird()
    font: Font = Font(Config.FONT_PATH, 72)

    SPAWNPIPE: int = pygame.USEREVENT + 2
    spawnpipe_interval: int = Config.PIPE_SPAWNING_SPEED
    pygame.time.set_timer(SPAWNPIPE, spawnpipe_interval)
    pipe_list: list = []

    game_over_surface: Surface = pygame.image.load(Config.GAME_OVER_PATH)
    game_over_surface = pygame.transform.scale2x(game_over_surface)
    game_over_rect = game_over_surface.get_rect(center=(Config.SCREEN_WIDTH/2, Config.SCREEN_HEIGHT/2))

    game_over = False
    game_active = False
    high_score = 0

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
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                flap = True in pygame.mouse.get_pressed(3) or event.key == pygame.K_SPACE
                if flap and not game_active:
                    game_active = True
                    game_over = False
                    pipe_list = []
                    bird = Bird()
                if flap and game_active:
                    bird.Flap()

        if game_active:
            bird.Move()
            world.Move()
            MovePipes(pipe_list, bird)

        DrawPipes(pipe_list, screen)
        bird.Draw(screen)

        if bird.score > high_score:
            high_score = bird.score

        if game_active and not game_over and (BirdCollided(bird, pipe_list) or bird.FloorTouched()):
            bird.PlaySound(Config.SOUND_HIT_PATH)
            game_active = False
            game_over = True

        if not game_active or game_over:
            screen.blit(game_over_surface, game_over_rect)
            if high_score > 0:
                DisplayHighScore(screen, high_score, font)
        else:
            DisplayScore(screen, bird.score, font)

        pygame.display.update()
        clock.tick(Config.GAME_FPS)


if __name__ == '__main__':
    main()
