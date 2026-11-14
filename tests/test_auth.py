from unittest.mock import MagicMock
from controller.auth_controller import AuthController, ROLE_ADMIN, ROLE_DEFAULT
from models.user_model import UserModel


def test_hash_password_sha256():
    raw = "rahasia123"
    hashed1 = UserModel.hash_password(raw)
    hashed2 = AuthController.hash_password(raw)
    assert len(hashed1) == 64
    assert hashed1 == hashed2
    assert hashed1 != raw


def test_register_validation():
    mock_user_model = MagicMock()
    mock_user_model.get_by_username.return_value = None
    mock_user_model.create_user.return_value = True

    auth = AuthController(user_model=mock_user_model)

    # Empty validation
    ok, msg = auth.register("", "pass")
    assert not ok
    assert "wajib diisi" in msg

    # Username too short
    ok, msg = auth.register("ab", "pass")
    assert not ok
    assert "minimal 3" in msg

    # Username with space
    ok, msg = auth.register("user baru", "pass")
    assert not ok
    assert "spasi" in msg

    # Password too short
    ok, msg = auth.register("user1", "12")
    assert not ok
    assert "minimal 4" in msg

    # Password confirmation mismatch
    ok, msg = auth.register("user1", "pass123", "pass999")
    assert not ok
    assert "tidak cocok" in msg


def test_register_user_role_assignment():
    mock_user_model = MagicMock()
    mock_user_model.get_by_username.return_value = None
    mock_user_model.create_user.return_value = True

    auth = AuthController(user_model=mock_user_model)
    ok, msg = auth.register("operator1", "sandi123", "sandi123")
    assert ok
    assert "role User" in msg

    # Pastikan create_user dipanggil dengan role="User"
    args, kwargs = mock_user_model.create_user.call_args
    assert args[0] == "operator1"
    assert kwargs.get("role") == ROLE_DEFAULT


def test_register_duplicate_username():
    mock_user_model = MagicMock()
    mock_user_model.get_by_username.return_value = {"id_user": 1, "username": "ada"}

    auth = AuthController(user_model=mock_user_model)
    ok, msg = auth.register("ada", "sandi123")
    assert not ok
    assert "sudah terdaftar" in msg


def test_login_success_and_fail():
    mock_user_model = MagicMock()
    mock_user_model.verify_user.side_effect = lambda u, p: (
        {"id_user": 1, "username": "atmin", "role": ROLE_ADMIN}
        if u == "atmin" and p == "atmin123"
        else None
    )

    auth = AuthController(user_model=mock_user_model)

    # Sukses
    ok, msg, user = auth.login("atmin", "atmin123")
    assert ok
    assert user["role"] == ROLE_ADMIN
    assert auth.current_user == user

    # Gagal
    ok, msg, user = auth.login("atmin", "salah")
    assert not ok
    assert user is None
