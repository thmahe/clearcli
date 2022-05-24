ClearCLI
--------

### *Build Command Line Interface with ease*


## Install with pip

```shell
$ pip install clearcli
```
> No third-party dependencies, for maximum compatibility and stability ClearCLI only rely on [Python Standard Library](https://docs.python.org/3/library/).
>

## Example: Greeting command

```python
# greet.py
import argparse
import clearcli


class Greet(clearcli.ClearCliCommand):
    """
    Simple greeting command

    Example:
        prog-name greet Tom
    """

    @staticmethod
    def populate_args(parser: argparse.ArgumentParser):
        parser.add_argument('name', help="Name of user to greet")

    def __call__(self, name):
        print(f'Hi, {name}!')


descriptor = {
    "greet": Greet
}

cli = clearcli.ClearCli(prog="prog-name", descriptor=descriptor)

# Parse arguments and run command
cli.big_bang()
```

#### Top level helpers
```shell
# Top level helpers
$ python3 ./greet.py -h
usage: prog-name [-h] {greet} ...

optional arguments:
  -h, --help  show this help message and exit

command:
  greet .... Simple greeting command
```

#### Command helpers
```shell
# Top level helpers
$ python3 ./greet.py greet -h
usage: prog-name greet [-h] name

Simple greeting command  Example:     prog-name greet Tom

positional arguments:
  name        Name of user to greet

optional arguments:
  -h, --help  show this help message and exit
```

#### Run your command
```shell
# Top level helpers
$ python3 ./greet.py greet Thomas
Hi, Thomas!
```