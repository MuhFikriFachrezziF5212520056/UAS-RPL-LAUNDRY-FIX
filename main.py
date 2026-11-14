import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from config.database import Database
from controller.laundry_controller import LaundryController
from controller.auth_controller import AuthController
from models.user_model import UserModel
from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.laundry_view import LaundryView, _label, _tombol

JUDUL = "SIM Laundry - Sistem Informasi Manajemen Operasional Jasa Laundry"

LATAR = "#eff9f6"
SIDE = "#ffffff"
KARTU = "#ffffff"
MINT = "#0d9488"
MINT_GELAP = "#0f766e"
MINT_MUDA = "#ccfbf1"
TEKS = "#0f3d38"
TEKS_LUNAK = "#5f8a84"
MERAH = "#f43f5e"


def terapkan_tema() -> None:
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")


def koneksi_tersedia() -> bool:
    conn = Database().get_connection()
    if conn is None:
        return False
    conn.close()
    return True


def muat_icon_logo(ukuran=(48, 48)):
    logo_path = Path(__file__).resolve().parent / "assets" / "logo.png"
    if logo_path.exists():
        try:
            img = Image.open(logo_path).resize(ukuran)
            return ctk.CTkImage(light_image=img, dark_image=img, size=ukuran)
        except Exception:
            pass
    return None


def buka_splash_screen(durasi_ms: int = 1500) -> None:
    splash = ctk.CTk(fg_color=MINT)
    splash.overrideredirect(True)

    w, h = 420, 260
    sw = splash.winfo_screenwidth()
    sh = splash.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    splash.geometry(f"{w}x{h}+{x}+{y}")

    konten = ctk.CTkFrame(splash, fg_color="transparent")
    konten.pack(expand=True, fill="both", padx=20, pady=20)

    logo_img = muat_icon_logo((72, 72))
    if logo_img:
        lbl_logo = ctk.CTkLabel(konten, image=logo_img, text="")
        lbl_logo.pack(pady=(12, 6))
    else:
        _label(konten, "\U0001F9FA", 0, 0, gaya={"font": ("Segoe UI", 48)})

    lbl_judul = ctk.CTkLabel(
        konten,
        text="SIM LAUNDRY",
        font=("Segoe UI", 20, "bold"),
        text_color="#ffffff",
    )
    lbl_judul.pack(pady=(0, 2))

    lbl_sub = ctk.CTkLabel(
        konten,
        text="Sistem Informasi Manajemen Operasional Jasa Laundry",
        font=("Segoe UI", 11),
        text_color=MINT_MUDA,
    )
    lbl_sub.pack(pady=(0, 14))

    progres = ctk.CTkProgressBar(
        konten,
        width=280,
        height=8,
        corner_radius=4,
        progress_color="#ffffff",
        fg_color=MINT_GELAP,
    )
    progres.pack(pady=(0, 6))
    progres.set(0)

    langkah = 30
    jeda = durasi_ms // langkah

    def update_bar(i=0):
        if i <= langkah:
            progres.set(i / langkah)
            splash.after(jeda, lambda: update_bar(i + 1))
        else:
            splash.destroy()

    splash.after(50, update_bar)
    splash.mainloop()


def buka_jendela_login(controller) -> dict:
    jendela = ctk.CTk(fg_color=LATAR)
    jendela.title("Login - SIM Laundry")
    jendela.geometry("880x640")
    jendela.resizable(False, False)

    view = LoginView(jendela, controller)
    view.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
    jendela.grid_rowconfigure(0, weight=1)
    jendela.grid_columnconfigure(0, weight=1)

    jendela.mainloop()

    if getattr(view, "pengguna_masuk", None) is None:
        raise SystemExit

    return view.pengguna_masuk


def _sidebar(bangunan, pengguna_info, aktif: str):
    if isinstance(pengguna_info, dict):
        nama = pengguna_info.get("username", "operator")
        role = pengguna_info.get("role", "User")
    else:
        nama = str(pengguna_info)
        role = "User"

    sisi = ctk.CTkFrame(bangunan, width=236, corner_radius=0, fg_color=SIDE)
    sisi.pack(side="left", fill="y")
    sisi.grid_propagate(False)
    sisi.grid_columnconfigure(0, weight=1)
    sisi.grid_rowconfigure(5, weight=1)

    # Logo & judul sidebar
    logo_img = muat_icon_logo((44, 44))
    if logo_img:
        lbl_logo = ctk.CTkLabel(sisi, image=logo_img, text="")
        lbl_logo.grid(row=0, column=0, pady=(20, 0))
    else:
        _label(sisi, "\U0001F9FA", 0, 0, gaya={"font": ("Segoe UI", 30)}, pady=(24, 0))

    _label(
        sisi,
        "SIM Laundry",
        1,
        0,
        gaya={"font": ("Segoe UI", 18, "bold"), "text_color": TEKS},
        pady=(4, 0),
    )
    _label(
        sisi,
        "Manajemen Operasional\nJasa Laundry",
        2,
        0,
        gaya={
            "font": ("Segoe UI", 11),
            "text_color": TEKS_LUNAK,
            "justify": "center",
        },
        pady=(2, 20),
    )

    # Menu navigasi
    menu = {}
    for baris, (item_nama, ikon) in enumerate(
        (("Dashboard", "\U0001F4CA"), ("Transaksi Laundry", "\U0001F9FA")),
        start=3,
    ):
        terpilih = item_nama == aktif
        menu[item_nama] = _tombol(
            sisi,
            f"  {ikon}   {item_nama}",
            None,
            baris,
            0,
            gaya={
                "anchor": "w",
                "corner_radius": 12,
                "height": 44,
                "font": ("Segoe UI", 13, "bold"),
                "hover_color": MINT_MUDA,
                "border_width": 0,
                "fg_color": MINT_MUDA if terpilih else "transparent",
                "text_color": MINT_GELAP if terpilih else TEKS,
            },
            sticky="ew",
            padx=14,
            pady=4,
        )

    # Kartu pengguna di bawah sidebar
    kartu = ctk.CTkFrame(sisi, fg_color=LATAR, corner_radius=12)
    kartu.grid(row=6, column=0, sticky="ew", padx=14, pady=(0, 20))

    _label(
        kartu,
        f"Role: {role}",
        0,
        0,
        gaya={"font": ("Segoe UI", 10, "bold"), "text_color": MINT_GELAP, "anchor": "w"},
    ).grid(sticky="ew", padx=12, pady=(8, 0))

    _label(
        kartu,
        nama,
        1,
        0,
        gaya={"font": ("Segoe UI", 13, "bold"), "text_color": TEKS, "anchor": "w"},
    ).grid(sticky="ew", padx=12, pady=(0, 8))

    _tombol(
        kartu,
        "Keluar",
        None,
        2,
        0,
        gaya={
            "height": 32,
            "corner_radius": 10,
            "fg_color": "transparent",
            "border_width": 1,
            "border_color": MERAH,
            "text_color": MERAH,
            "font": ("Segoe UI", 12, "bold"),
        },
    ).grid(sticky="ew", padx=12, pady=(0, 10))

    return sisi, menu, kartu


