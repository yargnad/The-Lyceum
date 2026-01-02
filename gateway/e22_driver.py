import serial
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from typing import Optional


class E22Serial:
    def __init__(self, port: str, baud: int = 115200, timeout: float = 1.0):
        self.port = port
        self.baud = baud
        self.s = serial.Serial(port, baud, timeout=timeout)

    def close(self):
        self.s.close()

    def send_plain(self, data: bytes):
        self.s.write(data)

    def read(self, n: int = 1) -> bytes:
        return self.s.read(n)

    # Configuration commands use the C0/C1 protocol described in the datasheet.
    # Module must be in configuration mode (9600,8N1) when calling these.
    def config_write(self, start_addr: int, data: bytes) -> Optional[bytes]:
        # C0 + start + len + params
        cmd = bytes([0xC0, start_addr & 0xFF, len(data)]) + data
        self.s.write(cmd)
        # Expect C1 + start + len + params
        resp = self.s.read(3)
        if len(resp) < 3:
            return None
        if resp[0] != 0xC1:
            return None
        addr = resp[1]
        length = resp[2]
        body = self.s.read(length) if length > 0 else b""
        return resp + body


class LyceumGateway:
    def __init__(self, port: str, baud: int = 115200, aes_key: bytes = None):
        self.e22 = E22Serial(port, baud=baud)
        self.aes_key = aes_key
        self.seq = 0

    def close(self):
        self.e22.close()

    def set_fixed_point_mode(self) -> bool:
        # write to register 0x07 value 0x01
        # Module must be in configuration mode (9600,8N1)
        resp = self.e22.config_write(0x07, bytes([0x01]))
        return resp is not None

    def set_crypt_key(self, key16: int) -> bool:
        # write two byte key at 0x08 (CRYPT_H, CRYPT_L)
        hi = (key16 >> 8) & 0xFF
        lo = key16 & 0xFF
        resp = self.e22.config_write(0x08, bytes([hi, lo]))
        return resp is not None

    def encrypt_payload(self, plaintext: bytes) -> bytes:
        if not self.aes_key:
            return plaintext
        nonce = get_random_bytes(12)
        cipher = AES.new(self.aes_key, AES.MODE_GCM, nonce=nonce)
        ct, tag = cipher.encrypt_and_digest(plaintext)
        return nonce + tag + ct

    def decrypt_payload(self, blob: bytes) -> Optional[bytes]:
        if not self.aes_key:
            return blob
        if len(blob) < 12 + 16:
            return None
        nonce = blob[:12]
        tag = blob[12:28]
        ct = blob[28:]
        cipher = AES.new(self.aes_key, AES.MODE_GCM, nonce=nonce)
        try:
            pt = cipher.decrypt_and_verify(ct, tag)
            return pt
        except Exception:
            return None

    def send_lyceum_frame(self, dst_addr: int, channel: int, lyceum_bytes: bytes):
        # For fixed-point mode, the first 3 bytes are destination: ADDH, ADDL, CH
        # prefix dest address and channel
        packet = self.encrypt_payload(lyceum_bytes)
        dest = dst_addr & 0xFFFF
        prefix = dest.to_bytes(2, "big") + bytes([channel & 0xFF])
        self.e22.send_plain(prefix + packet)

    def send_text(self, dst_addr: int, channel: int, text: str, src: int = 0x0001):
        # simple Lyceum framing: src(2)+dst(2)+seq(1)+flags(1)+payload
        hdr = src.to_bytes(2, "big") + dst_addr.to_bytes(2, "big") + bytes([self.seq & 0xFF, 0])
        self.seq = (self.seq + 1) & 0xFF
        payload = text.encode("utf-8")
        frame = hdr + payload
        self.send_lyceum_frame(dst_addr, channel, frame)


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--port", required=True)
    p.add_argument("--dst", required=True)
    p.add_argument("--channel", type=int, default=4)
    p.add_argument("--key", default=None, help="AES key hex (16,24,32 bytes)")
    p.add_argument("message")
    args = p.parse_args()

    aes_key = bytes.fromhex(args.key) if args.key else None
    gw = LyceumGateway(args.port, baud=115200, aes_key=aes_key)
    try:
        # Note: ensure module is in configuration mode if you want to call set_* methods.
        gw.send_text(int(args.dst, 0), args.channel, args.message or "hello")
    finally:
        gw.close()
