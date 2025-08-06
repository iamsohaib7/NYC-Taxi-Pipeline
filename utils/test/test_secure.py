import hashlib
import tempfile

from utils.cryptography.secure import decrypt_file, encrypt_file


def compute_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def test_encrypt_decrypt():
    # test encrypting and decrypting a file by calculating the hash before and after
    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp:
        original_data = b"Secret content here"
        tmp.write(original_data)
        orig_path = tmp.name
    orig_hash = compute_hash(original_data)
    print(orig_hash)
    encrypt_file(orig_path)
    decrypt_file(orig_path)
    with open(orig_path, "rb") as f:
        decrypted_data = f.read()
    decrypted_hash = compute_hash(decrypted_data)

    assert orig_hash == decrypted_hash
