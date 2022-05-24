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
from clearcli import ClearCliCommand, ClearCli
import clearcli.mock


class TestClearCli(TestCase):

    @clearcli.mock.with_arguments('-h')
    def test_empty_descriptor(self):
        cli = ClearCli(descriptor={}, prog="empty-prog")

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            with self.assertRaises(SystemExit) as ctx:
                cli.big_bang()
        expected = """\
usage: empty-prog [-h]

optional arguments:
  -h, --help  show this help message and exit
"""

        self.assertEqual(expected, f.getvalue())
        self.assertEqual(0, ctx.exception.code)

    def test_incorrect_descriptor_type(self):
        with self.assertRaises(TypeError) as ctx:
            ClearCli(descriptor=None, prog="empty-prog")
        self.assertEqual("ClearCli descriptor must be of type <dict>", str(ctx.exception))

    def test_incorrect_sub_descriptor_type(self):
        descriptor = {
            "command": None
        }
        with self.assertRaises(TypeError) as ctx:
            ClearCli(descriptor=descriptor, prog="empty-prog")
        self.assertEqual("ClearCli sub-descriptor must be of type <dict>", str(ctx.exception))

    def test_incorrect_sub_descriptor_class(self):
        class NotCommand(object):
            def __init__(self):
                print(None)

        descriptor = {
            "command": NotCommand
        }
        with self.assertRaises(TypeError) as ctx:
            ClearCli(descriptor=descriptor, prog="empty-prog")
        self.assertEqual("Classes is descriptor must be of type <ClearCliCommand>, Found <NotCommand>", str(ctx.exception))

    def test_incorrect_sub_descriptor_unsuported_type(self):
        def function():
            print("test")

        descriptor = {
            "command": function
        }
        with self.assertRaises(TypeError) as ctx:
            ClearCli(descriptor=descriptor, prog="empty-prog")
        self.assertEqual("Supported types for descriptor items {<lambda>, <ClearCliCommand>}, Found <function>", str(ctx.exception))

    @clearcli.mock.with_arguments()
    def test_empty_args_show_help(self):
        cli = ClearCli(descriptor={}, prog="no-arg-prog")

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            with self.assertRaises(SystemExit) as ctx:
                cli.big_bang()
        expected = """\
usage: no-arg-prog [-h]

optional arguments:
  -h, --help  show this help message and exit
"""

        self.assertEqual(expected, f.getvalue())
        self.assertEqual(0, ctx.exception.code)

    @clearcli.mock.with_arguments('-h')
    def test_from_dict_descriptor(self):
        class HelloWorld(ClearCliCommand):
            """
            Help for "hello-world" command
            """

            @staticmethod
            def populate_args(parser: argparse.ArgumentParser):
                pass

        descriptor = {
            "hello-world": HelloWorld,
            "test": lambda x: print(x)
        }

        cli = ClearCli(descriptor, prog="test-prog")

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            with self.assertRaises(SystemExit) as ctx:
                cli.big_bang()

        expected = """\
usage: test-prog [-h] {hello-world,test} ...

optional arguments:
  -h, --help          show this help message and exit

commands:
  hello-world .... Help for "hello-world" command
  test
"""

        self.assertEqual(expected, f.getvalue())
        self.assertEqual(0, ctx.exception.code)

    @clearcli.mock.with_arguments('child', '--name', 'Thomas', '--parent-arg', 'Hello')
    def test_hello_world_command(self):
        class Parent(ClearCliCommand):

            @staticmethod
            def populate_args(parser: argparse.ArgumentParser):
                parser.add_argument("--parent-arg", required=True)

        class ChildCommand(Parent):

            @staticmethod
            def populate_args(parser: argparse.ArgumentParser):
                Parent.populate_args(parser)
                parser.add_argument("--name", required=True)

            def __call__(self, name, parent_arg):
                print(parent_arg, name)

        descriptor = {
            "child": ChildCommand
        }

        cli = ClearCli(descriptor, prog="test-prog")

        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            with contextlib.redirect_stdout(f):
                with self.assertRaises(SystemExit) as ctx:
                    cli.big_bang()

        expected = """\
Hello Thomas
"""
        self.assertEqual(expected, f.getvalue())
        self.assertEqual(0, ctx.exception.code)

    @clearcli.mock.with_arguments('-h')
    def test_root_help(self):
        class Parent(ClearCliCommand):

            @staticmethod
            def populate_args(parser: argparse.ArgumentParser):
                parser.add_argument("--parent-arg", help="Populated from Parent", required=True)

        class ChildCommand(Parent):

            @staticmethod
            def populate_args(parser: argparse.ArgumentParser):
                Parent.populate_args(parser)
                parser.add_argument("--name", required=True)

            def __call__(self, name, parent_arg):
                print(parent_arg, name)

        descriptor = {
            "child": ChildCommand
        }

        cli = ClearCli(descriptor, prog="test-prog")

        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            with contextlib.redirect_stdout(f):
                with self.assertRaises(SystemExit) as ctx:
                    cli.big_bang()

        expected = """\
usage: test-prog [-h] {child} ...

optional arguments:
  -h, --help  show this help message and exit

command:
  child
"""
        self.assertEqual(expected, f.getvalue())
        self.assertEqual(0, ctx.exception.code)

    @clearcli.mock.with_arguments('-h')
    def test_root_help_description(self):
        descriptor = {}

        description = """\
Welcome in ClearCLI top level
-------------------------------

Helpers : 
Multiline
"""

        cli = ClearCli(descriptor, prog="test-prog", description=description)

        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            with contextlib.redirect_stdout(f):
                with self.assertRaises(SystemExit) as ctx:
                    cli.big_bang()

        expected = """\
usage: test-prog [-h]

Welcome in ClearCLI top level
-------------------------------

Helpers : 
Multiline

optional arguments:
  -h, --help  show this help message and exit
"""
        self.assertEqual(expected, f.getvalue())
        self.assertEqual(0, ctx.exception.code)

    @clearcli.mock.with_arguments('command', '-h')
    def test_command_help(self):
        class Command(ClearCliCommand):
            """
            First line of command help with maximum of 80 characters long in description and max width in commands list
            """

            @staticmethod
            def populate_args(parser: argparse.ArgumentParser):
                parser.add_argument('positional', help="One positional argument\nMultiline capable")
                parser.add_argument('--flag', '-f', help="One flag argument", action='store_true')
                parser.add_argument('--option', '-o', help="One optional argument", required=True)
                parser.add_argument('--choices', choices=["choice_1", "choice_2", "choice_3"])

        descriptor = {
            "command": Command
        }

        description = """\
Welcome in ClearCLI top level
-------------------------------

Helpers : 
Multiline
"""

        cli = ClearCli(descriptor, prog="test-prog", description=description)

        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            with contextlib.redirect_stdout(f):
                with self.assertRaises(SystemExit) as ctx:
                    cli.big_bang()

        expected = """\
usage: test-prog command [-h] [--flag] --option OPTION
                         [--choices {choice_1,choice_2,choice_3}]
                         positional

First line of command help with maximum of 80 characters long in description and
max width in commands list

positional arguments:
  positional                       One positional argument
                                   Multiline capable

optional arguments:
  -h, --help                       show this help message and exit
  --flag, -f                       One flag argument
  --option, -o OPTION              One optional argument
  --choices {choice_1,choice_2,choice_3}
"""
        self.assertEqual(expected, f.getvalue())
        self.assertEqual(0, ctx.exception.code)

    @clearcli.mock.with_arguments('-h')
    def test_command_help_upper_level_long(self):
        class Command(ClearCliCommand):
            """
            First line of command help with maximum of 80 characters long in description and max width in commands list
            """

            @staticmethod
            def populate_args(parser: argparse.ArgumentParser):
                parser.add_argument('positional', help="One positional argument\nMultiline capable")
                parser.add_argument('--flag', '-f', help="One flag argument", action='store_true')
                parser.add_argument('--option', '-o', help="One optional argument", required=True)
                parser.add_argument('--choices', choices=["choice_1", "choice_2", "choice_3"])

        descriptor = {
            "command": Command
        }

        description = """\
Welcome in ClearCLI top level
-------------------------------

Helpers : 
Multiline
"""

        cli = ClearCli(descriptor, prog="test-prog", description=description)

        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            with contextlib.redirect_stdout(f):
                with self.assertRaises(SystemExit) as ctx:
                    cli.big_bang()

        expected = """\
usage: test-prog [-h] {command} ...

Welcome in ClearCLI top level
-------------------------------

Helpers : 
Multiline

optional arguments:
  -h, --help  show this help message and exit

command:
  command .... First line of command help with maximum of 80 characters long...
"""
        self.assertEqual(expected, f.getvalue())
        self.assertEqual(0, ctx.exception.code)
