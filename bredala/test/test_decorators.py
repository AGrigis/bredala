##########################################################################
# Bredala - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import os
import unittest
import numpy

# Package import
from bredala.demo.myfunctions import mytype
from bredala.exceptions import ArgumentValidationError
from bredala.exceptions import InvalidArgumentNumberError
from bredala.exceptions import InvalidReturnType
from bredala.exceptions import InvalidReturnNumberError
from bredala.typedecorator import inputs
from bredala.typedecorator import returns


class TestDecorators(unittest.TestCase):
    """ Test function input/output parameters decorators.
    """

    def setUp(self):
        """ Initialize the TestDecorators class.
        """
        pass

    def test_raises(self):
        """ Method to test that the exceptions are raised properly.
        """
        # Return to new line
        print

        # Check raises
        decorated_func = inputs(float, )(mytype)
        self.assertRaises(InvalidArgumentNumberError, decorated_func, 10., 10.)
        decorated_func = inputs(float, float)(mytype)
        self.assertRaises(ArgumentValidationError, decorated_func, 10., 10)
        decorated_func = returns(float, float)(inputs(float, float)(mytype))
        self.assertRaises(InvalidReturnNumberError, decorated_func, 10., 10.)
        decorated_func = returns(float)(inputs(float, float)(mytype))
        self.assertRaises(InvalidReturnType, decorated_func, 10., 10.)

    def test_normal_exec(self):
        """ Method to test the normal exception.
        """
        decorated_func = returns(str)(inputs(float, float)(mytype))
        result = decorated_func(10., 10.)
        self.assertEqual(result, repr(float))


def test():
    """ Function to execute unitests.
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDecorators)
    runtime = unittest.TextTestRunner(verbosity=2).run(suite)
    return runtime.wasSuccessful()


if __name__ == "__main__":
    test()
