#!/usr/bin/env python

import json
from sopel.module import rule, commands
import os.path

basepath = os.path.dirname(__file__)
jsonfile = os.path.abspath(os.path.join(basepath, 'mons.json'))
with open(jsonfile) as f:
    j = json.load(f)


@rule('.*')
def panswer(bot, trigger):
    pass


@commands('pquiz')
def pquiz(bot, trigger):
    try:
        args = [int(i) for i in trigger.args[1].split()[1:]]
    except ValueError:
        bot.say('Error: arguments must be integer values')
        return

    if len(args) == 0:
        pj = j
    elif len(args) == 1:
        pj = {i: j[i] for i in j if int(i) <= args[0]}
    else:
        pj = {i: j[i] for i in j if int(i) >= args[0] and int(i) <= args[1]}


