from typing import Iterable, Any
import random

import pygame
import numpy as np

import flappy_bird_app.bird as BIRD
import flappy_bird_app.pipe as PIPE
from flappy_bird_app.pipe import Pipe
from flappy_bird_app.pipes import Pipes, INTERVAL
from genetic_algorithm import Population
from .player import Player
from .settings import genetic_algorithm_settings


##bind settings to variables
population_size = genetic_algorithm_settings['population_size']
total_generations = genetic_algorithm_settings['total_generations']
history_folder = genetic_algorithm_settings['history_folder']
history_type = genetic_algorithm_settings['history_type']
history_value = genetic_algorithm_settings['history_value']


def custom_cycle(items: Iterable[Any], count: int) -> Any:
    """Performs like itertools.cycle except yields each element count times."""

    saved = []
    for item in items:
        for _ in range(count):
            yield item
        saved.append(item)
    while saved:
        for item in saved:
            for _ in range(count):
                yield item


def playback() -> None:
    """Show playback of the result of running the genetic algorithm on Flappy Bird.
    
    Do not alter settings.py between running the genetic algorithm and running this.
    Switch between generations with the left and right arrow keys.
    Slow down up or speed up the playback with the j and k keys.
    """

    #pygame setup
    width = 480
    game_height = 620
    floor_height = 0.04 * game_height
    screen = pygame.display.set_mode((width, game_height + floor_height))
    pygame.display.set_caption("Flappy Bird")
    pygame.font.init()
    font_height = int(0.06 * game_height)
    score_font = pygame.font.Font(pygame.font.get_default_font(), font_height)
    stats_font = pygame.font.Font(pygame.font.get_default_font(), int(0.7 * font_height))
    clock = pygame.time.Clock()
    running = True

    #initialise sprites
    bg = pygame.image.load('./flappy_bird_app/resources/background.bmp')
    bg = pygame.transform.scale(bg, (width, game_height))
    bird_sprites = [pygame.image.load('./flappy_bird_app/resources/bird_1.bmp'), pygame.image.load('./flappy_bird_app/resources/bird_2.bmp'), pygame.image.load('./flappy_bird_app/resources/bird_3.bmp')]
    bird_sprites = [pygame.transform.scale(bird_sprite, (BIRD.RADIUS * 8/3 * game_height, BIRD.RADIUS * 2 * game_height)) for bird_sprite in bird_sprites]
    bird_sprite_numbers = custom_cycle([0, 1, 2, 1], 5)
    pipe_top_sprite = pygame.image.load('./flappy_bird_app/resources/pipe_top.bmp')
    pipe_bottom_sprite = pygame.image.load('./flappy_bird_app/resources/pipe_bottom.bmp')
    pipe_top_sprite = pygame.transform.scale(pipe_top_sprite, (PIPE.WIDTH * width, (1 - PIPE.MIN_HEIGHT - PIPE.GAP) * game_height))
    pipe_bottom_sprite = pygame.transform.scale(pipe_bottom_sprite, (PIPE.WIDTH * width, (1 - PIPE.MIN_HEIGHT - PIPE.GAP) * game_height))
    floor_sprite = pygame.image.load('./flappy_bird_app/resources/floor.bmp')
    floor_sprite = pygame.transform.scale(floor_sprite, (width, floor_height))
    floor_rect = floor_sprite.get_rect(topleft=(0,game_height))

    #intialize the playback population
    playback_pop = PlaybackPopulation(history_folder=history_folder, 
                                      history_type=history_type,
                                      history_value=history_value, 
                                      og_pop_size=population_size,
                                      total_generations=total_generations)
    
    #get and start the first birds
    birds = playback_pop.current_players
    seed = random.randint(0,100)
    for bird in birds:
        bird.pipes = PlaybackPipes(seed)
        bird.start_state()

    base_speed = 60
    speed_multiplier = 1

    while running:
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            #handle key presses
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT and playback_pop.current_generation != total_generations:
                    playback_pop.current_generation += 1
                    if not playback_pop.is_champs:
                        playback_pop.new_gen(playback_pop.current_generation)
                    birds = playback_pop.current_players
                    seed = random.randint(0,100)
                    for bird in birds:
                        bird.pipes = PlaybackPipes(seed)
                        bird.start_state()
                    
                elif event.key == pygame.K_LEFT and playback_pop.current_generation != 1:
                    playback_pop.current_generation -= 1
                    if not playback_pop.is_champs:
                        playback_pop.new_gen(playback_pop.current_generation)
                    birds = playback_pop.current_players
                    seed = random.randint(0,100)
                    for bird in birds:
                        bird.pipes = PlaybackPipes(seed)
                        bird.start_state()

                elif event.key == pygame.K_j:
                    speed_multiplier = max(1, speed_multiplier // 2)
                elif event.key == pygame.K_k:
                    speed_multiplier *= 2

        #move all birds
        for bird in birds:
            bird.look()
            move = bird.think()
            bird.move(move)

            #remove any that have died
            if bird.is_dead:
                birds.remove(bird)

        #restart them if all are dead
        if len(birds) == 0:
            birds = playback_pop.current_players
            seed = random.randint(0,100)
            for bird in birds:
                bird.pipes = PlaybackPipes(seed)
                bird.start_state()

        #fill the screen to wipe last frame
        screen.blit(bg, (0,0))

        #draw the pipes
        for item in birds[0].pipes.items:
            pipe_top_rect = pipe_top_sprite.get_rect(bottomleft=(item.position * width, item.height * game_height))
            pipe_bottom_rect = pipe_bottom_sprite.get_rect(topleft=(item.position * width, item.bottom_height * game_height))
            screen.blit(pipe_top_sprite, pipe_top_rect)
            screen.blit(pipe_bottom_sprite, pipe_bottom_rect)

        #draw the birds
        for bird in birds:
            sprite_id = next(bird_sprite_numbers)
            bird_sprite_rotated = pygame.transform.rotate(bird_sprites[sprite_id], bird.angle)
            bird_sprite_rect = bird_sprite_rotated.get_rect(center=(bird.x * width, bird.position * game_height))
            screen.blit(bird_sprite_rotated, bird_sprite_rect)

        #draw the floor
        screen.blit(floor_sprite, floor_rect)

        #show the score (all remaining will have the same score)
        score = score_font.render(f'{birds[-1].score}', True, 'white')
        score_rect = score.get_rect(center=(width/2, 0.05 * game_height))
        screen.blit(score, score_rect)
                    
        #show the gen
        gen = stats_font.render(f'Gen: {playback_pop.current_generation}', True, 'white')
        gen_rect = gen.get_rect(topleft=(0.05 * width, 0.03 * game_height))
        screen.blit(gen, gen_rect)

        #show the speed
        speed = stats_font.render(f'Speed: {speed_multiplier}x', True, 'white')
        speed_rect = speed.get_rect(topright=(0.95 * width, 0.03 * game_height))
        screen.blit(speed, speed_rect)

        #display the changes
        pygame.display.flip()
        
        #advance to next frame at chosen speed
        clock.tick(base_speed * speed_multiplier)

    pygame.quit()


class PlaybackPipes(Pipes):
    """Extension of Population class which overloads the generation of new pipes
    and sets a seed for generating their height."""

    def __init__(self, seed:int) -> None:
        super(PlaybackPipes, self).__init__()
        self.generator = np.random.RandomState(seed)

    def start_state(self) -> None:
        super().start_state()
        self.items[0].height = round(self.generator.uniform(PIPE.MIN_HEIGHT, 1 - PIPE.MIN_HEIGHT - PIPE.GAP) * 100) / 100

    def update(self) -> None:
        """Overload Pipes.update, appending pipes with height generated from a seed."""

        for pipe in self.items:
            pipe.update()

        if (end_pipe_position := self.items[-1].position) < 1:
            new_pipe = Pipe(end_pipe_position + INTERVAL)
            new_pipe.height = round(self.generator.uniform(PIPE.MIN_HEIGHT, 1 - PIPE.MIN_HEIGHT - PIPE.GAP) * 100) / 100
            self.items.append(new_pipe)

        if self.items[0].position < self.items[0].width * -1:
            self.items.popleft()   


class PlaybackPopulation(Population):
    """Extension of Population class with methods allowing us to manipulate
    which genomes are loaded.

    Will determine its own size and automatically load the first genomes.
    """

    def __init__(self, 
                 history_folder: str,
                 history_type: str, 
                 history_value: int, 
                 og_pop_size: int, 
                 total_generations: int,
                 ) -> None:
        
        self.folder = history_folder
        self.current_generation = 1

        self.is_champs = False
        match(history_type):
            case('none'):
                raise Exception('No history was saved during evolution. If you would like ' + \
                                'to view playback, please adjust history settings and run again.')
            case('champ'):
                pop_size = total_generations
                self.is_champs = True
            case('absolute'):
                pop_size = history_value
            case('percentage'):
                pop_size = int(og_pop_size * history_value)
            case('entire'):
                pop_size = og_pop_size
            case _:
                raise Exception(f'Invalid history type {history_type}')
        self.size = pop_size
        self.players = [Player() for _ in range(pop_size)]

        if self.is_champs:
            self.load(history_folder)   #load all champs
        else:
            self.new_gen()              #load just the first gen

    def new_gen(self, gen_id: int = 1) -> None:
        """Load generation {gen_id}.
        
        Sets self.current_generation to gen_id.
        """

        self.load(f'{history_folder}/{gen_id}')
        self.current_generation = gen_id

    @property
    def current_players(self) -> list[Player]:
        """Return the players we're currently playing back."""

        if self.is_champs:
            return self.players[self.current_generation - 1:self.current_generation]
        else:
            return self.players[:]