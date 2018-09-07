#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pathlib
import re
from datetime import datetime
from model import dirFunc
from functools import wraps
from shutil import copyfile


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
                         'ScriptVersion': r'(?<=ersion.)(.*)(?=\s,)',
                         'MAC': r'MAC.*',
                         'StartTime': r'Start\sTime.*(................:.......)',
                         'Total': r'otal\s.*',
                         'StationID': r'Station.\s.*?\s',
                         'DutID': r'dut_id.*|station_ip.*',
                         'FailReason': r'ErrorCode.*\s?.*|Fail.*|.*-\sfail|.*FAIL..*|failed.*|.*\sEnd\sTime'}

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
        def walk_read(*args):
            result = func(args[0], args[1])
            # result format: [result,mac,start_time,total_time,station,dut_id,fail_reason]
            if not result[0]:
                copyfile('{}'.format(args[2]),
                         '{}/{}/Fail/{}'.format(args[3][0], args[4], args[5]))
            else:
                copyfile('{}'.format(args[2]),
                         '{}/{}/PASS/{}'.format(args[3][0], args[4], args[5]))
            args[0].parseResult.append(result)
            return args[0].parseResult
        return walk_read

    @logRead
    def logParse(self, *args):
        logResult = list()
        for regex in self.regexDic.keys():
            parse = None
            pattern = re.compile(self.regexDic[regex], re.MULTILINE)
            # method: re.compile(regex, flag = re.MULTILINE | re.IGNORECASE)
            parsing = (pattern.findall(args[0]))
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
                        try:
                            for idx, string in enumerate(parsing):
                                if 'Test Result' in string and len(parsing) == 1:
                                    parse = 'Others'
                                    break
                                if 'Test Result' in string and len(parsing) > 1:
                                    parsing.pop(idx)
                                    continue
                                if 'ErrorCode' in string:
                                    parse = re.split(r'\nEnd\sTime', string)[0]
                                    break
                            if not parse:
                                if 'None' in parsing[-1]:
                                    parse = 'Script trace'
                                else:
                                    parse = re.split(r'\nEnd\sTime', parsing[-1])[0]
                        except:
                            print ('valueError')


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
    anaDir = dirFunc().createAnalizydir(list(af.fileDic.keys()))[1]
    # andDir format: (mainpath, subfolder, file)
    for station in af.fileDic:
        for log in af.fileDic[station]:
            if dirFunc().walkDir(af.rawpath)[1]:
                logPath = af.rawpath + '\\' + station + '\\' + log
            else:
                logPath = af.rawpath + '\\' + log
            with open(logPath, 'r') as f:
                content = f.read()
            f.close()
            result = af.logParse(content, logPath, anaDir, station, log)

    for i in result:
        if not i[0]:
            print (i)
    print (len(result))


if __name__ == '__main__':
    main()
