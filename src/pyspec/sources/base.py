"""Common interface implemented by each ticket source (Trello, Shortcut, manual)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


class SourceError(RuntimeError):
    """Error configuring or querying a ticket source."""


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
        """Fetches a normalized ticket by its id from the configured source."""
        ...
