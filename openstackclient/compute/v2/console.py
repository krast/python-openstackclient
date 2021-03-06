#   Copyright 2012-2013 OpenStack Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

"""Console action implementations"""

import logging
import sys

from cliff import command
from cliff import show

from openstackclient.common import utils


class ShowConsoleLog(command.Command):
    """Show console-log command"""

    log = logging.getLogger(__name__ + '.ShowConsoleLog')

    def get_parser(self, prog_name):
        parser = super(ShowConsoleLog, self).get_parser(prog_name)
        parser.add_argument(
            'server',
            metavar='<server>',
            help='Name or ID of server to display console log',
        )
        parser.add_argument(
            '--lines',
            metavar='<num-lines>',
            type=int,
            default=None,
            help='Number of lines to display from the end of the log '
                 '(default=all)',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        compute_client = self.app.client_manager.compute

        server = utils.find_resource(
            compute_client.servers,
            parsed_args.server,
        )
        # NOTE(dtroyer): get_console_output() appears to shortchange the
        #                output by one line
        data = server.get_console_output(length=parsed_args.lines + 1)
        sys.stdout.write(data)
        return


class ShowConsoleURL(show.ShowOne):
    """Show console-url command"""

    log = logging.getLogger(__name__ + '.ShowConsoleURL')

    def get_parser(self, prog_name):
        parser = super(ShowConsoleURL, self).get_parser(prog_name)
        parser.add_argument(
            'server',
            metavar='<server>',
            help='Name or ID of server to display console log',
        )
        type_group = parser.add_mutually_exclusive_group()
        type_group.add_argument(
            '--novnc',
            dest='url_type',
            action='store_const',
            const='novnc',
            default='novnc',
            help='Show noVNC console URL (default)',
        )
        type_group.add_argument(
            '--xvpvnc',
            dest='url_type',
            action='store_const',
            const='xvpvnc',
            help='Show xpvnc console URL',
        )
        type_group.add_argument(
            '--spice',
            dest='url_type',
            action='store_const',
            const='spice',
            help='Show SPICE console URL',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        compute_client = self.app.client_manager.compute
        server = utils.find_resource(
            compute_client.servers,
            parsed_args.server,
        )

        print "type: %s" % parsed_args.url_type
        if parsed_args.url_type in ['novnc', 'xvpvnc']:
            data = server.get_vnc_console(parsed_args.url_type)
        if parsed_args.url_type in ['spice']:
            data = server.get_spice_console(parsed_args.url_type)

        if not data:
            return ({}, {})
        print "data: %s" % data['console']

        info = {}
        info.update(data['console'])
        return zip(*sorted(info.iteritems()))
