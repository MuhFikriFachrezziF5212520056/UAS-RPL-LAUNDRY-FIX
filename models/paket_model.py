import mysql.connector
from config.database import Database


class PaketModel:
    def __init__(self, db=None):
        self.db = db or Database()
        self.conn = self.db.get_connection()
        self.table_name = "paket_layanan"

    def _get_conn(self):
        if self.conn is None or not self.conn.is_connected():
            self.conn = self.db.get_connection()
        return self.conn

    def get_all_paket(self):
        conn = self._get_conn()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as e:
            print(f"Error Read Paket: {e}")
            return []

    def get_paket_by_id(self, id_paket):
        conn = self._get_conn()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name} WHERE id_paket = %s"
            cursor.execute(query, (id_paket,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as e:
            print(f"Error Read Paket By ID: {e}")
            return None

    def create_paket(self, nama_paket, jenis, harga_per_kg):
        conn = self._get_conn()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = (
                f"INSERT INTO {self.table_name} "
                "(nama_paket, jenis, harga_per_kg) VALUES (%s, %s, %s)"
            )
            cursor.execute(query, (nama_paket, jenis, harga_per_kg))
            conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            conn.rollback()
            print(f"Error Create Paket: {e}")
            return False

    def update_paket(self, id_paket, nama_paket, jenis, harga_per_kg):
        conn = self._get_conn()
        if not conn:
            return False
        try:
            if not self.get_paket_by_id(id_paket):
                return False
            cursor = conn.cursor()
            query = (
                f"UPDATE {self.table_name} "
                "SET nama_paket = %s, jenis = %s, harga_per_kg = %s "
                "WHERE id_paket = %s"
            )
            cursor.execute(query, (nama_paket, jenis, harga_per_kg, id_paket))
            conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            conn.rollback()
            print(f"Error Update Paket: {e}")
            return False

    def delete_paket(self, id_paket):
        conn = self._get_conn()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = f"DELETE FROM {self.table_name} WHERE id_paket = %s"
            cursor.execute(query, (id_paket,))
            affected = cursor.rowcount
            conn.commit()
            cursor.close()
            return affected > 0
        except mysql.connector.Error as e:
            conn.rollback()
            print(f"Error Delete Paket: {e}")
            return False
