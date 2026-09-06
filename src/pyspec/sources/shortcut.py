from __future__ import annotations

import os

import requests

from pyspec.sources.base import SourceError, Ticket

SHORTCUT_API = "https://api.app.shortcut.com/api/v3"


class ShortcutSource:
    def __init__(self, config):
        self.config = config

    def _token(self) -> str:
        token = os.environ.get(self.config.token_env, "")
        if not token:
            raise SourceError(
                f"Missing Shortcut token. Set the environment variable "
                f"{self.config.token_env!r}."
            )
        return token

    def fetch(self, ticket_id: str) -> Ticket:
        token = self._token()
        resp = requests.get(
            f"{SHORTCUT_API}/stories/{ticket_id}",
            headers={"Shortcut-Token": token},
            timeout=15,
        )
        if resp.status_code == 404:
            raise SourceError(f"Could not find Shortcut story {ticket_id!r}.")
        resp.raise_for_status()
        data = resp.json()

        labels = [label.get("name", "") for label in data.get("labels", []) if label.get("name")]

        return Ticket(
            id=str(data.get("id", ticket_id)),
            title=data.get("name", ""),
            description=data.get("description", ""),
            url=data.get("app_url", ""),
            labels=labels,
            raw=data,
        )
