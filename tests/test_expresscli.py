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
import sys
import unittest.mock
from unittest import TestCase
from expresscli import ExpressCliCommand, ExpressCli


class TestExpressCli(TestCase):

    @unittest.mock.patch('argparse._sys.argv', ['prog', '-h'])
    def test_from_dict_descriptor(self):

        class HelloWorld(ExpressCliCommand):

            @staticmethod
            def populate_args(parser: argparse.ArgumentParser):
                pass

        descriptor = {
            "hello-world": HelloWorld
        }

        cli = ExpressCli(descriptor)

        with self.assertRaises(SystemExit) as ctx:
            cli.big_bang()

        self.assertEqual(0, ctx.exception.code)
