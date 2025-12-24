"""Render module for 3D visualization of celestial bodies and spacecraft."""
from boinor.render.data_loader import load_data

__all__ = ["MainWindow", "load_data"]


def __getattr__(name):
    """
    Lazy import MainWindow (requires OpenGL, not available on headless CI). (PEP 562)
    """

    if name == "MainWindow":
        from boinor.render.scene import MainWindow

        return MainWindow

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
