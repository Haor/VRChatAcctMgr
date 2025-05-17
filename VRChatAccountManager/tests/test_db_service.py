from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from vrchataccountmanager import db_service


def test_add_and_bind(tmp_path):
    db_path = tmp_path / "test.db"
    db_service.init_db(db_path)
    acc = db_service.Account(username="u", token="t")
    db_service.add_account(acc)
    accounts = db_service.list_accounts()
    assert len(accounts) == 1
    aid = accounts[0].id
    db_service.bind_account_to_project(aid, "ProjectA")
    bindings = db_service.list_bindings()
    assert len(bindings) == 1
    assert bindings[0].product_name == "ProjectA"
