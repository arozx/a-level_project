from passlib.hash import pbkdf2_sha256


def hash_password(password):
    # TODO Save to database
    return pbkdf2_sha256.hash(password)


# Returns True or False
def verify_password(password, hash):
    return pbkdf2_sha256.verify(password, hash)
