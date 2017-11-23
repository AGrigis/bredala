##########################################################################
# Bredala - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Module current version
version_major = 1
version_minor = 0
version_micro = 3

# Expected by setup.py: string of form "X.Y.Z"
__version__ = "{0}.{1}.{2}".format(version_major, version_minor, version_micro)

# Expected by setup.py: the status of the project
CLASSIFIERS = [
    "Intended Audience :: Developers",
    ("License :: OSI Approved :: GNU General Public License v2 or later "
     "(GPLv2+)"),
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development"]

# Project descriptions
description = """
Easy to use pure-python caller signature and profiler.
"""
SUMMARY = """
.. container:: summary-carousel

    Bredala is a Python module for **pure-python caller signature and
    profiler.**
"""
long_description = """
=======
Bredala
=======

With Python's standard profiling tools, it is not possible to tell
dynamically which function is a hot-spot. On top of that the resulting
execution output is not filtered and the information of interest may be
difficult to find. Those drawbacks made me start **bredala** which provides:

* a dynamic API to define which functions/methods to follow: based on the
  **New Import Hooks' PEP0302**. The declaration has to be done before any
  processing import.
* a signature mechanism that display the prototype of the called
  function/method and the corresponding execution time.
* a filtered line-profile to access quickly to the execution time of interest.
"""

# Main setup parameters
NAME = "Bredala"
ORGANISATION = ""
MAINTAINER = "Antoine Grigis"
MAINTAINER_EMAIL = "antoine.grigis@cea.fr"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "https://github.com/AGrigis/bredala"
DOWNLOAD_URL = "https://github.com/AGrigis/bredala"
LICENSE = "GPL 2+"
CLASSIFIERS = CLASSIFIERS
AUTHOR = "Antoine Grigis"
AUTHOR_EMAIL = "antoine.grigis@cea.fr"
PLATFORMS = "OS Independent"
ISRELEASE = True
VERSION = __version__
PROVIDES = ["bredala"]
REQUIRES = [
    "pprofile>=1.6"
]
EXTRA_REQUIRES = {}
