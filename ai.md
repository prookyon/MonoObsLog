# Observation Log Application - AI Documentation

## Project Overview

This is a PyQt6-based desktop application for managing astronomical observation sessions. It tracks objects, cameras, telescopes, filters, and observation records in a SQLite database.

## Architecture

The application follows a **modular architecture** with clear separation of concerns:
- **Entry Point**: Single main.py file
- **Main Window**: Coordinator that delegates to specialized managers
- **Tab Managers**: Each tab has its own manager class handling all UI and business logic
- **Dialogs**: Reusable dialog classes for editing entities
- **Database**: Centralized database access layer

## File Structure and Purpose

### Core Application Files

#### `main.py`
**Purpose**: Application entry point
**Key Functions**:
- `main()`: Initializes QApplication and MainWindow, starts event loop. Checks for database_path setting on startup and shows file selection dialog if not configured. Performs automatic weekly backup check before opening main window.
**Dependencies**: PyQt6, main_window.MainWindow, settings, backup
**When to modify**: Rarely - only for application-level configuration changes

#### `main_window.py`
**Purpose**: Main application window coordinator
**Key Responsibilities**:
- Loads main UI file (`mainwindow.ui`)
- Initializes database connection with user-specified path
- Creates and manages tab manager instances
- Handles tab change events
- Manages application lifecycle (close event)
**Key Methods**:
- `__init__(db_path)`: Sets up window, database with specified path, and tab managers
- `on_tab_changed(index)`: Updates UI when switching tabs
- `closeEvent(event)`: Cleans up database connection on exit
**Dependencies**: PyQt6, database.Database, all tab managers
**When to modify**:
- Adding new tabs (create manager instance)
- Adding global application behavior
- Modifying tab change logic

#### `calculations.py`
**Purpose**: Astronomical calculations module
**Key Functions**:
- `calculate_moon_data(date)`: Calculates moon illumination percentage, Right Ascension (RA), and Declination (Dec) for a given date using astropy
- `lookup_object_coordinates(object_name)`: Queries Simbad astronomical database via astropy to resolve object names to equatorial coordinates (returns RA in degrees)
- `calculate_angular_separation(ra1_deg, dec1_deg, ra2_deg, dec2_deg)`: Calculates angular separation between two celestial coordinates using astropy
**Dependencies**: astropy (Time, coordinates, solar_system_ephemeris, SkyCoord), numpy, datetime
**Returns**:
  - `calculate_moon_data()`: Tuple of (illumination_percent, moon_ra_degrees, moon_dec_degrees)
  - `lookup_object_coordinates()`: Tuple of (ra_degrees, dec_degrees) or raises Exception with user-friendly error message
  - `calculate_angular_separation()`: Angular separation in degrees (float)
**Usage**:
  - Moon data: Called automatically when adding/editing sessions to store moon data
  - Object coordinates: Called when user clicks "Lookup Coordinates" button in EditObjectDialog; RA is converted from degrees to hours for storage
  - Angular separation: Used in observations tab to show distance between observed objects and moon
**Storage Format**:
  - RA: Stored in decimal hours (0-24h, where 1h = 15°)
  - Dec: Stored in decimal degrees (-90° to +90°)
**Error Handling**: Provides descriptive error messages for network issues, unknown objects, and other failures
**When to modify**: Adding other astronomical calculations or celestial body data

#### `database.py`
**Purpose**: Database access layer
**Key Responsibilities**:
- SQLite database connection management
- CRUD operations for all entities
- Database schema initialization
**Entities Managed**:
- Objects (celestial objects with optional equatorial coordinates)
- Sessions (observation sessions with moon data)
- Cameras (imaging equipment)
- Filter Types (categories of filters)
- Filters (optical filters)
- Telescopes (optical equipment)
- Observations (observation records)
**Object Coordinate Storage**:
- Objects table includes optional `ra` (decimal hours, 0-24h) and `dec` (decimal degrees, -90° to +90°)
- Coordinates are NULL by default
- Can be set manually or via astropy online lookup (lookup returns degrees, converted to hours for storage)
**Moon Data Storage**:
- Sessions table includes `moon_illumination` (illumination %), `moon_ra` (Right Ascension in degrees), and `moon_dec` (Declination in degrees)
- Moon data is automatically calculated and stored when sessions are added/edited using `calculations.calculate_moon_data()`
**When to modify**:
- Adding new database tables
- Modifying existing schemas
- Adding new queries or operations

