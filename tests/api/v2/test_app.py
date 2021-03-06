# -*- encoding: utf-8 -*-
#
# Copyright © 2013 Julien Danjou
#
# Author: Julien Danjou <julien@danjou.info>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Test basic ceilometer-api app
"""
import os
import tempfile
import unittest

from oslo.config import cfg

from ceilometer.api import app
from ceilometer.api import acl
from ceilometer import service


class TestApp(unittest.TestCase):

    def tearDown(self):
        cfg.CONF.reset()

    def test_keystone_middleware_conf(self):
        cfg.CONF.set_override("auth_protocol", "foottp",
                              group=acl.OPT_GROUP_NAME)
        cfg.CONF.set_override("auth_version", "v2.0", group=acl.OPT_GROUP_NAME)
        api_app = app.setup_app()
        self.assertEqual(api_app.auth_protocol, 'foottp')

    def test_keystone_middleware_parse_conffile(self):
        tmpfile = tempfile.mktemp()
        with open(tmpfile, "w") as f:
            f.write("[%s]\nauth_protocol = barttp" % acl.OPT_GROUP_NAME)
            f.write("\nauth_version = v2.0")
        service.prepare_service(['ceilometer-api',
                                 '--config-file=%s' % tmpfile])
        api_app = app.setup_app()
        self.assertEqual(api_app.auth_protocol, 'barttp')
        os.unlink(tmpfile)
