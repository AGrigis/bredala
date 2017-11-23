##########################################################################
# Bredala - Copyright (C) AGrigis, 2015
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
#
# Based on: https://www.python.org/dev/peps/pep-0302/
##########################################################################

"""
Module that implements the New Import Hooks' PEP0302.
"""


# System import
import sys
import os
import inspect
import imp

# Bredala import
import bredala
from .signaturedecorator import bredala_signature
from .typedecorator import inputs, returns
from .decorations import Decorations


def register(module, decorator=bredala_signature, names=None,
             decorator_type="signature", **kwargs):
    """ Function to register a decorator for a list of module names.

    Parameters
    ----------
    module: str (mandatory)
        a module name whose functions will be decorated.
    decorator: callable (optional, default  @bredala_signature)
        a decorator function.
    names: list of str (optional, default None)
        a list of function or methods we want to decorate, if None all the
        module functions or methods will be decorated.
    decorator_type: str
        the decorator type. Supported values are 'signature', 'inputs' and
        'outputs'.
    kwargs: dict (optional)
        extra arguments used during the dynamic decorations: 'istype' and
        'types'.
    """
    if decorator_type not in ("signature", "inputs", "outputs"):
        raise ValueError("'{0}' decorator type not recognized.".format(
            decorator_type))
    if module not in bredala._modules:
        bredala._modules[module] = {}
    if names is None:
        names = ["ALL"]
    for name in names:
        kwargs["decorator"] = decorator
        bredala._modules[module].setdefault(name, {})[decorator_type] = kwargs


def itype(module, name, input_types, decorator=inputs):
    """ Function to register a decorator to type inputs.

    Parameters
    ----------
    module: str (mandatory)
        a module name whose functions will be decorated.
    name: str ((mandatory)
        a function or a method we want to decorate.
    input_types: tuple of types (mandatory)
        the decorate function input types.
    decorator: callable (optional, default @inputs)
        a decorator function.
    """
    register(module, decorator=decorator, names=[name],
             decorator_type="inputs", types=input_types)


def otype(module, name, output_types, decorator=returns):
    """ Function to register a decorator to type outputs.

    Parameters
    ----------
    module: str (mandatory)
        a module name whose functions will be decorated.
    name: str ((mandatory)
        a function or a method we want to decorate.
    output_types: tuple of types (mandatory)
        the decorate function returned types.
    decorator: callable (optional, default @returns)
        a decorator function.
    """
    register(module, decorator=decorator, names=[name],
             decorator_type="outputs", types=output_types)


def modulehacker_register(obj):
    """ A simple registery to define new hackers.
    """
    bredala._hackers.append(obj)


class BredalaMetaImportHook(object):
    """ A class that import a module like normal and then passed to a hacker
    object that gets to do whatever it wants to the module. Then the return
    value from the hack call is put into sys.modules.
    """
    def __init__(self):
        self.module = None

    def find_module(self, name, path=None):
        """ This method is called by Python if this class is on sys.path.
        'name' is the fully-qualified name of the module to look for, and
        'path' is either __path__ (for submodules and subpackages) or None (for
        a top-level module/package).

        Note that this method will be called every time an import statement
        is detected (or __import__ is called), before Python's built-in
        package/module-finding code kicks in.
        """
        # Use this loader only on registered modules
        if name not in bredala._modules:
            return None

        # Get parent module and associated sub module names
        self.sub_name = name.split(".")[-1]
        self.mod_name = name.rpartition(".")[0]

        # Find the sub module and build the module path
        try:
            self.file, self.filename, self.stuff = imp.find_module(
                self.sub_name, path)
            self.path = [self.filename]
        except ImportError:
            return None

        # Return The loader, here the object itself
        return self

    def load_module(self, name):
        """ This method is called by Python if BredalaImportHook 'find_module'
         does not return None. 'name' is the fully-qualified name
         of the module/package that was requested.
        """
        # Load the module
        module = imp.load_module(name, self.file, self.filename,
                                 self.stuff)
        if self.file:
            self.file.close()

        # Decorate the function/methods
        for hacker in bredala._hackers:
            module = hacker.hack(module, name)

        # Update the module required information
        module.__path__ = self.path
        module.__loader__ = self
        module.__package__ = name
        module.__name__ = name
        if self.stuff[0] == ".py":
            module.__file__ = self.path[0]
        else:
            module.__file__ = os.path.join(self.path[0], "__init__.py")

        return module


modulehacker_register(Decorations())
sys.meta_path.insert(0, BredalaMetaImportHook())
