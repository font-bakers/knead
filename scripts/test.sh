#!/bin/bash
set -e

# Hash all files in data/ and write it to a temporary file.
find ../data/ -type f -exec shasum {} \; > tmp0

# Convert ttf to ttx. Rehash, and if data/ differs, test fail.
python main.py --input ttf --output ttx --directory ../data/
find ../data/ -type f -exec shasum {} \; > tmp1
diff tmp0 tmp1 > /dev/null
if [ $? -eq 1 ]
then
    echo "Test failed from ttf to ttx."
    rm tmp*
    exit 1
else
    echo "Success!"
fi

# Convert ttx to json. Rehash, and if data/ differs, test fail.
python main.py --input ttx --output json --directory ../data/
find ../data/ -type f -exec shasum {} \; > tmp2
diff tmp0 tmp2 > /dev/null
if [ $? -eq 1 ]
then
    echo "Test failed from ttf to ttx."
    rm tmp*
    exit 1
else
    echo "Success!"
fi

# Remove temporary files.
rm tmp*
