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
import contextlib
import io
from unittest import TestCase
from expresscli import ExpressCliCommand, ExpressCli
import expresscli.mock


class TestExpressCli(TestCase):

    @expresscli.mock.with_arguments('-h')
    def test_empty_descriptor(self):
        cli = ExpressCli(descriptor={}, prog="empty-prog")

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            with self.assertRaises(SystemExit) as ctx:
                cli.big_bang()
        expected = """\
usage: empty-prog [-h]

options:
  -h, --help  show this help message and exit
"""

        self.assertEqual(expected, f.getvalue())
        self.assertEqual(0, ctx.exception.code)

    @expresscli.mock.with_arguments()
    def test_empty_args_show_help(self):
        cli = ExpressCli(descriptor={}, prog="no-arg-prog")

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            with self.assertRaises(SystemExit) as ctx:
                cli.big_bang()
        expected = """\
usage: no-arg-prog [-h]

options:
  -h, --help  show this help message and exit
"""

        self.assertEqual(expected, f.getvalue())
        self.assertEqual(0, ctx.exception.code)

    @expresscli.mock.with_arguments('-h')
    def test_from_dict_descriptor(self):
        class HelloWorld(ExpressCliCommand):

            @staticmethod
            def populate_args(parser: argparse.ArgumentParser):
                pass

        descriptor = {
            "hello-world": HelloWorld,
            "test": lambda x: print(x)
        }

        cli = ExpressCli(descriptor, prog="test-prog")

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            with self.assertRaises(SystemExit) as ctx:
                cli.big_bang()
        self.assertEqual("""usage: test-prog [-h] {hello-world,test} ...

options:
  -h, --help          show this help message and exit

commands:
  {hello-world,test}
    hello-world       Helper class that provides a standard way to create an ABC using
    test
""", f.getvalue())
        self.assertEqual(0, ctx.exception.code)
