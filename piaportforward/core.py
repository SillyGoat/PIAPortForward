#
# core.py
#
# Copyright (C) 2009 Lee Nguyen <nospam@spam.org>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#

from deluge.log import LOG as log
from deluge.plugins.pluginbase import CorePluginBase
import deluge.component as component
import deluge.configmanager
from deluge.core.rpcserver import export
from twisted.internet.task import LoopingCall

import pia_port

DEFAULT_PREFS = {
    'pia_username': '',
    'pia_password': '',
}


class Core(CorePluginBase):
    def __init__(self):
        self.successfully_acquired_port = False
        self.pia_username = ''
        self.pia_password = ''

    def enable(self):
        log.info('Enabling')
        self.config = deluge.configmanager.ConfigManager(
            'piaportforward.conf', DEFAULT_PREFS)
        self.pia_username = self.config['pia_username']
        self.pia_password = self.config['pia_password']
        self.pia_client_id = pia_port.generate_client_id()

        self.successfully_acquired_port = False

        self.update_status_fast_timer = LoopingCall(self.fast_check)
        time_in_sec_interval = 5
        self.update_status_fast_timer.start(time_in_sec_interval)

        self.update_status_slow_timer = LoopingCall(self.slow_check)
        time_in_sec_interval = 3600
        self.update_status_slow_timer.start(time_in_sec_interval)

    def disable(self):
        log.info('Disabling')
        self.update_status_fast_timer.stop()
        self.update_status_slow_timer.stop()

        self.config['pia_username'] = self.pia_username
        self.config['pia_password'] = self.pia_password

    def update(self):
        pass

    def slow_check(self):
        if self.successfully_acquired_port:
            log.info('Slow port refresh')
            self.refresh_connection()

    def fast_check(self):
        if not self.successfully_acquired_port:
            log.info('Fast port refresh')
            self.refresh_connection()

    def refresh_connection(self):
        log.info('Refreshing listening port...')
        local_ip = pia_port.get_active_local_ip()
        if not local_ip.startswith('10.'):
            log.info('Not a VPN local IP')
            return

        core = component.get('Core')
        previous_listen_port = core.get_listen_port()
        log.info('Current listening port: {}'.format(previous_listen_port))

        def acquire_port(is_open):
            ''' Callback after test_listen_port is complete '''
            if is_open:
                log.info('port is open')
                self.successfully_acquired_port = True
                return

            log.info('port is not open')
            self.successfully_acquired_port = False
            self.pia_username = self.config['pia_username']
            self.pia_password = self.config['pia_password']
            new_port = pia_port.acquire_port(self.pia_username,
                                             self.pia_password,
                                             self.pia_client_id,
                                             local_ip,
                                             log.info)
            if new_port is None:
                log.info('Failed to acquire port')
                return

            if new_port == previous_listen_port:
                log.info(
                    'Something wrong with the port forward.  Same port as the previous.')
                return

            core.set_config({'random_port': False})
            core.set_config({'listen_ports': [new_port, new_port]})
            log.info('Config successfully changed')

        core.test_listen_port().addCallback(acquire_port)

    @export
    def set_config(self, config):
        '''Sets the config dictionary'''
        for key in config.keys():
            self.config[key] = config[key]
        self.config.save()

    @export
    def get_config(self):
        '''Returns the config dictionary'''
        return self.config.config
