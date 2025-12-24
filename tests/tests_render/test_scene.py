"""Tests for render.scene module."""
import numpy as np
import pytest

try:
    from vispy import gloo  # noqa: F401
except OSError:
    pytest.skip("OpenGL not available", allow_module_level=True)

from boinor.render.data_loader import load_data
from boinor.render.scene import MainWindow


@pytest.fixture
def window():
    """Create and cleanup a MainWindow."""
    w = MainWindow()
    yield w
    w.close()


def test_mainwindow_default_initialization(window):
    """Test MainWindow initializes with expected defaults."""
    # Window should exist with reasonable dimensions
    assert window.size[0] > 0
    assert window.size[1] > 0
    assert window.view.camera.fov == 60


def test_mainwindow_custom_parameters():
    """Test MainWindow accepts custom parameters."""
    window = MainWindow(size=(1024, 768), fov=45, bgcolor="navy")

    assert window.size == (1024, 768)
    assert window.view.camera.fov == 45

    window.close()


def test_set_model_adds_mesh_to_scene(window):
    """Test set_model adds a mesh to the view."""
    vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float32)
    faces = np.array([[0, 1, 2]], dtype=np.int32)

    children_before = len(window.view.scene.children)
    window.set_model(vertices, faces)
    children_after = len(window.view.scene.children)

    assert children_after == children_before + 1


def test_load_and_render_integration(tmp_path, window):
    """Test the full pipeline: load file → render mesh."""

    obj_file = tmp_path / "triangle.obj"
    obj_file.write_text("v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n")

    vertices, faces = load_data(str(obj_file))
    window.set_model(vertices, faces)

    assert len(window.view.scene.children) >= 1
