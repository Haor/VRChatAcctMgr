"""SQLite database access via SQLModel."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List

from sqlmodel import Field, Session, SQLModel, create_engine, select

_engine = None


class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    token: str
    note: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Binding(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    account_id: int = Field(foreign_key="account.id")
    product_name: str
    last_used: datetime = Field(default_factory=datetime.utcnow)


def init_db(path: Path = Path("accounts.db")) -> None:
    global _engine
    _engine = create_engine(f"sqlite:///{path}")
    SQLModel.metadata.create_all(_engine)


def _ensure_engine() -> Session:
    if _engine is None:
        init_db()
    return Session(_engine)


def add_account(acc: Account) -> None:
    with _ensure_engine() as session:
        session.add(acc)
        session.commit()


def remove_account(acc_id: int) -> None:
    """Delete an account and any bindings."""
    with _ensure_engine() as session:
        acc = session.get(Account, acc_id)
        if acc:
            session.delete(acc)
            for b in session.exec(select(Binding).where(Binding.account_id == acc_id)):
                session.delete(b)
            session.commit()


def list_accounts() -> List[Account]:
    with _ensure_engine() as session:
        statement = select(Account)
        return list(session.exec(statement))


def list_bindings() -> List[Binding]:
    """Return all account-to-project bindings."""
    with _ensure_engine() as session:
        return list(session.exec(select(Binding)))


def accounts_for_project(product: str) -> List[Account]:
    with _ensure_engine() as session:
        stmt = (
            select(Account)
            .join(Binding, Binding.account_id == Account.id)
            .where(Binding.product_name == product)
        )
        return list(session.exec(stmt))


def bind_account_to_project(acc_id: int, product: str) -> None:
    with _ensure_engine() as session:
        binding = session.exec(select(Binding).where(Binding.account_id == acc_id, Binding.product_name == product)).first()
        if binding:
            binding.last_used = datetime.utcnow()
        else:
            binding = Binding(account_id=acc_id, product_name=product)
            session.add(binding)
        session.commit()

