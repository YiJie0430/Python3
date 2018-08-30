#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pathlib
import re
from model import dirFunc
from functools import wraps


class analizyFun:
    def __init__(self, *args):
        self.fileFolder = list()
        self.parseResult = list()
        self.fileDic = dict()
        self.rawpath = args[0]
        self.regex = [r'Test Result.*', r'MAC Address.*',
                      r'^Start\sTime.*', r'Station.\s.*?\s', r'dut_id.*']
        self.regexDic = {'TestResult': r'Test Result.*',
                         'MAC': r'MAC Address.*',
                         'StartTime': r'Start\sTime.*(................:.......)',
                         'StationID': r'Station.\s.*?\s',
                         'DutID': r'dut_id.*'}

    def fileCollect(self):
        dirList = dirFunc().walkDir(self.rawpath)
        for dir in dirList:
            dirPath = self.rawpath + '\\' + dir
            fileList = next(os.walk(dirPath))[-1]
            self.fileDic.update({dir: fileList})
            # self.fileFolder.append(fileList)
        return self.fileDic

    def logParse(self, data):
        for regex in self.regexDic.keys():
            pattern = re.compile(self.regexDic[regex], re.MULTILINE | re.IGNORECASE)
            parsing = (pattern.findall(data))
            print ('parsing {}: {}'.format(regex, parsing))
            if parsing:
                if regex is 'StartTime':
                    parse = parsing[0]
                else:
                    parse = parsing[0].split(':')[-1].split('\n')[0].strip()
                print (parse)
            else:
                parse = 'NONE'
            self.parseResult.append(parse)
        return self.parseResult

    def fileAnalizy(self, files):
        anaDir = dirFunc().createAnalizydir(list(files.keys()))[1][0]
        print (anaDir)
        for station in files:
            for log in files[station]:
                logPath = self.rawpath + '\\' + station + '\\' + log
                with open(logPath, 'r') as f:
                    content = f.read()
                f.close()
                a = self.logParse(content)
        print (a)
        print (len(a))




def main():
    dirpath = dirFunc().openRawdir()[1]
    af = analizyFun(dirpath)
    fileDic = af.fileCollect()
    af.fileAnalizy(fileDic)



if __name__ == '__main__':
    main()
