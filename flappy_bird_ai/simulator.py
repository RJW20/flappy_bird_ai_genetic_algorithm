from .player import Player


def simulate(player: Player) -> Player:
    """Assign the player its fitness.
    
    Run the player in its environment and then calculate it's and assign it.
    """

    player.start_state()

    fitness = 0     #fitness is just the number of frames alive for
    while not player.is_dead:
        player.look()
        move = player.think()
        player.move(move)

        fitness += 1

        if player.score == 2000:
            break

    player.best_score = player.score
    player.fitness = fitness
    return player