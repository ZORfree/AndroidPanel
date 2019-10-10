# -*- coding: utf8 -*-

import subprocess
import os

class AndroidCommands(object):
    def __init__(self,device):
        self._device = device
        self.showPage = False
        self.proPage = False
        self.scriptPage = False
        self.enabled = 1
        try:
            subprocess.Popen('adb -s ' + self._device + ' root && ' + 'adb -s ' + self._device + ' remount')
        except:
            self.enabled = 0
    def RunShellCommand(self,command):
        try:
            result = subprocess.Popen('adb -s ' + self._device + ' shell ' + command, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    stdin=subprocess.PIPE, shell=True).communicate()[0].strip().splitlines()
            result = [l.decode("utf-8") for l in result if not l.decode("utf-8").startswith('WARNING')]
            # print("result:%s" % result)
            return result
        except:
          self.enabled = 0

    def RunShellCommandNoResult(self, command):
        subprocess.call('adb -s ' + self._device + ' shell ' + command,stdout=subprocess.PIPE)

    def ospopen(self,command):
        try:
            os.popen('adb -s ' + self._device + ' shell ' + command)
        except:
          self.enabled = 0




# print(adb.RunShellCommand("cat /proc/stat"))
# print(adb.RunShellCommand("ps"))