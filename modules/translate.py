#!/usr/bin/env python
# coding=utf-8
"""
Code Copyright (C) 2012-2013 Liam Stanley
Credits: Sean B. Palmer, Michael Yanovich
translate.py - Code Translation Module
http://code.liamstanley.net/
"""

import json
import time
import urllib
import urllib2
import web

def translate(text, input='auto', output='en', use_proxy=False):
    raw = False
    if output.endswith('-raw'):
        output = output[:-4]
        raw = True

    opener = urllib2.build_opener()
    opener.addheaders = [(
        'User-Agent', 'Mozilla/5.0' +
        '(X11; U; Linux i686)' +
        'Gecko/20071127 Firefox/2.0.0.11'
    )]

    input, output = urllib.quote(input), urllib.quote(output)
    text = urllib.quote(text)

    uri = 'https://translate.google.com/translate_a/t?'
    params = {
            'sl': input,
            'tl': output,
            'js': 'n',
            'prev': '_t',
            'hl': 'en',
            'ie': 'UTF-8',
            'text': text,
            'client': 't',
            'multires': '1',
            'sc': '1',
            'uptl': 'en',
            'tsel': '0',
            'ssel': '0',
            'otf': '1',
    }

    for x in params:
        uri += '&%s=%s' % (x, params[x])

    if use_proxy:
        print 'USING PROXY'
        result = proxy.get(uri)
    else:
        print 'NOT USING PROXY'
        result = opener.open(uri).read()

    ## this is hackish
    ## this makes the returned data parsable by the json module
    result = result.replace(',,', ',').replace('[,', '["",')

    while ',,' in result:
        result = result.replace(',,', ',null,')
    data = json.loads(result)

    if raw:
        return str(data), 'en-raw'

    try:
        language = data[2] # -2][0][0]
    except:
        language = '?'

    if isinstance(language, list):
        language = data[-2][0][0]

    return ''.join(x[0] for x in data[0]), language

def tr(code, context):
    """Translates a phrase, with an optional language hint."""
    input, output, phrase = context.groups()

    phrase = phrase.encode('utf-8')

    if (len(phrase) > 350) and (not context.admin):
        return code.reply('Phrase must be under 350 characters.')

    input = input or 'auto'
    input = input.encode('utf-8')
    output = (output or 'en').encode('utf-8')

    if input != output:
        msg, input = translate(phrase, input, output)
        if isinstance(msg, str):
            msg = msg.decode('utf-8')
        if msg:
            msg = web.decode(msg) # msg.replace('&#39;', "'")
            msg = '"%s" (%s to %s)' % (msg, input, output)
        else: msg = 'The %s to %s translation failed, sorry!' % (input, output)

        code.reply(msg)
    else: code.reply('Language guessing failed, so try suggesting one!')

tr.rule = ('$nick', ur'(?:([a-z]{2}) +)?(?:([a-z]{2}|en-raw) +)?["“](.+?)["”]\? *$')
tr.example = '$nickname: "mon chien"? or $nickname: fr "mon chien"?'
tr.priority = 'low'

def tr2(code, input):
    """Translates a phrase, with an optional language hint."""
    if not input.group(2): return code.say("No input provided.")
    command = input.group(2).encode('utf-8')

    def langcode(p):
        return p.startswith(':') and (2 < len(p) < 10) and p[1:].isalpha()

    args = ['auto', 'en']

    for i in xrange(2):
        if not ' ' in command: break
        prefix, cmd = command.split(' ', 1)
        if langcode(prefix):
            args[i] = prefix[1:]
            command = cmd
    phrase = command

    if (len(phrase) > 350) and (not input.admin):
        return code.reply('Phrase must be under 350 characters.')

    src, dest = args
    if src != dest:
        msg, src = translate(phrase, src, dest)
        if isinstance(msg, str):
            msg = msg.decode('utf-8')
        if msg:
            msg = web.decode(msg) # msg.replace('&#39;', "'")
            msg = '"%s" (%s to %s)' % (msg, src, dest)
        else: msg = 'The %s to %s translation failed, sorry!' % (src, dest)

        code.reply(msg)
    else: code.reply('Language guessing failed, so try suggesting one!')

tr2.cmds = ['tr']
tr2.priority = 'low'

def mangle(code, input):
    phrase = input.group(2).encode('utf-8')
    for lang in ['fr', 'de', 'es', 'it', 'ja']:
        backup = phrase
        phrase = translate(phrase, 'en', lang)
        if not phrase:
            phrase = backup
            break
        __import__('time').sleep(0.5)

        backup = phrase
        phrase = translate(phrase, lang, 'en')
        if not phrase:
            phrase = backup
            break
        __import__('time').sleep(0.5)

    code.reply(phrase or 'ERRORS D:')
mangle.cmds = ['mangle']

if __name__ == '__main__':
    print __doc__.strip()
