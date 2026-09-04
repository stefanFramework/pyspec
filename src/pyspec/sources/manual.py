from __future__ import annotations

import typer

from pyspec.sources.base import Ticket


class ManualSource:
    """Fuente sin integracion: pide el titulo y la descripcion del ticket por consola."""

    def fetch(self, ticket_id: str) -> Ticket:
        title = typer.prompt(f"Titulo del ticket {ticket_id}")
        typer.echo("Descripcion del ticket (linea vacia para terminar):")
        lines: list[str] = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)

        return Ticket(id=ticket_id, title=title, description="\n".join(lines))
