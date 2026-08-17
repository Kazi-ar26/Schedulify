"""
Schedulify Database Seeder

Responsible for:
- Creating default system data
- Creating development demo data
- Preparing fresh installations
"""


import argparse
import logging

from Database.session import database_session



# -------------------------------------------------
# System Seed
# -------------------------------------------------

def seed_roles(session):
    """
    Creates default application roles.

    Roles:
    - ADMIN
    - TEACHER
    - STUDENT

    """

    # Models will be connected later.

    logging.info(
        "Role seeding initialized."
    )



# -------------------------------------------------
# Default Settings Seed
# -------------------------------------------------

def seed_default_settings(session):
    """
    Creates default application settings.
    """

    logging.info(
        "Default settings seeding initialized."
    )



# -------------------------------------------------
# Development Data Seed
# -------------------------------------------------

def seed_development_data(session):
    """
    Inserts development-only data.

    Includes:
    - Demo users
    - Example tasks
    - Sample schedules
    """

    logging.info(
        "Development data seeding initialized."
    )



# -------------------------------------------------
# Main Seeder
# -------------------------------------------------

def run_seed(development=False):
    """
    Executes database seeding.
    """

    logging.info(
        "Starting database seed..."
    )


    with database_session() as session:

        seed_roles(
            session
        )

        seed_default_settings(
            session
        )


        if development:

            seed_development_data(
                session
            )


    logging.info(
        "Database seed completed."
    )



# -------------------------------------------------
# CLI Entry Point
# -------------------------------------------------

if __name__ == "__main__":


    parser = argparse.ArgumentParser(
        description="Schedulify Database Seeder"
    )


    parser.add_argument(
        "--development",
        action="store_true",
        help="Insert development demo data"
    )


    args = parser.parse_args()


    run_seed(
        development=args.development
    )