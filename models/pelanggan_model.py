import mysql.connector
from config.database import Database


class PelangganModel:
    def __init__(self, db=None):
        self.db = db or Database()
        self.conn = self.db.get_connection()
        self.table_name = "pelanggan"

    def _get_conn(self):
        if self.conn is None or not self.conn.is_connected():
            self.conn = self.db.get_connection()
        return self.conn

    def get_all_pelanggan(self):
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
            print(f"Error Read Pelanggan: {e}")
            return []

    def get_pelanggan_by_id(self, id_pelanggan):
        conn = self._get_conn()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name} WHERE id_pelanggan = %s"
            cursor.execute(query, (id_pelanggan,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as e:
            print(f"Error Read Pelanggan By ID: {e}")
            return None

    def create_pelanggan(self, nama, no_telp, alamat):
        conn = self._get_conn()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = (
                f"INSERT INTO {self.table_name} (nama, no_telp, alamat) "
                "VALUES (%s, %s, %s)"
            )
            cursor.execute(query, (nama, no_telp, alamat))
            conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            conn.rollback()
            print(f"Error Create Pelanggan: {e}")
            return False

    def update_pelanggan(self, id_pelanggan, nama, no_telp, alamat):
        conn = self._get_conn()
        if not conn:
            return False
        try:
            if not self.get_pelanggan_by_id(id_pelanggan):
                return False
            cursor = conn.cursor()
            query = (
                f"UPDATE {self.table_name} "
                "SET nama = %s, no_telp = %s, alamat = %s "
                "WHERE id_pelanggan = %s"
            )
            cursor.execute(query, (nama, no_telp, alamat, id_pelanggan))
            conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            conn.rollback()
            print(f"Error Update Pelanggan: {e}")
            return False

    def delete_pelanggan(self, id_pelanggan):
        conn = self._get_conn()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = f"DELETE FROM {self.table_name} WHERE id_pelanggan = %s"
            cursor.execute(query, (id_pelanggan,))
            affected = cursor.rowcount
            conn.commit()
            cursor.close()
            return affected > 0
        except mysql.connector.Error as e:
            conn.rollback()
            print(f"Error Delete Pelanggan: {e}")
            return False