def buka_jendela_utama(controller, pengguna_info) -> None:
    controller.set_user(pengguna_info)

    jendela = ctk.CTk(fg_color=LATAR)
    jendela.title(JUDUL)
    jendela.geometry("1280x800+20+20")
    jendela.minsize(1040, 640)

    _, menu, kartu = _sidebar(jendela, pengguna_info, "Dashboard")

    konten = ctk.CTkFrame(jendela, fg_color=LATAR, corner_radius=0)
    konten.pack(side="right", fill="both", expand=True)
    konten.grid_rowconfigure(1, weight=1)
    konten.grid_columnconfigure(0, weight=1)

    _label(
        konten,
        "Selamat datang di Sistem Informasi Manajemen Operasional Jasa Laundry",
        0,
        0,
        gaya={"font": ("Segoe UI", 12), "text_color": TEKS_LUNAK, "anchor": "w"},
        sticky="ew",
        padx=22,
        pady=(18, 8),
    )

    wadah = ctk.CTkFrame(konten, fg_color=LATAR)
    wadah.grid(row=1, column=0, sticky="nsew", padx=22, pady=(0, 18))
    wadah.grid_rowconfigure(0, weight=1)
    wadah.grid_columnconfigure(0, weight=1)

    view_dashboard = DashboardView(wadah, controller, pengguna_info)
    view_transaksi = LaundryView(wadah, controller)

    for tampilan in (view_dashboard, view_transaksi):
        tampilan.configure(fg_color=LATAR)
        tampilan.grid(row=0, column=0, sticky="nsew")
    for bingkai in (
        view_dashboard.frame_kartu,
        view_dashboard.frame_kontak,
        view_dashboard.frame_status,
        view_dashboard.frame_terbaru,
        view_transaksi.frame_form,
        view_transaksi.frame_tabel,
    ):
        bingkai.configure(fg_color=KARTU, corner_radius=14)

    for kartu_kecil in view_dashboard.frame_kartu_isi:
        kartu_kecil.configure(fg_color=KARTU)
    view_dashboard.btn_refresh.configure(fg_color=MINT, hover_color=MINT_GELAP)
    view_transaksi.grid_rowconfigure(1, weight=1)
    view_transaksi.grid_columnconfigure(1, weight=1)

    def tampilkan(nama: str) -> None:
        for kunci, tombol in menu.items():
            terpilih = kunci == nama
            tombol.configure(
                fg_color=MINT_MUDA if terpilih else "transparent",
                text_color=MINT_GELAP if terpilih else TEKS,
            )
        if nama == "Dashboard":
            view_dashboard.muat_data()
            view_dashboard.tkraise()
        else:
            view_transaksi.sesuaikan_hak_akses()
            view_transaksi.muat_data_pendukung()
            view_transaksi.muat_daftar()
            view_transaksi.tkraise()

    menu["Dashboard"].configure(command=lambda: tampilkan("Dashboard"))
    menu["Transaksi Laundry"].configure(
        command=lambda: tampilkan("Transaksi Laundry")
    )
    kartu.winfo_children()[-1].configure(command=jendela.destroy)

    tampilkan("Dashboard")
    jendela.mainloop()


def main() -> None:
    buka_splash_screen(durasi_ms=1200)

    if not koneksi_tersedia():
        jalan = messagebox.askyesno(
            "Basis Data Tidak Terjangkau",
            "Tidak dapat terhubung ke MySQL.\n\n"
            "Pastikan Laragon/MySQL berjalan dan database 'db_laundry' sudah "
            "dibuat. Tetap jalankan aplikasi?",
            icon="warning",
        )
        if not jalan:
            return

    terapkan_tema()

    # Pastikan tabel users terpasang
    UserModel().ensure_table()

    auth_controller = AuthController()
    controller = LaundryController(auth_controller=auth_controller)

    try:
        pengguna_info = buka_jendela_login(controller)
    except SystemExit:
        return

    buka_jendela_utama(controller, pengguna_info)


if __name__ == "__main__":
    main()
