#!/bin/bash

find ../data/ -type f -exec sha1sum {} \; > tmp0

python knead.py --input font --output ttx --directory ../data/

find ../data/ -type f -exec sha1sum {} \; > tmp1
diff tmp0 tmp1 > /dev/null
if [ $? -eq 1 ]
then
    echo "Test failed from font to ttx."
    rm tmp0 tmp1
    exit 1
fi

rm tmp0 tmp1
