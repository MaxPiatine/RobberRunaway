"""
This module loads, configures and runs the main game.
"""

from game import Game
from actors import *
from typing import List
import random

icon = pygame.image.load("../images/thief.png")
pygame.display.set_icon(icon)


def load_map(filename: str) -> List[List[str]]:
    """
    Load the map data from the given filename and return as a list of lists.
    """

    with open(filename) as f:
        map_data = [line.split() for line in f]
    return map_data

if __name__ == "__main__":

    data = load_map("../data/final_maze.txt") # Set the filename where maze data is

    width = len(data[0])
    height = len(data)

    game = Game(width, height)
    player, chaser_1 = None, None

    #initialzing the map and icons in the game from the given file
    for i in range(len(data)):
        for j in range(len(data[i])):
            key = data[i][j]
            if key == 'P':
                player = Player("../images/thief.png", j, i)
            elif key == 'C':
                chaser_1 = Chaser("../images/police-car.png", j, i)
            elif key == 'X':
                game.add_actor(Wall("../images/wall-24.png", j, i))
        


    game.set_player(player)
    game.add_actor(player)
    game.add_actor(chaser_1)
    game.goal_stars = 10
    #setting the number of stars needed to win the game
    num_stars = 0
    while num_stars < 10:
        x = random.randrange(game.stage_width)
        y = random.randrange(game.stage_height)
        if game.get_actor(x,y) == None:
            game.add_actor(Star("../images/money.png", x, y))
            num_stars += 1



    game.on_execute()

