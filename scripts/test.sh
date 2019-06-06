#!/bin/bash

# Hash all files in data/ and write it to a temporary file.
find ../data/ -type f -exec shasum {} \; > tmp0

# Convert font to ttx. Rehash, and if data/ differs, test fail.
python main.py --input font --output ttx --directory ../data/
find ../data/ -type f -exec shasum {} \; > tmp1
diff tmp0 tmp1 > /dev/null
if [ $? -eq 1 ]
then
    echo "Test failed from font to ttx."
    rm tmp0 tmp1
    exit 1
fi

# Remove temporary files.
rm tmp0 tmp1
