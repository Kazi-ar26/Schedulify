"""
Schedulify Encryption Utilities

Handles:
- Password hashing
- Password verification

Uses:
- bcrypt

Security layer for authentication.
"""


import bcrypt



class Encryption:



    # -------------------------------------------------
    # Hash Password
    # -------------------------------------------------

    @staticmethod
    def hash_password(
        password: str
    ) -> str:


        password_bytes = (

            password.encode(
                "utf-8"
            )

        )


        salt = bcrypt.gensalt()



        hashed = bcrypt.hashpw(

            password_bytes,

            salt

        )



        return hashed.decode(
            "utf-8"
        )



    # -------------------------------------------------
    # Verify Password
    # -------------------------------------------------

    @staticmethod
    def verify_password(
        password: str,
        hashed_password: str
    ) -> bool:


        password_bytes = (

            password.encode(
                "utf-8"
            )

        )


        hashed_bytes = (

            hashed_password.encode(
                "utf-8"
            )

        )



        return bcrypt.checkpw(

            password_bytes,

            hashed_bytes

        )