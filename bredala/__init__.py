##########################################################################
# Bredala - Copyright (C) AGrigis, 2015
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Easy to use pure-python caller signature and line-profiler.
"""

# Bredala globals
USE_PROFILER = True
_modules = {}
_hackers = []

# Bredala import
from .info import __version__
from .modulehacker import register
from .modulehacker import itype
from .modulehacker import otype
