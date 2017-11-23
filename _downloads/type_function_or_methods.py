"""
Type function or methods
========================

Credit: A Grigis

The proposed module display function/method signatures and by default function
line profiles. The latest option can be disabled::

    import bredala
    bredala.USE_PROFILER = False

At the beginning of your script import the project and select all the
functions/methods of a module that must be profiled/signed (it must be done
before any import).

In this example we want to add or substract only integer values and we show
only the 'addition' function signature:
"""

import bredala
bredala.USE_PROFILER = False
bredala.register("bredala.demo.myfunctions", names=["addition"])
bredala.itype("bredala.demo.myfunctions", name="addition",
              input_types=(int, int))
bredala.otype("bredala.demo.myfunctions", name="addition",
              output_types=(int, ))
bredala.itype("bredala.demo.myfunctions", name="substraction",
              input_types=(int, int))
bredala.otype("bredala.demo.myfunctions", name="substraction",
              output_types=(int, ))
from bredala.demo.myfunctions import addition, substraction

addition(2, 1)
substraction(2, 1)


#############################################################################
# Play with the function parameters to generate errors in your notebook/code.
#
# We can perform the same type checking on class methods:

bredala.register("bredala.demo.myclasses", names=[
    "Square.area", "Triangle.__init__"])
bredala.itype("bredala.demo.myclasses", name="Square.area",
              input_types=("self", float, ))
bredala.otype("bredala.demo.myclasses", name="Square.area",
              output_types=(float, ))
bredala.itype("bredala.demo.myclasses", name="Triangle.area",
              input_types=("self", float, float))
bredala.otype("bredala.demo.myclasses", name="Triangle.area",
              output_types=(float, ))
from bredala.demo.myclasses import Square, Triangle


o = Square("my_square")
o.area(2.)
o = Triangle("my_square")
o.area(2., vertical_height=3.)

#############################################################################
# Again fill free to play with the function parameters to generate errors
# in your notebook/code.