#### `utilities.py`
**Purpose**: Console utilities for astronomical calculations and database maintenance, plus reusable UI utility classes
**Key Functions**:
- `--calc-moon`: Recalculates moon illumination, Right Ascension, and Declination for all sessions in database
- `calculate_moon_data_for_all_sessions()`: Core function that processes all sessions and updates moon data
**Key Classes**:
- `NumericTableWidgetItem`: QTableWidgetItem subclass that sorts numerically instead of alphabetically.
**Dependencies**: calculations.py, database.py, argparse, datetime, PyQt6 (optional for UI classes)
**Usage**:
  - Command-line interface for batch operations on moon data
  - Import NumericTableWidgetItem for use in tab managers: `from utilities import NumericTableWidgetItem`
  - Create numeric table items: `table.setItem(row, col, NumericTableWidgetItem(numeric_value))`
**When to modify**: Adding new console utilities, batch processing features, or reusable UI utility classes

#### `backup.py`
**Purpose**: Automatic weekly database backup management
**Key Functions**:
- `check_and_create_backup(db_path)`: Main function called at startup to check if backup is needed and create one
- `create_backup(db_path)`: Creates zipped backup with date-stamped filename
- `is_backup_needed(db_path)`: Checks if latest backup is older than 7 days
- `get_latest_backup_info(db_path)`: Retrieves most recent backup filename and date
**Dependencies**: os, zipfile, datetime
**Backup Location**: Creates 'ObsLogBackup' subfolder next to database file
**Backup Format**: Zipped files named as `observations_backup_YYYY-MM-DD.zip`
**Backup Interval**: 7 days between backups
**When to modify**: Changing backup frequency, location, or naming conventions

#### `settings.py`
**Purpose**: Settings storage and management module
**Key Functions**:
- `load_settings()`: Loads settings from JSON file, creates with defaults if missing
- `save_settings(settings)`: Saves settings dictionary to JSON file
- `get_moon_illumination_warning()`: Returns moon illumination warning percentage
- `get_moon_angular_separation_warning()`: Returns angular separation warning degrees
- `set_moon_illumination_warning(value)`: Sets moon illumination warning percentage
- `set_moon_angular_separation_warning(value)`: Sets angular separation warning degrees
- `get_database_path()`: Returns database path if set, None otherwise
- `set_database_path(path)`: Sets database path
**Dependencies**: json, os
**Storage**: settings.json file with default values (moon_illumination_warning_percent: 75, moon_angular_separation_warning_deg: 60). database_path has no default - user must select on first run.
**When to modify**: Adding new configurable settings

### Dialog Classes

#### `dialogs.py`
**Purpose**: Reusable edit dialogs for all entities
**Classes**:
- `EditSessionDialog`: Edit session ID and start date
- `EditCameraDialog`: Edit camera specifications (name, sensor, pixel size, dimensions)
- `EditFilterDialog`: Edit filter name and type
- `EditTelescopeDialog`: Edit telescope parameters (name, aperture, f-ratio, focal length)
- `EditObservationDialog`: Edit observation records (all fields with combo boxes)
- `EditObjectDialog`: Edit object name and optional equatorial coordinates (RA/Dec) with online lookup capability
**Pattern**: All dialogs follow the same structure:
1. Constructor accepts current values and parent
2. `get_values()` method returns edited values as tuple
3. Uses QFormLayout with OK/Cancel buttons
**EditObjectDialog Special Features**:
- RA spin box: 0-24 hours (stored in decimal hour format)
- Dec spin box: -90 to +90 degrees
- "Lookup Coordinates" button: Queries Simbad database via astropy to auto-populate coordinates (converts RA from degrees to hours)
- Error handling: Shows user-friendly messages for network issues and unknown objects
- Returns None for coordinates if not set (supports optional coordinates)
- Display format: RA shown as "X.XXXXXXh", Dec shown as "X.XXXXXX°"
**Dependencies**: PyQt6 widgets, calculations.lookup_object_coordinates()
**When to modify**:
- Adding new fields to entities
- Changing validation logic
- Adding new dialog types

