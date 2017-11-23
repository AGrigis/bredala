##########################################################################
# Bredala - Copyright (C) AGrigis, 2015
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Module that sets the package decoration functions dynamically.
"""


# System import
import sys
import inspect
import types

# Bredala import
import bredala


class Decorations(object):
    """ A class that decorate a module functions based on the factory, ie.
    the '_modules' mapping.
    """
    def hack(self, module, name):
        """ Method invoked to transform the input module.

        Parameters
        ----------
        module: object (mandatory)
            a python module object.
        name: str (mandatory)
            the name of the input module.

        Returns
        -------
        decorated_module: object
            if a decorator has been registered for this module in the registery
            return the decorated input python module object, otherwise directly
            the input python module object.
        """
        # If a decorator is decalred for the module apply it now
        decorators_struct = bredala._modules.get(name)
        if decorators_struct is not None:
            self.decorate(module, name, decorators_struct)
        return module

    def decorate(self, module, name, decorators_struct):
        """ Method that decorates the registered function and class methods
        of a module.

        Parameters
        ----------
        module: object (mandatory)
            a python module object.
        name: str (mandatory)
            the name of the input module.
        decorators_struct: dict of dict
            a dictionary with the functions/methods to be decorated as first
            keys, the decorator type as second keys and the decorator -
            decorator parameters as values.
        """
        # Create a class mapping
        mapping = {}
        for filter_name in decorators_struct:
            kname, mname = Decorations.split_class(filter_name)
            mapping.setdefault(kname, []).append(mname)

        # Walk on all the module items
        for module_attr, module_object in module.__dict__.items():

            # Function case
            if isinstance(module_object, types.FunctionType):
                if "ALL" in decorators_struct:
                    key = "ALL"
                elif module_object.__name__ in decorators_struct:
                    key = module_object.__name__
                else:
                    continue
                Decorations._decorate(module, module_attr, module_object,
                                      decorators_struct[key])

            # Class case
            elif inspect.isclass(module_object):
                if "ALL" in mapping:
                    allowed_methods = "ALL"
                elif module_object.__name__ in mapping:
                    allowed_methods = mapping[module_object.__name__]
                else:
                    continue
                if sys.version_info[:2] >= (3, 0):
                    methods = inspect.getmembers(
                        module_object, predicate=inspect.isfunction)
                else:
                    methods = inspect.getmembers(
                        module_object, predicate=inspect.ismethod)
                for method_name, method in methods:
                    if allowed_methods == "ALL":
                        decorator_struct = decorators_struct["ALL"]
                    elif method_name in allowed_methods:
                        decorator_struct = decorators_struct["{0}.{1}".format(
                            module_object.__name__, method_name)]
                    else:
                        continue
                    Decorations._decorate(
                        module_object, method_name, method, decorator_struct,
                        is_method=True)

    @classmethod
    def _decorate(cls, module, module_attr, module_object, decorator_struct,
                  is_method=False):
        """ Method that decorates a specific function or class method.

        Parameters
        ----------
        module: object (mandatory)
            a python module object.
        module_attr: str (mandatory)
            the name of the mofule attribute to be decorated.
        module_object: object
            the function/method to be decorated.
        decorator_struct: dict
            a dictionary with the decorator types as keys and the decorator -
            decorator parameters as values.
        is_method: bool (optional, default False)
            True if the module object is a method of a class, False otherwise.
        """
        # Get the declared type decorators
        type_decorators = []
        for key in ("inputs", "outputs"):
            if key not in decorator_struct:
                continue
            decorator = decorator_struct[key]["decorator"]
            registered_types = decorator_struct[key]["types"]
            type_decorators.append((decorator, registered_types))

        # Apply decorators
        if "signature" in decorator_struct:
            decorator = decorator_struct["signature"]["decorator"]
            setattr(module, module_attr, decorator(
                module_object,
                use_profiler=bredala.USE_PROFILER,
                is_method=is_method,
                type_decorators=type_decorators))
        else:
            for decorator, registered_types in type_decorators:
                setattr(module, module_attr,
                        decorator(*registered_types)(module_object))
                module_object = getattr(module, module_attr)

    @classmethod
    def split_class(cls, name):
        """ Split a  module name.

        Parameters
        ----------
        name: str (mandatory)
            a name describing a class or a class method: <klass> or
            <klass>.<method>.

        Returns
        -------
        kname: str
            the class name.
        mname: str
            the associated module name.
        """
        if "." in name:
            try:
                kname, mname = name.split(".")
            except:
                raise ValueError("'{0}' is not a valid name class or class "
                                 "method description.".format(name))
        else:
            kname = name
            mname = None
        return kname, mname
