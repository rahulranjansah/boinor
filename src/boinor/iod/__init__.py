""" Sub-package holding all modules for Initial Orbit Determination (IOD)"""
# Select default algorithm
from boinor.iod.izzo import lambert

__all__ = ["lambert"]
