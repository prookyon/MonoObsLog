import sqlite3
from typing import List, Dict, Optional


class Database:
    def __init__(self, db_path: str = "objects.db"):
        """Initialize database connection and create tables if they don't exist."""
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create all tables if they don't exist."""
        # Objects table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS objects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                ra REAL,
                dec REAL
            )
        """)
        
        # Sessions table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL UNIQUE,
                start_date TEXT NOT NULL,
                moon_illumination REAL,
                moon_ra REAL,
                moon_dec REAL
            )
        """)
        
        # Cameras table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cameras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                sensor TEXT NOT NULL,
                pixel_size REAL NOT NULL,
                width INTEGER NOT NULL,
                height INTEGER NOT NULL
            )
        """)
        
        # Filter Types table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS filter_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        
        # Filters table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS filters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                type TEXT NOT NULL,
                FOREIGN KEY (type) REFERENCES filter_types(name)
            )
        """)
        
        # Telescopes table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS telescopes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                aperture INTEGER NOT NULL,
                f_ratio REAL NOT NULL,
                focal_length INTEGER NOT NULL
            )
        """)
        
        # Observations table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                object_name TEXT NOT NULL,
                camera_name TEXT NOT NULL,
                telescope_name TEXT NOT NULL,
                filter_name TEXT NOT NULL,
                image_count INTEGER NOT NULL,
                exposure_length INTEGER NOT NULL,
                total_exposure INTEGER NOT NULL,
                comments TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id),
                FOREIGN KEY (object_name) REFERENCES objects(name),
                FOREIGN KEY (camera_name) REFERENCES cameras(name),
                FOREIGN KEY (telescope_name) REFERENCES telescopes(name),
                FOREIGN KEY (filter_name) REFERENCES filters(name)
            )
        """)
        
        self.connection.commit()
    
    def add_object(self, name: str, ra: Optional[float] = None, dec: Optional[float] = None) -> int:
        """Add a new object to the database.
        
        Args:
            name: The name of the object
            ra: Optional Right Ascension in degrees (0-360)
            dec: Optional Declination in degrees (-90 to +90)
            
        Returns:
            The ID of the newly created object
        """
        self.cursor.execute(
            "INSERT INTO objects (name, ra, dec) VALUES (?, ?, ?)",
            (name, ra, dec)
        )
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_all_objects(self) -> List[Dict]:
        """Get all objects from the database.
        
        Returns:
            List of dictionaries containing object data (id, name, ra, dec)
        """
        self.cursor.execute("SELECT id, name, ra, dec FROM objects ORDER BY name")
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def update_object(self, object_id: int, name: str, ra: Optional[float] = None, dec: Optional[float] = None) -> bool:
        """Update an existing object.
        
        Args:
            object_id: The ID of the object to update
            name: The new name for the object
            ra: Optional Right Ascension in degrees (0-360)
            dec: Optional Declination in degrees (-90 to +90)
            
        Returns:
            True if the update was successful, False otherwise
        """
        self.cursor.execute(
            "UPDATE objects SET name = ?, ra = ?, dec = ? WHERE id = ?",
            (name, ra, dec, object_id)
        )
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def delete_object(self, object_id: int) -> bool:
        """Delete an object from the database.
        
        Args:
            object_id: The ID of the object to delete
            
        Returns:
            True if the deletion was successful, False otherwise
        """
        self.cursor.execute("DELETE FROM objects WHERE id = ?", (object_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def close(self):
        """Close the database connection."""
        self.connection.close()
    # ==================== Session Methods ====================
    
    def add_session(self, session_id: str, start_date: str, moon_illumination: float = None, moon_ra: float = None, moon_dec: float = None) -> int:
        """Add a new session to the database."""
        self.cursor.execute(
            "INSERT INTO sessions (session_id, start_date, moon_illumination, moon_ra, moon_dec) VALUES (?, ?, ?, ?, ?)",
            (session_id, start_date, moon_illumination, moon_ra, moon_dec)
        )
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_all_sessions(self) -> List[Dict]:
        """Get all sessions from the database."""
        self.cursor.execute("SELECT id, session_id, start_date, moon_illumination, moon_ra, moon_dec FROM sessions ORDER BY id DESC")
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def update_session(self, session_id: int, new_session_id: str, start_date: str, moon_illumination: float = None, moon_ra: float = None, moon_dec: float = None) -> bool:
        """Update an existing session."""
        self.cursor.execute(
            "UPDATE sessions SET session_id = ?, start_date = ?, moon_illumination = ?, moon_ra = ?, moon_dec = ? WHERE id = ?",
            (new_session_id, start_date, moon_illumination, moon_ra, moon_dec, session_id)
        )
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def delete_session(self, session_id: int) -> bool:
        """Delete a session from the database."""
        self.cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def session_id_exists(self, session_id: str, exclude_id: Optional[int] = None) -> bool:
        """Check if a session ID already exists in the database.

        Args:
            session_id: The session ID to check
            exclude_id: Optional internal ID to exclude from the check (for updates)

        Returns:
            True if the session ID exists, False otherwise
        """
        query = "SELECT id FROM sessions WHERE session_id = ?"
        params = (session_id,)
        if exclude_id is not None:
            query += " AND id != ?"
            params = (session_id, exclude_id)
        self.cursor.execute(query, params)
        return self.cursor.fetchone() is not None

    def object_name_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if an object name already exists in the database.

        Args:
            name: The object name to check
            exclude_id: Optional internal ID to exclude from the check (for updates)

        Returns:
            True if the object name exists, False otherwise
        """
        query = "SELECT id FROM objects WHERE name = ?"
        params = (name,)
        if exclude_id is not None:
            query += " AND id != ?"
            params = (name, exclude_id)
        self.cursor.execute(query, params)
        return self.cursor.fetchone() is not None

    def camera_name_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if a camera name already exists in the database.

        Args:
            name: The camera name to check
            exclude_id: Optional internal ID to exclude from the check (for updates)

        Returns:
            True if the camera name exists, False otherwise
        """
        query = "SELECT id FROM cameras WHERE name = ?"
        params = (name,)
        if exclude_id is not None:
            query += " AND id != ?"
            params = (name, exclude_id)
        self.cursor.execute(query, params)
        return self.cursor.fetchone() is not None

    def filter_type_name_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if a filter type name already exists in the database.

        Args:
            name: The filter type name to check
            exclude_id: Optional internal ID to exclude from the check (for updates)

        Returns:
            True if the filter type name exists, False otherwise
        """
        query = "SELECT id FROM filter_types WHERE name = ?"
        params = (name,)
        if exclude_id is not None:
            query += " AND id != ?"
            params = (name, exclude_id)
        self.cursor.execute(query, params)
        return self.cursor.fetchone() is not None

    def filter_name_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if a filter name already exists in the database.

        Args:
            name: The filter name to check
            exclude_id: Optional internal ID to exclude from the check (for updates)

        Returns:
            True if the filter name exists, False otherwise
        """
        query = "SELECT id FROM filters WHERE name = ?"
        params = (name,)
        if exclude_id is not None:
            query += " AND id != ?"
            params = (name, exclude_id)
        self.cursor.execute(query, params)
        return self.cursor.fetchone() is not None

    def telescope_name_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if a telescope name already exists in the database.

        Args:
            name: The telescope name to check
            exclude_id: Optional internal ID to exclude from the check (for updates)

        Returns:
            True if the telescope name exists, False otherwise
        """
        query = "SELECT id FROM telescopes WHERE name = ?"
        params = (name,)
        if exclude_id is not None:
            query += " AND id != ?"
            params = (name, exclude_id)
        self.cursor.execute(query, params)
        return self.cursor.fetchone() is not None
    
    # ==================== Camera Methods ====================
    
    def add_camera(self, name: str, sensor: str, pixel_size: float, width: int, height: int) -> int:
        """Add a new camera to the database."""
        self.cursor.execute(
            "INSERT INTO cameras (name, sensor, pixel_size, width, height) VALUES (?, ?, ?, ?, ?)",
            (name, sensor, pixel_size, width, height)
        )
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_all_cameras(self) -> List[Dict]:
        """Get all cameras from the database."""
        self.cursor.execute("SELECT id, name, sensor, pixel_size, width, height FROM cameras ORDER BY id")
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def update_camera(self, camera_id: int, name: str, sensor: str, pixel_size: float, width: int, height: int) -> bool:
        """Update an existing camera."""
        self.cursor.execute(
            "UPDATE cameras SET name = ?, sensor = ?, pixel_size = ?, width = ?, height = ? WHERE id = ?",
            (name, sensor, pixel_size, width, height, camera_id)
        )
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def delete_camera(self, camera_id: int) -> bool:
        """Delete a camera from the database."""
        self.cursor.execute("DELETE FROM cameras WHERE id = ?", (camera_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    # ==================== Filter Type Methods ====================
    
    def add_filter_type(self, name: str) -> int:
        """Add a new filter type to the database."""
        self.cursor.execute(
            "INSERT INTO filter_types (name) VALUES (?)",
            (name,)
        )
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_all_filter_types(self) -> List[Dict]:
        """Get all filter types from the database."""
        self.cursor.execute("SELECT id, name FROM filter_types ORDER BY id")
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def update_filter_type(self, filter_type_id: int, name: str) -> bool:
        """Update an existing filter type."""
        self.cursor.execute(
            "UPDATE filter_types SET name = ? WHERE id = ?",
            (name, filter_type_id)
        )
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def delete_filter_type(self, filter_type_id: int) -> bool:
        """Delete a filter type from the database."""
        self.cursor.execute("DELETE FROM filter_types WHERE id = ?", (filter_type_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    # ==================== Filter Methods ====================
    
    def add_filter(self, name: str, filter_type: str) -> int:
        """Add a new filter to the database."""
        self.cursor.execute(
            "INSERT INTO filters (name, type) VALUES (?, ?)",
            (name, filter_type)
        )
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_all_filters(self) -> List[Dict]:
        """Get all filters from the database."""
        self.cursor.execute("SELECT id, name, type FROM filters ORDER BY id")
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def update_filter(self, filter_id: int, name: str, filter_type: str) -> bool:
        """Update an existing filter."""
        self.cursor.execute(
            "UPDATE filters SET name = ?, type = ? WHERE id = ?",
            (name, filter_type, filter_id)
        )
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def delete_filter(self, filter_id: int) -> bool:
        """Delete a filter from the database."""
        self.cursor.execute("DELETE FROM filters WHERE id = ?", (filter_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    # ==================== Telescope Methods ====================
    
    def add_telescope(self, name: str, aperture: int, f_ratio: float, focal_length: int) -> int:
        """Add a new telescope to the database."""
        self.cursor.execute(
            "INSERT INTO telescopes (name, aperture, f_ratio, focal_length) VALUES (?, ?, ?, ?)",
            (name, aperture, f_ratio, focal_length)
        )
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_all_telescopes(self) -> List[Dict]:
        """Get all telescopes from the database."""
        self.cursor.execute("SELECT id, name, aperture, f_ratio, focal_length FROM telescopes ORDER BY id")
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def update_telescope(self, telescope_id: int, name: str, aperture: int, f_ratio: float, focal_length: int) -> bool:
        """Update an existing telescope."""
        self.cursor.execute(
            "UPDATE telescopes SET name = ?, aperture = ?, f_ratio = ?, focal_length = ? WHERE id = ?",
            (name, aperture, f_ratio, focal_length, telescope_id)
        )
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def delete_telescope(self, telescope_id: int) -> bool:
        """Delete a telescope from the database."""
        self.cursor.execute("DELETE FROM telescopes WHERE id = ?", (telescope_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0
    # ==================== Observation Methods ====================
    
    def add_observation(self, session_id: str, object_name: str, camera_name: str,
                       telescope_name: str, filter_name: str, image_count: int,
                       exposure_length: int, comments: str) -> int:
        """Add a new observation to the database."""
        total_exposure = image_count * exposure_length
        self.cursor.execute(
            """INSERT INTO observations
               (session_id, object_name, camera_name, telescope_name, filter_name,
                image_count, exposure_length, total_exposure, comments)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (session_id, object_name, camera_name, telescope_name, filter_name,
             image_count, exposure_length, total_exposure, comments)
        )
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_all_observations(self) -> List[Dict]:
        """Get all observations from the database."""
        self.cursor.execute("""
            SELECT o.id, o.session_id, o.object_name, o.camera_name, o.telescope_name,
                   o.filter_name, o.image_count, o.exposure_length, o.total_exposure, o.comments,
                   s.moon_illumination, s.moon_ra, s.moon_dec, s.start_date, obj.ra, obj.dec
            FROM observations o
            JOIN sessions s ON o.session_id = s.session_id
            JOIN objects obj ON o.object_name = obj.name
            ORDER BY o.id DESC
        """)
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def update_observation(self, observation_id: int, session_id: str, object_name: str,
                          camera_name: str, telescope_name: str, filter_name: str,
                          image_count: int, exposure_length: int, comments: str) -> bool:
        """Update an existing observation."""
        total_exposure = image_count * exposure_length
        self.cursor.execute(
            """UPDATE observations
               SET session_id = ?, object_name = ?, camera_name = ?, telescope_name = ?,
                   filter_name = ?, image_count = ?, exposure_length = ?, total_exposure = ?, comments = ?
               WHERE id = ?""",
            (session_id, object_name, camera_name, telescope_name, filter_name,
             image_count, exposure_length, total_exposure, comments, observation_id)
        )
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def delete_observation(self, observation_id: int) -> bool:
        """Delete an observation from the database."""
        self.cursor.execute("DELETE FROM observations WHERE id = ?", (observation_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def get_object_stats(self) -> List[Dict]:
        """Get cumulative exposure statistics for each object grouped by filter type.
        
        Returns:
            List of dictionaries containing object_name, filter_type, and total_exposure
        """
        self.cursor.execute("""
            SELECT
                o.object_name,
                f.type as filter_type,
                SUM(o.total_exposure) as total_exposure
            FROM observations o
            JOIN filters f ON o.filter_name = f.name
            GROUP BY o.object_name, f.type
            ORDER BY o.object_name, f.type
        """)
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_monthly_stats(self) -> List[Dict]:
        """Get cumulative exposure statistics grouped by month.

        Returns:
            List of dictionaries containing year_month and total_exposure in hours
        """
        self.cursor.execute("""
            SELECT
                strftime('%Y-%m', s.start_date) as year_month,
                SUM(o.total_exposure)/3600.0 as total_exposure
            FROM observations o
            JOIN sessions s ON o.session_id = s.session_id
            GROUP BY strftime('%Y-%m', s.start_date)
            ORDER BY year_month
        """)
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]