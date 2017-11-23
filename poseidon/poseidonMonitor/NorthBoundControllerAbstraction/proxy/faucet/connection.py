#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Copyright (c) 2016-2017 In-Q-Tel, Inc, All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
Created on 18 November 2017
@author: cglewis
"""
from paramiko import AutoAddPolicy, SSHClient
from scp import SCPClient

from poseidon.baseClasses.Logger_Base import Logger

module_logger = Logger.logger


class Connection:

    def __init__(self, host, user=None, pw=None, config_file=None, log_file=None, *args, **kwargs):
        self.logger = module_logger
        self.host = host
        self.user = user
        self.pw = pw
        self.config_file = config_file
        self.log_file = log_file
        self.ssh = None

    def _connect(self):
        # TODO better logging
        try:
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.load_system_host_keys()
            ssh.connect(self.host, username=self.user, password=self.pw)
            self.ssh = ssh
        except Exception as e:  # pragma: no cover
            pass

    def _disconnect(self):
        if self.ssh:
            self.ssh.close()

    def exec_command(self, command):
        pass

    def receive_file(self, f_type):
        self._connect()
        # TODO better logging
        try:
            scp = SCPClient(self.ssh.get_transport())
            if f_type == 'config':
                scp.get(self.config_file, local_path='/tmp/faucet.yaml')
            elif f_type == 'log':
                scp.get(self.log_file, local_path='/tmp/faucet.log')
            else:
                pass
            scp.close()
        except Exception as e:  # pragma: no cover
            pass
        self._disconnect()

    def send_file(self, f_type):
        self._connect()
        # TODO better logging
        try:
            scp = SCPClient(self.ssh.get_transport())
            if f_type == 'config':
                scp.put('/tmp/faucet.yaml', self.config_file)
            elif f_type == 'log':
                scp.put('/tmp/faucet.log', self.log_file)
            else:
                pass
            scp.close()
        except Exception as e:  # pragma: no cover
            pass
        self._disconnect()