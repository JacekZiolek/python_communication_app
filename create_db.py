from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

"""One time run script that creates database."""
user = ""
host = ""
password = ""
database = ""

create_db = f"CREATE DATABASE {database};"

users_table = """CREATE TABLE users(
    user_id serial,
    username varchar(255),
    hashed_password varchar(80),
    PRIMARY KEY (user_id));"""

messages_table = """CREATE TABLE messages(
    message_id serial,
    from_id int,
    to_id int,
    creation_date timestamp default current_timestamp,
    text varchar(255),
    PRIMARY KEY (message_id),
    FOREIGN KEY (from_id) REFERENCES users(user_id),
    FOREIGN KEY (to_id) REFERENCES users(user_id));"""

if __name__ == "__main__":
    try:
        cnx = connect(user=user, password=password, host=host)
        cnx.autocommit = True
        cur = cnx.cursor()
        try:
            cur.execute(create_db)
            print(f"Database {database} has been created.")
        except DuplicateDatabase:
            print(f"Database {database} already exists.")
        cur.close()
        cnx.close()
    except OperationalError as err:
        print("Connection error: ", err)

    try:
        cnx = connect(user=user, password=password, host=host, database=database)
        cnx.autocommit = True
        cur = cnx.cursor()
        try:
            cur.execute(users_table)
            print("Table 'users' has been created")
        except DuplicateTable as err:
            print("Table already exists: ", err)
        try:
            cur.execute(messages_table)
            print("Table 'messages' has been created")
        except DuplicateTable as err:
            print("Table already exists: ", err)
        cur.close()
        cnx.close()
    except OperationalError as err:
        print("Connection error: ", err)
