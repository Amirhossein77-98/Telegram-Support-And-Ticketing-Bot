import sqlite3
from config import admin_id

# Defining database manager class
class DBManager:

    # Initializing database and class
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()

    # Create tables if they don't exist
    def create_tables(self):
        # Creating history table to store messages and user's data
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS history
                (id INTEGER PRIMARY KEY,
                chat_id TEXT,  
                user_id TEXT,
                user_name TEXT,
                message_id TEXT,
                message_date TEXT,
                message TEXT,
                reply_id TEXT,
                admin_id TEXT,
                message_read_state INTEGER,
                photo_id INTEGER)
                """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS admin_replied_messages_to_users
            (id INTEGER PRIMARY KEY,
            user_id TEXT,
            user_name TEXT,
            user_message_id TEXT,
            admin_id TEXT,
            admin_replied_message_id TEXT,
            admin_replied_message_text TEXT)""")
        
        # Creating blocked_users table to store blocked users data
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS blocked_users
                (id INTEGER PRIMARY KEY,
                user_id TEXT,
                user_name TEXT)
                """)
            
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users
            (user_id INTEGER PRIMARY KEY,
            user_name TEXT)""")

    # Defining database methods
    # Saving message recieved from users to database history table
    def save_message(self, chat_id, user_id, user_name, message, message_id, message_date, reply_id, admin_id, photo_id=None):
        self.conn.execute("""
        INSERT INTO history (user_id, chat_id, user_name, message_id, message_date, message, reply_id, admin_id, message_read_state, photo_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (chat_id, user_id, user_name, message_id, message_date, message, reply_id, admin_id, 0, photo_id))
        self.conn.commit()
    
    def save_user(self, user_id, user_name):
        try:
            if user_id not in admin_id:
                self.conn.execute("""
                INSERT INTO users (user_id, user_name) VALUES (?, ?)
                """, (user_id, user_name))
                self.conn.commit()
        except sqlite3.IntegrityError:
            pass

    def count_users(self):
        cursor = self.conn.execute("SELECT COUNT(*) FROM users")
        result = cursor.fetchone()[0]
        return result

    def save_admin_replied_messages(self, user_id, user_name, user_message_id, admin_id, admin_replied_message_id, admin_message_text):
        self.conn.execute("""
        INSERT INTO admin_replied_messages_to_users (user_id, user_name, user_message_id, admin_id, admin_replied_message_id, admin_replied_message_text) VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, user_name, user_message_id, admin_id, admin_replied_message_id, admin_message_text))
        self.conn.commit()


    def admin_replied_message_index_to_a_specific_users_message(self, user_id, message):
        cursor = self.conn.execute("SELECT admin_id, admin_replied_message_id FROM admin_replied_messages_to_users WHERE user_id = ? AND admin_replied_message_text = ?", (user_id, message))
        result = cursor.fetchone()
        return result

    # Getting all messages from a specific user from database
    def get_user_messages(self, user_id):
        cursor = self.conn.execute("""SELECT message_id, message_date, reply_id, admin_id, message, message_read_state, photo_id FROM history WHERE user_id = ?""", (user_id,))
        return cursor.fetchall()
    
    def update_message_read_state(self, user_id, message_id):
        self.conn.execute("UPDATE history SET message_read_state = 1 WHERE user_id = ? AND message_id = ?", (user_id, message_id))
        self.conn.commit()

    # Getting user's name from database
    def get_users_name(self, user_id):
        cursor = self.conn.execute("SELECT user_name FROM history WHERE user_id = ?", (user_id,))
        return cursor.fetchone()

    # Getting all users list
    def get_user_list(self):
        cursor = self.conn.execute("SELECT DISTINCT user_id, user_name FROM history")
        users = cursor.fetchall()
        return [user for user in users if user[0] != None]

    # Getting all blocked users list
    def get_blocked_user_list(self):
        cursor = self.conn.execute("SELECT DISTINCT user_id, user_name FROM blocked_users")
        users = cursor.fetchall()
        return [user for user in users if user[0] != None]

    # Adding user to blocklist
    def add_user_to_blocklist(self, user_id, users_first_name):
        self.conn.execute("INSERT INTO blocked_users (user_id, user_name) VALUES (?, ?)", 
                    (user_id, users_first_name))
        self.conn.commit()

    # Checking if the user's ID is in blocklist or not
    def block_checker(self, user_id):
        cursor = self.conn.execute("SELECT COUNT(*) FROM blocked_users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()[0]
        return result

    def add_user_to_blocklist(self, user_id, users_first_name):
        cursor = self.conn.execute("INSERT INTO blocked_users (user_id, user_name) VALUES (?, ?)", (user_id, users_first_name))
        self.conn.commit()
    
    def delete_user_history(self, user_id):
        cursor = self.conn.execute("DELETE FROM history WHERE user_id = ?", (user_id,))
        self.conn.commit()

    def unblock_user(self, user_id):
        cursor = self.conn.execute("DELETE FROM blocked_users WHERE user_id = ?", (user_id,))
        self.conn.commit()

# Create DB instance
db = DBManager('data.db')