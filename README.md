<img src="images/icon.png" width="256">

# MonoObsLog - astrophotography logging application

## ⚠️⚠️⚠️
## This application is still under initial active development. Things can unexpectedly change and break.
## No installer / compiled release is provided at this point - some Python knowledge is expected.
## ⚠️⚠️⚠️

Application for managing astrophotography observations with SQLite database storage.

Special focus is on supporting mono workflows.

This was an Excel workbook, but it was too limiting and I did not want to start adding VBA code.

## Features

- **Observation Log View**
<img src="screenshots/observations.png">

- **Object statistics**: Per filter-type exposure totals for each object.
<img src="screenshots/object_stats.png">

- **Monthly statisctis**: Cumulative observation hours per month.
- **Moon data**: Illumination percentages and angular separation calculated for each observation (not intended to be super precise - just there to get a rough overview of potential data quality issues)
- **Export**: Observations can be exported as an Excel or HTML file.
- **SQLite Storage**: All data persisted in a local SQLite database.
- **Database backup**: Database is backed up weekly to a subfolder. The size is expected to be small so no automatic cleanup exists.

## Requirements for running development version

- Python 3.8 or higher
- PyQt6
- matplotlib
- astropy
- astroplan

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
On Windows it might be desirable to create a shortcut with target:
```bash
pythonw main.py
```
This avoids the console window.


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
- Supports querying location data from Simbad server. Or you can add the coordinates yourself. This is not required but needed for Moon angular separation calculations and altitude plot.

### Sessions Tab
- Intended usage is to add sessions by the date of the evening before the session. (So if you started imaging after midnight enter the previous day) The logic for moon calculations is based on that. Why? Personal preference 🙂

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
- **Coding**: Some of the code is written by using AI coding agents. I don't blindly trust what they spit out, but there certainly can be some weird choices in architecture and code logic. It's a hobby project so I appreciate the time it saves me.