#!/usr/bin/env python
"""
Code Copyright (C) 2012-2013 Liam Stanley
minecraft.py - Code Urban Dictionary Module
http://code.liamstanley.net/
"""
# http://api.urbandictionary.com/v0/define?term=

import urllib2
import re
import HTMLParser

h = HTMLParser.HTMLParser()

# My present to you.
def urban(code, input):
    # clean and split the input
    if input.group(2):
        msg = input.group(2).lower().strip()
        parts = msg.split()
        if parts[-1].replace('-','').isdigit():
            if int(parts[-1]) <= 0:
                id = 1
            else:
                id = int(parts[-1].replace('-',''))
            del parts[-1]
            query = '+'.join(parts)
        else:
            id = 1
            query = msg.replace(' ', '+')
        uri = 'http://www.urbandictionary.com/define.php?term=%s'
        query = re.sub(r'[^\w\s]', '+', query)
        query = query.replace('.', '+')
        while query.find('++') > -1:
            query = query.replace('++', '+').strip('+')
        try:
            r = urllib2.urlopen(uri % (query)).read().replace('\t','').replace('\r',' ').replace('\n','').decode('utf-8')
        except urllib2.HTTPError as e:
            return code.say(code.color('red', 'urbandictionary.com did not respond correctly, is it down?'))
        definitive = 'Definition'
    else:
        id = 1
        uri = 'http://www.urbandictionary.com/random.php'
        try:
            r = urllib2.urlopen(uri).read().replace('\t','').replace('\r','').replace('\n',' ').decode('utf-8')
        except urllib2.HTTPError as e:
            return code.say(code.color('red', 'urbandictionary.com did not respond correctly, is it down?'))
        name = re.compile(r'<title>.*?</title>').findall(r)[0].replace('Urban Dictionary: ','')
        name = re.sub(r'\<.*?\>', '', name).strip()
        definitive = 'Definition (%s)' % name
    definition = re.compile(r'<div class="definition">.*?</div>').findall(r)
    example = re.compile(r'<div class="example">.*?</div>').findall(r)
    did = len(definition)
    if did == 0: return code.say('The definition for "%s" wasn\'t found.' % (code.color('purple', ' '.join(parts))))
    if id > did:
        id = did
    definition = re.sub(r'\<.*?\>', '', definition[id-1]).strip()
    example = re.sub(r'\<.*?\>', '', example[id-1]).strip()
    if (len(definition) + len(example)) > 490:
        # cap at definition, skip example
        code.say('(%s/%s) %s: %s' % (str(id), str(did), code.color('purple', 'Definition'), \
                 h.unescape(definition)))
    else:
        code.say('(%s/%s) %s: %s %s: %s' % (str(id), str(did), code.color('purple', definitive), \
                 h.unescape(definition), code.color('purple', 'Ex'), h.unescape(example)))
urban.cmds = ['urban', 'ur']
urban.example = '.urban liam'


if __name__ == '__main__':
    print __doc__.strip()
