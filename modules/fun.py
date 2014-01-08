#!/usr/bin/env python
"""
Code Copyright (C) 2012-2013 Liam Stanley
Credits: Sean B. Palmer, Michael Yanovich
fun.py - Fun Module
http://code.liamstanley.net/
"""

import random
#from random import randint

def sexycomment(rand):
    """finds a random comment dependant on what the rating was."""
    rand = int(rand)
    high = ['Now that\'s sexy!', 'Damn!', 'Nice!', 'Sweet!', 'Very sexy!', 'You\'re on fire!']
    medium = ['You could do better..', 'Nice man..', 'That\'s alright..', 'Not as sexy as me!']
    low = ['Try harder next time...', 'Ouch.', 'Uhh...', 'You don\'t even match me!', 'HA!', 'Oh man! DX']
    if rand == 100:
        response = 'You\'re perfect!'
    if rand > 80:
        response = random.choice(high)
    elif rand == 69:
        response = 'It\'s getting sexy in here!'
    elif rand < 81 and rand > 50:
        response = random.choice(medium)
    elif rand == 0:
        response = 'Wow.. You\'re not even on the scale. :('
    else:
        response = random.choice(low)
    return response

def roulette(code, input):
    """Play a little gruesome russian roulette."""
    chance = str(random.randint(1,6))
    if chance == '1':
        response = code.color('red', code.bold('dies!')) + ' :O'
    else:
        response = code.color('green', code.bold('is OK')) + ', the chamber was empty!'
    if input.group(2):
        nick = input.group(2)
        if nick.lower() == 'myself' or nick.lower() == code.nick.lower() or \
           nick.lower() == 'me' or nick.lower() == 'himself':
            nick = input.nick
        else:
            nick = input.nick
    else:
        nick = input.nick
    code.say('*Points gun at %s, and pulls the trigger* %s %s' % (nick, nick, response))
roulette.cmds = ['rr', 'russianroulette', 'roulette']
roulette.priority = 'medium'
roulette.example = '.roulette Timothy'
roulette.rate = 20

def sexymeter(code, input):
    hotuser = ['amber', 'mel', 'alaska', 'zac', 'zacbatt'] #remember, lowercase
    notuser = ['taq', 'taq|away', 'retro', 'retro|away', 'jonny'] #because lazy
    text = input.group().split()
    """Rates users on sexiness"""
    if len(text) > 2: return
    try:
        name = text[1]
        name = True
    except:
        name = False
    if not name:
        nick = input.nick
        ishot = nick.lower() in hotuser
        isnot = nick.lower() in notuser
        if ishot or input.admin:
            rand = str(random.randint(81,100))
        elif isnot:
            rand = str(random.randint(0,20))
        else:
            rand = str(random.randint(0,100))
        code.say('Rating %s on a scale of 1-100 of sexiness. Result: %s. %s' % (code.bold(nick), \
            code.bold(rand), code.bold(sexycomment(rand))))
    else:
        nick = text[1]
        ishot = nick.lower() in hotuser
        isnot = nick.lower() in notuser
        rand = str(random.randint(0,100))
        if len(nick) > 20:
            code.say(input.nick + code.color('red', ': The syntax is .sexymeter <name>.'))
            return
        if nick.lower() == code.nick.lower():
            nick = 'myself'
            rand = '100'
        elif text[1].lower() in map(str.lower,code.config.admins):
            rand = str(random.randint(81,100))
        elif nick.lower() == 'myself' or nick.lower() == 'me':
            nick = input.nick
        elif ishot:
            rand = str(random.randint(81,100))
        elif isnot:
            rand = str(random.randint(0,20))
        else:
            nick = text[1]
        code.say('Rating %s on a scale of 1-100 of sexiness. Result: %s. %s' % (code.bold(nick), \
            code.bold(rand), code.bold(sexycomment(rand))))
sexymeter.cmds = ['sm', 'sexymeter', 'um', 'uglymeter']
sexymeter.priority = 'medium'
sexymeter.example = '.sexymeter Code'
sexymeter.rate = 20

