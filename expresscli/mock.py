import sys
from unittest.mock import patch


def with_arguments(*args, **kwargs):
    arguments = list(args)
    arguments.insert(0, 'prog_name')

    def decorator_with_arguments(func):
        def inner(*args, **kwargs):
            with patch.object(sys, 'argv', arguments):
                return func(*args, **kwargs)

        return inner

    return decorator_with_arguments
