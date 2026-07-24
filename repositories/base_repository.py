from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Generic CRUD helper for repository classes."""

    def __init__(self, model_class: type[T], session: Session) -> None:
        self.model_class = model_class
        self.session = session

    def create(self, instance: T) -> T:
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def get_by_id(self, instance_id: int) -> T | None:
        return self.session.get(self.model_class, instance_id)

    def update(self, instance: T) -> T:
        self.session.merge(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def delete(self, instance: T) -> None:
        self.session.delete(instance)
        self.session.commit()
