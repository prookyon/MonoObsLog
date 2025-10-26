# Astronomy Observation Log - Python Qt6 Application

A comprehensive Qt6-based desktop application for managing astronomy observation data with SQLite database storage.

## Features

- **Multiple Data Types**: Manage Objects, Sessions, Cameras, Filters, Filter Types, and Telescopes
- **Tab-based Interface**: Each data type has its own dedicated tab
- **Full CRUD Operations**: Add, edit, and delete entries for all data types
- **Data Relationships**: Filters are linked to Filter Types through foreign key relationships
- **User-friendly Interface**: Intuitive forms with appropriate input controls (date pickers, spin boxes, combo boxes)
- **SQLite Storage**: All data persisted in a local SQLite database

## Requirements

- Python 3.8 or higher
- PyQt6

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

## Application Structure

### Core Files
- **[`main.py`](main.py:1)** - Main application with UI logic and database integration
- **[`database.py`](database.py:1)** - SQLite database operations module with CRUD methods for all data types
- **`objects.db`** - SQLite database file (created automatically on first run)

### UI Files
- **[`mainwindow.ui`](mainwindow.ui:1)** - Main window with tab widget and Objects tab
- **[`session_tab.ui`](session_tab.ui:1)** - Sessions tab interface
- **[`camera_tab.ui`](camera_tab.ui:1)** - Cameras tab interface
- **[`filter_type_tab.ui`](filter_type_tab.ui:1)** - Filter Types tab interface
- **[`filter_tab.ui`](filter_tab.ui:1)** - Filters tab interface
- **[`telescope_tab.ui`](telescope_tab.ui:1)** - Telescopes tab interface

## Data Types

### 1. Objects
- **Fields**: Name
- **Purpose**: General astronomical objects

### 2. Sessions
- **Fields**: 
  - Session ID (text identifier)
  - Start Date (date)
- **Purpose**: Track observation sessions

### 3. Cameras
- **Fields**:
  - Name
  - Sensor (type/model)
  - Pixel Size (μm, floating point)
  - Width (pixels, integer)
  - Height (pixels, integer)
- **Purpose**: Manage imaging equipment specifications

### 4. Filter Types
- **Fields**: Name
- **Purpose**: Define categories of filters (e.g., Luminance, Red, Green, Blue, Ha, OIII)
- **Note**: Must be created before adding Filters

### 5. Filters
- **Fields**:
  - Name
  - Type (relation to Filter Type)
- **Purpose**: Track individual filter instances
- **Relationship**: Each filter is linked to a Filter Type

### 6. Telescopes
- **Fields**:
  - Name
  - Aperture (mm, integer)
  - F-ratio (floating point)
  - Focal Length (mm, integer)
- **Purpose**: Manage telescope specifications

## Database Schema

### Objects Table
- `id` (INTEGER PRIMARY KEY) - Auto-incrementing
- `name` (TEXT) - Object name

### Sessions Table
- `id` (INTEGER PRIMARY KEY) - Auto-incrementing
- `session_id` (TEXT) - Session identifier
- `start_date` (TEXT) - Start date in YYYY-MM-DD format

### Cameras Table
- `id` (INTEGER PRIMARY KEY) - Auto-incrementing
- `name` (TEXT) - Camera name
- `sensor` (TEXT) - Sensor type/model
- `pixel_size` (REAL) - Pixel size in micrometers
- `width` (INTEGER) - Sensor width in pixels
- `height` (INTEGER) - Sensor height in pixels

### Filter Types Table
- `id` (INTEGER PRIMARY KEY) - Auto-incrementing
- `name` (TEXT UNIQUE) - Filter type name

### Filters Table
- `id` (INTEGER PRIMARY KEY) - Auto-incrementing
- `name` (TEXT) - Filter name
- `type` (TEXT) - Foreign key to filter_types.name

### Telescopes Table
- `id` (INTEGER PRIMARY KEY) - Auto-incrementing
- `name` (TEXT) - Telescope name
- `aperture` (INTEGER) - Aperture in millimeters
- `f_ratio` (REAL) - F-ratio (focal ratio)
- `focal_length` (INTEGER) - Focal length in millimeters

## How to Use

### Adding Data
1. Navigate to the appropriate tab
2. Fill in the required fields
3. Click the "Add" button or press Enter

### Editing Data
1. Select a row in the table
2. Click "Edit Selected"
3. Modify the values in the dialog
4. Click OK to save changes

### Deleting Data
1. Select a row in the table
2. Click "Delete Selected"
3. Confirm the deletion

### Working with Filters
**Important**: You must create Filter Types before you can add Filters, as each Filter requires a Filter Type.

1. Go to the "Filter Types" tab
2. Add filter types (e.g., "Luminance", "Red", "Ha")
3. Go to the "Filters" tab
4. Add filters and select their type from the dropdown

## Features by Tab

### Objects Tab
- Simple name-based entries
- Quick add with Enter key support

### Sessions Tab
- Date picker for start date
- Session ID text field
- Chronological tracking

### Cameras Tab
- Comprehensive sensor specifications
- Numeric spin boxes for precise values
- Decimal support for pixel size

### Filter Types Tab
- Simple type definitions
- Unique constraint prevents duplicates
- Required before adding filters

### Filters Tab
- Dropdown selection of filter types
- Enforces relationship integrity
- Easy type assignment

### Telescopes Tab
- Complete optical specifications
- Aperture, f-ratio, and focal length tracking
- Decimal support for f-ratio precision

## Technical Details

- **UI Framework**: PyQt6
- **Database**: SQLite3
- **UI Design**: Qt Designer (.ui files)
- **Architecture**: Separation of concerns (UI, business logic, data access)
- **Edit Dialogs**: Custom dialog classes for complex data types
- **Input Validation**: Client-side validation before database operations

## Future Enhancements

Potential additions:
- Image management and linking
- Observation notes and conditions
- Equipment combinations/profiles
- Data export (CSV, JSON)
- Statistics and reporting
- Dark/light theme support