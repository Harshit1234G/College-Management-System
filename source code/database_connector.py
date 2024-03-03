import sqlite3


class DatabaseConnector:
    """
    A context manager for connecting to a sqlite database.

    Usage:
    ```
    with DatabaseConnector() as connector:
        # Use the connector to perform database operations within this block
        # The connection and cursor are automatically closed when the block exits.
    ```

    Attributes:
    - `db`: Represents the sqlite database connection.
    - `cursor`: Represents the database cursor used for executing SQL queries.
    The attributes `db` and `cursor` are created upon entering the context and are used for database operations.

    Example:
    ```
    with DatabaseConnector() as connector:
        connector.cursor.execute("SELECT * FROM students;")
        results = connector.cursor.fetchall()
        for row in results:
            print(row)
    ```

    Note:
    - Ensure that the sqlite server is running and accessible with the provided credentials.
    - It is recommended to use the `with` statement to ensure proper resource cleanup.
    - The `exc_tb` parameter is related to exception handling and is provided by the `with` statement when an exception occurs.
    """

    def __enter__(self):
        """
        Establishes a connection to the sqlite database and returns the DatabaseConnector instance.

        Returns:
        - DatabaseConnector: The instance of the DatabaseConnector with an active connection and cursor.
        """

        self.db = sqlite3.connect('data.sqlite')
        self.cursor = self.db.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the database cursor and connection when exiting the context.

        Parameters:
        - exc_type: The type of exception that occurred, if any.
        - exc_val: The exception instance, if any.
        - exc_tb: The traceback object, if any.
        """
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
