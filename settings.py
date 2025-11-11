import json
import os
from database_versioning import VERSION

SETTINGS_FILE = 'settings.json'

DEFAULT_SETTINGS = {
    'moon_illumination_warning_percent': 75,
    'moon_angular_separation_warning_deg': 60,
    'latitude': 0.0,
    'longitude': 0.0,
    'database_version': VERSION
    # Note: database_path intentionally has no default - user must select on first run
}

def load_settings():
    """Load settings from file, create with defaults if file doesn't exist."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    # Create file with defaults if it doesn't exist or failed to load
    save_settings(DEFAULT_SETTINGS)
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """Save settings to file."""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
    except IOError:
        pass

def get_moon_illumination_warning():
    """Get moon illumination warning percentage."""
    return load_settings()['moon_illumination_warning_percent']

def get_moon_angular_separation_warning():
    """Get moon angular separation warning degrees."""
    return load_settings()['moon_angular_separation_warning_deg']

def set_moon_illumination_warning(value):
    """Set moon illumination warning percentage."""
    settings = load_settings()
    settings['moon_illumination_warning_percent'] = value
    save_settings(settings)

def set_moon_angular_separation_warning(value):
    """Set moon angular separation warning degrees."""
    settings = load_settings()
    settings['moon_angular_separation_warning_deg'] = value
    save_settings(settings)

def get_latitude():
    """Get latitude."""
    return load_settings()['latitude']

def get_longitude():
    """Get longitude."""
    return load_settings()['longitude']

def set_latitude(value):
    """Set latitude."""
    settings = load_settings()
    settings['latitude'] = value
    save_settings(settings)

def set_longitude(value):
    """Set longitude."""
    settings = load_settings()
    settings['longitude'] = value
    save_settings(settings)

def get_database_path():
    """Get database path.
    
    Returns:
        Database path if set, None otherwise
    """
    settings = load_settings()
    return settings.get('database_path', None)

def set_database_path(path):
    """Set database path."""
    settings = load_settings()
    settings['database_path'] = path
    save_settings(settings)

def get_database_version():
    """Get database version."""
    return load_settings()['database_version']

def set_database_version(version):
    """Set database version."""
    settings = load_settings()
    settings['database_version'] = version
    save_settings(settings)