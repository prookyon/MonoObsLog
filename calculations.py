from astropy.time import Time
from astropy.coordinates import get_body, get_sun, solar_system_ephemeris
from astropy.coordinates import EarthLocation
import astropy.units as u
import numpy as np
from datetime import datetime, timezone


def calculate_moon_data(date: str) -> tuple[float, float, float]:
    """
    Calculate moon illumination percentage and equatorial coordinates for a given date.
    
    Parameters:
    -----------
    date : str or astropy.Time
        Date in ISO format (e.g., '2025-10-28') or astropy.Time object
    
    Returns:
    --------
    float : Percentage of moon illuminated (0-100)
    float : Right Ascension in degrees
    float : Declination in degrees
    """
    # Convert to Time object if string
    if isinstance(date, str):
        # Parse the date string as a local datetime
        local_dt = datetime.fromisoformat(date)
        
        # If the datetime is naive (no timezone info), assume it's in local timezone
        if local_dt.tzinfo is None:
            # Make it timezone-aware using the system's local timezone
            local_dt = local_dt.astimezone()
        
        # Convert to UTC
        utc_dt = local_dt.astimezone(timezone.utc)
        
        # Create Time object from UTC datetime
        time = Time(utc_dt)
    else:
        time = date
    
    # Get positions of Sun and Moon from Earth
    with solar_system_ephemeris.set('builtin'):
        sun = get_sun(time)
        moon = get_body("moon", time)
    
    # Calculate elongation (angular separation between Sun and Moon)
    elongation = sun.separation(moon)
    
    # Calculate phase angle
    phase_angle = np.arctan2(
        sun.distance * np.sin(elongation),
        moon.distance - sun.distance * np.cos(elongation)
    )
    
    # Calculate illumination fraction using Lambert's law
    # Formula: (1 + cos(phase_angle)) / 2
    illumination_fraction = (1 + np.cos(phase_angle)) / 2
    illumination_percent = float(illumination_fraction * 100.0)

    return illumination_percent, float(moon.ra.degree), float(moon.dec.degree)
