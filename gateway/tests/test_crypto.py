"""Tests for AES-GCM crypto module."""
import pytest
from lyceum.crypto.aes_gcm import AESGCMCipher, derive_session_key


class TestAESGCMCipher:
    @pytest.fixture
    def cipher(self):
        key = bytes.fromhex("deadbeefcafebabe0011223344556677")
        return AESGCMCipher(key)

    @pytest.fixture
    def cipher_256(self):
        key = bytes(32)  # 256-bit zero key for testing
        return AESGCMCipher(key)

    def test_encrypt_decrypt_roundtrip(self, cipher):
        plaintext = b"Hello, Lyceum!"
        blob = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(blob)
        assert decrypted == plaintext

    def test_encrypt_decrypt_with_aad(self, cipher):
        plaintext = b"Secret message"
        aad = b"node_id:!node_a1b2"
        
        blob = cipher.encrypt(plaintext, associated_data=aad)
        decrypted = cipher.decrypt(blob, associated_data=aad)
        assert decrypted == plaintext

    def test_decrypt_fails_wrong_aad(self, cipher):
        plaintext = b"Secret message"
        aad = b"correct_aad"
        wrong_aad = b"wrong_aad"
        
        blob = cipher.encrypt(plaintext, associated_data=aad)
        decrypted = cipher.decrypt(blob, associated_data=wrong_aad)
        assert decrypted is None

    def test_decrypt_fails_corrupted(self, cipher):
        plaintext = b"Test data"
        blob = cipher.encrypt(plaintext)
        
        # Corrupt the ciphertext
        corrupted = blob[:-1] + bytes([blob[-1] ^ 0xFF])
        decrypted = cipher.decrypt(corrupted)
        assert decrypted is None

    def test_decrypt_fails_too_short(self, cipher):
        # Less than nonce + tag (12 + 16 = 28 bytes)
        short_blob = b"too short"
        decrypted = cipher.decrypt(short_blob)
        assert decrypted is None

    def test_different_nonces(self, cipher):
        plaintext = b"Same message"
        blob1 = cipher.encrypt(plaintext)
        blob2 = cipher.encrypt(plaintext)
        
        # Same plaintext should produce different ciphertexts (different nonces)
        assert blob1 != blob2
        
        # But both should decrypt correctly
        assert cipher.decrypt(blob1) == plaintext
        assert cipher.decrypt(blob2) == plaintext

    def test_json_convenience_methods(self, cipher):
        json_data = '{"type": "test", "value": 42}'
        blob = cipher.encrypt_json(json_data)
        decrypted = cipher.decrypt_json(blob)
        assert decrypted == json_data

    def test_invalid_key_length(self):
        with pytest.raises(ValueError, match="Key must be 16, 24, or 32 bytes"):
            AESGCMCipher(b"short")

    def test_256_bit_key(self, cipher_256):
        plaintext = b"Testing with 256-bit key"
        blob = cipher_256.encrypt(plaintext)
        decrypted = cipher_256.decrypt(blob)
        assert decrypted == plaintext


class TestDeriveSessionKey:
    def test_derive_deterministic(self):
        secret = b"shared_ecdh_secret"
        key1 = derive_session_key(secret)
        key2 = derive_session_key(secret)
        assert key1 == key2
        assert len(key1) == 32  # AES-256

    def test_derive_different_secrets(self):
        key1 = derive_session_key(b"secret_a")
        key2 = derive_session_key(b"secret_b")
        assert key1 != key2
