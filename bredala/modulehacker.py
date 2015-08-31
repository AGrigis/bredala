#! /usr/bin/env python
##########################################################################
# Bredala - Copyright (C) AGrigis, 2015
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
#
# From: http://code.activestate.com/recipes/577742
##########################################################################

# System import
import sys
import importlib


_hackers = []


def register(obj):
    """ A simple registery to define new hackers.
    """
    _hackers.append(obj)


class BredalaImportHook(object):
    """ A class that import a module like normal and then passed to a hacker
    object that gets to do whatever it wants to the module. Then the return
    value from the hack call is put into sys.modules.
    """
    def __init__(self):
        self.module = None

    def find_module(self, name, path):
        """ This method is called by Python if this class is on sys.path.
        'name' is the fully-qualified name of the module to look for, and
        'path' is either __path__ (for submodules and subpackages) or None (for
        a top-level module/package).

        Note that this method will be called every time an import statement
        is detected (or __import__ is called), before Python's built-in
        package/module-finding code kicks in.
        """
        sys.meta_path.remove(self)
        try:
            self.module = importlib.import_module(name)
        finally:
            sys.meta_path.insert(0, self)
        return self

    def load_module(self, name):
        """ This method is called by Python if BredalaImportHook 'find_module'
         does not return None. 'name' is the fully-qualified name
         of the module/package that was requested.
        """
        if not self.module:
            raise ImportError("Unable to load module.")
        module = self.module
        for hacker in _hackers:
            module = hacker.hack(module, name)
        sys.modules[name] = module
        return module


sys.meta_path.insert(0, BredalaImportHook())
