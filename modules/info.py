#!/usr/bin/env python
"""
Code Copyright (C) 2012-2013 Liam Stanley
Credits: Sean B. Palmer, Michael Yanovich
info.py - Code Information Module
http://code.liamstanley.net/
"""

from tools import *

@hook(['commands','cmds'])
@rate(30)
def commands(code, input):
    """Get a list of function-names (commands), that the bot has."""
    if input.group(2): return help(code, input)
    names = ', '.join(sorted(code.doc.iterkeys()))
    if input.sender.startswith('#'):
        code.reply('I am sending you a private message of all my commands.')
    count = 0
    cmds = []
    commands = list(set(input.commands))
    full = len(commands)
    count = 0
    tmp = []
    # Make a list, of lists, of lines. :)
    for i in sorted(commands):
        count += 1
        if count == 40:
            # Assume new line!
            cmds.append(tmp)
            tmp, count = [], 0
            tmp.append(i)
        else:
            # Assume appending to tmp
            tmp.append(i)
    cmds.append(tmp)
    code.msg(input.nick, 'Commands I recognize:')
    for line in cmds:
        code.msg(input.nick, '# %s' % (', '.join(line)))
    code.msg(input.nick, ('For help, do \'.help example\' where ' +
                          '"example" is the name of the command you want ' +
                          'help for.'))


@hook(['help'], '.help fml')
@rate(30)
def help(code, input):
    if input.group(2):
        name = input.group(2)
        if name in code.doc:
            desc = code.doc[name][0]
            while '  ' in desc:
                desc = desc.replace('  ',' ')
            code.say(code.color('purple','Description') + ': ' + desc)
            if code.doc[name][1]:
                ex = code.doc[name][1]
                while '  ' in ex:
                    ex = ex.replace('  ',' ')
                code.say(code.color('purple','Example') + ': ' + ex)
        else:
            code.reply(code.color('red','I\'m sorry, there is no documentation for that command.'))
    else:
        try:
            website = code.config.website
        except: #revert to default - The Code homepage.
            website = 'http://code.liamstanley.net'
        response = (
            'Hi, I\'m a bot. Say "%s" to me in private for a list ' +
            'of my commands, or see %s for more general details.' +
            ' %s is my owner.')
        code.reply(response % (code.color('purple', '.cmds'),website,code.color('gold', code.config.owner)))


@hook(['about','author'])
@rate(60)
def about(code, input):
    response = (
       code.nick + ' was developed by Liam Stanley and many others. ' + code.nick + ' is a open-source ' + 
       'Python Modular IRC Bot, that serves as a fun, fast, and collective resource ' + 
       'for large, and small channels. More info: http://code.liamstanley.net'
    )
    code.reply(response)


@hook(['report','issue','bug','issues'])
@rate(60)
def issue(code, input):
    code.reply('Having an issue with ' + code.bold(code.nick) + '? Post a bug report here:')
    code.say('https://github.com/Liamraystanley/Code/issues/new')


@hook(['stats'])
def stats(code, input): 
    """Show information on command usage patterns."""
    commands = {}
    users = {}
    channels = {}

    ignore = set(['f_note', 'startup', 'message', 'noteuri',
                      'say_it', 'collectlines', 'oh_baby', 'chat',
                      'collect_links','welcomemessage','auth_request'])
    for (name, user), count in code.stats.items(): 
        if name in ignore: continue
        if not user: continue

        if not user.startswith('#'): 
            try: users[user] += count
            except KeyError: users[user] = count
        else: 
            try: commands[name] += count
            except KeyError: commands[name] = count

            try: channels[user] += count
            except KeyError: channels[user] = count

    comrank = sorted([(b, a) for (a, b) in commands.iteritems()], reverse=True)
    userank = sorted([(b, a) for (a, b) in users.iteritems()], reverse=True)
    charank = sorted([(b, a) for (a, b) in channels.iteritems()], reverse=True)

    # most heavily used commands
    creply = code.color('green', 'Most used commands: ')
    for count, command in comrank[:10]: 
        creply += '%s (%s), ' % (command, count)
    code.say(creply.rstrip(', '))

    # most heavy users
    reply = code.color('blue', 'Power users: ')
    for count, user in userank[:10]: 
        reply += '%s (%s), ' % (user, count)
    code.say(reply.rstrip(', '))

    # most heavy channels
    chreply = code.color('purple', 'Power channels: ')
    for count, channel in charank[:3]: 
        chreply += '%s (%s), ' % (channel, count)
    code.say(chreply.rstrip(', '))


if __name__ == '__main__': 
    print __doc__.strip()