#   Copyright 2013 OpenStack, LLC.
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

"""Hypervisor action implementations"""

import logging

from cliff import lister
from cliff import show

from openstackclient.common import utils


class ListHypervisor(lister.Lister):
    """List hypervisor command"""

    log = logging.getLogger(__name__ + ".ListHypervisor")

    def get_parser(self, prog_name):
        parser = super(ListHypervisor, self).get_parser(prog_name)
        parser.add_argument(
            "--matching",
            metavar="<hostname>",
            help="List hypervisors with hostnames matching the given"
                 " substring")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        compute_client = self.app.client_manager.compute
        columns = (
            "ID",
            "Hypervisor Hostname"
        )

        if parsed_args.matching:
            data = compute_client.hypervisors.search(parsed_args.matching)
        else:
            data = compute_client.hypervisors.list()

        return (columns,
                (utils.get_item_properties(
                    s, columns,
                ) for s in data))


class ShowHypervisor(show.ShowOne):
    """Show hypervisor command"""

    log = logging.getLogger(__name__ + ".ShowHypervisor")

    def get_parser(self, prog_name):
        parser = super(ShowHypervisor, self).get_parser(prog_name)
        parser.add_argument(
            "id",
            metavar="<id>",
            help="ID of the hypervisor to display")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        compute_client = self.app.client_manager.compute
        hypervisor = utils.find_resource(compute_client.hypervisors,
                                         parsed_args.id)._info.copy()

        hypervisor["service_id"] = hypervisor["service"]["id"]
        hypervisor["service_host"] = hypervisor["service"]["host"]
        del hypervisor["service"]

        return zip(*sorted(hypervisor.iteritems()))
