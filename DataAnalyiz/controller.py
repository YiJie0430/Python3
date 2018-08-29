#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pathlib
from model import dirFunc


class analizyFun:
    def __init__(self, *args):
        self.fileFolder = list()
        self.fileDic = dict()
        self.rawpath = args[0]

    def fileCollect(self):
        dirList = dirFunc().walkDir(self.rawpath)
        for dir in dirList:
            dirPath = self.rawpath + '\\' + dir
            fileList = next(os.walk(dirPath))[-1]
            self.fileDic.update({dir: fileList})
            # self.fileFolder.append(fileList)
        return self.fileDic

    def logParse(self, log):
        with open(log, 'r') as f:
            read_data = f.read()
            # print (read_data)
        f.close()
        return read_data

    def fileAnalizy(self, files):
        anaDir = dirFunc().createAnalizydir(list(files.keys()))[1][0]
        print (anaDir)
        for station in files:
            for log in files[station]:
                logPath = self.rawpath + '\\' + station + '\\' + log
                a = self.logParse(logPath)
                print (a)


def main():
    dirpath = dirFunc().openRawdir()[1]
    af = analizyFun(dirpath)
    fileDic = af.fileCollect()
    af.fileAnalizy(fileDic)



if __name__ == '__main__':
    main()
