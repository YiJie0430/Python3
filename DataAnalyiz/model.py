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
        self.folder = str()
        self.dirList = list()
        self.rootpath = str()

    # open the open file gui (tkinter)
    # return (True/None, folder path)
    def openRawdir(self):
        from tkinter.filedialog import askdirectory
        self.folder = askdirectory()
        if self.folder:
            return(1, self.folder)
        else:
            return(0, 'no select dir')

    # consume the folder/file in the foler pathlib
    # return tuple: (folder path, [subfolder name], [file])
    def walkDir(self, dirPath):
        self.dirList = next(os.walk(dirPath))
        return self.dirList

    # create the analizy folder
    # the folder path is $analizyDir/sub-folder/[Pass/Fail]
    # return tuple(True/None, /$analizyDir)
    def createAnalizydir(self, dirList):
        self.rootpath = os.getcwd() + '\\' + 'analizyDir'
        # delete the analizyDir folder
        shutil.rmtree(self.rootpath, ignore_errors=True)
        # create the analizyDir folder
        pathlib.Path(self.rootpath).mkdir(exist_ok=True)
        for dir in dirList:
            subpath = self.rootpath + '\\' + dir
            pathlib.Path(subpath).mkdir(exist_ok=True)
            for subdir in ['Pass', 'Fail']:
                subdirpath = subpath + '\\' + subdir
                pathlib.Path(subdirpath).mkdir(exist_ok=True)
        try:
            if next(os.walk(self.rootpath))[1] == dirList:
                return (1, next(os.walk(self.rootpath)))
            else:
                return (0, '{} creat failed'.format(self.rootpath))
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
