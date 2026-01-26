"""tests related to module aitoff in sub-package plotting"""
import glob

from astropy import units as u
from astropy.time import Time
from matplotlib import pyplot as plt
import numpy as np
import pytest
import spiceypy

from boinor.plotting.aitoff import AitoffPlotter

# even internal stuff needs to be tested
# pylint: disable=protected-access


@pytest.mark.mpl_image_compare
def test_aitoff_basic_plotting():
    """Test basic Aitoff plotting with RA/Dec coordinates."""
    plotter = AitoffPlotter(epoch=Time("2024-01-01T00:00:00"))

    # Plot points at different locations
    plotter.plot_ra_dec(ra=0 * u.deg, dec=0 * u.deg, label="Equator", color="yellow", markersize=10)
    plotter.plot_ra_dec(ra=6 * u.hourangle, dec=30 * u.deg, label="Test Point", color="cyan", markersize=10)
    plotter.plot_ra_dec(ra=np.pi / 2, dec=np.radians(45), label="Radians Test", color="red", markersize=8)

    plotter.set_title("Basic Aitoff Plot Test")
    plotter.set_labels()
    plotter.set_ticks()

    return plotter.fig


@pytest.mark.parametrize(
    "show_ecliptic",
    [True, False],
)
def test_aitoff_ecliptic_option(show_ecliptic):
    """Test that ecliptic can be shown or hidden."""
    plotter = AitoffPlotter(epoch=Time.now(), show_ecliptic=show_ecliptic)

    # Plot a single point
    plotter.plot_ra_dec(ra=0 * u.deg, dec=0 * u.deg, label="Origin")

    # Check that ecliptic line exists or doesn't exist
    lines = plotter.ax.lines
    if show_ecliptic:
        assert any(line.get_label() == "Ecliptic" for line in lines)
    else:
        assert not any(line.get_label() == "Ecliptic" for line in lines)


@pytest.mark.parametrize(
    "style",
    ["default", "dark_background", "seaborn-v0_8"],
)
def test_aitoff_different_styles(style):
    """Test that different matplotlib styles can be applied."""
    plotter = AitoffPlotter(epoch=Time.now(), style=style)
    plotter.plot_ra_dec(ra=0 * u.deg, dec=0 * u.deg, label="Test")

    # Just check it doesn't raise an exception
    assert plotter.fig is not None


@pytest.mark.parametrize(
    "ra, dec",
    [
        (0 * u.deg, 0 * u.deg),
        (np.pi * u.rad, 0 * u.deg),
        (2 * np.pi * u.rad, 0 * u.deg),
        (np.pi / 2 * u.rad, 45 * u.deg),
        (0 * u.hourangle, 0 * u.deg),
        (12 * u.hourangle, 0 * u.deg),  # 12h = 180deg = π rad
        (6 * u.hourangle, 30 * u.deg),
        (18 * u.hourangle, -45 * u.deg),
    ],
)
def test_aitoff_plot_ra_dec_coordinate_formats(ra, dec):
    """Test plot_ra_dec with different coordinate formats."""
    plotter = AitoffPlotter(epoch=Time.now(), show_ecliptic=False)

    line = plotter.plot_ra_dec(ra=ra, dec=dec, label="Test")

    # Check that a line was returned
    assert line is not None
    # Check that data was plotted
    assert len(line.get_xdata()) > 0
    assert len(line.get_ydata()) > 0


@pytest.mark.parametrize(
    "color, marker, markersize",
    [
        (None, "o", 12),
        ("red", "s", 10),
        ("blue", "^", 15),
        ("green", "*", 20),
    ],
)
def test_aitoff_plot_ra_dec_styling(color, marker, markersize):
    """Test plot_ra_dec with different styling options."""
    plotter = AitoffPlotter(epoch=Time.now(), show_ecliptic=False)

    line = plotter.plot_ra_dec(
        ra=0 * u.deg, dec=0 * u.deg, color=color, marker=marker, markersize=markersize, label="Test"
    )

    assert line.get_marker() == marker
    assert line.get_markersize() == markersize
    if color is not None:
        assert line.get_color() == color


def test_axes_labels_and_title():
    """Test axes labels and title methods."""
    plotter = AitoffPlotter(epoch=Time("2024-01-01T12:00:00"), show_ecliptic=False)
    plotter.plot_ra_dec(ra=0 * u.deg, dec=0 * u.deg, label="Test")

    # Test default title (uses epoch)
    plotter.set_title()
    title = plotter.ax.get_title()
    assert "2024-01-01" in title
    assert "UTC" in title

    # Test custom title
    plotter.set_title("Custom Title")
    assert plotter.ax.get_title() == "Custom Title"

    # Test labels
    plotter.set_labels()
    xlabel = plotter.ax.get_xlabel()
    ylabel = plotter.ax.get_ylabel()

    assert "Eq. long" in xlabel
    assert "Eq. lat" in ylabel


def test_aitoff_set_ticks():
    """Test set_ticks method."""
    plotter = AitoffPlotter(epoch=Time.now(), show_ecliptic=False)
    plotter.set_ticks()

    # Check that ticks are set
    xticks = plotter.ax.get_xticks()
    xticklabels = [label.get_text() for label in plotter.ax.get_xticklabels()]

    assert len(xticks) > 0
    assert len(xticklabels) > 0
    # Check that labels contain hour format
    assert any("h" in label for label in xticklabels)


def test_aitoff_custom_axes():
    """Test that AitoffPlotter can use custom axes."""
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={"projection": "aitoff"})

    plotter = AitoffPlotter(epoch=Time.now(), ax=ax, show_ecliptic=False)
    plotter.plot_ra_dec(ra=0 * u.deg, dec=0 * u.deg, label="Test")

    # Check that the same axes object is used
    assert plotter.ax is ax
    assert plotter.fig is fig


