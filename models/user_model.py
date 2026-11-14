import hashlib
import mysql.connector
from config.database import Database


class UserModel:
    def __init__(self, db=None):
        self.db = db or Database()
        self.conn = self.db.get_connection()
        self.table_name = "users"

    def _get_conn(self):
        if self.conn is None or not self.conn.is_connected():
            self.conn = self.db.get_connection()
        return self.conn

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(str(password).encode("utf-8")).hexdigest()

    def ensure_table(self) -> bool:
        """Memastikan tabel users tersedia beserta akun Admin bawaan."""
        conn = self._get_conn()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                    `id_user` int(11) NOT NULL AUTO_INCREMENT,
                    `username` varchar(50) NOT NULL UNIQUE,
                    `password` varchar(64) NOT NULL,
                    `role` enum('Admin','User') NOT NULL DEFAULT 'User',
                    `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
                    PRIMARY KEY (`id_user`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cursor.execute(
                f"SELECT id_user FROM {self.table_name} WHERE username = %s",
                ("atmin",),
            )
            if cursor.fetchone() is None:
                cursor.execute(
                    f"INSERT INTO {self.table_name} (username, password, role) "
                    "VALUES (%s, %s, %s)",
                    ("atmin", self.hash_password("atmin123"), "Admin"),
                )
            conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            conn.rollback()
            print(f"Error Ensure Users Table: {e}")
            return False

    def get_all_users(self):
        conn = self._get_conn()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            query = (
                f"SELECT id_user, username, role, created_at "
                f"FROM {self.table_name}"
            )
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as e:
            print(f"Error Read Users: {e}")
            return []

    def get_by_username(self, username: str):
        conn = self._get_conn()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name} WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as e:
            print(f"Error Read User By Username: {e}")
            return None

    def create_user(self, username: str, password_hash: str, role: str = "User") -> bool:
        conn = self._get_conn()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = (
                f"INSERT INTO {self.table_name} (username, password, role) "
                "VALUES (%s, %s, %s)"
            )
            cursor.execute(query, (username, password_hash, role))
            conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            conn.rollback()
            print(f"Error Create User: {e}")
            return False

    def verify_user(self, username: str, password: str):
        user = self.get_by_username(username)
        if not user:
            return None
        if user.get("password") == self.hash_password(password):
            return {
                "id_user": user.get("id_user"),
                "username": user.get("username"),
                "role": user.get("role", "User"),
            }
        return None
