.. image:: https://travis-ci.org/AGrigis/breadala.svg?branch=master
    :target: https://travis-ci.org/AGrigis/breadala


.. image:: https://coveralls.io/repos/AGrigis/breadala/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/AGrigis/breadala


Easy to use pure-python caller signature and profiler.
Based on Pelletier's _pprofile_.

Overview
========

With Python's standard profiling tools, it is not possible to tell
dynamically which function is a hot-spot. On top of that the resulting
execution ioutput is not filtered and the information of interest may be
difficult to find. Those drawbacks made me start 'bredala' which provide:

- A dynamic API to define which functions/methods to follow.

- A signature mechanism that display the prototype of the called
  function/method.

- A filtered profile to access quickly to the execution time of interest.

Usage
=====


.. _pprofile: https://github.com/vpelletier/pprofile


