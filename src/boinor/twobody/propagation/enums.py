"""module enums of sub-package propagation of sub-package twobody"""
from enum import Flag, auto


class PropagatorKind(Flag):
    """helper class to define different kind of propagators"""

    ELLIPTIC = auto()
    PARABOLIC = auto()
    HYPERBOLIC = auto()
