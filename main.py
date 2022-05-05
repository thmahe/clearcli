# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import abc
import argparse
import inspect
import os
import sys
from abc import ABC


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


class ExpressCliCommand(ABC):

    @abc.abstractmethod
    def __init__(self, parser: argparse.ArgumentParser):
        print('Hello')


class HelloWorld(ExpressCliCommand):
    """
    First line help !! so maybe you can test this new approach

    Next lines this is very dense poziqjdpoiqjfsf INFIENIFNEIFNEIFNEIFNEIFNEINFIENFEINFIENF \


    test
    """

    def __init__(self, parser):
        parser.add_argument("--test")

    def __call__(self, test):
        print(test)
        sys.exit(1)

class HelloWorldCommon(ExpressCliCommand):

    def __init__(self, parser):
        parser.add_argument("--test")

class HelloWorld2(HelloWorldCommon):

    def __init__(self, parser):
        parser.add_argument("args1")
        super().__init__(parser)

    def __call__(self, test, args1):
        print(test, args1)


class _ExpressCliCommand:

    def __init__(self, executable, parent):
        self.parent = parent
        self.executable = executable


class ExpressCli:

    def __init__(self, descriptor: dict, prog=os.path.basename(sys.argv[0])):
        self._descriptor = descriptor
        self._cli = argparse.ArgumentParser(prog=prog, formatter_class=argparse.RawTextHelpFormatter)
        self.from_dict_descriptor(self._descriptor, self._cli)

    def from_dict_descriptor(self, descriptor, cli: argparse.ArgumentParser, depth=0):
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
                                                                                0][:50],
                                                                            description=inspect.getdoc(sub_descriptor))
                except TypeError:
                    parser: argparse.ArgumentParser = sub_parser.add_parser(command_name, help='sub-command')
                self.from_dict_descriptor(sub_descriptor, parser, depth + 1)

        elif issubclass(descriptor, ExpressCliCommand):
            cli.help = "test"
            cli.add_argument('--ExpressCli-Callable', required=False, default=descriptor)
            descriptor(cli)

        else:
            raise TypeError('ExpressCli descriptor must be a dictionary')


descriptor = {
    "hello": {
        "world": {
            "my_name": HelloWorld
        }
    },
    "hello-world": HelloWorld2
}

if __name__ == '__main__':
    e = ExpressCli(descriptor)
    args = e._cli.parse_args()

    callable_args = args.__dict__.copy()
    del callable_args['ExpressCli_Callable']
    print(args.__dict__)
    args.ExpressCli_Callable(argparse.ArgumentParser())(**callable_args)
