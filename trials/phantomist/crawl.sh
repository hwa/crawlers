#!/bin/bash

URLS_FILE=$1

OUT_DIR=data/`basename $URLS_FILE`

SCRIPT=weibo-crawler.js
PHANTOMJS="../vendor/phantomjs-1.8.1-linux-x86_64/bin/phantomjs  --load-images=no $SCRIPT"

# if [ ! -d $OUT_DIR ]
# then
#     mkdir $OUT_DIR
# fi

for url in `cat $URLS_FILE`
do
    echo crawling $url
    $PHANTOMJS $url $OUT_DIR/$url
done

    
