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


from gi.repository import GObject, GLib
import argparse
import signal
import logging

## local modules
import caffeine
import core

logging.basicConfig(level=logging.INFO)

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    GObject.threads_init()

    ## handle command line arguments
    parser = argparse.ArgumentParser(prog='caffeine', description='Prevent desktop idleness in full-screen mode')
    parser.add_argument('-V', '--version', action='version', version='caffeine ' + caffeine.VERSION)
    parser.parse_args()

    core.Caffeine()
    GLib.MainLoop().run()
