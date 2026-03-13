# SN-112BA: Kyber (post-quantum) handshake simulation. Main developer: shellworlds.
"""Simulated Kyber-style KEM for POC; not for production use."""

import hashlib
import os
from typing import Tuple


def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, "big")


def int_to_bytes(n: int, length: int) -> bytes:
    return n.to_bytes(length, "big")


def kyber_sim_keygen() -> Tuple[bytes, bytes]:
    sk = os.urandom(32)
    pk = sk
    return pk, sk


def kyber_sim_encaps(pk: bytes) -> Tuple[bytes, bytes]:
    r = os.urandom(32)
    shared = hashlib.sha256(pk + r).digest()
    return r, shared


def kyber_sim_decaps(sk: bytes, ciphertext: bytes) -> bytes:
    return hashlib.sha256(sk + ciphertext).digest()


if __name__ == "__main__":
    pk, sk = kyber_sim_keygen()
    ct, shared_a = kyber_sim_encaps(pk)
    shared_b = kyber_sim_decaps(sk, ct)
    print("Kyber sim handshake OK:", shared_a == shared_b)
