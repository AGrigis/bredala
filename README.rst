.. image:: https://travis-ci.org/AGrigis/bredala.svg?branch=master
    :target: https://travis-ci.org/AGrigis/bredala

.. image:: https://coveralls.io/repos/AGrigis/bredala/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/AGrigis/bredala

.. |Python27| image:: https://img.shields.io/badge/python-2.7-blue.svg
.. _Python27: https://badge.fury.io/py/bredala

.. |Python34| image:: https://img.shields.io/badge/python-3.4-blue.svg
.. _Python34: https://badge.fury.io/py/bredala


Easy to use pure-python caller signature and line-profiler.
Based on Pelletier's pprofile_.
Visit also the main `documentation <http://AGrigis.github.io/bredala>`_.

Overview
========

With Python's standard profiling tools, it is not possible to tell
dynamically which function is a hot-spot. On top of that the resulting
execution output is not filtered and the information of interest may be
difficult to find. Those drawbacks made me start 'bredala' which provide:

- a dynamic API to define which functions/methods to follow:based on the 'New
  Import Hooks' PEP0302_. The declaration has to be done before any processing
  import.

- a signature mechanism that display the prototype of the called
  function/method and the corresponding execution time. 

- a filtered line-profile to access quickly to the execution time of interest.

Usage
=====

The proposed module display function signatures and by default function line
profiles. The latest option can be disabled::

    import bredala
    bredala.USE_PROFILER = False

At the beginning of your script import the project and select which
functions/methods have to be profiled (it must be done before any import)::

    import bredala
    bredala.register("bredala.demo.myfunctions", names=["addition",
                                                        "substraction"])
    from bredala.demo.myfunctions import addition, substraction, factorial
    addition(2, 1)
    substraction(2, 1)
    factorial(5)
    ________________________________________________________________________________
    [bredala] Calling bredala.demo.myfunctions.addition...
    addition(a=2, b=1)
    Line #|      Hits|         Time| Time per hit|      %|Source code
    ------+----------+-------------+-------------+-------+-----------
        11|         1|  3.69549e-05|  3.69549e-05| 13.15%|def addition(a, b):
        12|         0|            0|            0|  0.00%|    """ Demonstration function.
        13|         0|            0|            0|  0.00%|    """
        14|         1|  5.00679e-05|  5.00679e-05| 17.81%|    return a + b
    ____________________________________________________________________0.0s, 0.0min
    ________________________________________________________________________________
    [bredala] Calling bredala.demo.myfunctions.substraction...
    substraction(a=2, b=1)
    Line #|      Hits|         Time| Time per hit|      %|Source code
    ------+----------+-------------+-------------+-------+-----------
        17|         1|  3.00407e-05|  3.00407e-05| 13.17%|def substraction(a, b):
        18|         0|            0|            0|  0.00%|    """ Demonstration function.
        19|         0|            0|            0|  0.00%|    """
        20|         1|  3.00407e-05|  3.00407e-05| 13.17%|    return a - b
    ____________________________________________________________________0.0s, 0.0min

It is possible to profile all the functions/methods of a module by removing
the optional 'names' argument. In another script::

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
    ________________________________________________________________________________
    [bredala] Calling bredala.demo.myfunctions.addition...
    addition(a=2, b=1)
    ____________________________________________________________________0.0s, 0.0min
    ________________________________________________________________________________
    [bredala] Calling bredala.demo.myfunctions.substraction...
    substraction(a=2, b=1)
    ____________________________________________________________________0.0s, 0.0min
    ________________________________________________________________________________
    [bredala] Calling bredala.demo.myfunctions.factorial...
    factorial(a=2)
    ________________________________________________________________________________
    [bredala] Calling bredala.demo.myfunctions.factorial...
    factorial(a=1)
    ____________________________________________________________________0.0s, 0.0min
    ____________________________________________________________________0.0s, 0.0min
    ________________________________________________________________________________
    [bredala] Calling bredala.demo.myclasses.Square.__init__...
    __init__(self=<bredala.demo.myclasses.Square object at 0x7fde3ce049d0>, name='my_square')
    ____________________________________________________________________0.0s, 0.0min
    ________________________________________________________________________________
    [bredala] Calling bredala.demo.myclasses.Square.area...
    area(self=<bredala.demo.myclasses.Square object at 0x7fde3ce049d0>, length_of_side=2)
    ____________________________________________________________________0.0s, 0.0min
    ________________________________________________________________________________
    [bredala] Calling bredala.demo.myclasses.Triangle.__init__...
    __init__(self=<bredala.demo.myclasses.Triangle object at 0x7fde3ce04b50>, name='my_square')
    ____________________________________________________________________0.0s, 0.0min
    ________________________________________________________________________________
    [bredala] Calling bredala.demo.myclasses.Triangle.area...
    area(self=<bredala.demo.myclasses.Triangle object at 0x7fde3ce04b50>, base=2, vertical_height=3)
    ____________________________________________________________________0.0s, 0.0min

