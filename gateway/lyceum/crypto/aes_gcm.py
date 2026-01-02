"""
AES-GCM Encryption for Lyceum Protocol

Provides end-to-end encryption for Pneuma message payloads.
All Layer 3 packets use Meshtastic's native AES256, but the
payload content is additionally encrypted using ephemeral
session keys derived from ECDH.

Format: nonce (12 bytes) + tag (16 bytes) + ciphertext
"""
from typing import Optional, Tuple
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class AESGCMCipher:
    """
    AES-GCM authenticated encryption.
    
    Used for:
    - End-to-end encryption of RoutingRequest payloads
    - SessionInit prompt encryption
    - DebatePacket content encryption
    """

    NONCE_SIZE = 12
    TAG_SIZE = 16

    def __init__(self, key: bytes):
        """
        Initialize cipher with a key.
        
        Args:
            key: AES key (16, 24, or 32 bytes)
        """
        if len(key) not in (16, 24, 32):
            raise ValueError("Key must be 16, 24, or 32 bytes")
        self.key = key

    def encrypt(self, plaintext: bytes, associated_data: bytes = b"") -> bytes:
        """
        Encrypt plaintext with optional associated data.
        
        Args:
            plaintext: Data to encrypt
            associated_data: Additional authenticated data (not encrypted)
            
        Returns:
            nonce + tag + ciphertext
        """
        nonce = get_random_bytes(self.NONCE_SIZE)
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        
        if associated_data:
            cipher.update(associated_data)
            
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        return nonce + tag + ciphertext

    def decrypt(
        self,
        blob: bytes,
        associated_data: bytes = b"",
    ) -> Optional[bytes]:
        """
        Decrypt and verify ciphertext.
        
        Args:
            blob: nonce + tag + ciphertext
            associated_data: Additional authenticated data (must match encryption)
            
        Returns:
            Decrypted plaintext, or None if verification fails
        """
        min_size = self.NONCE_SIZE + self.TAG_SIZE
        if len(blob) < min_size:
            return None
            
        nonce = blob[:self.NONCE_SIZE]
        tag = blob[self.NONCE_SIZE:self.NONCE_SIZE + self.TAG_SIZE]
        ciphertext = blob[self.NONCE_SIZE + self.TAG_SIZE:]
        
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        
        if associated_data:
            cipher.update(associated_data)
            
        try:
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext
        except (ValueError, KeyError):
            return None

    def encrypt_json(self, data: str, associated_data: bytes = b"") -> bytes:
        """Convenience method for encrypting JSON strings."""
        return self.encrypt(data.encode("utf-8"), associated_data)

    def decrypt_json(
        self,
        blob: bytes,
        associated_data: bytes = b"",
    ) -> Optional[str]:
        """Convenience method for decrypting to JSON string."""
        plaintext = self.decrypt(blob, associated_data)
        if plaintext is None:
            return None
        try:
            return plaintext.decode("utf-8")
        except UnicodeDecodeError:
            return None


def derive_session_key(shared_secret: bytes) -> bytes:
    """
    Derive an AES-256 key from an ECDH shared secret.
    
    Uses HKDF with SHA-256 for key derivation.
    This is a placeholder - production would use cryptography.hazmat.
    """
    import hashlib
    # Simple KDF for now - production should use HKDF
    return hashlib.sha256(b"lyceum-session-v1" + shared_secret).digest()
