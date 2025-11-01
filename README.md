# ObsLog - Python Qt6 astrophotography logging application

Qt6-based desktop application for managing astrophotography observations with SQLite database storage.

Special focus is on supporting mono workflows.

A lot of the coding is done by using AI coding agents. I don't blindly trust what they spit out, but there certainly can be some weird choices in architecture and code logic.

## Features

- **Object statistics**: Per filter-type exposure totals for each object.
- **Monthly statisctis**: Cumulative observation hours per month.
- **SQLite Storage**: All data persisted in a local SQLite database. I personally make backups of the database file.

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


## How to Use

### Adding Data
1. Add Telescopes, Cameras, Filter Types, Filters, Objects and Sessions first
2. Now you can add Observations


### Working with Filters
**Important**: You must create Filter Types before you can add Filters, as each Filter requires a Filter Type.

1. Go to the "Filter Types" tab
2. Add filter types (e.g., "Luminance", "Red", "Ha")
3. Go to the "Filters" tab
4. Add filters (e.g. My Favorite Company 12nm Ha) and select their type from the dropdown

## Features by Tab

### Objects Tab
- Supports querying location data from Simbad server. Or you can add the coordinates yourself. This is not required but needed for Moon angular distance calculations.

### Sessions Tab
- Intended usage is to add sessions by the date of the evening before the session. The logic for moon calculations is based on that.

### Cameras Tab
- The technical data is not used at the moment. Maybe in the future.

### Filter Types Tab
- Meant to allow combining statistical data from different filters of the same type. If you don't want that then feel free to create a different filter type for each filter.

### Telescopes Tab
- The technical data is not used at the moment. Maybe in the future.

## Technical Details

- **UI Framework**: PyQt6
- **Database**: SQLite3
- **UI Design**: Qt Designer (.ui files)