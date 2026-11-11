from src.data_pipeline import sha256_bytes

def test_hash_is_deterministic():
    assert sha256_bytes(b"abc") == sha256_bytes(b"abc")
    assert len(sha256_bytes(b"abc")) == 64
