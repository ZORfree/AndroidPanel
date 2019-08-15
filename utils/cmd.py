# -*- coding: utf8 -*-

import subprocess
import os

class AndroidCommands(object):
  def __init__(self,device):
    self._device = device
    subprocess.Popen('adb -s ' + self._device + ' root && ' + 'adb -s ' + self._device + ' remount')
    
  def RunShellCommand(self,command):
  	# print('adb -s ' + self._device + ' shell ' + command)
    result = subprocess.Popen('adb -s ' + self._device + ' shell ' + command, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     stdin=subprocess.PIPE, shell=True).communicate()[0].strip().splitlines()
    result = [ l for l in result if not l.startswith('WARNING') ]
    return result

deviceName = os.popen('adb devices').readlines()[1].split()[0]
adb = AndroidCommands(deviceName)


# print(adb.RunShellCommand("cat /proc/stat"))
# print(adb.RunShellCommand("ps"))