#!/usr/bin/python
# -*- coding: utf-8 -*-
import pathlib
import os
import shutil
import time


class dirFunc:
    def __init__(self, *args):
        pass
        # rawDir = args[0]
        # analizyDir = args[1]

    def createAnalizydir(self, dirlist):
        path = os.getcwd() + '\\' + 'analizyDir'
        pathlib.Path(path).mkdir(exist_ok=True)
        # shutil.rmtree(path, ignore_errors=True)
        for dir in dirlist:
            subpath = path + '\\' + dir
            pathlib.Path(subpath).mkdir(exist_ok=True)
        try:
            if next(os.walk(path))[1] == dirlist:
                return (1, next(os.walk(path)))
            else:
                return (0, '{} creat failed'.format(path))
        except Exception:
            return (0, 'err')


    def walkDir(self, rawDir):
        print (rawDir)
        dirname = next(os.walk(rawDir))[1]; print (dirname)
        return dirname


def openDir():
    from tkinter.filedialog import askdirectory
    folder = askdirectory()
    if folder:
        return(1, folder)
    else:
        return(0, 'no select dir')

if __name__ == '__main__':
    df = dirFunc()
    a = openDir()
    a = df.walkDir(a[1])
    a = df.createAnalizydir(a); print (a)


    '''
    a = createAnalizydir('testdir_')
    print (a)
    a = openDir()
    print (a)
    '''
