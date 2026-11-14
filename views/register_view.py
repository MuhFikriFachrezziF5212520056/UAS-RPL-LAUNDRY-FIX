import customtkinter as ctk
from views.laundry_view import bind_event, _label, _input, _tombol

PALET = {
    "kartu": "#ffffff",
    "aksen": "#0d9488",
    "aksen_gelap": "#0f766e",
    "aksen_muda": "#ccfbf1",
    "teks": "#0f3d38",
    "teks_lunak": "#5f8a84",
    "konsol": "#eff9f6",
    "salah": "#e11d48",
    "sukses": "#059669",
}


class RegisterView(ctk.CTkFrame):
    def __init__(self, master, auth_controller, on_switch_to_login=None):
        super().__init__(master, fg_color="transparent")
        self.auth_controller = auth_controller
        self.on_switch_to_login = on_switch_to_login
        self.warna = PALET
        self.sandi_terlihat = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._build_kartu()

    def _build_kartu(self) -> None:
        w = self.warna
        isi = {
            "height": 40,
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

        self.kartu = ctk.CTkFrame(
            self, fg_color=w["kartu"], corner_radius=20, width=470
        )
        kartu = self.kartu
        kartu.grid(row=0, column=0, padx=24, pady=(16, 6))
        kartu.grid_columnconfigure(0, weight=1)

        # Header kartu
        kepala = ctk.CTkFrame(kartu, fg_color=w["aksen"], corner_radius=14)
        kepala.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 0))
        kepala.grid_columnconfigure(1, weight=1)

        lencana = ctk.CTkFrame(
            kepala,
            fg_color=w["aksen_muda"],
            width=50,
            height=50,
            corner_radius=14,
        )
        lencana.grid(row=0, column=0, rowspan=2, padx=(14, 0), pady=12)
        lencana.grid_propagate(False)
        _label(lencana, "\U0001F4DD", 0, 0, gaya={"font": ("Segoe UI", 22)})

        _label(
            kepala,
            "Registrasi Akun",
            0,
            1,
            gaya={
                "font": ("Segoe UI", 18, "bold"),
                "text_color": "#ffffff",
                "anchor": "w",
            },
            sticky="sw",
            padx=(12, 14),
            pady=(12, 0),
        )
        _label(
            kepala,
            "Daftar akun operator baru (role User otomatis)",
            1,
            1,
            gaya={
                "font": ("Segoe UI", 11),
                "text_color": "#d6e4ff",
                "anchor": "w",
            },
            sticky="nw",
            padx=(12, 14),
            pady=(2, 12),
        )

        # Username
        _label(
            kartu,
            "Username",
            1,
            0,
            gaya=judul,
            sticky="ew",
            padx=28,
            pady=(16, 4),
        )
        self.entry_username = _input(
            kartu,
            ctk.CTkEntry,
            2,
            0,
            gaya={**isi, "placeholder_text": "Minimal 3 karakter tanpa spasi"},
            sticky="ew",
            padx=28,
            pady=(0, 10),
        )

        # Password
        _label(
            kartu,
            "Password",
            3,
            0,
            gaya=judul,
            sticky="ew",
            padx=28,
            pady=(0, 4),
        )
        self.entry_password = _input(
            kartu,
            ctk.CTkEntry,
            4,
            0,
            gaya={
                **isi,
                "placeholder_text": "Minimal 4 karakter",
                "show": "*",
            },
            sticky="ew",
            padx=28,
            pady=(0, 10),
        )

        # Konfirmasi Password
        _label(
            kartu,
            "Konfirmasi Password",
            5,
            0,
            gaya=judul,
            sticky="ew",
            padx=28,
            pady=(0, 4),
        )
        self.entry_konfirmasi = _input(
            kartu,
            ctk.CTkEntry,
            6,
            0,
            gaya={
                **isi,
                "placeholder_text": "Ulangi password di atas",
                "show": "*",
            },
            sticky="ew",
            padx=28,
            pady=(0, 6),
        )

        # Pesan status/kesalahan
        self.label_pesan = _label(
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
            pady=(0, 6),
        )

        # Tombol Register
        self.btn_register = _tombol(
            kartu,
            "Daftar Akun Baru",
            self._aksi_register,
            8,
            0,
            gaya={
                "height": 42,
                "corner_radius": 10,
                "fg_color": w["aksen"],
                "hover_color": w["aksen_gelap"],
                "text_color": "#ffffff",
                "font": ("Segoe UI", 13, "bold"),
            },
            sticky="ew",
            padx=28,
            pady=(0, 10),
        )

        # Tombol Beralih ke Login
        baris_bawah = ctk.CTkFrame(kartu, fg_color="transparent")
        baris_bawah.grid(row=9, column=0, sticky="ew", padx=28, pady=(0, 18))
        baris_bawah.grid_columnconfigure((0, 1), weight=1)

        _label(
            baris_bawah,
            "Sudah punya akun?",
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
        self.btn_ke_login = _tombol(
            baris_bawah,
            "Kembali ke Login",
            self._ke_login,
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

        reg = lambda _e: self._aksi_register()  # noqa: E731
        bind_event(self.entry_username, "<Return>", reg)
        bind_event(self.entry_password, "<Return>", reg)
        bind_event(self.entry_konfirmasi, "<Return>", reg)

    def _aksi_register(self) -> None:
        self.label_pesan.configure(text="", text_color=self.warna["salah"])
        u = self.entry_username.get().strip()
        p = self.entry_password.get()
        k = self.entry_konfirmasi.get()

        ok, pesan = self.auth_controller.register(u, p, k)
        if ok:
            self.label_pesan.configure(
                text=pesan, text_color=self.warna["sukses"]
            )
            self.entry_password.delete(0, "end")
            self.entry_konfirmasi.delete(0, "end")
            if self.on_switch_to_login:
                self.after(1200, self.on_switch_to_login)
        else:
            self.label_pesan.configure(
                text=pesan, text_color=self.warna["salah"]
            )

    def _ke_login(self) -> None:
        if self.on_switch_to_login:
            self.on_switch_to_login()
