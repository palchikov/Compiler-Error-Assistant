#!/bin/sh

#USAGE: gcc -Wall {your-source.c} 2>&1 | get-errors.sh

while IFS= read; do
   res=`echo $REPLY | grep -E '(error|warning)'`
   echo "$REPLY"
   if [ -n "$res" ]; then
      line=`echo $REPLY | grep -E '(error|warning)' |\
            sed 's/^.*warning: //' | sed 's/^.*error: //' |\
            sed 's/\[.*\]$//' | sed 's/ /+/g'`
      url='http://stackoverflow.com/search?q="'$line'"+is:question'
      #qlist=`cat tmp.html | grep '<span><a'`
      #TODO: Uncomment to download actual url
      qlist=`wget -O - $url 2>/dev/null | grep '<span><a'`
      printf %s "$qlist" | while IFS= read; do
         link='http://stackoverflow.com'`echo $REPLY | sed -r 's/^.*href="([^"]+)".*/\1/'`
         title=`echo $REPLY | sed -r 's/^.*title="([^"]+)".*/\1/'`
         echo "   " $title --- $link
      done
   fi
done
