# -*- coding: utf-8 -*-
#
# Copyright © 2009-2014 The Caffeine Developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import os
from gi.repository import Gtk, GObject
import ctypes
import argparse
import signal

## local modules
import caffeine
import core
import applicationinstance
import logging

logging.basicConfig(level=logging.INFO)

class GUI(object):
    def __init__(self):
        self.Core = core.Caffeine()
        
def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    GObject.threads_init()

    ## register the process id as 'caffeine'
    libc = ctypes.cdll.LoadLibrary('libc.so.6')
    libc.prctl(15, 'caffeine', 0, 0, 0)
  
    ## handle command line arguments
    parser = argparse.ArgumentParser(prog='caffeine', description='Prevent desktop idleness in full-screen mode')
    parser.add_argument('-V', '--version', action='version', version='caffeine ' + caffeine.VERSION)
    parser.parse_args()
    
    ## Makes sure that only one instance of the Caffeine is run for
    ## each user on the system.
    pid_name = '/tmp/caffeine' + str(os.getuid()) + '.pid'
    appInstance = applicationinstance.ApplicationInstance(pid_name)
    if appInstance.isAnother():
        appInstance.killOther()

    GUI()
    appInstance.startApplication()
    Gtk.main()
    appInstance.exitApplication()
