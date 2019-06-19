#!/bin/bash
set -e

# Hash all files in data/ and write it to a temporary file.
HASH0=$(find data/ -type f -exec shasum {} +)
find data/ -type f -exec shasum {} +
echo

# Convert ttf to ttx. Rehash, and if hashes differ, fail test.
knead --input ttf --output ttx --directory data/
HASH1=$(find data/ -type f -exec shasum {} +)
find data/ -type f -exec shasum {} +
if [ "$HASH0" != "$HASH1" ]
then
    echo "Test failed from ttf to ttx."
    exit 1
else
    echo "Success from ttf to ttx!"
fi
echo

# Convert ttx to json. Rehash, and if hashes differ, fail test.
knead --input ttx --output json --directory data/
HASH2=$(find data/ -type f -exec shasum {} +)
find data/ -type f -exec shasum {} +
if [ "$HASH0" != "$HASH2" ]
then
    echo "Test failed from ttx to json."
    exit 1
else
    echo "Success from ttx to json!"
fi
echo

# Serialized protobuf output change upon every write, so we cannot check
# correctness by hashing.  The next best thing is to merely convert json to pb
# and check that nothing fails.
knead --input json --output pb --directory data/
NUMPBS=$(ls -1 data/pb | wc -l)
ls -1 data/pb | wc -l
if [ $NUMPBS != 70 ]
then
    echo "Test failed from json to pb."
    exit 1
else
    echo "Success from json to pb!"
fi
echo

# Convert pb to npy. Rehash, and if hashes differ, fail test.
knead --input pb --output npy --directory data/
rm -rf data/pb/  # Clean up after ourselves.
HASH3=$(find data/ -type f -exec shasum {} +)
find data/ -type f -exec shasum {} +
if [ "$HASH0" != "$HASH3" ]
then
    echo "Test failed from pb to npy."
    exit 1
else
    echo "Success from pb to npy!"
fi
echo
