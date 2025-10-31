from astropy.time import Time
from astropy.coordinates import get_body, get_sun, solar_system_ephemeris, SkyCoord
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


def calculate_angular_separation(ra1_deg: float, dec1_deg: float, ra2_deg: float, dec2_deg: float) -> float:
    """
    Calculate the angular separation between two points on the celestial sphere.

    Parameters:
    -----------
    ra1_deg : float
        Right Ascension of first point in degrees
    dec1_deg : float
        Declination of first point in degrees
    ra2_deg : float
        Right Ascension of second point in degrees
    dec2_deg : float
        Declination of second point in degrees

    Returns:
    --------
    float : Angular separation in degrees
    """

    coord1 = SkyCoord(ra=ra1_deg*u.degree, dec=dec1_deg*u.degree)
    coord2 = SkyCoord(ra=ra2_deg*u.degree, dec=dec2_deg*u.degree)

    return float(coord1.separation(coord2).degree)


def lookup_object_coordinates(object_name: str) -> tuple[float, float]:
    """
    Look up equatorial coordinates for a celestial object using astropy's online resolver.

    Uses the Simbad astronomical database to resolve object names to coordinates.

    Parameters:
    -----------
    object_name : str
        Name of the celestial object (e.g., 'M31', 'NGC7000', 'Andromeda Galaxy')

    Returns:
    --------
    tuple[float, float] : (ra_degrees, dec_degrees)
        Right Ascension in degrees (0-360)
        Declination in degrees (-90 to +90)

    Raises:
    -------
    Exception : If object cannot be resolved or network error occurs
        Includes descriptive error message for user feedback
    """
    try:

        # Query Simbad database for object coordinates
        coord = SkyCoord.from_name(object_name)

        ra_degrees = float(coord.ra.degree)
        dec_degrees = float(coord.dec.degree)

        return ra_degrees, dec_degrees

    except Exception as e:
        # Provide user-friendly error messages
        error_msg = str(e)
        if "Unable to find coordinates" in error_msg or "name could not be resolved" in error_msg.lower():
            raise Exception(f"Object '{object_name}' not found in Simbad database. Please check the spelling and try again.")
        elif "Connection" in error_msg or "timeout" in error_msg.lower():
            raise Exception(f"Network error while looking up '{object_name}'. Please check your internet connection and try again.")
        else:
            raise Exception(f"Failed to look up coordinates for '{object_name}': {error_msg}")
