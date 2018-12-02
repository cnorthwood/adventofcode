#!/bin/bash

set +ex

YEAR="${1}"
DAY="${2}"

cd /code
git pull
git checkout ${YEAR}day${DAY}

time sh -c './part1.py; ./part2.py'
