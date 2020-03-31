
""" What we write here will end up in tha package __doc__
    Initialisation file for Package: iso3166_ext
    from: EC-software """

import os  # Needed for definition of root_dir
from iso3166_ext.world import Territories  # import this module on package import

# The names: 'countries' and 'get' makes the module compatible with https://pypi.org/project/iso3166/
countries = world.Territories
get = countries.get

__version__ = "0.0.3"  # Version of the iso3166_ext package
__all__ = [get]  # import these modules on package import *

# The root path of this package, for later reference, I think ...
root_dir = os.path.dirname(os.path.realpath(__file__))

