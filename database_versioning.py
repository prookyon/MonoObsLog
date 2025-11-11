"""
Database versioning and migrations module.

This module manages database schema migrations. Each migration is a SQL statement
that updates the database schema. Migrations are run sequentially starting from
the current database_version setting.
"""

VERSION = 1

# List of migrations, indexed from 0. Migration N is at index N-1.
# For example, to run migration 1, run migrations[0]
migrations = [
    # Migration 1: Add Priority column to filter_types table
    "ALTER TABLE filter_types ADD COLUMN priority INTEGER DEFAULT 0"
]