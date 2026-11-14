from unittest.mock import MagicMock
from controller.laundry_controller import LaundryController


def test_hitung_total_biaya():
    controller = LaundryController()
    controller.harga_paket = MagicMock(return_value=8000.0)

    # 3.5 kg * 8000 = 28000.0
    total = controller.hitung_total(3.5, 1)
    assert total == 28000.0

    # Berat 0 atau minus
    assert controller.hitung_total(0, 1) == 0.0
    assert controller.hitung_total(-2, 1) == 0.0
    assert controller.hitung_total("bukan_angka", 1) == 0.0


def test_rbac_transaksi_update_and_delete():
    mock_trx = MagicMock()
    mock_trx.update_transaksi.return_value = True
    mock_trx.delete_transaksi.return_value = True

    # User biasa (bukan Admin)
    controller_user = LaundryController(
        transaksi_model=mock_trx,
        current_user={"username": "budi", "role": "User"},
    )

    # User ditolak saat update transaksi
    ok, msg = controller_user.perbarui(1, 10, 2, 4.0, "2026-11-14", None, "Proses")
    assert not ok
    assert "Akses ditolak" in msg
    mock_trx.update_transaksi.assert_not_called()

    # User ditolak saat hapus transaksi
    ok, msg = controller_user.hapus(1)
    assert not ok
    assert "Akses ditolak" in msg
    mock_trx.delete_transaksi.assert_not_called()

    # Admin diizinkan
    controller_admin = LaundryController(
        transaksi_model=mock_trx,
        current_user={"username": "atmin", "role": "Admin"},
    )
    ok, msg = controller_admin.perbarui(
        1, 10, 2, 4.0, "2026-11-14", None, "Proses"
    )
    assert ok
    assert "berhasil diperbarui" in msg
    mock_trx.update_transaksi.assert_called_once()

    ok, msg = controller_admin.hapus(1)
    assert ok
    assert "berhasil dihapus" in msg
    mock_trx.delete_transaksi.assert_called_once()


def test_rbac_paket_dan_pelanggan_admin_only():
    mock_paket = MagicMock()
    mock_pelanggan = MagicMock()
    mock_pelanggan.get_all_pelanggan.return_value = [{"id_pelanggan": 5, "nama": "Rina"}]
    mock_pelanggan.delete_pelanggan.return_value = True

    controller_user = LaundryController(
        paket_model=mock_paket,
        pelanggan_model=mock_pelanggan,
        current_user={"username": "ani", "role": "User"},
    )

    # User dilarang tambah paket
    ok, msg = controller_user.tambah_paket("Express", "Cuci Kering", 12000)
    assert not ok
    assert "Akses ditolak" in msg

    # User dilarang hapus pelanggan
    ok, msg = controller_user.hapus_pelanggan(5)
    assert not ok
    assert "Akses ditolak" in msg


def test_update_transaksi_memperbarui_bukan_hapus_lalu_buat_baru():
    mock_trx = MagicMock()
    mock_trx.update_transaksi.return_value = True

    controller = LaundryController(
        transaksi_model=mock_trx,
        current_user={"username": "atmin", "role": "Admin"},
    )

    ok, msg = controller.perbarui(
        id_transaksi=99,
        id_pelanggan=10,
        id_paket=2,
        berat_kg=3.0,
        tgl_terima="2026-11-14",
        tgl_selesai="2026-11-16",
        status_cucian="Selesai",
    )

    assert ok
    # Memastikan delete_transaksi TIDAK dipanggil sama sekali saat update
    mock_trx.delete_transaksi.assert_not_called()
    mock_trx.update_transaksi.assert_called_once_with(
        99, 10, 2, 3.0, "2026-11-14", "2026-11-16", 0.0, "Selesai"
    )


def test_validasi_transaksi():
    controller = LaundryController(
        current_user={"username": "atmin", "role": "Admin"}
    )

    # Tanpa pelanggan
    ok, msg = controller.simpan(None, None, 1, 2.0, "2026-11-14", None, "Antrean")
    assert not ok
    assert "Pelanggan wajib" in msg

    # Tanpa paket
    ok, msg = controller.simpan(None, 1, None, 2.0, "2026-11-14", None, "Antrean")
    assert not ok
    assert "Paket layanan wajib" in msg

    # Berat tidak valid
    ok, msg = controller.simpan(None, 1, 1, -1, "2026-11-14", None, "Antrean")
    assert not ok
    assert "lebih besar dari nol" in msg

    # Status tidak valid
    ok, msg = controller.simpan(None, 1, 1, 2.0, "2026-11-14", None, "Batal")
    assert not ok
    assert "Status cucian tidak valid" in msg
