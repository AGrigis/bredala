"""
Profile/signe your code dynamically (global)
============================================

Credit: A Grigis

The proposed module display function signatures and by default function
line profiles. The latest option can be disabled::

    import bredala
    bredala.USE_PROFILER = False

At the beginning of your script import the project and select all the
functions/methods of a module that must be profiled/signed (it must be done
before any import):
"""

import bredala
bredala.USE_PROFILER = False
bredala.register("bredala.demo.myfunctions")
bredala.register("bredala.demo.myclasses")
from bredala.demo.myfunctions import addition, substraction, factorial
from bredala.demo.myclasses import Square, Triangle


addition(2, 1)
substraction(2, 1)
factorial(2)
o = Square("my_square")
o.area(2)
o = Triangle("my_square")
o.area(2, 3)
