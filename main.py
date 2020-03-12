import socket
from configparser import ConfigParser
from time import sleep

import pyautogui as p

from allowed_key import *


def load_params(file):
    """
    load configuration fot twitch

    :param file: config ini file
    :return: saved parameters
    """
    config = ConfigParser()
    config.read(file)

    return config['DEFAULT']


def join_chat(params):
    """
    bot joins chat and posts a message in chat

    :param params: params from config
    :return: irc object
    """
    irc = socket.socket()
    irc.connect((params['server'], int(params['port'])))
    irc.send(f'PASS {params["oath"]}\nNICK {params["bot"]}\n Join #{params["channel"]}\n'.encode())

    loading = True
    while loading:
        read_buffer_join = irc.recv(1024)
        read_buffer_join = read_buffer_join.decode()

        for line in read_buffer_join.split('\n')[0:-1]:
            # checks if loading is complete
            loading = 'End of /NAMES list' not in line

    # confirm messages
    send_to_chat(irc, 'Joined Channel', params)
    print(f'joined:{params["channel"]}')

    return irc


def send_to_chat(irc, message, params):
    """
    sends a message in chat

    :param irc: irc object
    :param message: message for chat
    :param params: params from config
    :return:
    """
    message_temp = f'PRIVMSG #{params["channel"]} :{message}'
    irc.send(f'{message_temp}\n'.encode())


def listen_to_chat(irc):
    """
    listens to chat and uses massage_to_interaction

    :param irc: irc object
    :return: this is a server loop
    """
    while True:
        try:
            read_buffer = irc.recv(1024).decode()
        except:
            # incase there is nothing
            read_buffer = ''
        for line in read_buffer.split('\r\n'):
            # ping pong to stay alive | PRIVMSG marks every interaction with users
            if 'PING' in line and 'PRIVMSG' not in line:
                irc.send('PONG tmi.twitch.tv\r\n'.encode())

            # only interact if
            elif line != '':
                # makes message to interaction
                message = get_message(line)
                message_to_interaction(message)


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


def get_user(line):
    """

    :param line: answer line from twitch
    :return: user
    """
    parts = line.split(':', 2)
    return parts[1].split('!', 1)[0]


def get_message(line):
    """

    :param line: answer line from twitch
    :return: message
    """
    try:
        message = line.split(':', 2)[2]
    except IndexError:
        message = ''
    return message


def main():
    params = load_params('config.ini')
    irc = join_chat(params)
    listen_to_chat(irc)


if __name__ == '__main__':
    main()
