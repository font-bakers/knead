#!/bin/bash
set -e

# Hash all files in data/ and write it to a temporary file.
HASH0=$(find ../data/ -type f -exec shasum {} \;)

# Convert ttf to ttx. Rehash, and if hashes differ, fail test.
python main.py --input ttf --output ttx --directory ../data/
HASH1=$(find ../data/ -type f -exec shasum {} \;)
if [ "$HASH0" != "$HASH1" ]
then
    echo "Test failed from ttf to ttx."
    exit 1
else
    echo "Success from ttf to ttx!"
fi

# Convert ttx to json. Rehash, and if hashes differ, fail test.
python main.py --input ttx --output json --directory ../data/
HASH2=$(find ../data/ -type f -exec shasum {} \;)
if [ "$HASH1" != "$HASH2" ]
then
    echo "Test failed from ttx to json."
    exit 1
else
    echo "Success from ttx to json!"
fi
