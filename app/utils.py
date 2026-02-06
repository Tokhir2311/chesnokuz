from passlib.context import CryptContext

pass_context = CryptContext(schemes=["argon2"], deprecated="auto")


def generate_slug(title):
    return title.lower().replace(" ", "-")


def hash_it(registr_pass:str):
    return pass_context.hash(registr_pass)


def verify_it(first_p:str, second_p):
    return pass_context.verify(first_p, second_p)