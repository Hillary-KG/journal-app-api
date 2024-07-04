"""This module contains functionality to generate and verify password hash"""

import bcrypt


def hash_password(password_str: str):
    password_hash = bcrypt.hashpw(password_str.encode("utf-8"), bcrypt.gensalt())

    return password_hash


def check_password(password_str: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password_str.encode("utf-8"), password_hash.encode("utf-8"))
