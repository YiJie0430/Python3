#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import tkinter as tk
from tkinter import ttk
from functools import wraps
from controller import analizyFun
from controller import cutepandas
from model import dirFunc

'''Author: Y.J. Wang @2018.09.01
Descrtiption:
visualize module'''

# class for the progress bar
class barStatus(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self)
        self.cunt = 0
        self.max = args[0]

        self.style = ttk.Style(self)
        # add label in the layout
        self.style.layout('text.Horizontal.TProgressbar',
                          [('Horizontal.Progressbar.trough',
                           {'children': [('Horizontal.Progressbar.pbar',
                                          {'side': 'left', 'sticky': 'ns'})],
                            'sticky': 'nswe'}),
                           ('Horizontal.Progressbar.label', {'sticky': ''})])
        # set initial text
        self.style.configure('text.Horizontal.TProgressbar', text='0 %')
        # create progressbar
        self.variable = tk.DoubleVar(self)
        self.progress = ttk.Progressbar(self, orient="horizontal",
                                        length=200, mode="determinate",
                                        style='text.Horizontal.TProgressbar',
                                        variable=self.variable)

        self.progress['maximum'] = args[0]
        self.progress.pack()

    def consume(self, *args):
        # self.progress['value'] = args[0]
        self.progress.step()
        self.style.configure('text.Horizontal.TProgressbar',
                             text='{:0.1f} %'.format((self.variable.get() / self.max) * 100))  # update label
        self.progress.update()

    def update(self, *args):
        if self.variable.get() >= self.max:
            self.clear()
        else:
            self.after(1, self.consume())

    def clear(self):
        self.destroy()

# decoractor: display the processing progress
def progressBar(cunt):
    def _BAR(func):
        @wraps(func)
        def progress(analizyFun):
            bar = barStatus(analizyFun.fileCollect())
            anaDir = dirFunc().createAnalizydir(list(analizyFun.fileDic.keys()))[1]
            # andDir format: (mainpath, [subfolder], [file])
            for station in analizyFun.fileDic:
                for log in analizyFun.fileDic[station]:
                    if dirFunc().walkDir(analizyFun.rawpath)[1]:
                        logPath = analizyFun.rawpath + '\\' + station + '\\' + log
                    else:
                        logPath = analizyFun.rawpath + '\\' + log
                    with open(logPath, 'r') as f:
                        content = f.read()
                    f.close()
                    parsing = func(analizyFun, content, logPath, anaDir, station, log)
                    '''callback function: logParse()
                       result list: [result, station, log name, script version,
                                     mac, start_time, total_time, station id,
                                     dut id, main issue, sub issue, fail_reason]'''
                    bar.update()
            return parsing
        return progress
    return _BAR


@progressBar(0)
def startAnalizy(*args):
    return analizyFun.logParse(args[0], args[1], args[2], args[3], args[4], args[5])


def main():
    result = startAnalizy(analizyFun())
    for x in result:
        if not x[0]:
            print (x)
    pd_ = cutepandas()
    data = pd_.toDataframd(result)

    logfail = data.loc[data['Main Issue'] != 'NONE']
    count = logfail['Main Issue'].count()
    print (count)

    mainissue = logfail.groupby('Main Issue')
    print (mainissue.size())

    for name in mainissue.size().index:
        print ('{} - count:{}, rate:{:0.1f}%'.format(name,
                                                     mainissue.size().loc[name],
                                                     (mainissue.size().loc[name] / count) * 100))
        subname = logfail.loc[logfail['Main Issue'] == name,
                              ['Log Name', 'Sub Issue']]
        count_ = subname['Sub Issue'].count()
        subissue = subname.groupby('Sub Issue')
        for name_ in subissue.size().index:
            print ('---{} -- count:{}, rate:{:0.1f}%'.format(name_,
                                                             subissue.size().loc[name_],
                                                             (subissue.size().loc[name_] / count_) * 100))
            failreason = logfail.loc[logfail['Sub Issue'] == name_,
                                     ['Log Name', 'Fail Reason']]
            detail = failreason.groupby('Fail Reason')
            for name__ in detail.size().index:
                logname = failreason.loc[failreason['Fail Reason'] == name__,
                                                   ['Log Name']].values
                print ('------{} -- count:{}\n{}'.format(name__,
                                                         detail.size().loc[name__],
                                                         logname))
    '''
    subissue = data.loc[data['Main Issue'] == 'Online issue',
                        ['Log Name', 'Sub Issue']]
    print (subissue)
    subissue_ = subissue.groupby('Sub Issue')
    print (subissue_.size())


    failreason = data.loc[data['Sub Issue'] == 'SNMP Issue',
                          ['Log Name', 'Sub Issue', 'Fail Reason']]
    print (failreason)
    failreason_ = failreason.groupby('Fail Reason')
    print (failreason_.size())

    #print (subissue_.describe(include='all'))
    '''


if __name__ == '__main__':
    main()
