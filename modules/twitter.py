#!/usr/bin/env python
"""
Code Copyright (C) 2012-2013 Liam Stanley
Credits: Sean B. Palmer, Michael Yanovich
twitter.py - Code Twitter Module
http://code.liamstanley.io/
"""

import re, time
import web

r_username = re.compile(r'^[a-zA-Z0-9_]{1,15}$')
r_link = re.compile(r'^https?://twitter.com/\S+$')
r_p = re.compile(r'(?ims)(<p class="js-tweet-text.*?</p>)')
r_tag = re.compile(r'(?ims)<[^>]+>')
r_anchor = re.compile(r'(?ims)(<a.*?</a>)')
r_expanded = re.compile(r'(?ims)data-expanded-url=["\'](.*?)["\']')
r_whiteline = re.compile(r'(?ims)[ \t]+[\r\n]+')
r_breaks = re.compile(r'(?ims)[\r\n]+')

def entity(*args, **kargs):
    return web.entity(*args, **kargs).encode('utf-8')

def decode(html):
    return web.r_entity.sub(entity, html)

def expand(tweet):
    def replacement(match):
        anchor = match.group(1)
        for link in r_expanded.findall(anchor):
            return link
        return r_tag.sub('', anchor)
    return r_anchor.sub(replacement, tweet)

def read_tweet(url):
    bytes = web.get(url)
    shim = '<div class="content clearfix">'
    if shim in bytes:
        bytes = bytes.split(shim, 1).pop()

    for text in r_p.findall(bytes):
        text = expand(text)
        text = r_tag.sub('', text)
        text = text.strip()
        text = r_whiteline.sub(' ', text)
        text = r_breaks.sub(' ', text)
        return decode(text)
    return "Sorry, couldn't get a tweet from %s" % url

def format(tweet, username):
    return '%s (@%s)' % (tweet, username)

def user_tweet(username):
    tweet = read_tweet('https://twitter.com/' + username + "?" + str(time.time()))
    return format(tweet, username)

def id_tweet(tid):
    link = 'https://twitter.com/twitter/status/' + tid
    data = web.head(link)
    message, status = tuple(data)
    if status == 301:
        url = message.get("Location")
        if not url: return "Sorry, couldn't get a tweet from %s" % link
        username = url.split('/')[3]
        tweet = read_tweet(url)
        return format(tweet, username)
    return "Sorry, couldn't get a tweet from %s" % link

def twitter(code, input):
    arg = input.group(2)
    if not arg:
        return code.reply("Give me a link, a username, or a tweet id")

    arg = arg.strip()
    if isinstance(arg, unicode):
        arg = arg.encode('utf-8')

    if arg.isdigit():
        code.say(id_tweet(arg))
    elif r_username.match(arg):
        code.say(user_tweet(arg))
    elif r_link.match(arg):
        username = arg.split('/')[3]
        tweet = read_tweet(arg)
        code.say(format(tweet, username))
    else: code.reply("Give me a link, a username, or a tweet id")

twitter.commands = ['tw', 'twitter']
twitter.thread = True

if __name__ == '__main__':
    print __doc__