@pytest.mark.parametrize(
    "longitude_rad, expected",
    [
        (0.0, 0.0),
        (np.pi, -np.pi),
        (2 * np.pi, 0.0),
        (np.pi / 2, -np.pi / 2),
        (3 * np.pi / 2, np.pi / 2),
    ],
)
def test_aitoff_convert_longitude_for_plot(longitude_rad, expected):
    """Test _convert_longitude_for_plot helper method."""
    plotter = AitoffPlotter(epoch=Time.now(), show_ecliptic=False)

    result = plotter._convert_longitude_for_plot(longitude_rad)

    assert np.isclose(result, expected, atol=1e-10)


def test_aitoff_convert_longitude_for_plot_array():
    """Test _convert_longitude_for_plot with array input."""
    plotter = AitoffPlotter(epoch=Time.now(), show_ecliptic=False)

    longitudes = np.array([0.0, np.pi, 2 * np.pi, np.pi / 2])
    result = plotter._convert_longitude_for_plot(longitudes)

    assert isinstance(result, np.ndarray)
    assert len(result) == len(longitudes)


def test_aitoff_multiple_points():
    """Test plotting multiple points."""
    plotter = AitoffPlotter(epoch=Time.now(), show_ecliptic=False)

    # Plot multiple points
    plotter.plot_ra_dec(ra=0 * u.deg, dec=0 * u.deg, label="Point 1", color="red")
    plotter.plot_ra_dec(ra=90 * u.deg, dec=45 * u.deg, label="Point 2", color="blue")
    plotter.plot_ra_dec(ra=180 * u.deg, dec=-30 * u.deg, label="Point 3", color="green")

    # Check that multiple lines exist
    lines = plotter.ax.lines
    assert len(lines) >= 3


def test_aitoff_epoch_handling():
    """Test that epoch can be Time object or None."""
    # Test with Time object
    plotter1 = AitoffPlotter(epoch=Time("2024-01-01T00:00:00"), show_ecliptic=False)
    assert isinstance(plotter1.epoch, Time)

    # Test with None (should use current time)
    plotter2 = AitoffPlotter(epoch=None, show_ecliptic=False)
    assert isinstance(plotter2.epoch, Time)


@pytest.mark.mpl_image_compare
def test_aitoff_full_plot():
    """Test a complete plot with all features."""
    plotter = AitoffPlotter(
        epoch=Time("2024-01-01T00:00:00"),
        figsize=(12, 8),
        style="dark_background",
        show_ecliptic=True,
    )

    # Plot points at various locations
    plotter.plot_ra_dec(ra=0 * u.deg, dec=0 * u.deg, label="Equator", color="yellow", markersize=10)
    plotter.plot_ra_dec(ra=6 * u.hourangle, dec=30 * u.deg, label="NE", color="cyan", markersize=10)
    plotter.plot_ra_dec(ra=12 * u.hourangle, dec=-30 * u.deg, label="South", color="orange", markersize=10)
    plotter.plot_ra_dec(ra=18 * u.hourangle, dec=60 * u.deg, label="High Dec", color="red", markersize=12)

    # Apply all formatting
    plotter.set_title("Full Aitoff Plot Test")
    plotter.set_labels()
    plotter.set_ticks()
    plotter.ax.legend()
    plotter.ax.grid(True)

    return plotter.fig


def test_aitoff_save():
    """Test save method."""
    import os
    import tempfile

    plotter = AitoffPlotter(epoch=Time.now(), show_ecliptic=False)
    plotter.plot_ra_dec(ra=0 * u.deg, dec=0 * u.deg, label="Test")

    # Save to temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        plotter.save(tmp_path)
        # Check that file was created
        assert os.path.exists(tmp_path)
        assert os.path.getsize(tmp_path) > 0
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@pytest.mark.parametrize(
    "ecliptic_obliquity",
    [23.439281, 23.5, 23.0],
)
def test_aitoff_ecliptic_obliquity(ecliptic_obliquity):
    """Test different ecliptic obliquity values."""
    plotter = AitoffPlotter(epoch=Time.now(), show_ecliptic=True, ecliptic_obliquity=ecliptic_obliquity)

    # Check that ecliptic was plotted
    lines = plotter.ax.lines
    assert any(line.get_label() == "Ecliptic" for line in lines)


def test_aitoff_legend():
    """Test that legend works correctly."""
    plotter = AitoffPlotter(epoch=Time.now(), show_ecliptic=False)

    plotter.plot_ra_dec(ra=0 * u.deg, dec=0 * u.deg, label="Point 1", color="red")
    plotter.plot_ra_dec(ra=90 * u.deg, dec=45 * u.deg, label="Point 2", color="blue")

    plotter.ax.legend()
    legend = plotter.ax.get_legend()

    assert legend is not None
    labels = [t.get_text() for t in legend.get_texts()]
    assert "Point 1" in labels
    assert "Point 2" in labels


@pytest.mark.skip(reason="Requires SPICE kernels - test manually or with mocked spiceypy")
def test_aitoff_plot_spice_position():
    """Test plot_spice_position method (requires SPICE kernels)."""
    # Try to load kernels
    kernel_paths = glob.glob("kernels/**/*")
    if not kernel_paths:
        pytest.skip("No SPICE kernels found")

    spiceypy.furnsh(kernel_paths)

    plotter = AitoffPlotter(epoch=Time.now(), show_ecliptic=False)

    # Plot Sun (should always be available)
    line = plotter.plot_spice_position(target="SUN", observer="EARTH", label="Sun", color="yellow", markersize=20)

    assert line is not None
    assert line.get_label() == "Sun"
