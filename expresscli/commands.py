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

import abc
import argparse
import inspect


def populate_args(command_item, cli):
    try:
        if issubclass(command_item, ExpressCliCommand):
            command_item.populate_args(cli)
            return
    except TypeError:
        pass

    # Handle Lambdas
    if command_item.__code__.co_name == "<lambda>":
        for item in inspect.signature(command_item).parameters.keys():
            cli.add_argument(item)


class ExpressCliCommand(abc.ABC):
    _reserved_arguments: set[str] = {"_EXPRESSCLI_CALLABLE"}

    def __init__(self, *args, **kwargs):
        try:
            self.filtered_args = {k: kwargs.get(k) for k in set(kwargs.keys()) - self._reserved_arguments}
        except AttributeError and IndexError:
            pass

    @staticmethod
    @abc.abstractmethod
    def populate_args(parser: argparse.ArgumentParser):
        pass