### Tab Manager Package

#### `tab_managers/__init__.py`
**Purpose**: Package initialization and exports
**Exports**: All tab manager classes
**When to modify**: When adding new tab managers

#### `tab_managers/objects_tab.py`
**Purpose**: Manages Objects tab (celestial objects like M31, NGC7000) with optional equatorial coordinates
**Key Methods**:
- `setup_tab()`: Loads UI, connects signals, configures table with RA/Dec columns
- `load_objects()`: Fetches and displays all objects including coordinates (RA in hours with 'h' suffix, Dec in degrees with '°' suffix)
- `add_object()`: Opens EditObjectDialog for object name and optional coordinate entry or lookup
- `edit_object()`: Opens EditObjectDialog to edit object name and coordinates
- `delete_object()`: Deletes object with confirmation
**UI Elements**: Table (with RA in hours and Dec in degrees columns), name input, add/edit/delete buttons
**Database Operations**: get_all_objects, add_object, update_object, delete_object
**Special Features**:
- Optional equatorial coordinate storage (RA in decimal hours 0-24h, Dec in decimal degrees -90° to +90°)
- Manual coordinate entry via spin boxes in EditObjectDialog (RA in hours, Dec in degrees)
- Online coordinate lookup via astropy Simbad resolver with "Lookup Coordinates" button (converts RA from degrees to hours)
- Coordinates display as empty strings if not set
- User-friendly error messages for network issues and unknown object names
- Display precision: 6 decimal places for both RA and Dec

#### `tab_managers/sessions_tab.py`
**Purpose**: Manages Sessions tab (observation sessions with dates and moon data)
**Key Methods**:
- `setup_tab()`: Loads UI, sets current date, connects signals, configures table columns
- `load_sessions()`: Fetches and displays sessions including moon illumination, RA, and Dec
- `add_session()`: Adds new session with ID, date, and automatically calculates moon data
- `edit_session()`: Opens EditSessionDialog, recalculates moon data on date change
- `delete_session()`: Deletes session with confirmation
**UI Elements**: Table (with moon columns), session ID input, date picker, add/edit/delete buttons
**Dependencies**: calculations.calculate_moon_data()
**Special Features**:
- Date picker with calendar popup
- Automatic moon data calculation for midnight following the start date
- Displays moon illumination percentage, RA, and Dec in table

#### `tab_managers/cameras_tab.py`
**Purpose**: Manages Cameras tab (imaging equipment specifications)
**Key Methods**:
- `setup_tab()`: Loads UI, connects signals, configures table columns
- `load_cameras()`: Fetches and displays all cameras
- `add_camera()`: Adds new camera with full specifications
- `edit_camera()`: Opens EditCameraDialog for editing
- `delete_camera()`: Deletes camera with confirmation
**UI Elements**: Table, name/sensor inputs, spin boxes for pixel size/dimensions
**Validation**: Ensures all numeric fields are non-zero

#### `tab_managers/filter_types_tab.py`
**Purpose**: Manages Filter Types tab (categories like Narrowband, Broadband, LRGB)
**Key Methods**:
- `setup_tab()`: Loads UI, connects signals
- `load_filter_types()`: Fetches and displays all filter types
- `add_filter_type()`: Adds new filter type
- `edit_filter_type()`: Opens input dialog to edit name
- `delete_filter_type()`: Deletes filter type with confirmation
**UI Elements**: Table, name input, add/edit/delete buttons
**Note**: Filter types are referenced by filters tab

