#!/bin/sh

#USAGE: gcc -Wall {your-source.c} 2>&1 | get-errors.sh

function search_so {
   local line=$1
   local url='http://stackoverflow.com/search?q="'$line'"+is:question'
   #qlist=`cat tmp.html | grep '<span><a'`
   #TODO: Uncomment to download actual url
   local qlist=`wget -O - $url 2>/dev/null | grep '<span><a'`
   if [ -z "$qlist" ]; then
      return
   fi
   local i=0
   echo "$qlist" | while IFS= read; do
      if (( i >= 5 )); then
         break;
      fi
      local link='http://stackoverflow.com'`echo $REPLY | sed -r 's/^.*href="([^"]+)".*/\1/'`
      local title=`echo $REPLY | sed -r 's/^.*title="([^"]+)".*/\1/'`
      echo "   " $title --- $link
      let "i+=1"
   done
}

function search_google {
   local line=$1
   local url='http://google.com/search?q='$line
   local site=`wget --user-agent="Lynx (textmode)" -O - "$url" 2> /dev/null`
   local qlist=`echo $site | grep '/url?q=' |\
          sed -r 's|/url\?q=|\n&|g' | sed -nr 's|^/url\?q=([^&]*)&amp;.*$|\1|p'`
   if [ -z "$qlist" ]; then
      return
   fi
   local i=0
   echo "$qlist" | while IFS= read; do
      if (( i >= 5 )); then
         break;
      fi
      echo "$REPLY"
      let "i+=1"
   done
}

function search_google_so {
   search_google "$1+site:stackoverflow.com"
}

while IFS= read; do
   res=`echo "$REPLY" | grep -E '(error|warning)'`
   echo "$REPLY"
   if [ -n "$res" ]; then
      line=`echo $REPLY | grep -E '(error|warning)' |\
            sed 's/^.*warning: //' | sed 's/^.*error: //' |\
            sed 's/\[.*\]$//' | sed 's/ /+/g'`
      echo "SO:"
      search_so $line
      echo "Google-SO:"
      search_google_so $line
      echo "Google:"
      search_google $line
   fi
done
