
import World

from User import *
from World import *
# from globals import *


import os, sys, time
import threading
from game_data import rooms
from mudserver import MudServer
from lib.constants import DEFAULT_START_LOCATION
from lib.command import Commands
from lib.models.game_state import GameState


gameloop = None
lock = threading.Lock()
users = []


def sprint(message):
    lock.acquire()
    print(message)
    lock.release()


def tick():
    for user in Asigna.users:
        user.send("tick")


def clear_screen():
    os.system('clear')


def reset_screen():
    os.system('reset')


def menu():
    sprint("""
    Welcome to the Asigna Server:
        0) Big Bang the World
        1) Start/Restart Service
        2) Stop Serving Asigna Mud
    """)
    choice = input("    Enter menu choice:")
    handle_input(choice)


def zero():     #0) Big Bang the World
    globals.world = None
    globals.world = World()


def one():      # 1) Start/Restart Service
    globals.server = None
    globals.server = Server()
    globals.server.start()


def two():      # 2) Stop Serving Asigna Mud
    pass


def handle_input(choice):
    switcher = {
        0: zero(),
        1: one(),
        2: two(),
    }
    func = switcher.get(choice, menu())
    return func()


def main():
    globals.gameloop = threading.Thread(target=asigna)
    globals.gameloop.start()


def asigna():
    while True:
        time.sleep(.3)
        tick()


if __name__ == "__main__":
    globals.world = World()
    globals.server = Server()
    main()
    menu()