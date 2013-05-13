#!/usr/bin/env python3

import sys
import re

match_error = re.compile("^([^:]*):([^:]*):([^:]*): (warning|error): (.*)$")
match_tagged_message = re.compile("^(.*) (\[[^ ]*\])$")

messages = []

# parse stdin
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

# display user menu
sys.stdin = open('/dev/tty')

i = 1
for m in messages:
    print(str(i) + ": " + m['message'])
    i = i + 1
print("==> Enter message number")
print("==> --------------------")

try:
    num = int(input('==> '))
except ValueError:
    sys.exit(0)
if num > len(messages) or num <= 0:
    sys.exit(0)

message = messages[num-1]
print(message['message'])