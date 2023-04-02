from clcrypto import hash_password


class Users:
    """
    Stores user data.

    :param str username: user's name
    :param str password: user's password
    :param str salt: salt for hashed password
    """
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        """Hashes and sets new password."""
        self._hashed_password = hash_password(password, salt)

    def save_to_db(self, cur):
        """
        Saves user to database or updates existing one.

        :param object cur: cursor object
        """
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password) VALUES(%s, %s) RETURNING user_id"""
            values = (self.username, self.hashed_password)
            cur.execute(sql, values)
            self._id = cur.fetchone()[0]
        else:
            sql = """UPDATE users SET username=%s, hashed_password=%s WHERE user_id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cur.execute(sql, values)

    @staticmethod
    def load_user_by_username(username, cur):
        """Loads user by name."""
        sql = """SELECT user_id, username, hashed_password FROM users WHERE username=%s"""
        cur.execute(sql, (username,))
        data = cur.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_user_by_id(id_, cur):
        """Loads user by id."""
        sql = """SELECT user_id, username, hashed_password FROM users WHERE user_id=%s"""
        cur.execute(sql, (id_,))
        data = cur.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_all_users(cur):
        """Loads list of all users."""
        sql = """SELECT user_id, username, hashed_password FROM users"""
        users = []
        cur.execute(sql)
        for row in cur.fetchall():
            id_, username, hashed_password = row
            loaded_user = Users()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete_user(self, cur):
        """Deletes user."""
        sql = """DELETE FROM users WHERE user_id=%s"""
        cur.execute(sql, (self.id,))
        self._id = -1


class Messages:
    """
    Stores messages.

    :param int from_id: id of a sender
    :param int to_id: id of a receiver
    :param str text: a message
    """
    def __init__(self, from_id=None, to_id=None, text=""):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self._creation_date = None
        self.text = text

    @property
    def id(self):
        return self._id

    @property
    def creation_date(self):
        return self._creation_date

    def save_to_db(self, cur):
        """
        Saves the message to the database.

        :param object cur: cursor object
        """
        if self._id == -1:
            sql = """
                INSERT INTO messages(from_id, to_id, text)
                VALUES(%s, %s, %s)
                RETURNING message_id, creation_date
                """
            values = (self.from_id, self.to_id, self.text)
            cur.execute(sql, values)
            self._id, self._creation_date = cur.fetchone()
        # else:
        #     sql = """UPDATE messages SET from_id=%s, to_id=%s, text=%s WHERE message_id=%s"""
        #     values = (self.from_id, self.to_id, self.text, self.id)
        #     cur.execute(sql, values)

    @staticmethod
    def load_all_messages(cur):
        """
        List all messages in the database.

        :param object cur: cursor object
        :return: list of messages, where each message is a Message() instance
        """
        sql = """SELECT message_id, from_id, to_id, creation_date, text FROM messages"""
        messages = []
        cur.execute(sql)
        for row in cur.fetchall():
            id_, from_id, to_id, creation_date, text = row
            loaded_message = Messages()
            loaded_message._id = id_
            loaded_message.from_id = from_id
            loaded_message.to_id = to_id
            loaded_message._creation_date = creation_date
            loaded_message.text = text
            messages.append(loaded_message)
        return messages
