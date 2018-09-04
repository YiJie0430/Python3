#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pathlib
import re
from view import progressBar
from datetime import datetime
from model import dirFunc
from functools import wraps
from shutil import copyfile
from math import trunc


class analizyFun:
    def __init__(self, *args):
        self.fileFolder = list()
        self.parseResult = list()
        self.fileDic = dict()
        self.fileCunt = int()
        self.rawpath = dirFunc().openRawdir()[1]
        self.regex = [r'Test Result.*', r'MAC Address.*',
                      r'^Start\sTime.*', r'Station.\s.*?\s', r'dut_id.*']
        self.regexDic = {'TestResult': r'Test Result.*',
                         'MAC': r'MAC.*',
                         'StartTime': r'Start\sTime.*(................:.......)',
                         'Total': r'otal\s.*',
                         'StationID': r'Station.\s.*?\s',
                         'DutID': r'dut_id.*|station_ip.*',
                         'FailReason': r'ErrorCode.*\s?.*|Fail.*|.*-\sfail|.*FAIL..*|failed.*'}

    def fileCollect(self):
        fileCunt = int()
        dirList = dirFunc().walkDir(self.rawpath)
        if dirList[1]:
            for dir in dirList[1]:
                dirPath = self.rawpath + '\\' + dir
                fileList = next(os.walk(dirPath))[-1]
                self.fileDic.update({dir: fileList})
                self.fileCunt += len(fileList)
        else:
            dir = self.rawpath.split('/')[-1]
            dirPath = self.rawpath
            fileList = next(os.walk(dirPath))[-1]
            self.fileDic.update({dir: fileList})
            self.fileCunt += len(fileList)
        return self.fileCunt

    def logRead(func):
        @wraps(func)
        @progressBar
        def walk_read(self):
            anaDir = dirFunc().createAnalizydir(list(self.fileDic.keys()))[1]
            # andDir format: (mainpath, subfolder, file)
            for station in self.fileDic:
                for log in self.fileDic[station]:
                    if dirFunc().walkDir(self.rawpath)[1]:
                        logPath = self.rawpath + '\\' + station + '\\' + log
                    else:
                        logPath = self.rawpath + '\\' + log
                    with open(logPath, 'r') as f:
                        content = f.read()
                    f.close()
                    result = func(self, content)
                    # result format: [result,mac,start_time,station,dut_id]
                    if not result[0]:
                        copyfile(logPath, '{}/{}/Fail/{}'.format(anaDir[0],
                                                                 station,
                                                                 log))
                    else:
                        copyfile(logPath, '{}/{}/PASS/{}'.format(anaDir[0],
                                                                 station,
                                                                 log))
                    self.parseResult.append(result)
            return self.parseResult
        return walk_read

    @logRead
    def logParse(self, data):
        logResult = list()
        for regex in self.regexDic.keys():
            pattern = re.compile(self.regexDic[regex], re.MULTILINE)
            # method: re.compile(regex, flag = re.MULTILINE | re.IGNORECASE)
            parsing = (pattern.findall(data))
            # print ('parsing {}: {}'.format(regex, parsing))
            if parsing:
                parsing[0] = parsing[0].replace('=', ':')
                if 'time' in regex.lower():
                    parse = datetime.strptime(parsing[0],
                                              "%a %b %d %H:%M:%S %Y"
                                              ).isoformat()
                    # parse format -> ex: '2018-08-14T23:02:27'
                elif 'reason' in regex.lower():
                    if logResult[0] == 1:
                        parse = 'NONE'
                    else:
                        parse = re.split(r'\nEnd\sTime', parsing[-1])[0]
                else:
                    parse = parsing[0].split(':', 1)[-1].split('\n')[0].strip()
                    if 'PASS' in parse.upper():
                        parse = 1
                    elif 'FAIL' in parse.upper():
                        parse = 0
            else:
                parse = 'NONE'
            logResult.append(parse)
        return logResult


def main():
    af = analizyFun()
    af.fileCollect()
    result = af.logParse()
    for i in result:
        if not i[0]:
            print (i)
    print (len(result))


if __name__ == '__main__':
    main()
