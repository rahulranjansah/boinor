# SPICE Kernels

This directory contains SPICE kernel files used by boinor for computing spacecraft and planetary ephemerides. SPICE is a NASA/JPL system for spacecraft navigation and planetary science computations. Kernels are data files that provide different types of information needed for these calculations.

## Kernel Types

### LSK - Leap Second Kernel
Leap Second Kernels contain leap second data used to convert between different time systems (UTC, TDB, TT, etc.). These kernels store temporal adjustment information necessary for precise time calculations in astronomical computations.

### PCK - Planetary Constants Kernel
Planetary Constants Kernels provide physical and cartographic constants for celestial bodies, including:
- Gravitational parameters (GM values)
- Body radii and shape parameters
- Orientation data (pole direction, rotation rate)
- Quadratic expressions for the direction (RA, Dec) of the north pole

### SPK - Spacecraft and Planet Kernel
SPK kernels contain ephemeris data (position and velocity) for spacecraft, planets, satellites, comets, and asteroids. They store continuous position and velocity data organized in segments by target body, reference frame, and time span.

## Directory Structure

- **lsk/** - Leap Second Kernels
  - `naif0012.tls` - Current leap second data for UTC/ET time conversions

- **pck/** - Planetary Constants Kernels
  - `gm_de440.tpc` - Gravitational parameters (GM values) for solar system bodies from DE440

- **spk/** - SPK Ephemeris Kernels
  - `de432s.bsp` - JPL Development Ephemeris 432s (compact version) containing positions of major solar system bodies

## Source

These kernels are obtained from NASA's Navigation and Ancillary Information Facility (NAIF) at JPL:
https://naif.jpl.nasa.gov/naif/data.html

## Terms of Use

As per [NAIF Rules](https://naif.jpl.nasa.gov/naif/rules.html), SPICE data and software may be used freely, including in commercial products, with no fees or licensing required. Acknowledging use of SPICE/NAIF resources in publications is encouraged as it helps support continued funding. The software and data are provided "AS-IS" without warranty of performance, merchantability, or fitness for purpose. Users may modify kernels with proper annotation, though modified kernels should have changed filenames and updated attribution. NAIF/SPICE software is designated "Technology and Software Publicly Available" (TSPA), making export unrestricted.