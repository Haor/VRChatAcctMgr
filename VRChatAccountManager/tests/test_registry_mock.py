from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from vrchataccountmanager.crypto_service import md5_key


def test_md5_key():
    assert md5_key("username") == "14C4B06B824EC593239362517F538B29"


