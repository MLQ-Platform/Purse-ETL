import os
import logging


def setup_logger(
    loggger_name: str, file_name: str, log_dir: str = "./logs"
) -> logging.Logger:
    """
    Set up logger

    Args:
        log_file_name (str): log file name
        log_dir (str): base log directory path './logs'

    Returns:
        logging.Logger: Logger instance
    """
    # 로그 디렉토리 생성
    os.makedirs(log_dir, exist_ok=True)

    # Logger
    logger = logging.getLogger(name=loggger_name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # File Handler
        file_handler = logging.FileHandler(os.path.join(log_dir, file_name))
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)

        # Add Handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    logger.propagate = False  # 상위 logger로 메시지 전달 방지

    return logger
