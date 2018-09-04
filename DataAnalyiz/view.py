import os
import sys
import time
import model
import tkinter as tk
from math import trunc
from functools import wraps
import controller
dd = controller.analizyFun()
print (dd.fileDic)

def progressBar(func):

    fileDic = controller.analizyFun().fileDic
    @wraps(func)
    def progress(self):
        print ('1')
        for station in self.fileDic:
            for log in self.fileDic[station]:
                if dirFunc().walkDir(self.rawpath)[1]:
                    logPath = self.rawpath + '\\' + station + '\\' + log
                else:
                    logPath = self.rawpath + '\\' + log
                with open(logPath, 'r') as f:
                    content = f.read()
                f.close()
                a = func(self, station, log, content)
        return a
    return progress
