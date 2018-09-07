#!/usr/bin/python
# -*- coding: utf-8 -*-
import pathlib
import os
import shutil

'''Author: Y.J. Wang @2018.09.01
Descrtiption:
define folder/file and database control module'''

# Class for subfolder collect method and new folder creation
class dirFunc:
    def __init__(self, *args):
        pass

    # open the open file gui (tkinter)
    # return (True/None, folder path)
    def openRawdir(self):
        from tkinter.filedialog import askdirectory
        folder = askdirectory()
        if folder:
            return(1, folder)
        else:
            return(0, 'no select dir')

    # consume the folder/file in the foler pathlib
    # return tuple: (folder path, [subfolder name], [file])
    def walkDir(self, dirPath):
        dirList = next(os.walk(dirPath))
        return dirList

    # create the analizy folder
    # the folder path is $analizyDir/sub-folder/[Pass/Fail]
    # return tuple(True/None, /$analizyDir)
    def createAnalizydir(self, dirList):
        rootpath = os.getcwd() + '\\' + 'analizyDir'
        # delete the analizyDir folder
        shutil.rmtree(rootpath, ignore_errors=True)
        # create the analizyDir folder
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


# Class for Mongo DB control method definition
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
