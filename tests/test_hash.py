import hashlib
import tempfile
import os
from scripts.cli import get_sha256

def test_sha256():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"test123")
        f.flush()
        expected = hashlib.sha256(b"test123").hexdigest()
        actual = get_sha256(f.name)
        assert expected == actual
    os.unlink(f.name)
