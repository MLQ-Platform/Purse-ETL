from etl.logger import setup_logger
from etl.loader import BaseLoader
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


# Logger 설정
logger = setup_logger(
    loggger_name="SQLDatabaseLoader",
    file_name="loader@sql_database_connector.log",
)


class SQLDatabaseLoader(BaseLoader):
    """
    SQL Database Loader Singleton Class
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)

        return cls._instance

    def __init__(self, db_uri: str):
        """
        Args
            db_uri (`str`): sql db uri
        """

        if not hasattr(self, "initialized"):
            self.db_uri = db_uri
            self.sql_engine = None
            self.initialized = True

    def connect(self):
        """
        Connecting SQL Engine
        """
        try:
            self.sql_engine = create_engine(self.db_uri)
            logger.info("SQL database connection established")

        except SQLAlchemyError as e:
            logger.error(f"Failed to connect to the database: {e}")

        return self.sql_engine

    def close(self):
        """
        Close SQL Engine
        """
        if self.sql_engine:
            self.sql_engine.dispose()
            logger.info("SQL database connection closed")

    def transaction(self, query):
        """
        General Transaction Function.
        Query Commit -> (Rollback) -> Session Close

        Args:
            data: list or rows
            table_name: table name
        """
        connection = self.sql_engine.connect()
        transaction = connection.begin()

        try:
            # Executing the query
            connection.execute(query)
            # Commit the transaction
            transaction.commit()

        except SQLAlchemyError as e:
            transaction.rollback()
            logger.error(f"Failed to load data and roll back: {e}")

        finally:
            connection.close()
