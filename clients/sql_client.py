
import os
import sqlite3

from configs.settings import DATABASE_PATH


class SQLClient:
    """Thin wrapper around a SQLite database connection.

    The client validates the database path, opens a connection on demand, and
    closes it automatically after queries are executed.
    """

    def __init__(self, connection_string=DATABASE_PATH):
        """Initialize the SQL client with a database path.

        Args:
            connection_string: File path to the SQLite database to use.
        """
        self.connection_string = connection_string
        self.connection = None

    def _connect(self):
        """Open the database connection if one is not already established.

        Raises:
            Exception: If the configured database path is missing or invalid.
        """
        if not self.connection_string:
            raise Exception(f"The database path is not set. Please set environment variable: DATABASE_PATH")

        if not os.path.exists(self.connection_string):
            raise Exception(f"The database file does not exist: {self.connection_string}")

        if not self.connection:
            self.connection = sqlite3.connect(self.connection_string)

    def _close(self):
        """Close any active database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query):
        """Execute a SQL query and return every row as a dictionary.

        Args:
            query: SQL statement to execute.

        Returns:
            A list of dictionaries, each representing a row from the result set.
        """
        self._connect()
        self.connection.row_factory = sqlite3.Row
        cursor = self.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall() # returns a list of sqlite3.Row objects, which can be converted to dicts
        cursor.close()
        self._close()

        return [dict(row) for row in rows]
