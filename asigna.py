#!/usr/bin/env python3
import time
import os, sys
import threading
from game_data import rooms
from mudserver import MudServer
from lib.constants import DEFAULT_START_LOCATION
from lib.command import Commands
from lib.models.game_state import GameState

lock = threading.Lock()
global gameloop
game = GameState(MudServer())
commands = Commands(game)


def sprint(message):
    lock.acquire()
    print(message)
    lock.release()


def clear_screen():
    os.system('clear')


def reset_screen():
    os.system('reset')


# main game loop. We loop forever (i.e. until the program is terminated)
def asigna():
    while True:
        # pause for 1/5 of a second on each loop, so that we don't constantly
        # use 100% CPU time
        time.sleep(0.2)

        # 'update' must be called in the loop to keep the game running and give
        # us up-to-date information
        game.update()

        # go through any newly connected players
        new_players = game.handle_player_join()

        # go through any recently disconnected players
        game.handle_player_leave()

        # go through any new commands sent from players
        for event in game.server.get_commands():
            client = event.client
            command = event.command
            params = event.params

            player = game.find_player_by_client_id(client.uuid)

            # if for any reason the player isn't in the player map, skip them and
            # move on to the next one
            if not player:
                continue

            if player.name is None:
                # Any new command event will become the player's name.
                player.name = command.capitalize()
                sprint(f"{player.name} entered the game.")
                game.broadcast(f"{player.name} entered the game.")

                player.message(f"Welcome to the game, {player.name}.")
                player.message("Type 'help' for a list of commands. Have fun!")
                player.move(DEFAULT_START_LOCATION)

                continue

            # each of the possible commands is handled below. Try adding new
            # commands to the game!
            commands.execute_command(player, command, params)


def main():
    gameloop = threading.Thread(target=asigna)
    gameloop.start()
    sprint("Asigna is now being served!")


if __name__ == "__main__":
    main()
