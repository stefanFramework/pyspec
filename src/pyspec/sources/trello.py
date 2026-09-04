from __future__ import annotations

import os

import requests

from pyspec.sources.base import SourceError, Ticket

TRELLO_API = "https://api.trello.com/1"


class TrelloSource:
    def __init__(self, config):
        self.config = config

    def _credentials(self) -> tuple[str, str]:
        api_key = os.environ.get(self.config.api_key_env, "")
        token = os.environ.get(self.config.token_env, "")
        if not api_key or not token:
            raise SourceError(
                f"Faltan credenciales de Trello. Definí las variables de entorno "
                f"{self.config.api_key_env!r} y {self.config.token_env!r}."
            )
        return api_key, token

    def fetch(self, ticket_id: str) -> Ticket:
        api_key, token = self._credentials()
        # ticket_id puede ser el id largo de Trello o el shortLink (ej. "aBc123De")
        resp = requests.get(
            f"{TRELLO_API}/cards/{ticket_id}",
            params={
                "key": api_key,
                "token": token,
                "fields": "name,desc,shortUrl,idLabels",
                "labels": "true",
            },
            timeout=15,
        )
        if resp.status_code == 404:
            raise SourceError(f"No encontre la tarjeta de Trello {ticket_id!r}.")
        resp.raise_for_status()
        data = resp.json()

        labels = [label.get("name", "") for label in data.get("labels", []) if label.get("name")]

        return Ticket(
            id=ticket_id,
            title=data.get("name", ""),
            description=data.get("desc", ""),
            url=data.get("shortUrl", ""),
            labels=labels,
            raw=data,
        )
