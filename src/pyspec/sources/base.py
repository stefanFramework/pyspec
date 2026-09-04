"""Interfaz comun que implementa cada fuente de tickets (Trello, Shortcut, manual)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


class SourceError(RuntimeError):
    """Error al configurar o consultar una fuente de tickets."""


@dataclass
class Ticket:
    id: str
    title: str
    description: str = ""
    url: str = ""
    labels: list[str] = field(default_factory=list)
    raw: dict = field(default_factory=dict)


class TicketSource(Protocol):
    def fetch(self, ticket_id: str) -> Ticket:
        """Trae un ticket normalizado a partir de su id en la fuente configurada."""
        ...
