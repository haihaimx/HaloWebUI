"""
Symmetric encryption utility for sensitive tokens (OAuth id_token, etc.).

Uses AES-CBC via the cryptography library's Fernet scheme.
Key is derived deterministically from WEBUI_SECRET_KEY so no extra
configuration is needed.
"""

import base64
import hashlib
import logging

from cryptography.fernet import Fernet, InvalidToken

from open_webui.env import WEBUI_SECRET_KEY

log = logging.getLogger(__name__)


def _derive_key(secret: str) -> bytes:
    """Derive a 32-byte URL-safe base64-encoded key from an arbitrary secret."""
    raw = hashlib.sha256(secret.encode()).digest()
    return base64.urlsafe_b64encode(raw)


_fernet: Fernet | None = None


def _get_fernet() -> Fernet:
    global _fernet
    if _fernet is None:
        _fernet = Fernet(_derive_key(WEBUI_SECRET_KEY))
    return _fernet


def encrypt_token(plaintext: str) -> str:
    """Encrypt a plaintext string and return a URL-safe base64 ciphertext."""
    return _get_fernet().encrypt(plaintext.encode()).decode()


def decrypt_token(ciphertext: str) -> str | None:
    """Decrypt a ciphertext string. Returns None if decryption fails."""
    try:
        return _get_fernet().decrypt(ciphertext.encode()).decode()
    except (InvalidToken, Exception) as e:
        log.warning(f"Token decryption failed: {e}")
        return None