#### `tab_managers/filters_tab.py`
**Purpose**: Manages Filters tab (specific filters like Ha, OIII, Red)
**Key Methods**:
- `setup_tab()`: Loads UI, connects signals, updates filter type combo
- `update_filter_type_combo()`: Populates combo box with available filter types
- `load_filters()`: Fetches and displays all filters
- `add_filter()`: Adds new filter with name and type
- `edit_filter()`: Opens EditFilterDialog for editing
- `delete_filter()`: Deletes filter with confirmation
**UI Elements**: Table, name input, filter type combo box, add/edit/delete buttons
**Dependencies**: Requires filter types to exist

#### `tab_managers/telescopes_tab.py`
**Purpose**: Manages Telescopes tab (optical equipment specifications)
**Key Methods**:
- `setup_tab()`: Loads UI, connects signals including f-ratio calculation
- `load_telescopes()`: Fetches and displays all telescopes
- `add_telescope()`: Adds new telescope with specifications
- `edit_telescope()`: Opens EditTelescopeDialog for editing
- `delete_telescope()`: Deletes telescope with confirmation
- `calculate_f_ratio()`: Auto-calculates f-ratio from aperture and focal length
**UI Elements**: Table, name input, spin boxes for aperture/f-ratio/focal length
**Special Features**: Automatic f-ratio calculation when aperture or focal length changes
**Formula**: f_ratio = focal_length / aperture (rounded to 1 decimal)

#### `tab_managers/observations_tab.py`
**Purpose**: Manages Observations tab (observation records linking all entities)
**Key Methods**:
- `setup_tab()`: Loads UI, connects signals, configures table columns
- `update_observation_combos()`: Populates all combo boxes with current data
- `update_filter_list()`: Populates filter list with unique object names from observations
- `load_observations()`: Fetches and displays observations (optionally filtered by object)
- `filter_observations()`: Handles filter selection changes
- `add_observation()`: Adds new observation record
- `edit_observation()`: Opens EditObservationDialog for editing
- `delete_observation()`: Deletes observation with confirmation
- `export_observations_to_excel()`: Exports current filtered observations to Excel file with same columns as visible in table
- `export_observations_to_html()`: Exports current filtered observations to HTML file with same columns as table using template system
**UI Elements**: Table, combo boxes for session/object/camera/telescope/filter, spin boxes for counts/exposure, comments input, QListView for object filtering, "Export" button with Excel/HTML menu
**Dependencies**: Requires data in all other tabs (sessions, objects, cameras, telescopes, filters), openpyxl for Excel export, template file for HTML export
**Validation**: Ensures all required fields are selected and numeric values are non-zero
**Calculated Field**: Total exposure = image_count × exposure_length (calculated in database)
**Special Features**:
- QListView filter showing "< All Names >" and unique observed objects
- Displays session date, moon illumination percentage, and angular separation between object and moon
- Conditional highlighting: pastel red background for moon illumination > configurable warning % and angular separation < configurable warning °
- **Excel Export**: "Export to Excel" button exports current filtered observations with same columns as table, includes formatted headers, auto-sized columns, and date-stamped filenames
- **HTML Export**: "Export to HTML" action exports observations using template file with professional styling, warning highlighting, and responsive design

#### `tab_managers/object_stats_tab.py`
**Purpose**: Manages Object Stats tab (cumulative exposure statistics by object and filter type)
**Key Methods**:
- `setup_tab()`: Loads UI, gets table reference, loads initial data
- `load_stats()`: Fetches stats from database, dynamically creates table columns based on filter types, populates table with cumulative exposures
- `apply_conditional_formatting()`: Applies color gradient to Total column (red-yellow-green for low to high values)
**UI Elements**: Table with dynamic columns (Object Name + filter types + Total)
**Dependencies**: Requires observations with associated filters
**Special Features**:
- Dynamically generates columns based on unique filter types in observations
- Shows cumulative total exposure for each object/filter type combination
- Includes Total column summing all exposures per object with conditional formatting
- Auto-refreshes when tab is selected

