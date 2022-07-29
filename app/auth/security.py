import bcrypt

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(14)).decode("utf-8")

'''Tests'''
if __name__ == "__main__":
    hp = hash_password("ArjunMakesGoodPasswords")
    print(hp, type(hp))
    print(verify_password("ArjunMakesGoodPasswords", hp))
