from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(raw_pass):
    return pwd_context.hash(raw_pass)


def verify_password(raw_password, hash_password):
    return pwd_context.verify(raw_password, hash_password)