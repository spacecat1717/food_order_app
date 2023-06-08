""" There are some utils for hashing and verification """

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(raw_pass):
    """
    Hashing user's password before saving in DB
    :param raw_pass: raw user's password
    :return: hashed password
    """
    return pwd_context.hash(raw_pass)


def verify_password(raw_password, hashed_password):
    """
    Check password by hash
    :param raw_password: raw user's password from login form
    :param hashed_password: hashed user's password from DB
    :return: bool
    """
    return pwd_context.verify(raw_password, hashed_password)