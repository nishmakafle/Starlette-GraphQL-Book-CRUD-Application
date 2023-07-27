import bcrypt

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    # Return the hashed password as a string
    return hashed_password.decode()

def verify_password(hashed_password, input_password):
    # Verify the input password against the hashed password
    return bcrypt.checkpw(input_password.encode(), hashed_password.encode())



class CustomError(Exception):
    def __init__(self, message: str):
        self.message = message