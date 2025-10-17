from pynput.keyboard import Controller, Key
from pyautogui import click
from time import sleep  
import os
import sys


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

NEXT_BUTTON = Point(x=1107, y=212)
SELECT_ALL = Point(x=1135, y=257)
DOWNLOAD = Point(x=1137, y=165)
RANDOM = Point(x=704, y=211)


DIRECTORY = "..\\Chess Games"


def press_enter():
    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


def main():
    before = set(os.listdir(DIRECTORY))

    click(NEXT_BUTTON.x, NEXT_BUTTON.y)
    sleep(2)
    click(SELECT_ALL.x, SELECT_ALL.y)
    sleep(0.5)
    click(DOWNLOAD.x, DOWNLOAD.y)
    sleep(3)
    press_enter()
    sleep(1)
    click(RANDOM.x, RANDOM.y)
    sleep(0.5)

    after = set(os.listdir(DIRECTORY))
    new_files = after - before

    if new_files:
        print("File downloaded:", new_files)
    else:
        sys.exit(1)

sleep(3)
while True:
    main()