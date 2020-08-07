from configparser import ConfigParser
from time import sleep

import pyautogui as p

from allowed_key import *
from twitch_chat import join_chat


def load_params(file):
    """
    load configuration fot twitch

    :param file: config ini file
    :return: saved parameters
    """
    config = ConfigParser()
    config.read(file)

    return config['DEFAULT']


def message_to_interaction(message):
    """
    converts a message to an interaction and interacts

    :param message: message from chat
    :return:
    """
    if message in game_key:
        p.keyDown(message)
        sleep(press_time)
        p.keyUp(message)
        return

    if message in tool_key:
        p.press(message)
        return

    if mouse:
        if message == 'click' and click_allowed:
            p.click(clicks=click_amount)
            return
        if ':' in message:
            x, y = message.split(':')
            try:
                x = float(x)
                y = float(y)

                # only move if it is ok
                if max_movement * (-1) < x < max_movement and max_movement * (-1) < y < max_movement:
                    p.move(x, y)

            # catches everything with is no number in x and y
            except ValueError:
                ...


def main():
    params = load_params('config.ini')
    chat = join_chat(oath=params['oath'], channel_name=params['channel'], bot_name=params['bot'])
    chat.send_to_chat('connected')
    while True:
        _, message = chat.listen_to_chat()
        if message:
            message_to_interaction(message)


if __name__ == '__main__':
    main()
