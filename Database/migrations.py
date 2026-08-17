"""
Schedulify Database Migration Manager

Handles:
- Database schema upgrades
- Database schema downgrades
- Migration status checking

Powered by Alembic.
"""


import logging
import subprocess
import sys

from pathlib import Path



# -------------------------------------------------
# Paths
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

ALEMBIC_PATH = BASE_DIR / "alembic.ini"



# -------------------------------------------------
# Alembic Command Runner
# -------------------------------------------------

def run_alembic_command(arguments: list[str]):
    """
    Executes Alembic CLI commands.

    Example:

        run_alembic_command(
            ["upgrade", "head"]
        )

    """


    if not ALEMBIC_PATH.exists():

        raise FileNotFoundError(
            "alembic.ini not found."
        )


    command = [
        sys.executable,
        "-m",
        "alembic"
    ]

    command.extend(arguments)


    try:

        result = subprocess.run(
            command,
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )


        if result.returncode != 0:

            logging.error(
                result.stderr
            )

            raise RuntimeError(
                "Alembic command failed."
            )


        logging.info(
            result.stdout
        )


        return result.stdout


    except Exception as error:

        logging.error(
            f"Migration error: {error}"
        )

        raise



# -------------------------------------------------
# Upgrade Database
# -------------------------------------------------

def upgrade_database():
    """
    Applies all pending migrations.
    """

    return run_alembic_command(
        [
            "upgrade",
            "head"
        ]
    )



# -------------------------------------------------
# Downgrade Database
# -------------------------------------------------

def downgrade_database():
    """
    Rolls back the latest migration.
    """

    return run_alembic_command(
        [
            "downgrade",
            "-1"
        ]
    )



# -------------------------------------------------
# Migration Status
# -------------------------------------------------

def migration_status():
    """
    Displays current database migration status.
    """

    return run_alembic_command(
        [
            "current"
        ]
    )



# -------------------------------------------------
# Create Migration
# -------------------------------------------------

def create_migration(message: str):
    """
    Creates a new migration file.

    Example:

        create_migration(
            "add task table"
        )

    """

    return run_alembic_command(
        [
            "revision",
            "--autogenerate",
            "-m",
            message
        ]
    )