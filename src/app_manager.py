# -*- coding: utf-8 -*-

# Copyright (C) 2010 - 2012 Sebastian Ruml <sebastian.ruml@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 1, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from fswatcher import FSWatcher
from api_server import ApiServer
from config import Config
from configuration import Configuration
from systray import Systray
from daemon import Daemon
from web_server import WebServer
import globals
import log

import os


# Initialize some global variables
globalVars = globals.Globals()
globalVars.baseDir = os.path.dirname(os.path.realpath(__file__))


class AppManager(Daemon):
    def __init__(self, pidfile, debug=False):
        Daemon.__init__(self, pidfile=pidfile, verbose=0)

        self._systray = None

        # Get the globals
        self._globals = globals.Globals()

        # Create the logger
        self._logger = log.Logger(self._globals.logFile)

		# Load settings
        self._configOld = Config(self._globals.cfgFile, self._globals.DEFAULT_CONFIG)
        self._config = Configuration()
        self._globals.config = self._config
        self._config.debugEnabled = debug

        # Set the log level
        self._logger.set_level(self._config.logLevel)

    def run(self):
        self._logger.info("Starting PythonDrop v" + self._globals.version + "...")

		# Create and start the API server
        if self._config.enableApi:
            self._api_server = ApiServer(self, self._config.tcpListenIp, self._config.tcpListenPort)

        # Start the web server
        if self._config.enableWebServer:
            self._web_server = WebServer()

        # Check if the systray should be shown
        #if self._config.enableSystray:
        if True:
            self._logger.debug("Creating systray...")
            self._systray = Systray(self._globals)

		# Create the file watcher
        self._fswatcher = FSWatcher(self._configOld)

        self._fswatchers = []
        for share in self._config.shares:
            print share.sync_folder

        # Start watching and syncing files
        self._fswatcher.watch()

        # TODO: Create a thread for every share

    def start(self):
        Daemon.start(self)

    def stop(self):
        # TODO: Stop the fswatcher and the web server
        self.exit()
        Daemon.stop(self)

    def restart(self):
        self.stop()
        self.start()

    def pause(self):
        pass

    def exit(self):
        #if self._config.get_option('enableGui', 'general'):
        #    self._systray.exit()
        pass
