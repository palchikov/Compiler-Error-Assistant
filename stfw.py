#!/usr/bin/env python2
# -*-coding: utf-8 -*-

from __future__ import print_function
import sys
import re
import urllib2
import zlib
import json
import subprocess, os
import argparse
import webbrowser
import HTMLParser

# Consts
match_error = re.compile("^([^:]*):([^:]*):([^:]*): (warning|error|fatal error): (.*)$")
match_tagged_message = re.compile("^(.*) (\[[^ ]*\])$")

# Arguments
parser = argparse.ArgumentParser(description='StackOverflow helper.')
parser.add_argument('-v', '--verbose', dest='verbose_output', action='store_const',
                   const=1, default=0,
                   help='show verbose output')
parser.add_argument('-s', '--system-open', dest='system_open', action='store_const',
                   const=1, default=0,
                   help='use system URL open command')
parser.add_argument('-o', '--open-with', dest='open_with', action='store',
                   default='',
                   help='use custom URL open command')
args = parser.parse_args()

# Colors
C_HEADER = '\033[43m\033[30m\033[1m'
C_ERROR = '\033[31m'
C_IMPORTANT = '\033[34m'
C_ENDC = '\033[0m'

def paint(s, color):
    return color + str(s) + C_ENDC

# StackExchange API
request_url = "https://api.stackexchange.com/2.1/search/advanced?order=desc&sort=relevance&site=stackoverflow&q="
url_opener = urllib2.build_opener()

def load_stackoverflow(request):
    req = request_url + (urllib2.quote(request))
    try:
        data = url_opener.open(req).read()
        jsondata = json.loads(zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data))
        return jsondata['items']
    except IOError, e:
        print (paint("ERROR:", C_ERROR) + " Connection failed: " + str(e))
        return []

# Browser API
def open_url(link):
    print (paint("Opening: ", C_IMPORTANT) + link)

    if args.open_with:
        subprocess.call((args.open_with, link))
        sys.exit(0)

    if args.system_open:
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', link))
        elif os.name == 'nt':
            os.startfile(link)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', link.replace('*','\\*')))
        sys.exit(0)

    webbrowser.open(link.decode("utf-8").replace(u'’','\'').replace(u'‘','\''), new=0)

# Error menu
def display_error_menu(messages):
    if len(messages.items()) == 0:
        sys.exit(0)
    # if len(messages.items()) == 1:
    #     return 1
    i = 1
    for message,m in messages.items():
        print (paint(i, C_HEADER) + ' ' + m['level'] + ': ' + message)
        i = i + 1
    print ("==> Enter message number" )
    print ("==> --------------------")

    try:
        num = int(input('==> '))
    except:
        sys.exit(0)
    if num > len(messages) or num <= 0:
        sys.exit(0)
    print
    return num

# Display link menu
def display_link_menu(m, answers):
    print (paint("Request: ", C_IMPORTANT) + m['message'])
    print (paint(0, C_HEADER) + ' Google for me')
    j = 1
    for answer in answers:
        if j > 10:
           break
        print (paint(j, C_HEADER) + ' ' + HTMLParser.HTMLParser().unescape(answer['title']))
        j = j + 1
    print ("==> Enter post number")
    print ("==> --------------------")

    try:
        num = int(input('==> '))
    except:
        sys.exit(0)
    if num > len(answers) or num < 0:
        sys.exit(0)

    if num == 0:
        return "http://google.com/search?q=" + urllib2.quote(m['message'])
    else :
        return answers[num-1]['link']

# Parse stdin
messages = dict()
while 1:
    try:
        errorline = sys.stdin.readline()
        if args.verbose_output:
            print (errorline, end='')
    except KeyboardInterrupt:
        break

    if not errorline:
        break
    
    data = match_error.search(errorline)
    if data:
        try:
            codeline = sys.stdin.readline()
            if args.verbose_output:
                print (codeline, end='')
        except KeyboardInterrupt:
            break

        filename = data.group(1)
        line = data.group(2)
        row = data.group(3)
        level = data.group(4)
        data2 = match_tagged_message.search(data.group(5))
        if (data2):
            message = data2.group(1)
            tag = data2.group(2)
        else:    
            message = data.group(5)
            tag = ""
        
        if message not in messages:
           messages.update({message:{"codeline":[], "filename":[], "line":[], "row":[], "level":level, "message":message, "tag":tag}})

        messages[message]["codeline"].append(codeline)
        messages[message]["filename"].append(filename)
        messages[message]["line"].append(line)
        messages[message]["row"].append(row)
if args.verbose_output:
    print

sys.stdin = open('/dev/tty')

num = display_error_menu(messages)
message = messages[messages.keys()[num-1]]
answers = load_stackoverflow(message['message'])
link = display_link_menu(message, answers)
open_url(link)
