"""
The module designed to contain all the database access logic.
"""

import os

import pymysql


class Accessor:
    """
    This class is designed to contain all the database access logic.
    """

    def __init__(self) -> None:
        """
        The constructor of the Accessor class.

        We create a database connection to be used.
        """
        self.connection = pymysql.connect(
            host=os.environ["DB_SERVER"],
            user=os.environ["DB_USERNAME"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DB_DATABASE"],
            port=int(os.environ["DB_PORT"]),
        )
        self.cursor = None

    def __enter__(self):
        """
        The enter of the Accessor class for a context manager.

        This is designed to be used as a context manager and returns
        the underlying cursor.

        Returns:
            A cursor to execute queries on.
        """
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        return self.cursor

    def __exit__(self, ex_type, ex_value, traceback) -> None:
        """
        The exit of the Accessor class for a context manager.

        This designed to be used as a context manager and handles
        the cleanup of the cursor and database connection.

        Args:
            ex_type: The exception type.
            ex_value: The exception value.
            traceback: The traceback for the exception.
        """
        _, _, _ = ex_type, ex_value, traceback
        self.connection.commit()
        if self.cursor is not None:
            self.cursor.close()

        self.connection.close()
