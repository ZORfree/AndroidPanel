# -*- coding: utf8 -*-

import subprocess
import os

class AndroidCommands(object):
  def __init__(self,device):
    self._device = device
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
      except:
          self.enabled = 0
      result = [l for l in result if not l.startswith('WARNING')]
      return result




# print(adb.RunShellCommand("cat /proc/stat"))
# print(adb.RunShellCommand("ps"))