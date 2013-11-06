#!/usr/bin/env python
# Filename: cdn.py
# author: liandong (liu@liandong.org)
#
# usage:
# find ../src/css -type f -name '*.css' | xargs python cdn.py
## 

import sys
import re
import time
import os

stamp = int(time.time())
stamp = str(stamp)

##log message here
replace_log = [];
webpath = 'http://static.tuiguang.baidu.com'

#resulve path
# @param fname absPath of file
# @param targetPath, targetPath of source css file
def resolve(fname, targetPath):
    segs = targetPath.split('/')
    pres = re.findall(r'\.\.\/', fname)
    num = len(pres);
    if num > 0:
        return '/'.join(segs[:-num]) + re.sub(r'(\.\.\/)+', '/', fname)
    else:
        return webpath + fname

#resolve path of all images
# @param images , image-pathes to be resolved
# @param targetPath, targetPath of source css file
def resolveAll(images, targetPath):
    imgMap = {}
    for idx, image in enumerate(images):
        if ('http://' in image or 'data:' in image):
            continue
        img = resolve(image, targetPath)
        img = re.sub(r'\.(jpg|gif|png)', r'.\g<1>?v=' + stamp, img)
        imgMap[image] = img      
    return imgMap
#end resolveAll

#repalce images with cdnPath in source-content
# @param source , the css content
# @imgMap, the diction of images to be replaced
def replaceImages(source, imgMap):
    for key in imgMap.keys():
        replace_log.append(key + ' ' + imgMap[key])
        source = source.replace(key, imgMap[key])
    #replace all images
    return source
#end replace images


# replace css images with cdn pathes
# @param fname , the abspath of the css file
# @param webroot, the webroot of your match
def replaceCssImages(fname, webroot, targetFile):
    f = file(fname, 'r')
    lines = f.readlines()

    targetPath = fname.replace(webroot, webpath)

    for idx, line in enumerate(lines):
        images = re.findall(r'url\([\"\']*([^\)\"\']*)[\"\']*\)', line)
        if (len(images) > 0 ):
            imgMap = resolveAll(images, targetPath)
            #
            content = replaceImages(line, imgMap)
            lines[idx] = content
            #print content

    f.close()

    #targetFile = re.sub(r'(\.css)', r'__stamp__\g<1>', targetFile)
    #targetFile = targetFile.replace('_stamp_', stamp);
    #write to target file
    open(targetFile, 'w').write(''.join(lines))
#end repalceAssetImage


## walk dir and replace the url-path with cdn path
def walkDir(source, root):
    webroot = os.path.abspath(root)
    outputDir = os.path.abspath(source + '/_output/')

    if not os.path.exists(outputDir):
        os.mkdir(outputDir)

    for parent, dirnames, filenames in os.walk(source):
        if ('_output' in parent):
            continue

        targetDir = parent.replace(source, source + '/_output/')

        for dirname in dirnames:
            tdir = os.path.join(targetDir, dirname)
            if not os.path.exists(tdir):
                os.mkdir(tdir)
        for filename in filenames:
            filepath = os.path.join(parent, filename)
            [fname, extname] = os.path.splitext(filepath)
            if extname == '.css':
                replaceCssImages(filepath, webroot, targetDir + filename)

        


# run by shell
# python cdn.py ./src/css 

args = sys.argv
anum = len(args)

if anum > 1:
    source = os.path.abspath(args[1])
    root = source + '../../'

if anum > 2:
    root = args[2]

if anum > 3:
    webpath = args[3]

if anum > 1:
    walkDir(source, root)
#end if

#
#
print '############### replaced ############'
print '\n'.join(replace_log)

# print '############### mismatch ############'

# #print '\n'.join(warm_log)

# print '############## the end ##############'





