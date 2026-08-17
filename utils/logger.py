"""
Schedulify Logger Utility

Handles:
- Application logging
- Error tracking
- Debug information

Output:
logs/schedulify.log
"""


import logging

import os



class Logger:



    _logger = None



    # -------------------------------------------------
    # Logger Initialization
    # -------------------------------------------------

    @classmethod
    def get_logger(
        cls
    ):


        if cls._logger:

            return cls._logger



        log_directory = os.path.join(

            os.path.dirname(

                os.path.dirname(

                    os.path.abspath(__file__)

                )

            ),

            "logs"

        )



        os.makedirs(

            log_directory,

            exist_ok=True

        )



        log_file = os.path.join(

            log_directory,

            "schedulify.log"

        )



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