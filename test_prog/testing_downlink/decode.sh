#!/bin/bash

gzip -d -q $1.gz
sleep 1
base64 -d $2 > $2.jpg
rm $1