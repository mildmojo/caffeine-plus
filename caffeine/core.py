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

import applicationinstance


os.chdir(os.path.abspath(os.path.dirname(__file__)))

def subprocess_output(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    p.wait()
    return p

class Caffeine(GObject.GObject):

    def __init__(self):
        GObject.GObject.__init__(self)
        
        ## Status string.
        self.status_string = ""

        ## Makes sure that only one instance of Caffeine is run for
        ## each user on the system.
        self.pid_name = '/tmp/caffeine' + str(os.getuid()) + '.pid'
        self.appInstance = applicationinstance.ApplicationInstance( self.pid_name )

        # Set to True when sleep mode has been successfully inhibited somehow.
        self.sleepIsPrevented = False

        self.screenSaverCookie = None

        # Add hook for full-screen check (same interval as mplayer's heartbeat command)
        # FIXME: add capability to xdg-screensaver to report timeout
        GObject.timeout_add(30000, self._check_for_fullscreen)
        
        print self.status_string


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

        if activate and not self.getActivated():
            logging.info("Caffeine has detected a full-screen window, and will auto-activate")
        elif not activate and self.getActivated():
            logging.info("Caffeine detects no full-screen window and is not otherwise activated; deactivating...")
        self.setActivated(activate)

        return True

    def getActivated(self):
        return self.sleepIsPrevented

    def setActivated(self, activate):
        if self.getActivated() != activate:
            self.toggleActivated()

    def toggleActivated(self):
        """This function toggles the inhibition of desktop idleness."""

        self.sleepIsPrevented = not self.sleepIsPrevented

        bus = dbus.SessionBus()
        self.susuProxy = bus.get_object('org.freedesktop.ScreenSaver', '/org/freedesktop/ScreenSaver')
        self.iface = dbus.Interface(self.susuProxy, 'org.freedesktop.ScreenSaver')
        if not self.sleepIsPrevented:
            if self.screenSaverCookie != None:
                self.iface.UnInhibit(self.screenSaverCookie)
        else:
            self.screenSaverCookie = self.iface.Inhibit('net.launchpad.caffeine', "Caffeine is inhibiting desktop idleness")

        if self.sleepIsPrevented:
            logging.info("Caffeine is now preventing desktop idleness")
        else:
            logging.info("Caffeine is now dormant")
