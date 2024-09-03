from etl.logger import setup_logger
from etl.loader import BaseLoader

# Logger 설정
logger = setup_logger(
    loggger_name="RedisLDatabaseLoader",
    file_name="loader@redis_database_connector.log",
)


class RedisDatabaseLoader(BaseLoader):
    """
    Redis Database Loader Singleton Class
    """

    pass
