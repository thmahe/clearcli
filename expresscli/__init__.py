"""
Copyright 2022
Author: Thomas Mahé <contact@tmahe.dev>

This program is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import inspect
import os
import sys

from .commands import populate_args, ExpressCliCommand


class ExpressCli:

    def __init__(self, descriptor, prog=os.path.basename(sys.argv[0])):
        self._descriptor = descriptor
        self._cli = argparse.ArgumentParser(prog=prog, formatter_class=argparse.RawTextHelpFormatter)

        if isinstance(descriptor, dict):
            self._from_dict_descriptor(self._descriptor, self._cli)

    def big_bang(self):
        args = self._cli.parse_args()
        args.get('_EXPRESSCLI_CALLABLE')(**args)

    def _from_dict_descriptor(self, descriptor, cli: argparse.ArgumentParser, depth=0):
        if isinstance(descriptor, dict):
            title = "sub-" * min(1, depth) + "command"

            if len(descriptor.keys()) > 1:
                title = title + "s"

            sub_parser = cli.add_subparsers(title=title)
            for command_name, sub_descriptor in descriptor.items():
                try:
                    issubclass(sub_descriptor, ExpressCliCommand)
                    parser: argparse.ArgumentParser = sub_parser.add_parser(command_name,
                                                                            formatter_class=argparse.RawTextHelpFormatter,
                                                                            help=
                                                                            inspect.getdoc(sub_descriptor).split('\n')[
                                                                                0][:80],
                                                                            description=inspect.getdoc(sub_descriptor))
                except TypeError:
                    parser: argparse.ArgumentParser = sub_parser.add_parser(command_name, help='')
                self._from_dict_descriptor(sub_descriptor, parser, depth + 1)

        elif callable(ExpressCliCommand):
            cli.help = "test"
            cli.add_argument('--_EXPRESSCLI_CALLABLE', required=False, default=descriptor, help=argparse.SUPPRESS)
            populate_args(descriptor, cli)

        else:
            raise TypeError('ExpressCli descriptor must be a dictionary')