#!/bin/bash

find ../data/ -type f -exec sha1sum {} \; > tmp0

python knead.py --input font --output ttx --directory ../data/

find ../data/ -type f -exec sha1sum {} \; > tmp1
diff tmp0 tmp1 > /dev/null
is_diff=$?
if [ $is_diff -eq 1 ]
then
    echo "Files are different."
    exit 1
else
    echo "Success!"
fi

rm tmp0 tmp1
