from db_connector import DBConnector


def hash_password(username, password, database):
    db = DBConnector(database)
    db._connect()
    db.create_users_table()
    db.insert_user(username, password)
    db._disconnect()


def verify_password(username, password, database):
    db = DBConnector(database)
    db._connect()
    result = db.verify_user(username, password)
    db._disconnect()
    return result
