from unittest.mock import MagicMock
from models.pelanggan_model import PelangganModel
from models.paket_model import PaketModel


def test_pelanggan_model_crud():
    mock_db = MagicMock()
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db.get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    model = PelangganModel(db=mock_db)

    # 1. Read All
    mock_cursor.fetchall.return_value = [
        {"id_pelanggan": 1, "nama": "Budi", "no_telp": "08123456789", "alamat": "Jl. Mawar"}
    ]
    data = model.get_all_pelanggan()
    assert len(data) == 1
    assert data[0]["nama"] == "Budi"

    # 2. Create
    ok = model.create_pelanggan("Siti", "08987654321", "Jl. Melati")
    assert ok is True
    mock_conn.commit.assert_called()

    # 3. Update
    mock_cursor.fetchone.return_value = {"id_pelanggan": 1}
    ok_update = model.update_pelanggan(1, "Budi Santoso", "08123456789", "Jl. Mawar No. 10")
    assert ok_update is True

    # 4. Delete
    mock_cursor.rowcount = 1
    ok_delete = model.delete_pelanggan(1)
    assert ok_delete is True


def test_paket_model_crud():
    mock_db = MagicMock()
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db.get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    model = PaketModel(db=mock_db)

    # 1. Read All
    mock_cursor.fetchall.return_value = [
        {"id_paket": 1, "nama_paket": "Cuci Kering", "jenis": "Kiloan", "harga_per_kg": 7000.0}
    ]
    data = model.get_all_paket()
    assert len(data) == 1
    assert data[0]["nama_paket"] == "Cuci Kering"

    # 2. Create
    ok = model.create_paket("Express", "Kilat", 12000.0)
    assert ok is True
    mock_conn.commit.assert_called()

    # 3. Update
    mock_cursor.fetchone.return_value = {"id_paket": 1}
    ok_update = model.update_paket(1, "Cuci Setrika", "Kiloan", 9000.0)
    assert ok_update is True

    # 4. Delete
    mock_cursor.rowcount = 1
    ok_delete = model.delete_paket(1)
    assert ok_delete is True
