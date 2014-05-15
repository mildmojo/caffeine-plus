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


from gi.repository import GObject
import os
import os.path
import re
import subprocess
import dbus
import logging


os.chdir(os.path.abspath(os.path.dirname(__file__)))

def subprocess_output(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    p.wait()
    return p

class Caffeine(GObject.GObject):

    def __init__(self):
        GObject.GObject.__init__(self)
        
        # Set to True when idleness has been inhibited
        self.sleepIsPrevented = False

        self.screenSaverCookie = None

        # Add hook for full-screen check (same interval as mplayer's heartbeat command)
        # FIXME: add capability to xdg-screensaver to report timeout
        GObject.timeout_add(30000, self._check_for_fullscreen)
        
    def _check_for_fullscreen(self):
        activate = False

        # xvinfo returns 1 on normal exit: https://bugs.freedesktop.org/show_bug.cgi?id=74227
        p = subprocess_output(['xvinfo'])
        if 0 <= p.returncode <= 1:
            # Enumerate the attached screens
            display = os.getenv("DISPLAY")
            screens = []

            # Parse output
            for l in p.stdout.read().splitlines():
                m = re.match('screen #([0-9]+)$', str(l))
                if m:
                    screens.append(m.group(1))

                    # Loop through every screen looking for a full screen window
                    for s in screens:
                        # get ID of active window (the focussed window)
                        p = subprocess_output(['xprop', '-display', display + '.' + s, '-root', '-f', '_NET_ACTIVE_WINDOW', '32x', ' $0', '_NET_ACTIVE_WINDOW'])
                        if p.returncode == 0:
                            m = re.match('.* (.*)$', str(p.stdout.read()))
                            assert(m)
                            active_win = m.group(1)

                            # Check whether window is fullscreen
                            p = subprocess_output(['xprop', '-display', display + '.' + s, '-id', active_win, '_NET_WM_STATE'])
                            if p.returncode == 0:
                                m = re.search('_NET_WM_STATE_FULLSCREEN', str(p.stdout.read()))
                                if m:
                                    activate = True

        # Return True so timeout is rerun
        return True

    def setActivated(self, activate):
        if self.sleepIsPrevented != activate:
            self.sleepIsPrevented = activate

            bus = dbus.SessionBus()
            self.susuProxy = bus.get_object('org.freedesktop.ScreenSaver', '/org/freedesktop/ScreenSaver')
            self.iface = dbus.Interface(self.susuProxy, 'org.freedesktop.ScreenSaver')

            if activate:
                self.screenSaverCookie = self.iface.Inhibit('net.launchpad.caffeine', "Caffeine is inhibiting desktop idleness")
                logging.info("Caffeine is now dormant")
            else:
                if self.screenSaverCookie != None:
                    self.iface.UnInhibit(self.screenSaverCookie)
                logging.info("Caffeine is now preventing desktop idleness")
