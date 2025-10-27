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
- `main()`: Initializes QApplication and MainWindow, starts event loop
**Dependencies**: PyQt6, main_window.MainWindow
**When to modify**: Rarely - only for application-level configuration changes

#### `main_window.py`
**Purpose**: Main application window coordinator
**Key Responsibilities**:
- Loads main UI file (`mainwindow.ui`)
- Initializes database connection
- Creates and manages tab manager instances
- Handles tab change events
- Manages application lifecycle (close event)
**Key Methods**:
- `__init__()`: Sets up window, database, and tab managers
- `on_tab_changed(index)`: Updates UI when switching tabs
- `closeEvent(event)`: Cleans up database connection on exit
**Dependencies**: PyQt6, database.Database, all tab managers
**When to modify**: 
- Adding new tabs (create manager instance)
- Adding global application behavior
- Modifying tab change logic

#### `database.py`
**Purpose**: Database access layer
**Key Responsibilities**:
- SQLite database connection management
- CRUD operations for all entities
- Database schema initialization
**Entities Managed**:
- Objects (celestial objects)
- Sessions (observation sessions)
- Cameras (imaging equipment)
- Filter Types (categories of filters)
- Filters (optical filters)
- Telescopes (optical equipment)
- Observations (observation records)
**When to modify**:
- Adding new database tables
- Modifying existing schemas
- Adding new queries or operations

### Dialog Classes

#### `dialogs.py`
**Purpose**: Reusable edit dialogs for all entities
**Classes**:
- `EditSessionDialog`: Edit session ID and start date
- `EditCameraDialog`: Edit camera specifications (name, sensor, pixel size, dimensions)
- `EditFilterDialog`: Edit filter name and type
- `EditTelescopeDialog`: Edit telescope parameters (name, aperture, f-ratio, focal length)
- `EditObservationDialog`: Edit observation records (all fields with combo boxes)
**Pattern**: All dialogs follow the same structure:
1. Constructor accepts current values and parent
2. `get_values()` method returns edited values as tuple
3. Uses QFormLayout with OK/Cancel buttons
**Dependencies**: PyQt6 widgets
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
**Purpose**: Manages Objects tab (celestial objects like M31, NGC7000)
**Key Methods**:
- `setup_tab()`: Loads UI, connects signals, configures table
- `load_objects()`: Fetches and displays all objects
- `add_object()`: Adds new object to database
- `edit_object()`: Opens input dialog to edit object name
- `delete_object()`: Deletes object with confirmation
**UI Elements**: Table, name input, add/edit/delete buttons
**Database Operations**: get_all_objects, add_object, update_object, delete_object

#### `tab_managers/sessions_tab.py`
**Purpose**: Manages Sessions tab (observation sessions with dates)
**Key Methods**:
- `setup_tab()`: Loads UI, sets current date, connects signals
- `load_sessions()`: Fetches and displays all sessions
- `add_session()`: Adds new session with ID and date
- `edit_session()`: Opens EditSessionDialog for editing
- `delete_session()`: Deletes session with confirmation
**UI Elements**: Table, session ID input, date picker, add/edit/delete buttons
**Special Features**: Date picker with calendar popup

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
**UI Elements**: Table, combo boxes for session/object/camera/telescope/filter, spin boxes for counts/exposure, comments input, QListView for object filtering
**Dependencies**: Requires data in all other tabs (sessions, objects, cameras, telescopes, filters)
**Validation**: Ensures all required fields are selected and numeric values are non-zero
**Calculated Field**: Total exposure = image_count × exposure_length (calculated in database)
**Special Features**: QListView filter showing "< All Names >" and unique observed objects

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
- **SQLite3**: Database (built-in Python)
- **Python 3.x**: Runtime environment

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