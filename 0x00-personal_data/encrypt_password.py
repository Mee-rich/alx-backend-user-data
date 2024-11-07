#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt

def hash_password(password: str) -> bytes:
    """Hashes a pasword using random string
    """
    return bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a hashed password was formed from the given password
    """
    return bcrypt.checkpw(password.encode('UTF-8'), hashed_password)