#### `tab_managers/monthly_stats_tab.py`
**Purpose**: Manages Monthly Stats tab (cumulative exposure statistics by month)
**Key Methods**:
- `setup_tab()`: Loads UI, creates matplotlib figure and canvas, integrates with PyQt6
- `load_stats()`: Fetches monthly stats from database, generates bar chart with months on X-axis and total exposure on Y-axis
**UI Elements**: Bar chart widget using matplotlib
**Dependencies**: Requires observations with associated sessions (for dates), matplotlib
**Special Features**:
- Bar chart visualization with proper formatting, labels, and grid
- Displays cumulative exposure values on top of bars
- Auto-refreshes when tab is selected

#### `tab_managers/settings_tab.py`
**Purpose**: Manages Settings tab
**Key Methods**:
- `setup_tab()`: Loads UI, connects signals, loads current settings
- `load_settings()`: Populates UI with current settings values
- `save_settings()`: Saves UI values to settings file and refreshes observations table
**UI Elements**: Spin boxes for moon illumination warning % and angular separation warning °
**Dependencies**: settings.py module
**Special Features**:
- Real-time updates to observations table highlighting when settings change
- Automatic settings file creation with defaults if missing

## UI Files

The application uses Qt Designer `.ui` files for layouts:
- `mainwindow.ui`: Main application window with tab widget
- `object_tab.ui`: Objects tab layout
- `session_tab.ui`: Sessions tab layout
- `camera_tab.ui`: Cameras tab layout
- `filter_type_tab.ui`: Filter Types tab layout
- `filter_tab.ui`: Filters tab layout
- `telescope_tab.ui`: Telescopes tab layout
- `observation_tab.ui`: Observations tab layout
- `object_stats_tab.ui`: Object Stats tab layout
- `monthly_stats_tab.ui`: Monthly Stats tab layout
- `settings_tab.ui`: Settings tab layout

### Template Files

- `templates/observations_export.html`: HTML template for observations export with CSS styling and placeholders for dynamic content
  - Placeholders: `{{filter_name}}`, `{{export_date}}`, `{{total_records}}`, `{{table_rows}}`, `{{completion_date}}`
  - Features: Professional styling, conditional highlighting, responsive design

**Note**: UI files are loaded dynamically using `uic.loadUi()`. Widget references are obtained using `findChild()`.

## Common Patterns

### Tab Manager Pattern
All tab managers follow this structure:
```python
class XxxTabManager:
    def __init__(self, parent, db, tab_widget, statusbar):
        # Store references
        # Call setup_tab()
    
    def setup_tab(self):
        # Load UI file
        # Get widget references
        # Connect signals
        # Configure table
        # Load initial data
    
    def load_xxx(self):
        # Fetch from database
        # Populate table
        # Update status bar
    
    def add_xxx(self):
        # Validate input
        # Add to database
        # Clear inputs
        # Reload table
    
    def edit_xxx(self):
        # Get selected row
        # Open edit dialog
        # Update database
        # Reload table
    
    def delete_xxx(self):
        # Get selected row
        # Confirm deletion
        # Delete from database
        # Reload table
```

### Error Handling
All database operations are wrapped in try-except blocks:
```python
try:
    # Database operation
    self.statusbar.showMessage('Success message')
except Exception as e:
    QMessageBox.critical(self.parent, 'Error', f'Error message: {str(e)}')
```

### Table Configuration
Tables consistently:
- Hide ID column (column 0)
- Set appropriate column widths
- Display data starting from column 1

### UI File Loading
All `.ui` files are loaded using relative paths to ensure the application works regardless of the current working directory:
- Main window: `base_dir = os.path.dirname(__file__)`
- Tab managers: `base_dir = os.path.dirname(os.path.dirname(__file__))`
- Pattern: `ui_path = os.path.join(base_dir, 'filename.ui')` then `uic.loadUi(ui_path, widget)`

