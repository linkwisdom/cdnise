#!bin/sh

find ~/pan/fengchao/css/common -type f -name '*.css' | xargs python cdn.py
