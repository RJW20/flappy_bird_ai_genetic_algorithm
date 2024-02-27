from .player import Player


def simulate(player: Player) -> Player:
    """Assign the player its fitness.
    
    Run the player in its environment dependent on simulation_settings.
    Collect stats and then calculate the fitness of the player and assign it.
    """

    player.start_state()

    fitness = 0     #fitness is just the number of frames alive for
    while not player.is_dead:
        player.look()
        move = player.think()
        player.move(move)

        fitness += 1

    player.fitness = fitness
    return player