## Adding New Features

### Adding a New Tab
1. Create new tab manager in `tab_managers/new_tab.py`
2. Follow the tab manager pattern
3. Add to `tab_managers/__init__.py` exports
4. Create corresponding `.ui` file
5. Instantiate in `main_window.py.__init__()`
6. Add database methods in `database.py`
7. Create edit dialog in `dialogs.py` if needed

### Adding Fields to Existing Entity
1. Update database schema in `database.py`
2. Update corresponding tab manager's add/edit/load methods
3. Update edit dialog in `dialogs.py`
4. Update `.ui` file with new widgets
5. Update table column configuration

### Modifying Business Logic
1. Locate the appropriate tab manager
2. Modify the relevant method (add/edit/delete/load)
3. Update validation if needed
4. Test with the application

## Dependencies

- **PyQt6**: GUI framework
- **matplotlib**: Chart visualization (Monthly Stats tab)
- **astropy**: Astronomical calculations (Moon data computation)
- **openpyxl**: Excel file export functionality (Observations tab)
- **SQLite3**: Database (built-in Python)
- **Python 3.x**: Runtime environment
- **HTML Templates**: HTML export functionality using template system

## Testing

Run the application:
```bash
python main.py
```

The application will:
1. Create/open `observations.db` SQLite database
2. Initialize schema if needed
3. Display main window with all tabs
4. Allow CRUD operations on all entities

## Database Schema

Key relationships:
- Observations reference: Sessions, Objects, Cameras, Telescopes, Filters
- Filters reference: Filter Types
- All entities have auto-incrementing integer primary keys
- Foreign key constraints ensure referential integrity

### Statistics Queries
- `get_object_stats()`: Aggregates observations by object name and filter type, calculating cumulative total exposure for each combination
- `get_monthly_stats()`: Aggregates observations by month (from session dates), calculating cumulative total exposure per month

## Best Practices for Modifications

1. **Maintain Separation of Concerns**: Keep UI logic in tab managers, data access in database.py
2. **Follow Existing Patterns**: Use the established tab manager pattern for consistency
3. **Error Handling**: Always wrap database operations in try-except blocks
4. **User Feedback**: Update status bar on success, show message boxes on errors
5. **Validation**: Validate user input before database operations
6. **Confirmation**: Ask for confirmation before destructive operations (delete)
7. **Documentation**: Update this file when making structural changes
8. **Testing**: Test all CRUD operations after modifications

## Common Modification Scenarios

### Scenario 1: Add a new field to Cameras
1. Update `database.py`: Add column to cameras table, update add/update/get methods
2. Update `camera_tab.ui`: Add new input widget
3. Update `tab_managers/cameras_tab.py`: 
   - Add widget reference in `setup_tab()`
   - Update `add_camera()` to include new field
   - Update `load_cameras()` to display new field
4. Update `dialogs.py`: Add field to `EditCameraDialog`

### Scenario 2: Add validation to prevent duplicate names
1. Locate relevant tab manager's `add_xxx()` method
2. Before calling `db.add_xxx()`, query existing records
3. Check if name already exists
4. Show warning message if duplicate found
5. Return early to prevent addition

### Scenario 3: Add a calculated field
1. Add calculation logic in database.py (preferred) or tab manager
2. Update `load_xxx()` to display calculated value
3. Update table column configuration if needed
4. Consider whether field should be stored or calculated on-the-fly

## Notes for AI Assistants

- The codebase is well-structured and modular - respect the existing architecture
- Each tab manager is independent - changes to one shouldn't affect others
- The database.py file is the single source of truth for data operations
- UI files are separate from code - modifications require updating both
- Status bar messages provide user feedback - maintain this pattern
- All destructive operations require confirmation - maintain this safety feature
- The application uses Qt's signal/slot mechanism for event handling
- Widget references are obtained dynamically using `findChild()` - names must match .ui files