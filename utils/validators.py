"""
Schedulify Validation Utilities

Handles:
- Email validation
- Password validation
- General input validation
- Data sanitization
"""


import re



class Validator:



    # -------------------------------------------------
    # Email Validation
    # -------------------------------------------------

    @staticmethod
    def validate_email(
        email: str
    ) -> bool:


        pattern = (

            r"^[A-Za-z0-9._%+-]+@"

            r"[A-Za-z0-9.-]+\."

            r"[A-Za-z]{2,}$"

        )


        return bool(

            re.match(
                pattern,
                email
            )

        )



    # -------------------------------------------------
    # Password Validation
    # -------------------------------------------------

    @staticmethod
    def validate_password(
        password: str
    ) -> bool:


        """
        Password requirements:

        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number

        """


        if len(password) < 8:

            return False


        if not re.search(
            r"[A-Z]",
            password
        ):

            return False


        if not re.search(
            r"[a-z]",
            password
        ):

            return False


        if not re.search(
            r"[0-9]",
            password
        ):

            return False


        return True



    # -------------------------------------------------
    # Empty Field Validation
    # -------------------------------------------------

    @staticmethod
    def validate_required(
        value: str
    ) -> bool:


        if value is None:

            return False


        return bool(

            value.strip()

        )



    # -------------------------------------------------
    # Text Sanitization
    # -------------------------------------------------

    @staticmethod
    def sanitize_text(
        text: str
    ) -> str:


        if not text:

            return ""


        return (

            text

            .strip()

            .replace(
                "<",
                ""
            )

            .replace(
                ">",
                ""

            )

        )