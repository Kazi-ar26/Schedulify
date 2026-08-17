"""
Schedulify Helper Utilities

Reusable helper functions for:
- Date and time handling
- File operations
- Common calculations
"""


import os

from datetime import datetime, timedelta



# -------------------------------------------------
# Date / Time Helpers
# -------------------------------------------------

def format_datetime(
    value: datetime,
    format_string: str = "%d %b %Y %H:%M"
) -> str:


    if not value:

        return ""


    return value.strftime(
        format_string
    )



def get_current_datetime() -> datetime:


    return datetime.now()



def add_minutes(
    start_time: datetime,
    minutes: int
) -> datetime:


    return start_time + timedelta(

        minutes=minutes

    )



# -------------------------------------------------
# File Helpers
# -------------------------------------------------

def ensure_directory(
    path: str
) -> None:


    if not os.path.exists(
        path
    ):

        os.makedirs(
            path
        )



def read_file(
    file_path: str
) -> str:


    if not os.path.exists(
        file_path
    ):

        return ""


    with open(

        file_path,

        "r",

        encoding="utf-8"

    ) as file:


        return file.read()



def write_file(
    file_path: str,
    content: str
) -> None:


    directory = os.path.dirname(
        file_path
    )


    if directory:

        ensure_directory(
            directory
        )



    with open(

        file_path,

        "w",

        encoding="utf-8"

    ) as file:


        file.write(
            content
        )



# -------------------------------------------------
# Calculation Helpers
# -------------------------------------------------

def calculate_percentage(
    completed: int,
    total: int
) -> float:


    if total == 0:

        return 0.0


    return round(

        (completed / total) * 100,

        2

    )



def clamp(
    value: float,
    minimum: float,
    maximum: float
) -> float:


    return max(

        minimum,

        min(

            value,

            maximum

        )

    )