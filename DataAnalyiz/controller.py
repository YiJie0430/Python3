#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import pandas as pd
from datetime import datetime
from model import dirFunc
from functools import wraps
from shutil import copyfile

'''Author: Y.J. Wang @2018.09.01
Descrtiption:
file analizy module'''

# Class for the file analizy
class analizyFun:
    def __init__(self, *args):
        self.fileFolder = list()
        self.parseResult = list()
        self.fileDic = dict()
        self.fileCunt = int()
        self.rawpath = dirFunc().openRawdir()[1]
        # classify the fail issue
        self.issue = {'MES issue': ['check mes', 'get sn'],
                      'US Cal. issue': ['freq:', 'freq='],
                      'DS Cal. issue': ['dscal'],
                      'Ether issue': ['switch'],
                      'COM Port issue': ['cli', 'connection', '**',
                                         'return :'],
                      'Tftp issue': ['cmcert'],
                      'Online issue': [{'D3.1_OFDM_MER': ['ofdm rxmer'],
                                        'D3.0_DS_Lock': ['ds channel lock'],
                                        'D3.0_US_Power': ['us power check'],
                                        'SNMP Issue': ['query ds frequency',
                                                       'snmp get'],
                                        'D3.1_OFDMA_SNR': ['ofdma snr'],
                                        'D3.0_US_SNR': ['scqam snr']}],
                      'Booting issue': ['booting port'],
                      'LED issue': [' led '],
                      'I2C issue': ['device id'],
                      'USB issue': ['usb mount', 'mount', 'usb content'],
                      'Script issue': ['traceback']}
        self.subissue = {}
        # Regular expression
        self.regexDic = {'TestResult': r'Test Result.*',
                         'ScriptVersion': r'(?<=ersion.)(.*)(?=\s,)',
                         'MAC': r'MAC.*',
                         'StartTime': r'Start\sTime.*(................:.......)',
                         'Total': r'otal\s.*',
                         'StationID': r'Station.\s.*?\s',
                         'DutID': r'dut_id.*|station_ip.*',
                         'FailReason': r'ErrorCode.*\s?.*|Fail.*|.*-\sfail|.*FAIL..*|failed.*|.*\sEnd\sTime'}

    # consume the number of files
    def fileCollect(self):
        fileCunt = int()
        dirList = dirFunc().walkDir(self.rawpath)
        # dirList format: (folder path, [subfolder], [file])
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

    # catch main fail issue and reason
    def aiLike(self, *args):
        # args[0]: Fail reason related parisng string
        parse = None
        for idx, string in enumerate(args[0]):
            if 'Test Result' in string and len(args[0]) == 1:
                if 'None' in string:
                    return ['Script issue', 'no response', string]
                else:
                    return ['Others', 'NONE', string]
            elif 'Test Result' in string and len(args[0]) > 1:
                args[0].pop(idx)
                continue
            else:
                if 'ErrorCode' in string or idx == (len(args) - 1):
                    parse1 = re.split(r'\nEnd\sTime', string)[0]
                    parse = re.split(r'ErrorCode.*?:', parse1)[-1]
                    for mainissue in list(self.issue.keys()):
                        if type(self.issue[mainissue][0]) is dict:
                            for subissue in list(self.issue[mainissue][0].keys()):
                                for event in self.issue[mainissue][0][subissue]:
                                    if event in parse.lower():
                                        return [mainissue, subissue, parse]
                        else:
                            for event in self.issue[mainissue]:
                                if event in parse.lower():
                                    return [mainissue, parse, parse]
                    # return [parse, parse, parse]
        if not parse:
            if 'None' in args[0][-1]:
                return ['Script issue', 'no response', 'NONE']
            #else:
                #return [re.split(r'\nEnd\sTime', args[0][-1])[0], 'NONE']


    # decoractor: record the parsing value and copy the log to certain folder
    def logRead(func):
        @wraps(func)
        def walk_read(*args):
            '''args[0]: class self obect
               args[1]: current file content
               args[2]: current-filepath
               args[3]: (rootpath, [all-subfolder], [all-file])
               args[4]: current-subfolder name
               args[5]: current-file name'''
            result = func(args[0], args[1], args[4], args[5])
            '''callback function: logParse()
               result list: [result, station, log name, script version, mac,
                            start_time, total_time, station id, dut id, fail_reason]'''
            if not result[0]:
                copyfile('{}'.format(args[2]),
                         '{}/{}/Fail/{}'.format(args[3][0], args[4], args[5]))
            else:
                copyfile('{}'.format(args[2]),
                         '{}/{}/Pass/{}'.format(args[3][0], args[4], args[5]))
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
                    # switch datetime to y-M-D H:M:Sec
                    parse = datetime.strptime(parsing[0],
                                              "%a %b %d %H:%M:%S %Y"
                                              ).isoformat()
                    # parse format -> ex: '2018-08-14T23:02:27'
                elif 'reason' in regex.lower():
                    if logResult[0] == 1:
                        parse = 'NONE'
                    else:
                        parse = self.aiLike(parsing)
                        try:
                            parse = self.aiLike(parsing)
                        except:
                            parse = 'valueErr'
                            print ('valueError')
                else:
                    parse = parsing[0].split(':', 1)[-1].split('\n')[0].strip()
                    if 'PASS' in parse.upper():
                        parse = 1
                    elif 'FAIL' in parse.upper():
                        parse = 0
            else:
                parse = 'NONE'
            if type(parse) is list:
                logResult.extend(parse)
            else:
                logResult.append(parse)
        logResult.insert(1, args[1])
        logResult.insert(2, args[2])
        return logResult


class cutepandas:
    def __init__(self, *args, **kwargs):
        self.columns = ['Test Result', 'Station', 'Log Name', 'Script Version',
                        'MAC', 'Start Time', 'Total Time', 'Station ID',
                        'Dut ID', 'Main Issue', 'Sub Issue', 'Fail Reason']

    def toDataframd(self, *args):
        return pd.DataFrame(args[0], columns=self.columns)


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
