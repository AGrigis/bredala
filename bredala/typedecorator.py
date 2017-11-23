##########################################################################
# Bredala - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


"""
Modules that defines the package custom decorators that checks inputs/outputs
types.
"""


# System import
import __builtin__
import re
import inspect
import logging
import importlib
import functools

# Package import
from .exceptions import ArgumentValidationError
from .exceptions import InvalidArgumentNumberError
from .exceptions import InvalidReturnType
from .exceptions import InvalidReturnNumberError


# Global parameters
TYPES = [t for t in __builtin__.__dict__.itervalues() if isinstance(t, type)]


def ordinal(num):
    """ Compute the ordinal number of a given integer, as a string.

    Parameters
    ----------
    num: int
        an integer.

    Returns
    -------
    ordinal: str
        the ordinal representation of the input integer, eg. 1 -> 1st,
        2 -> 2nd, 3 -> 3rd, etc.
    """
    if 10 <= num % 100 < 20:
        return "{0}th".format(num)
    else:
        ord = {1: "st", 2: "nd", 3: "rd"}.get(num % 10, "th")
        return "{0}{1}".format(num, ord)


def inputs(*accepted_arg_types):
    """ A decorator to validate the parameter types of a given function.

    It is passed a tuple, eg. (<type 'tuple'>, <type 'int'>), and
    checks only types.

    Special types are 'self' and 'cls' and are usefull for class methods.

    Note: It doesn't do a deep check, for example checking through a
          tuple of types.
    """
    def input_decorator(validate_function):
        """ Decorate the 'validate_function' function.
        """
        @functools.wraps(validate_function)
        def decorator_wrapper(*function_args, **function_args_dict):
            """ Define a sub-decorator to check the function parameters.
            """
            nb_args = len(function_args) + len(function_args_dict)
            if len(accepted_arg_types) != nb_args:
                raise InvalidArgumentNumberError(validate_function.__name__)

            for arg_num, (actual_arg, accepted_arg_type) in enumerate(
                    zip(function_args, accepted_arg_types)):
                if accepted_arg_type in ("self", "cls"):
                    continue
                if accepted_arg_type not in TYPES:
                    raise InvalidType(accepted_arg_type)
                if type(actual_arg) is not accepted_arg_type:
                    ord_num = ordinal(arg_num + 1)
                    raise ArgumentValidationError(ord_num,
                                                  validate_function.__name__,
                                                  accepted_arg_type)
            return validate_function(*function_args, **function_args_dict)
        return decorator_wrapper
    return input_decorator


def returns(*accepted_return_type_tuple):
    """ Decorator to set the return types.

    It is passed a tuple, eg. (<type 'tuple'>, <type 'int'>), and
    checks only types.

    Note: It doesn't do a deep check, for example checking through a
          tuple of types.
    """
    def return_decorator(validate_function):
        """ Decorate the 'validate_function' function.
        """
        @functools.wraps(validate_function)
        def decorator_wrapper(*function_args, **function_args_dict):
            """ Define a sub-decorator to check the function parameters.
            """
            return_values = validate_function(
                *function_args, **function_args_dict)
            if return_values is None and len(accepted_return_type_tuple) == 0:
                return return_values
            flatten = False
            if not isinstance(return_values, tuple):
                flatten = True
                return_values = (return_values, )

            if len(return_values) != len(accepted_return_type_tuple):
                raise InvalidReturnNumberError(validate_function.__name__)

            for arg_num, (return_value, accepted_return_type) in enumerate(
                    zip(return_values, accepted_return_type_tuple)):
                if accepted_return_type not in TYPES:
                    raise InvalidType(accepted_return_type)
                if type(return_value) is not accepted_return_type:
                    ord_num = ordinal(arg_num + 1)
                    raise InvalidReturnType(ord_num,
                                            validate_function.__name__,
                                            accepted_return_type)

            if flatten:
                return_values = return_values[0]
            return return_values
        return decorator_wrapper
    return return_decorator
