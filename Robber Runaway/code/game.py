from __future__ import annotations
from typing import Optional
from actors import *
import pygame

class Game:
    """
    This class represents the main game.
    === Public Attributes ===
    stage_width:
        int representing the width of the stage

    stage_length:
        in representing the length of the stage

    size:
        int representing the size of each icon

    player:
        representation of the player in the game

    goal_stars:
        int representing the number of stars the player needs to collect to win

    keys_pressed:
        keeps track of the keys pressed, controlling the players movement

    screen:
        represents the screen the game is played on

    === Private Attributes ===
    running :
        a boolean representing whether of not the game is running

    actors:
        a list of the game's actors

    """

    def __init__(self, w: int, h: int) -> None:
        """
        Initialize a game that has a display screen and game actors.
        """

        self._running = False
        self._actors = []

        self.screen = None
        self.stage_width, self.stage_height = w, h-1
        self.size = (w * ICON_SIZE, h * ICON_SIZE)

        self.player = None
        self.goal_stars = 0

        self.keys_pressed = None

    def set_player(self, player: Player) -> None:
        """
        Set the game's player to be the given <player> object.
        """

        self.player = player

    def add_actor(self, actor: Actor) -> None:
        """
        Add the given <actor> to the game's list of actors.
        """

        self._actors.append(actor)

    def remove_actor(self, actor: Actor) -> None:
        """
        Remove the given <actor> from the game's list of actors.
        """

        self._actors.remove(actor)

    def get_actor(self, x: int, y: int) -> Optional[Actor]:
        """
        Return the actor object that exists in the location given by
        <x> and <y>. If no actor exists in that location, return None.
        """

        for item in self._actors:
            if item.x == x and item.y == y:
                return item
        return None

    def on_init(self) -> None:
        """
        Initialize the game's screen, and begin running the game.
        """

        pygame.init()
        pygame.display.set_caption("ROBBER RUNAWAY!")
        self.screen = pygame.display.set_mode \
            (self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event: pygame.Event) -> None:
        """
        React to the given <event> as appropriate.
        """

        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self) -> None:
        """
        Move all actors in the game as appropriate.
        Check for win/lose conditions and stop the game if necessary
        """

        self.keys_pressed = pygame.key.get_pressed()
        for actor in self._actors:
            actor.move(self)
            if self.player == None:
                self._running = False
                print("You lose :( better luck next time")
                return None

            elif self.player.has_won(self):
                self._running = False
                print("Congratualations! you won the game")
                return None


    def on_render(self) -> None:
        """
        Render all the game's elements onto the screen.
        """

        self.screen.fill(BLACK)
        for a in self._actors:
            rect = pygame.Rect(a.x * ICON_SIZE, a.y * ICON_SIZE, ICON_SIZE, ICON_SIZE)
            self.screen.blit(a.icon, rect)

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render("", True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.center = (self.stage_width * ICON_SIZE // 2, \
                           (self.stage_height + 0.5) * ICON_SIZE)
        self.screen.blit(text, textRect)

        pygame.display.flip()


    def on_cleanup(self) -> None:
        """
        Clean up and close the game.
        """

        pygame.quit()

    def on_execute(self) -> None:
        """
        Run the game until the game ends.
        """

        self.on_init()

        while self._running:
            pygame.time.wait(100)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()
        self.goal_message = "Objective: Collect {}".format(self.goal_stars) + \
                           " stars before the ghost gets you and head for the door"

    def game_over(self) -> None:
        """
        Set the game as over (remove the player from the game).
        """

        self.player = None
