from dataclasses import dataclass
from typing import Tuple


@dataclass
class LyceumFrame:
    src: int
    dst: int
    seq: int
    flags: int
    payload: bytes

    def to_bytes(self) -> bytes:
        return (
            self.src.to_bytes(2, "big")
            + self.dst.to_bytes(2, "big")
            + (self.seq & 0xFF).to_bytes(1, "big")
            + (self.flags & 0xFF).to_bytes(1, "big")
            + self.payload
        )

    @classmethod
    def from_bytes(cls, b: bytes) -> "LyceumFrame":
        if len(b) < 6:
            raise ValueError("Frame too short")
        src = int.from_bytes(b[0:2], "big")
        dst = int.from_bytes(b[2:4], "big")
        seq = b[4]
        flags = b[5]
        payload = b[6:]
        return cls(src=src, dst=dst, seq=seq, flags=flags, payload=payload)


def make_test_frame(src: int, dst: int, seq: int, payload: bytes) -> LyceumFrame:
    return LyceumFrame(src=src, dst=dst, seq=seq, flags=0, payload=payload)
