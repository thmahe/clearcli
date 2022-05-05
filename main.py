#!/bin/python3

import sys

from expresscli import ExpressCli, ExpressCliCommand


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


class HelloWorld(ExpressCliCommand):
    """
    First line help !! so maybe you can test this new approach

    Next lines this is very dense poziqjdpoiqjfsf INFIENIFNEIFNEIFNEIFNEIFNEINFIENFEINFIENF \


    test
    """

    def populate_args(self, parser):
        parser.add_argument("--test")

    def __call__(self, test):
        print(test)
        sys.exit(1)


class HelloWorldCommon(ExpressCliCommand):

    @staticmethod
    def populate_args(parser):
        parser.add_argument("--test")


class HelloWorld2(HelloWorldCommon):

    @staticmethod
    def populate_args(parser):
        HelloWorldCommon.populate_args(parser)
        parser.add_argument("args1")

    def __call__(self, test, args1):
        print(test, args1)


descriptor = {
    #"hello": lambda e: print(e),
    "hello-world": HelloWorld2
}

if __name__ == '__main__':
    e = ExpressCli(descriptor)
    args = e._cli.parse_args()

    callable_args = args.__dict__.copy()
    callable = args._EXPRESSCLI_CALLABLE(**callable_args)
    callable(**callable.filtered_args)
    #args.ExpressCli_Callable(argparse.ArgumentParser())(**callable_args)
