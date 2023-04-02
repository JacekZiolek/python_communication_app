import argparse
from psycopg2 import connect, OperationalError
from models import Users, Messages
from clcrypto import check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-t", "--to", help="To whom the message is to be sent.")
parser.add_argument("-s", "--send", help="the message")
parser.add_argument("-l", "--list", help="list all messages", action="store_true")
args = parser.parse_args()


def list_messages(cur):
    """
    Lists messages sent to currently logged user.

    :param object cur: cursor object
    """
    u = Users().load_user_by_username(args.username, cur)
    if not u:
        print("User does not exist.")
        return
    if not check_password(args.password, u.hashed_password):
        print("Incorrect password.")
        return
    messages = Messages().load_all_messages(cur)
    for m in messages:
        if m.to_id == u.id:
            author = Users().load_user_by_id(m.from_id, cur).username
            print(f'{author} on {m.creation_date} said "{m.text}"')


def send_message(cur):
    """
    Sends new message

    :param object cur: cursor object
    """
    from_ = Users().load_user_by_username(args.username, cur)
    to = Users().load_user_by_username(args.to, cur)
    if not from_:
        print("User does not exist.")
        return
    if not check_password(args.password, from_.hashed_password):
        print("Incorrect password.")
        return
    if not to:
        print("Addressee does not exist.")
        return
    if len(args.send) > 255:
        print("Message is to long.")
    new_msg = Messages(from_.id, to.id, args.send)
    new_msg.save_to_db(cur)
    print("Message sent.")


if __name__ == "__main__":
    try:
        cnx = connect(user="", password="", host="", database="")
        cnx.autocommit = True
        cur = cnx.cursor()
        if args.username and args.password and args.list:
            list_messages(cur)
        elif args.username and args.password and args.to and args.send:
            send_message(cur)
        else:
            parser.print_help()
        cur.close()
        cnx.close()
    except OperationalError as err:
        print("Connection error: ", err)