For classes we can select to follow all the methods of a class::

    import bredala
    bredala.register("bredala.demo.myclasses", names=["Square"])
    from bredala.demo.myclasses import Square, Triangle
    o = Square("my_square")
    o.area(2)
    o = Triangle("my_square")
    o.area(2, 3)
    ________________________________________________________________________________
    [bredala] Calling bredala.demo.myclasses.Square.__init__...
    __init__(self=<bredala.demo.myclasses.Square object at 0x7f26fa000f90>, name='my_square')
    Line #|      Hits|         Time| Time per hit|      %|Source code
    ------+----------+-------------+-------------+-------+-----------
        14|         1|  3.40939e-05|  3.40939e-05| 17.40%|    def __init__(self, name):
        15|         1|  2.69413e-05|  2.69413e-05| 13.75%|        self.name = name
    ____________________________________________________________________0.0s, 0.0min
    ________________________________________________________________________________
    [bredala] Calling bredala.demo.myclasses.Square.area...
    area(self=<bredala.demo.myclasses.Square object at 0x7f26fa000f90>, length_of_side=2)
    Line #|      Hits|         Time| Time per hit|      %|Source code
    ------+----------+-------------+-------------+-------+-----------
        24|         1|  2.09808e-05|  2.09808e-05| 13.19%|    def area(self, length_of_side):
        25|         1|  2.09808e-05|  2.09808e-05| 13.19%|        return length_of_side ** 2
    ____________________________________________________________________0.0s, 0.0min

Or we can select to follow specific methods::

    import bredala
    bredala.register("bredala.demo.myclasses", names=["Square.area",
                                                      "Triangle.area"])
    from bredala.demo.myclasses import Square, Triangle
    o = Square("my_square")
    o.area(2)
    o = Triangle("my_square")
    o.area(2, 3)
    ________________________________________________________________________________
    [bredala] Calling bredala.demo.myclasses.Square.area...
    area(self=<bredala.demo.myclasses.Square object at 0x7f52b5c10f90>, length_of_side=2)
    Line #|      Hits|         Time| Time per hit|      %|Source code
    ------+----------+-------------+-------------+-------+-----------
        24|         1|  3.38554e-05|  3.38554e-05| 17.09%|    def area(self, length_of_side):
        25|         1|   2.6226e-05|   2.6226e-05| 13.24%|        return length_of_side ** 2
    ____________________________________________________________________0.0s, 0.0min
    ________________________________________________________________________________
    [bredala] Calling bredala.demo.myclasses.Triangle.area...
    area(self=<bredala.demo.myclasses.Triangle object at 0x7f52b5540790>, base=2, vertical_height=3)
    Line #|      Hits|         Time| Time per hit|      %|Source code
    ------+----------+-------------+-------------+-------+-----------
        31|         1|  2.09808e-05|  2.09808e-05| 12.94%|    def area(self, base, vertical_height):
        32|         1|  2.09808e-05|  2.09808e-05| 12.94%|        return 0.5 * base * vertical_height
    ____________________________________________________________________0.0s, 0.0min

Perspectives
============

It will be nice to configure which functions/modules are followed on the fly.
It will be nice to add a backend in order to use 'line_profiler' or 'pprofile'.

.. _pprofile: https://github.com/vpelletier/pprofile
.. _PEP0302: https://www.python.org/dev/peps/pep-0302/


