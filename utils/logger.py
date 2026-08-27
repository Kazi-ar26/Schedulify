"""
Schedulify Logger Utility

Handles:
- Application logging
- Error tracking
- Debug information

Output:
%LOCALAPPDATA%/Schedulify/logs/schedulify.log
"""

import logging
import os
from pathlib import Path


class Logger:

    _logger = None

    # -------------------------------------------------
    # Logger Initialization
    # -------------------------------------------------

    @classmethod
    def get_logger(cls):

        if cls._logger:
            return cls._logger

        # Use the user's writable Local AppData directory.
        # This works both during development and when installed
        # under Program Files.
        app_data = Path(
            os.getenv(
                "LOCALAPPDATA",
                Path.home() / "AppData" / "Local"
            )
        )

        log_directory = app_data / "Schedulify" / "logs"

        log_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        log_file = log_directory / "schedulify.log"

        logging.basicConfig(
            level=logging.INFO,
            format=(
                "%(asctime)s | "
                "%(levelname)s | "
                "%(name)s | "
                "%(message)s"
            ),
            handlers=[
                logging.FileHandler(
                    log_file,
                    encoding="utf-8"
                ),
                logging.StreamHandler()
            ]
        )

        cls._logger = logging.getLogger(
            "Schedulify"
        )

        return cls._logger

    # -------------------------------------------------
    # Convenience Methods
    # -------------------------------------------------

    @classmethod
    def info(
        cls,
        message: str
    ):
        cls.get_logger().info(
            message
        )

    @classmethod
    def warning(
        cls,
        message: str
    ):
        cls.get_logger().warning(
            message
        )

    @classmethod
    def error(
        cls,
        message: str
    ):
        cls.get_logger().error(
            message
        )