#!/usr/bin/env python2

import sys
import re
import urllib2
import zlib
import json
import subprocess, os
import argparse

parser = argparse.ArgumentParser(description='StackOverflow helper.')
parser.add_argument('--verbose', dest='verbose', action='store_const',
                   const=1, default=0,
                   help='show verbose output')
args = parser.parse_args()

url = "https://api.stackexchange.com/2.1/search/advanced?order=desc&sort=relevance&site=stackoverflow&q="

match_error = re.compile("^([^:]*):([^:]*):([^:]*): (warning|error|fatal error): (.*)$")
match_tagged_message = re.compile("^(.*) (\[[^ ]*\])$")

# Colors
class bcolors:
    HEADER = '\033[43m\033[30m\033[1m'
    ENDC = '\033[0m'

def paint(s, color):
    return color + str(s) + bcolors.ENDC

# Parse stdin
messages = []
while 1:
    try:
        errorline = sys.stdin.readline()
        if args.verbose:
            print errorline,
    except KeyboardInterrupt:
        break

    if not errorline:
        break
    
    match = match_error.search(errorline)
    if match:
        try:
            codeline = sys.stdin.readline()
            if args.verbose:
                print codeline,
        except KeyboardInterrupt:
            break

        data = match_error.search(errorline)

        filename = data.group(1)
        line = data.group(2)
        row = data.group(3)
        level = data.group(4)
        if (match_tagged_message.match(data.group(5))):
            data2 = match_tagged_message.search(data.group(5))
            message = data2.group(1)
            tag = data2.group(2)
        else:    
            message = data.group(5)
            tag = ""
        
        messages.append( {"errorline":errorline, "codeline":[codeline], "filename":[filename], "line":[line], "row":[row], "level":level, "message":message, "tag":tag} )

# Display user menu
sys.stdin = open('/dev/tty')

if args.verbose:
    print
i = 1
for m in messages:
    print '{0} {1}: {2}'.format(paint(i, bcolors.HEADER), m['level'], m['message'])
    i = i + 1
print "==> Enter message number" 
print "==> --------------------"

try:
    num = int(input('==> '))
except:
    sys.exit(0)
if num > len(messages) or num <= 0:
    sys.exit(0)
print

message = messages[num-1]

# Hardwork
opener = urllib2.build_opener()
req = url + (urllib2.quote(message['message']))
data = opener.open(req).read()
jsondata = json.loads(zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data))


# Display user menu
print "Links: " + message['message']
print '{0} {1}'.format(paint(0, bcolors.HEADER), 'Google for me')
j = 1
for answer in jsondata['items']:
    if j > 10:
       break
    print '{0} {1}'.format(paint(j, bcolors.HEADER), answer['title'])
    j = j + 1
print "==> Enter post number"
print "==> --------------------"

try:
    num = int(input('==> '))
except:
    sys.exit(0)
if num > len(jsondata['items']) or num < 0:
    sys.exit(0)

if num == 0:
    link = "http://google.com/search?q=" + message['message']
else :
    link = jsondata['items'][num-1]['link']

print "Opening " + link
if sys.platform.startswith('darwin'):
    subprocess.call(('open', link))
elif os.name == 'nt':
    os.startfile(link)
elif os.name == 'posix':
    subprocess.call(('xdg-open', link))
