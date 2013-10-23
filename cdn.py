#!/usr/bin/env python
# Filename: cdn.py
# author: liandong (liu@liandong.org)
#
# usage:
# find ../src/css -type f -name '*.css' | xargs python cdn.py
## 

import sys
import re


IMG_MAP = {
    #! replace all img
    #"common": "../../common/img/", 
    "bg_icon": "../common/img/bg_icon.png",
    "bg_icon_left": "../common/img/bg_icon_left.png",
    "ui_icon": "../common/img/ui-icon.png",
    "loading": "../common/img/loading.gif"
}

#cdn base path

CDN_PATH = 'http://static.tuiguang.baidu.com/src/common/img/'

#replace function
def replaceImg(fname, source):
    f = file(fname, 'r')
    lines = f.readlines()

    for idx, line in enumerate(lines):
        match = re.match( r'.*url\((.*)\).*', line, re.I)

        if match and (source in line):
            print match.group(1)
            tplStr = re.sub('(../)+common/img/' , CDN_PATH , line)
            lines[idx] = tplStr


    f.close()
    
    ##save the result to source file
    open(fname, 'w').write(''.join(lines))
    f.close()

#end replace


args = sys.argv

# run by shell
# ls common/*.css | xargs python p2cdn.py 
#
if (len(args) > 1):
    for idx, fname in enumerate(args):
        if (idx < 1):
            continue

        for key in IMG_MAP.keys():
            replaceImg(fname, IMG_MAP[key])

        #for key

    #for fname
#end if




