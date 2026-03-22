
"""Encrypt CSV file output using Fernet symmetric encryption."""

import io
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

from . import config


def encrypt_csv_output(csv_file: str | Path) -> Path:

    """
    Encrypt a CSV file and save the encrypted output.

    Args:
        csv_file: Path to the CSV file to encrypt.

    Returns:
        Path to the encrypted output file.

    Raises:
        ValueError: If encryption key is not configured.
        FileNotFoundError: If the CSV file does not exist.
    """

    csv_path = Path(csv_file)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    if config.DEFAULT_KEY is None:
        raise ValueError(
            "Encryption key not configured. Set ENCRYPTION_KEY environment variable."
        )

    output_path = config.OUTPUT_DIR / f"{csv_path.stem}_encrypted.bin"
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    key = config.DEFAULT_KEY
    fernet = Fernet(key.encode() if isinstance(key, str) else key)

    # Chunked encryption for large files
    chunk_size = 1024 * 1024  # 1MB per chunk
    encrypted_chunks = []
    with open(csv_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            encrypted_chunk = fernet.encrypt(chunk)
            # Write the length of the encrypted chunk followed by the chunk itself
            encrypted_chunks.append(len(encrypted_chunk).to_bytes(4, 'big') + encrypted_chunk)

    with open(output_path, "wb") as f:
        for enc in encrypted_chunks:
            f.write(enc)

    return output_path





