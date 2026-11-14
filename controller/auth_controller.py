from models.user_model import UserModel

ROLE_DEFAULT = "User"
ROLE_ADMIN = "Admin"


class AuthController:
    def __init__(self, user_model=None):
        self.user_model = user_model or UserModel()
        self.current_user = None

    @staticmethod
    def hash_password(password: str) -> str:
        return UserModel.hash_password(password)

    def register(
        self,
        username: str,
        password: str,
        konfirmasi_password: str | None = None,
    ):
        username = str(username or "").strip()
        password = str(password or "")

        if not username or not password:
            return False, "Username dan password wajib diisi."
        if len(username) < 3:
            return False, "Username minimal 3 karakter."
        if " " in username:
            return False, "Username tidak boleh mengandung spasi."
        if len(password) < 4:
            return False, "Password minimal 4 karakter."
        if konfirmasi_password is not None and password != str(konfirmasi_password):
            return False, "Konfirmasi password tidak cocok."

        if self.user_model.get_by_username(username) is not None:
            return False, "Username sudah terdaftar."

        password_hash = self.hash_password(password)
        ok = self.user_model.create_user(
            username, password_hash, role=ROLE_DEFAULT
        )
        if not ok:
            return False, "Registrasi gagal disimpan."
        return True, "Registrasi berhasil! Akun terdaftar dengan role User."

    def login(self, username: str, password: str):
        username = str(username or "").strip()
        password = str(password or "")

        if not username or not password:
            return False, "Username dan password wajib diisi.", None

        user = self.user_model.verify_user(username, password)
        if user is None:
            return False, "Username atau password salah.", None

        self.current_user = user
        return True, f"Selamat datang, {user['username']}!", user

    def logout(self):
        self.current_user = None
