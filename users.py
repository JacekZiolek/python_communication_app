import argparse
from psycopg2 import connect, OperationalError
from models import Users
from clcrypto import check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new-pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")
args = parser.parse_args()


def create_user(cur):
    """
    Creares new user.

    :param object cur: cursor object
    """
    if Users().load_user_by_username(args.username, cur):
        print("User already exists.")
        return
    if len(args.password) < 8:
        print("Password must be at least 8 characters long.")
        return
    new_user = Users(args.username, args.password)
    new_user.save_to_db(cur)
    print("User has been created")



def edit_password(cur):
    """
    Sets new password.

    :param object cur: cursor object
    """
    u = Users().load_user_by_username(args.username, cur)
    if not u:
        print("User does not exist.")
        return
    if not check_password(args.password, u.hashed_password):
        print("Incorrect password.")
        return
    if len(args.new_pass) < 8:
        print("New password must be at least 8 characters long.")
        return
    u.set_password(args.new_pass)
    u.save_to_db(cur)
    print("Password has been updated.")


def delete_user(cur):
    """
    Deletes user.

    :param object cur: cursor object
    """
    u = Users().load_user_by_username(args.username, cur)
    if not check_password(args.password, u.hashed_password):
        print("Incorrect password.")
        return
    u.delete_user(cur)
    print("User has been deleted.")


def list_users(cur):
    """
    List all users

    :param object cur: cursor object
    """
    user_list = Users().load_all_users(cur)
    for u in user_list:
        print(f"User name: {u.username}, id: {u.id}.")


if __name__ == "__main__":
    try:
        cnx = connect(user="", password="", host="", database="")
        cnx.autocommit = True
        cur = cnx.cursor()
        if args.username and args.password and args.edit and args.new_pass:
            edit_password(cur)
        elif args.username and args.password and args.delete:
            delete_user(cur)
        elif args.username and args.password:
            create_user(cur)
        elif args.list:
            list_users(cur)
        else:
            parser.print_help()
        cur.close()
        cnx.close
    except OperationalError as err:
        print("Connection error: ", err)
