from pathlib import Path
import customtkinter as ctk
from PIL import Image
from views.laundry_view import bind_event, _label, _input, _tombol
from views.register_view import RegisterView

PALET = {
    "kartu": "#ffffff",
    "aksen": "#0d9488",
    "aksen_gelap": "#0f766e",
    "aksen_muda": "#ccfbf1",
    "teks": "#0f3d38",
    "teks_lunak": "#5f8a84",
    "konsol": "#eff9f6",
    "salah": "#e11d48",
}


class LoginView(ctk.CTkFrame):
    def __init__(self, master, controller, auth_controller=None):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.auth_controller = auth_controller or getattr(
            controller, "auth_controller", None
        )
        self.pengguna_masuk = None
        self.warna = PALET
        self.sandi_terlihat = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.wadah = ctk.CTkFrame(self, fg_color="transparent")
        self.wadah.grid(row=0, column=0, sticky="nsew")
        self.wadah.grid_rowconfigure(0, weight=1)
        self.wadah.grid_columnconfigure(0, weight=1)

        self._build_kartu_login()
        self._build_kartu_register()
        self._build_kaki()

        self._tampilkan_login()

    def _muat_logo_image(self, ukuran=(48, 48)):
        logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
        if logo_path.exists():
            try:
                pil_img = Image.open(logo_path).resize(ukuran)
                return ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=ukuran)
            except Exception:
                pass
        return None

    def _build_kartu_login(self) -> None:
        w = self.warna
        isi = {
            "height": 42,
            "corner_radius": 10,
            "border_width": 1,
            "fg_color": "#ffffff",
            "text_color": w["teks"],
            "placeholder_text_color": w["teks_lunak"],
        }
        judul = {
            "font": ("Segoe UI", 12, "bold"),
            "text_color": w["teks"],
            "anchor": "w",
        }

        self.kartu_login = ctk.CTkFrame(
            self.wadah, fg_color=w["kartu"], corner_radius=20, width=470
        )
        kartu = self.kartu_login
        kartu.grid(row=0, column=0, padx=24, pady=(16, 6))
        kartu.grid_columnconfigure(0, weight=1)

        # Header kartu
        kepala = ctk.CTkFrame(kartu, fg_color=w["aksen"], corner_radius=14)
        kepala.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 0))
        kepala.grid_columnconfigure(1, weight=1)

        lencana = ctk.CTkFrame(
            kepala,
            fg_color=w["aksen_muda"],
            width=56,
            height=56,
            corner_radius=16,
        )
        lencana.grid(row=0, column=0, rowspan=2, padx=(16, 0), pady=16)
        lencana.grid_propagate(False)

        logo_img = self._muat_logo_image((42, 42))
        if logo_img:
            lbl_logo = ctk.CTkLabel(lencana, image=logo_img, text="")
            lbl_logo.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        else:
            _label(lencana, "\U0001F9FA", 0, 0, gaya={"font": ("Segoe UI", 26)})

        _label(
            kepala,
            "SIM Laundry",
            0,
            1,
            gaya={
                "font": ("Segoe UI", 22, "bold"),
                "text_color": "#ffffff",
                "anchor": "w",
            },
            sticky="sw",
            padx=(14, 16),
            pady=(18, 0),
        )
        _label(
            kepala,
            "Sistem Informasi Manajemen Operasional\nJasa Laundry",
            1,
            1,
            gaya={
                "font": ("Segoe UI", 11),
                "text_color": "#d6e4ff",
                "justify": "left",
                "anchor": "w",
            },
            sticky="nw",
            padx=(14, 16),
            pady=(2, 18),
        )

        # Sub judul
        _label(
            kartu,
            "Masuk",
            1,
            0,
            gaya={
                "font": ("Segoe UI", 18, "bold"),
                "text_color": w["teks"],
                "anchor": "w",
            },
            sticky="ew",
            padx=28,
            pady=(20, 0),
        )
        _label(
            kartu,
            "Gunakan akun operator atau daftar akun baru.",
            2,
            0,
            gaya={
                "font": ("Segoe UI", 12),
                "text_color": w["teks_lunak"],
                "anchor": "w",
            },
            sticky="ew",
            padx=28,
            pady=(0, 12),
        )

        # Username
        _label(kartu, "Username", 3, 0, gaya=judul, sticky="ew", padx=28, pady=(0, 4))
        self.entry_username = _input(
            kartu,
            ctk.CTkEntry,
            4,
            0,
            gaya={**isi, "placeholder_text": "Masukkan username", "width": 420},
            sticky="ew",
            padx=28,
            pady=(0, 10),
        )

        # Password
        _label(kartu, "Password", 5, 0, gaya=judul, sticky="ew", padx=28, pady=(0, 4))
        bungkus = ctk.CTkFrame(kartu, fg_color="transparent")
        bungkus.grid(row=6, column=0, sticky="ew", padx=28, pady=(0, 4))
        bungkus.grid_columnconfigure(0, weight=1)

        self.entry_password = _input(
            bungkus,
            ctk.CTkEntry,
            0,
            0,
            gaya={**isi, "placeholder_text": "Masukkan password", "show": "*"},
            sticky="ew",
        )
        self.btn_lihat = _tombol(
            bungkus,
            "Lihat",
            self._tampilkan_sandi,
            0,
            1,
            gaya={
                "width": 66,
                "height": 42,
                "corner_radius": 10,
                "fg_color": w["aksen_muda"],
                "text_color": w["aksen"],
                "hover_color": w["aksen"],
                "font": ("Segoe UI", 12, "bold"),
            },
            padx=(8, 0),
        )

        # Label salah
        self.label_salah = _label(
            kartu,
            "",
            7,
            0,
            gaya={
                "font": ("Segoe UI", 11, "bold"),
                "text_color": w["salah"],
                "anchor": "w",
            },
            sticky="ew",
            padx=28,
            pady=(0, 4),
        )

        # Tombol Masuk
        self.btn_masuk = _tombol(
            kartu,
            "Masuk",
            self._aksi_masuk,
            8,
            0,
            gaya={
                "height": 44,
                "corner_radius": 10,
                "fg_color": w["aksen"],
                "hover_color": w["aksen_gelap"],
                "text_color": "#ffffff",
                "font": ("Segoe UI", 14, "bold"),
            },
            sticky="ew",
            padx=28,
            pady=(0, 10),
        )

        # Baris registrasi akun baru
        baris_reg = ctk.CTkFrame(kartu, fg_color="transparent")
        baris_reg.grid(row=9, column=0, sticky="ew", padx=28, pady=(0, 12))
        baris_reg.grid_columnconfigure((0, 1), weight=1)

        _label(
            baris_reg,
            "Belum punya akun?",
            0,
            0,
            gaya={
                "font": ("Segoe UI", 11),
                "text_color": w["teks_lunak"],
                "anchor": "e",
            },
            sticky="e",
            padx=(0, 6),
        )
        self.btn_ke_reg = _tombol(
            baris_reg,
            "Daftar Akun Baru",
            self._tampilkan_register,
            0,
            1,
            gaya={
                "height": 28,
                "corner_radius": 8,
                "fg_color": "transparent",
                "text_color": w["aksen"],
                "hover_color": w["aksen_muda"],
                "font": ("Segoe UI", 11, "bold"),
            },
            sticky="w",
        )

        # Demo info
        demo = ctk.CTkFrame(kartu, fg_color=w["konsol"], corner_radius=12)
        demo.grid(row=10, column=0, sticky="ew", padx=28, pady=(0, 16))
        demo.grid_columnconfigure(1, weight=1)

        _label(
            demo,
            "Akun bawaan",
            0,
            0,
            gaya={
                "font": ("Segoe UI", 11, "bold"),
                "text_color": w["teks"],
                "anchor": "w",
            },
            sticky="w",
            padx=(14, 8),
            pady=10,
        )
        _label(
            demo,
            "username: atmin  (Admin)  pw: atmin123",
            0,
            1,
            gaya={
                "font": ("Consolas", 11),
                "text_color": w["teks_lunak"],
                "anchor": "e",
            },
            sticky="e",
            padx=(8, 14),
            pady=10,
        )

        masuk = lambda _e: self._aksi_masuk()  # noqa: E731
        bind_event(self.entry_username, "<Return>", masuk)
        bind_event(self.entry_password, "<Return>", masuk)
        self.after(250, self.entry_username.focus_set)

    def _build_kartu_register(self) -> None:
        self.view_register = RegisterView(
            self.wadah,
            self.auth_controller or getattr(self.controller, "auth_controller", None),
            on_switch_to_login=self._tampilkan_login,
        )
        self.view_register.grid(row=0, column=0, sticky="nsew")

    def _tampilkan_login(self) -> None:
        self.view_register.grid_remove()
        self.kartu_login.grid()
        self.entry_username.focus_set()

    def _tampilkan_register(self) -> None:
        self.kartu_login.grid_remove()
        self.view_register.grid()
        self.view_register.entry_username.focus_set()

    def _build_kaki(self) -> None:
        _label(
            self,
            "Kelompok 3  \u00b7  Program Studi Sistem Informasi  \u00b7  "
            "Fakultas Teknik \u2013 Universitas Tadulako",
            1,
            0,
            gaya={"font": ("Segoe UI", 11), "text_color": self.warna["teks_lunak"]},
            sticky="ew",
            padx=24,
            pady=(0, 14),
        )

    def _tampilkan_sandi(self) -> None:
        self.sandi_terlihat = not self.sandi_terlihat
        self.entry_password.configure(show="" if self.sandi_terlihat else "*")
        self.btn_lihat.configure(
            text="Tutup" if self.sandi_terlihat else "Lihat",
            fg_color=(
                self.warna["aksen"]
                if self.sandi_terlihat
                else self.warna["aksen_muda"]
            ),
            text_color="#ffffff" if self.sandi_terlihat else self.warna["aksen"],
        )

    def _aksi_masuk(self) -> None:
        self.label_salah.configure(text="")
        berhasil, pesan, pengguna = self.controller.login(
            self.entry_username.get().strip(),
            self.entry_password.get(),
        )

        if berhasil:
            self.pengguna_masuk = pengguna
            self.master.destroy()
        else:
            self.label_salah.configure(text=pesan)
            self.entry_password.delete(0, "end")
            self.entry_password.focus_set()
