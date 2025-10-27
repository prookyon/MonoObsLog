"""Tab manager modules for the observation log application."""

from .objects_tab import ObjectsTabManager
from .sessions_tab import SessionsTabManager
from .cameras_tab import CamerasTabManager
from .filter_types_tab import FilterTypesTabManager
from .filters_tab import FiltersTabManager
from .telescopes_tab import TelescopesTabManager
from .observations_tab import ObservationsTabManager
from .object_stats_tab import ObjectStatsTabManager
from .monthly_stats_tab import MonthlyStatsTabManager

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
]