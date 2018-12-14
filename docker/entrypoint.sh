#!/bin/bash

set -eo pipefail

YEAR="${1}"
DAY="${2}"

cd /code/${YEAR}/`printf %02d $DAY`/

if [ -f "part2.py" ] ; then
    time sh -c './part1.py; ./part2.py'
elif [ -f "challenge2.py" ] ; then
    time sh -c './challenge.py; ./challenge2.py'
elif [ -f "challenge.py" ] ; then
    time sh -c './challenge.py'
elif [ -f "code.py" ] ; then
    time sh -c './code.py'
else
    echo "not sure how to run this"
    exit 1
fi
