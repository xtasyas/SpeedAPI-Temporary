from datetime import datetime
from typing import Annotated

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, registry

intpk = Annotated[int, mapped_column(primary_key=True)]

metadata_registry = registry()


@metadata_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[intpk] = mapped_column(init=False)

    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
