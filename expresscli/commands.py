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
