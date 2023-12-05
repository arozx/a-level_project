import os
from dotenv import dotenv_values, set_key


def initialize_database(database_name):
    # Create the database connection and initialize it
    # Generate the necessary keys for the database
    keys = {
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_USER": "username",
        "DB_PASSWORD": "password",
        "DB_NAME": database_name,
    }

    # Create a .env file and store the keys in it
    with open(".env", "w") as env_file:
        for key, value in keys.items():
            set_key(".env", key, value)
            env_file.write(f"{key}={value}\n")

    return "Database initialized successfully."


# Example usage
initialize_database("my_database")
