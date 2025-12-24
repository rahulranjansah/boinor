"""Tests for render.data_loader module."""
from io import StringIO

import numpy as np
from numpy.testing import assert_array_equal

from boinor.render.data_loader import load_data


def test_load_data_parses_vertices_and_faces():
    """Test basic OBJ parsing with vertices and faces."""
    data = """\
            v 0.0 0.0 0.0
            v 1.0 0.0 0.0
            v 0.0 1.0 0.0
            f 1 2 3
            """
    vertices, faces = load_data(StringIO(data))

    expected_vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    expected_faces = np.array([[0, 1, 2]])  # 0-indexed

    assert_array_equal(vertices, expected_vertices)
    assert_array_equal(faces, expected_faces)


def test_load_data_from_file(tmp_path):
    """Test loading from actual file."""
    obj_file = tmp_path / "mesh.obj"
    obj_file.write_text("v 1 2 3\nv 4 5 6\nv 7 8 9\nf 1 2 3\n")

    vertices, faces = load_data(str(obj_file))

    assert vertices.shape == (3, 3)
    assert faces.shape == (1, 3)
