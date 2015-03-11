# Caffeine Plus

Caffeine Plus is a small daemon that prevents the desktop from becoming idle
(and hence the screen saver and/or blanker from activating). It does this
automatically when the active window is full-screen, or on demand when enabled
through its system tray icon.

This is a fork of [Caffeine 2.7](http://launchpad.net/caffeine/) which restores
the system tray icon for toggling it on and off. Manual toggling is the primary
use case for many users, but the original author is [unwilling](https://bugs.launchpad.net/caffeine/+bug/1321750)
to restore that functionality.

I don't know Python, so this is a bit of copypasta from [Caffeine 2.5](https://github.com/mildmojo/caffeine-plus/tree/2.5)
and the [AppIndicator docs](https://wiki.ubuntu.com/DesktopExperienceTeam/ApplicationIndicators#Python_version).

## System requirements

- Any Linux desktop system that offers the `org.freedesktop.ScreenSaver` DBus API.
This includes, but is not limited to, Linux Mint 16 and Ubuntu 14.04. Probably
works on lots of older distributions, too.

- Python (Python 3 if you run it directly from the source tree w/o installing)

- `apt-get install python-xlib gir1.2-appindicator3-0.1` (python3-xlib if
running w/o installing)

## Installation

- `sudo python setup.py install --prefix /usr`

- (optional) To have Caffeine Plus run on startup, add it to your System
Settings => Startup Programs list.

## License

Caffeine Plus is distributed under the GNU General Public License, either version
3, or (at your option) any later version. See LICENSE.

The Caffeine Plus status icons are Copyright (C) 2014 mildmojo
(http://github.com/mildmojo), and distributed under the terms of the GNU Lesser
General Public License, either version 3, or (at your option) any later version.
See LICENSE.LESSER.

The Caffeine Plus SVG shortcut icons are Copyright (C) 2009 Tommy Brunn
(http://www.blastfromthepast.se/blabbermouth), and distributed under the
terms of the GNU Lesser General Public License, either version 3, or (at
your option) any later version. See LICENSE.LESSER.

Caffeine Plus uses pyewmh from http://sf.net/projects/pyewmh
