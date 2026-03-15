import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from sqlalchemy import create_engine

# Loading environment variables from .env file
load_dotenv()

# Loading secret key from .env file
secret_key = os.getenv("SECRET_KEY")

# Converting the key to bytes
cipher_suite = Fernet(secret_key.encode())

# Function to decrypt the values
def decrypt_value(encrypted_value):
    if encrypted_value is None:
        return None
    return cipher_suite.decrypt(encrypted_value.encode()).decode()

# Loading db credentials from .env file
enc_db_user = os.getenv("USER")
enc_db_pass = os.getenv("PASS")
enc_db_host = os.getenv("HOST")
enc_db_name = os.getenv("NAME")

# Decrypting credentials
db_user = decrypt_value(enc_db_user)
db_pass = decrypt_value(enc_db_pass)
db_host = decrypt_value(enc_db_host)
db_name = decrypt_value(enc_db_name)

def get_decrpted_values():
    return db_user, db_pass, db_host, db_name

def get_engine(): 
    # SQLALchemy connection string
    DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"

    # Creating engine
    engine = create_engine(DATABASE_URL, echo=False)
    return engine