def slap(code, input):
    """Slaps a person using random methods"""
    text = input.group().split()
    if len(text) < 2 or text[1].startswith('#'): return
    if text[1].lower() == code.nick.lower() or text[1].lower() == 'everyone' or \
       text[1].lower() == 'everybody' or text[1].lower() == 'himself':
        if (input.nick not in code.config.admins):
            text[1] = input.nick
        else: text[1] = 'himself'
    if text[1].lower() in map(str.lower,code.config.admins):
        if (input.nick not in code.config.admins):
            text[1] = input.nick

    verb = random.choice(('slaps', 'kicks', 'destroys', 'annihilates', 'punches', \
    'roundhouse kicks', 'rusty hooks', 'pwns', 'owns', 'karate chops', 'kills', \
    'disintegrates', 'demolishes', 'Pulverizes'))
    afterfact = random.choice(('to death', 'out of the channel', \
    'into a hole, till death', 'into mid-air disintegration', \
    'into a pancake'))
    code.write(['PRIVMSG', input.sender, ' :\x01ACTION', verb, text[1], afterfact, '\x01'])
slap.cmds = ['slap', 'slaps']
slap.priority = 'medium'
slap.rate = 20

def hug(code, input):
    """Hugs <target>"""
    text = input.group().split()
    if len(text) < 2 or text[1].startswith('#'): return
    if text[1].lower() == code.nick.lower() or text[1].lower() == 'himself':
        if (input.nick not in code.config.admins):
            text[1] = input.nick
        else: text[1] = 'himself'
    types = random.choice(('hugs', 'snuggles'))
    hugtype = random.choice(('real tight', 'strongly', 'like a bear', 'tight', ''))
    code.write(['PRIVMSG', input.sender, ' :\x01ACTION', types, text[1], hugtype, '\x01'])
hug.cmds = ['hug', 'hugs']
hug.priority = 'low'
hug.rate = 5

def magic(code, input):
    """Use the Magic 8 Ball"""
    luck = str(random.randint(1,4))
    # http://en.wikipedia.org/wiki/Magic_8-Ball#Possible_answers
    if luck == '1' or luck == '2':
        # chance: 50% - Affirmative/Green/Bold
        response = random.choice(('It is certain.', 'It is decidedly so.', \
                       'Without a doubt.', 'Yes, definitely.', 'You may rely on it.', \
                       'As I see it yes.', 'Most likely.', 'Outlook good.', 'Yes.', \
                       'Signs point to yes.'))
        response = code.color('green', response)
    elif luck == '3':
        # chance: 25% - Negative/Red/Bold
        response = random.choice(('Don\'t count on it.', 'My reply is no.', \
                       'My sources say no.', 'Outlook not so good.', 'Very doubtful.'))
        response = code.color('red', response)
    else:
        # chance 25% - Non-Committal/Yellow/Bold
        response = random.choice(('Reply hazy, try again.', 'Ask again later.', \
                       'Better not tell you now.', 'Cannot predict now.', \
                       'Concentrate and ask again.'))
        response = code.color('yellow', response)
    code.say('*%s shakes the Magic 8 Ball...* %s' % (code.nick, code.bold(response)))
magic.cmds = ['8ball', '8b', 'luck', 'eightball', 'magic8']
magic.priority = 'medium'
magic.example = '.8ball will i feel better tomorrow?'
magic.rate = 15

def rps(code, input):
    """Play some Rock-Paper-Scissors with Code!"""
    text = input.group().lower()
    text = text.split()
    cpu = random.randint(1,3)
    if cpu == 1:
        state = 'had a draw'
        color = 'blue'
    elif cpu == 2:
        state = 'won'
        color = 'green'
    else:
        state = 'lost'
        color = 'red'
               # 1=tie, 2=win, 3=loss
    syntax = 'The syntax is .(rock/paper/scissors)'
    if input.group(1) == 'rock':
        if cpu == 1:
            response = 'rock'
        elif cpu == 2:
            response = 'scissors'
        else:
            response = 'paper'
    elif input.group(1) == 'paper':
        if cpu == 1:
            response = 'paper'
        elif cpu == 2:
            response = 'rock'
        else:
            response = 'scissors'
    elif input.group(1) == 'scissors':
        if cpu == 1:
            response = 'scissors'
        elif cpu == 2:
            response = 'paper'
        else:
            response = 'rock'
    return code.say('*Rock... Paper... Scissors!* You %s! %s had %s!' % (code.color(color, \
          code.bold(state)), code.nick, code.bold(response)))
rps.cmds = ['rock', 'paper', 'scissors'] #screw combining .rps (cmd) and .(cmd)
rps.example = '.rock'
rps.rate = 15

if __name__ == '__main__':
    print __doc__.strip()

