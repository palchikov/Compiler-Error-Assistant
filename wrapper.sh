#!/bin/sh

executable=$1
shift
script=$1
shift

function usage() {
   echo "Wrapper usage: $script [stfw flags] -- [$executable flags]"
   echo -n "Utility "
   ./stfw.py --help
}

STFW_FLAGS=

while [ \( "$1" != '--' \) -a -n "$1" ]; do
   if [ \( $1 == '--help' \) -o \( $1 == '-h' \) ]; then
      usage
      exit 0
   fi
   STFW_FLAGS=$STFW_FLAGS' '$1
   shift
done

if [ -z $1 ]; then
   usage
   exit 0
fi

shift

$executable $* 2>&1 | ./stfw.py $STFW_FLAGS
