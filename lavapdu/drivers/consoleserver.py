#! /usr/bin/python

#  Copyright 2016 EfficiOS
#  Author Jonathan Rajotte-Julien <jonathan.rajotte-julien@efficios.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import logging
from lavapdu.drivers.consolerserverbase import ConsoleServerBase
log = logging.getLogger(__name__)


class ConsoleServer(ConsoleServerBase):

    @classmethod
    def accepts(cls, drivername):
        if drivername == "consoleserver":
            return True
        return False

    def _pdu_logout(self):
        log.debug("logging out")
        self.connection.send("\r")
        self.connection.send("quit")
        self.connection.send("\r")
        log.debug("done")

    def _pdu_get_to_prompt(self):
        self.connection.send("\r")
        self.connection.expect('Telnet Server>')

    def _port_interaction(self, command, port_number):
        log.debug("Attempting %s on port %i", command, port_number)
        self._pdu_get_to_prompt()
        self.connection.sendline(self.pdu_commands[command] +
                                 (" %i" % port_number))
        self.connection.expect("Power set to " + self.pdu_commands[command])
        self._pdu_get_to_prompt()
        log.debug("done")
