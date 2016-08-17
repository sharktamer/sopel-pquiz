#!/usr/bin/env python

import json
from sopel.module import rule, commands
import os.path


def setup(bot):
    bot.memory['pquiz'] = {
        'active': False,
        'scores': {}
    }

    basepath = os.path.dirname(__file__)
    jsonfile = os.path.abspath(os.path.join(basepath, 'mons.json'))
    with open(jsonfile) as f:
        bot.memory['pquiz']['list'] = json.load(f)


@commands('pquiz')
def pquiz(bot, trigger):
    try:
        args = [int(i) for i in trigger.args[1].split()[1:]]
    except ValueError:
        bot.say('Error: arguments must be integer values')
        return

    j = bot.memory['pquiz']['list']

    if len(args) == 0:
        pj = list(j.values())
        bot.say('Starting pquiz with all mons')
    elif len(args) == 1:
        pj = [j[i] for i in j if int(i) <= args[0]]
        bot.say('Starting pquiz with mons 1-{}'.format(args[0]))
    else:
        pj = [j[i] for i in j if int(i) >= args[0] and int(i) <= args[1]]
        bot.say('Starting pquiz with mons {}-{}'.format(*args[:2]))
    bot.memory['pquiz']['game_list'] = pj
    bot.memory['pquiz']['game_size'] = len(pj)
    bot.memory['pquiz']['active'] = True


@rule('[^\.].*')
def panswer(bot, trigger):
    if not bot.memory['pquiz']['active']:
        return

    removed = False
    for i in trigger.args[1].split():
        if i.lower() in bot.memory['pquiz']['game_list']:
            removed = True
            bot.memory['pquiz']['game_list'].remove(i.lower())
            if trigger.nick in bot.memory['pquiz']['scores']:
                bot.memory['pquiz']['scores'][trigger.nick] += 1
            else:
                bot.memory['pquiz']['scores'][trigger.nick] = 1
    if removed:
        size = bot.memory['pquiz']['game_size']
        remaining = size - len(bot.memory['pquiz']['game_list'])
        bot.say('pquiz: {}/{}'.format(remaining, size))
        if not len(bot.memory['pquiz']['game_list']):
            bot.say('You named all the pokemon!')
            bot.say('Scores:')
            scores_tup = bot.memory['pquiz']['scores'].items()
            for k, v in sorted(scores_tup, key=lambda x: x[1], reverse=True):
                bot.say('{}: {}'.format(k, v))
            bot.memory['pquiz']['active'] = False
