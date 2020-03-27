
# __init__.py

""" Initialisation file for Package: iso3166_ext
    from: EC-software """

import os  # Needed for definition of root_dir
import iso3166_ext.world  # import this module on package import

# print(f'Invoking __init__.py for {__name__}')

__version__ = "0.0.1"  # Version of the iso3166_ext package
__all__ = ['world']  # import these modules on package import *

# The root path of this package, for later reference, I think ...
root_dir = os.path.dirname(os.path.realpath(__file__))

