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

    def openRawdir(self):
        from tkinter.filedialog import askdirectory
        folder = askdirectory()
        if folder:
            return(1, folder)
        else:
            return(0, 'no select dir')

    def walkDir(self, dirPath):
        dirList = next(os.walk(dirPath))
        return dirList

    def createAnalizydir(self, dirList):
        rootpath = os.getcwd() + '\\' + 'analizyDir'
        shutil.rmtree(rootpath, ignore_errors=True)
        pathlib.Path(rootpath).mkdir(exist_ok=True)
        for dir in dirList:
            subpath = rootpath + '\\' + dir
            pathlib.Path(subpath).mkdir(exist_ok=True)
            for subdir in ['Pass', 'Fail']:
                subdirpath = subpath + '\\' + subdir
                pathlib.Path(subdirpath).mkdir(exist_ok=True)
        try:
            if next(os.walk(rootpath))[1] == dirList:
                return (1, next(os.walk(rootpath)))
            else:
                return (0, '{} creat failed'.format(rootpath))
        except Exception:
            return (0, 'err')


class dbFunction:
    def _init_(self, *args):
        pass


def main():
    df = dirFunc()
    a = df.openRawdir()
    a = df.walkDir(a[1])
    print (a)
    a = df.createAnalizydir(a[1])
    print (a)


if __name__ == '__main__':
    main()
