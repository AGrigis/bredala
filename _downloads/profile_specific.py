"""
Profile/signe your code dynamically (specific)
==============================================

Credit: A Grigis

The proposed module display function signatures and by default function
line profiles. The latest option can be disabled::

    import bredala
    bredala.USE_PROFILER = False

At the beginning of your script import the project and select which specific
functions/methods have to be profiled/signed (it must be done before any
import):
"""

import bredala
bredala.register("bredala.demo.myfunctions", names=["addition",
                                                    "substraction"])
from bredala.demo.myfunctions import addition, substraction, factorial


addition(2, 1)
substraction(2, 1)
factorial(5)


#############################################################################
# For classes we can select to follow all the methods of a class:

bredala.register("bredala.demo.myclasses", names=["Square"])
from bredala.demo.myclasses import Square, Triangle


o = Square("my_square")
o.area(2)
o = Triangle("my_square")
o.area(2, 3)


#############################################################################
# We can also choose to follow specific methods (you must reload the shell as
# the bredala regitry must be set before any import):

import bredala
bredala.register("bredala.demo.myclasses", names=["Square.area",
                                                  "Triangle.area"])
from bredala.demo.myclasses import Square, Triangle


o = Square("my_square")
o.area(2)
o = Triangle("my_square")
o.area(2, 3)
