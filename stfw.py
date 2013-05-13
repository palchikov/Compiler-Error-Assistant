#!/usr/bin/env python2

import sys
import re
import urllib2
import zlib
import json
import subprocess, os

url = "https://api.stackexchange.com/2.1/search/advanced?order=desc&sort=relevance&site=stackoverflow&q="

match_error = re.compile("^([^:]*):([^:]*):([^:]*): (warning|error): (.*)$")
match_tagged_message = re.compile("^(.*) (\[[^ ]*\])$")

messages = []

# Parse stdin
while 1:
    try:
        errorline = sys.stdin.readline()
    except KeyboardInterrupt:
        break

    if not errorline:
        break

    match = match_error.search(errorline)
    if match:
        try:
            codeline = sys.stdin.readline()
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
        
        messages.append( {"errorline":errorline, "codeline":codeline, "filename":filename, "line":line, "row":row, "level":level, "message":message, "tag":tag} )

# Display user menu
sys.stdin = open('/dev/tty')

i = 1
for m in messages:
    print('{0}: {1}: {2}'.format(i, m['level'], m['message']))
    i = i + 1
print("==> Enter message number")
print("==> --------------------")

try:
    num = int(input('==> '))
except ValueError:
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
print("Links: " + message['message'])
j = 1
for answer in jsondata['items']:
    if j > 5:
       break
    print('{0}: {1}'.format(j, answer['title']))
    j = j + 1
print("==> Enter post number")
print("==> --------------------")

try:
    num = int(input('==> '))
except ValueError:
    sys.exit(0)
if num > len(jsondata['items']) or num <= 0:
    sys.exit(0)

answer = jsondata['items'][num-1]
link = answer['link']

print (link)
if sys.platform.startswith('darwin'):
    subprocess.call(('open', link))
elif os.name == 'nt':
    os.startfile(link)
elif os.name == 'posix':
    subprocess.call(('xdg-open', link))
