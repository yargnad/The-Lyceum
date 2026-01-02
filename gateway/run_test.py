"""Small runner to exercise the gateway locally."""
from e22_driver import LyceumGateway


def main():
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--port", required=True)
    p.add_argument("--dst", required=True)
    p.add_argument("--channel", type=int, default=4)
    p.add_argument("--key", default=None, help="AES key hex (16/24/32 bytes)")
    p.add_argument("--set-fixed", action="store_true", help="Set module to fixed-point mode (requires config mode)")
    p.add_argument("--set-crypt", type=lambda x: int(x, 0), default=None, help="Set module 16-bit crypt key (requires config mode)")
    p.add_argument("message", nargs="?", default="hello lyceum")
    args = p.parse_args()

    aes_key = bytes.fromhex(args.key) if args.key else None
    gw = LyceumGateway(args.port, baud=115200, aes_key=aes_key)
    try:
        if args.set_fixed:
            print("Writing fixed-point mode (0x07 = 0x01). Ensure device is in config mode (9600,8N1).")
            ok = gw.set_fixed_point_mode()
            print("OK" if ok else "Failed")
        if args.set_crypt is not None:
            print(f"Writing 16-bit crypt key: 0x{args.set_crypt:04X}")
            ok = gw.set_crypt_key(args.set_crypt)
            print("OK" if ok else "Failed")

        print("Sending message...")
        gw.send_text(int(args.dst, 0), args.channel, args.message)
        print("Sent.")
    finally:
        gw.close()


if __name__ == "__main__":
    main()
