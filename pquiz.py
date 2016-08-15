#!/usr/bin/env python

import json
from sopel.module import rule, commands
import os.path

basepath = os.path.dirname(__file__)
jsonfile = os.path.abspath(os.path.join(basepath, 'mons.json'))
with open(jsonfile) as f:
    j = json.load(f)


@rule('[^\.].*')
def panswer(bot, trigger):
    if not bot.memory.contains('pq_active') or not bot.memory['pq_active']:
        return

    removed = False
    for i in trigger.args[1].split():
        if i.lower() in bot.memory['pj']:
            removed = True
            bot.memory['pj'].remove(i.lower())
    if removed:
        remaining = bot.memory['pj_size'] - len(bot.memory['pj'])
        bot.say('pquiz: {}/{}'.format(remaining, bot.memory['pj_size']))
        if not len(bot.memory['pj']):
            bot.say('You named all the pokemon!')
            bot.memory['pq_active'] = False


@commands('pquiz')
def pquiz(bot, trigger):
    try:
        args = [int(i) for i in trigger.args[1].split()[1:]]
    except ValueError:
        bot.say('Error: arguments must be integer values')
        return

    if len(args) == 0:
        pj = list(j.values())
        bot.say('Starting pquiz with all mons')
    elif len(args) == 1:
        pj = [j[i] for i in j if int(i) <= args[0]]
        bot.say('Starting pquiz with mons 1-{}'.format(args[0]))
    else:
        pj = [j[i] for i in j if int(i) >= args[0] and int(i) <= args[1]]
        bot.say('Starting pquiz with mons {}-{}'.format(*args[:2]))
    bot.memory['pj'] = pj
    bot.memory['pj_size'] = len(pj)
    bot.memory['pq_active'] = True
