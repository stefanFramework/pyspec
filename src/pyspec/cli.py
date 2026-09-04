from __future__ import annotations

from pathlib import Path

import click
import typer
from rich.console import Console
from rich.table import Table

from pyspec import scaffold
from pyspec.adapters import claude_code
from pyspec.config import (
    SUPPORTED_AGENTS,
    SUPPORTED_SOURCES,
    ConfigNotFoundError,
    DataSourceConfig,
    PyspecConfig,
    ShortcutConfig,
    TrelloConfig,
    load_config,
)
from pyspec.sources import SourceError, get_source

app = typer.Typer(
    add_completion=False,
    help="pyspec: framework de specs multi-repo para trabajar tickets con agentes de codigo.",
)
console = Console()
err_console = Console(stderr=True, style="bold red")


def _load_or_exit() -> PyspecConfig:
    try:
        return load_config()
    except ConfigNotFoundError as exc:
        err_console.print(str(exc))
        raise typer.Exit(code=1) from exc


@app.command()
def init(
    path: Path = typer.Option(
        Path.cwd(), "--path", help="Raiz del repo de specs (por defecto, el directorio actual)."
    ),
) -> None:
    """Configura pyspec en este repo: fuente de datos, repos del equipo y comandos de Claude Code."""
    specs_root = path.resolve()
    console.print(f"[bold]Inicializando pyspec en[/bold] {specs_root}\n")

    source_type = typer.prompt(
        "Fuente de datos de tickets",
        type=click.Choice(SUPPORTED_SOURCES),
        default="manual",
    )

    trello = TrelloConfig()
    shortcut = ShortcutConfig()

    if source_type == "trello":
        console.print(
            "\nTrello se lee via API. Necesitas dos variables de entorno con "
            "tu API key y tu token (https://trello.com/power-ups/admin)."
        )
        trello.api_key_env = typer.prompt(
            "Nombre de la variable de entorno con la API key", default=trello.api_key_env
        )
        trello.token_env = typer.prompt(
            "Nombre de la variable de entorno con el token", default=trello.token_env
        )
        trello.board_id = typer.prompt("Board id (opcional)", default="", show_default=False)
    elif source_type == "shortcut":
        console.print(
            "\nShortcut se lee via API. Necesitas una variable de entorno con tu token "
            "(https://app.shortcut.com/settings/account/api-tokens)."
        )
        shortcut.token_env = typer.prompt(
            "Nombre de la variable de entorno con el token", default=shortcut.token_env
        )
    else:
        console.print("\nSin integracion: vas a pegar titulo y descripcion a mano en cada ticket.")

    console.print("\n[bold]Repos del equipo[/bold] (ruta relativa a este repo de specs, dejar vacio si no aplica):")
    repos = {}
    for name in ("backend", "frontend", "infra"):
        value = typer.prompt(f"  {name}", default="", show_default=False)
        if value:
            repos[name] = value

    agent = typer.prompt(
        "\nAgente de codigo a usar",
        type=click.Choice(SUPPORTED_AGENTS),
        default="claude-code",
    )

    config = PyspecConfig(
        specs_root=specs_root,
        data_source=DataSourceConfig(type=source_type, trello=trello, shortcut=shortcut),
        repos=repos,
        agent=agent,
    )
    config.save()
    console.print(f"\n[green]OK[/green] Config guardada en {config.config_path}")

    created = scaffold.ensure_structure(config)
    if created:
        console.print(f"[green]OK[/green] Estructura creada: {', '.join(p.name for p in created)}")
    else:
        console.print("[dim]La estructura specs/current, active, archive ya existia.[/dim]")

    if agent == "claude-code":
        written = claude_code.install(config)
        console.print(f"[green]OK[/green] Comandos de Claude Code generados en .claude/commands/:")
        for p in written:
            console.print(f"  - /{p.stem}")

    console.print(
        "\n[bold]Listo.[/bold] Proximo paso: en Claude Code, corre "
        "[cyan]/pyspec-explore <ticket-id>[/cyan] para arrancar un ticket."
    )


@app.command()
def fetch(ticket_id: str) -> None:
    """Trae un ticket normalizado desde la fuente configurada y lo imprime."""
    config = _load_or_exit()
    try:
        source = get_source(config)
        ticket = source.fetch(ticket_id)
    except SourceError as exc:
        err_console.print(str(exc))
        raise typer.Exit(code=1) from exc

    console.print(f"[bold]{ticket.id}[/bold] — {ticket.title}")
    if ticket.url:
        console.print(f"[dim]{ticket.url}[/dim]")
    if ticket.labels:
        console.print(f"Labels: {', '.join(ticket.labels)}")
    if ticket.description:
        console.print("\n" + ticket.description)


@app.command()
def new(
    ticket_id: str,
    title: str = typer.Option("", "--title", help="Titulo del ticket (si no se pasa, se busca en la fuente configurada)."),
    modulo: str = typer.Option("<modulo>", "--modulo", help="Modulo/dominio principal que toca el ticket."),
    overwrite: bool = typer.Option(False, "--overwrite", help="Sobreescribir el spec activo si ya existe."),
) -> None:
    """Crea specs/active/sc-<id>.spec desde la plantilla."""
    config = _load_or_exit()

    if title:
        from pyspec.sources.base import Ticket

        ticket = Ticket(id=ticket_id, title=title)
    else:
        try:
            source = get_source(config)
            ticket = source.fetch(ticket_id)
        except SourceError as exc:
            err_console.print(str(exc))
            raise typer.Exit(code=1) from exc

    try:
        path = scaffold.new_active_spec(config, ticket, modulo=modulo, overwrite=overwrite)
    except scaffold.SpecError as exc:
        err_console.print(str(exc))
        raise typer.Exit(code=1) from exc

    console.print(f"[green]OK[/green] Spec creado en {path}")


@app.command()
def archive(ticket_id: str) -> None:
    """Mueve specs/active/sc-<id>.spec a specs/archive/."""
    config = _load_or_exit()
    try:
        dst = scaffold.move_to_archive(config, ticket_id)
    except scaffold.SpecError as exc:
        err_console.print(str(exc))
        raise typer.Exit(code=1) from exc
    console.print(f"[green]OK[/green] Spec archivado en {dst}")


@app.command()
def status() -> None:
    """Lista tickets activos y modulos documentados en current/."""
    config = _load_or_exit()

    active = scaffold.list_active(config)
    table = Table(title="Tickets activos")
    table.add_column("Ticket")
    table.add_column("Archivo")
    for path in active:
        table.add_row(path.stem.removeprefix("sc-"), str(path))
    console.print(table)

    modules = scaffold.list_current_modules(config)
    console.print(f"\n[bold]Modulos documentados en current/:[/bold] {len(modules)}")
    for path in modules:
        console.print(f"  - {path.stem}")


if __name__ == "__main__":
    app()
