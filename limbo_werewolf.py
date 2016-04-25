"""!werewolf <command> echos what you said"""

import json
import random
import re
import sys
import time

sys.path.append('/Users/ameliaarbisser/workspace/personal')
import one_night.game as game
import one_night.role as role

GAME = None
MYSELF = 'U0LFPJJLR'

class SimplePlayer:
    def __init__(self, name, inform, ask):
        self.name = name
        self.inform = inform
        self.ask = ask


def create_inform(server, dm_channel):
    def inform(amsg, statement):
        text = '%s\n%s' % (amsg, statement)
        server.slack.rtm_send_message(dm_channel, text)
    return inform


def create_ask(server, dm_channel):
    def ask(amsg, options):
        text = '%s\n Select one of (type just the number):' % amsg
        c = 1
        for o in options:
            text += '\n%s. %s' % (c, o)
            c += 1
        server.slack.rtm_send_message(dm_channel, text)

        option_id = None
        while option_id is None:
            recent_msgs = json.loads(server.slack.api_call('im.history?channel=%s' % dm_channel))['messages']
            if recent_msgs[0]['user'] != MYSELF:
                response = recent_msgs[0]['text']
                try:
                    option_id = int(response) - 1
                    if not (option_id >= 0 and option_id < len(options)):
                        raise Exception('Option ID not in range.')
                except:
                    option_id = None
                    server.slack.rtm_send_message(dm_channel, 'Try again...' + text)

            time.sleep(1)

        return options[option_id]

    return ask


def start(players_roles, msg, server):
    global GAME

    channel_info = json.loads(server.slack.api_call('channels.info?channel=%s' % msg['channel']))['channel']
    dms = json.loads(server.slack.api_call('im.list'))['ims']

    players = []
    for user in channel_info['members']:
        dm_channel = [dm['id'] for dm in dms if dm['user'] == user]
        if not dm_channel:
            continue
        else:
            dm_channel = dm_channel[0]

        name = json.loads(server.slack.api_call('users.info?user=%s' % user))['user']['name']

        players.append(SimplePlayer(name, create_inform(server, dm_channel), create_ask(server, dm_channel)))

    if GAME:
        return 'Game is already in progress.'
    GAME = game.Game(players,
                     [role.WEREWOLF,
                      role.WEREWOLF,
                      role.VILLAGER,
                      role.SEER,
                      role.TROUBLEMAKER,
                      role.ROBBER,
                      role.INSOMNIAC,
                      role.MINION][:len(players) + 3])

    server.slack.rtm_send_message(msg['channel'], 'Everyone! Go to sleep.')
    GAME.play_night()
    warnings = [
        'Be afraid. Be VERY afraid. ',
        '',
        'Are you afraid of the dark? ',
        'BOO! ',
        'Mwahahaha....... '
    ]
    player_names = ', '.join([p.name for p in GAME.active_players()])
    game_roles = ', '.join([str(r) for r in GAME.roles])
    game_setup = 'Players: %s\nRoles: %s' % (player_names, game_roles)
    server.slack.rtm_send_message(msg['channel'], game_setup)
    return '%sEveryone, wake up!' % random.choice(warnings)


def cancel(_, msg, server):
    global GAME
    GAME = None
    return 'Canceled game.'


def vote(players, msg, server):
    global GAME
    votes = GAME.vote()
    results = '\n'.join(['\t%s -> %s' % (v, votes[v]) for v in votes])
    if votes:
        final_msg = 'You all voted:\n%s\nThe roles are: \n%s' % (results, GAME.current)
        GAME = None
        return final_msg
    else:
        return 'Vote vetoed.'


def werewolf(command, arguments, msg, server):
    actions = {
        'start': start,
        'vote': vote,
        'cancel': cancel
    }

    # try:
    return actions[command](arguments, msg, server)
    # except KeyError:
    #     return '"%s" is not a command' % command


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!ww (.*)", text)
    if not match:
        return

    commands = match[0].split(' ')
    return werewolf(commands[0], commands[0:], msg, server)
