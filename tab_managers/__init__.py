"""Tab manager modules for the observation log application."""

from .objects_tab import ObjectsTabManager
from .sessions_tab import SessionsTabManager
from .cameras_tab import CamerasTabManager
from .filtertypes_tab import FilterTypesTabManager
from .filters_tab import FiltersTabManager
from .telescopes_tab import TelescopesTabManager
from .observations_tab import ObservationsTabManager
from .objectstats_tab import ObjectStatsTabManager
from .monthlystats_tab import MonthlyStatsTabManager
from .settings_tab import SettingsTabManager
from .about_tab import AboutTabManager

__all__ = [
    'ObjectsTabManager',
    'SessionsTabManager',
    'CamerasTabManager',
    'FilterTypesTabManager',
    'FiltersTabManager',
    'TelescopesTabManager',
    'ObservationsTabManager',
    'ObjectStatsTabManager',
    'MonthlyStatsTabManager',
    'SettingsTabManager',
    'AboutTabManager',
]