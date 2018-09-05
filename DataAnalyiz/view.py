#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import tkinter as tk
from tkinter import ttk
from functools import wraps
from controller import analizyFun
from model import dirFunc


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


def progressBar(cunt):
    def _BAR(func):
        @wraps(func)
        def progress(analizyFun):
            bar = barStatus(analizyFun.fileCollect())
            anaDir = dirFunc().createAnalizydir(list(analizyFun.fileDic.keys()))[1]
            # andDir format: (mainpath, subfolder, file)
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
                    bar.update()
            return parsing
        return progress
    return _BAR


@progressBar(0)
def startAnalizy(*args):
    return analizyFun.logParse(args[0], args[1], args[2], args[3], args[4], args[5])


def main():
    result = startAnalizy(analizyFun())
    for i in result:
        if not i[0]:
            print (i)
    print (len(result))


if __name__ == '__main__':
    main()
