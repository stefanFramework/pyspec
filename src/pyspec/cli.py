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
    help="pyspec: a specs framework for working tickets with coding agents.",
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
        Path.cwd(), "--path", help="Root of the specs repo (defaults to the current directory)."
    ),
) -> None:
    """Configures pyspec in this repo: data source, team repos, and Claude Code commands."""
    specs_root = path.resolve()
    console.print(f"[bold]Initializing pyspec in[/bold] {specs_root}\n")

    source_type = typer.prompt(
        "Ticket data source",
        type=click.Choice(SUPPORTED_SOURCES),
        default="manual",
    )

    trello = TrelloConfig()
    shortcut = ShortcutConfig()

    if source_type == "trello":
        console.print(
            "\nTrello is read via API. You need two environment variables with "
            "your API key and token (https://trello.com/power-ups/admin)."
        )
        trello.api_key_env = typer.prompt(
            "Environment variable name for the API key", default=trello.api_key_env
        )
        trello.token_env = typer.prompt(
            "Environment variable name for the token", default=trello.token_env
        )
        trello.board_id = typer.prompt("Board id (optional)", default="", show_default=False)
    elif source_type == "shortcut":
        console.print(
            "\nShortcut is read via API. You need an environment variable with your token "
            "(https://app.shortcut.com/settings/account/api-tokens)."
        )
        shortcut.token_env = typer.prompt(
            "Environment variable name for the token", default=shortcut.token_env
        )
    else:
        console.print("\nNo integration: you'll paste the title and description by hand for each ticket.")

    console.print("\n[bold]Team repos[/bold] (path relative to this specs repo, leave empty if not applicable):")
    repos = {}
    for name in ("backend", "frontend", "infra"):
        value = typer.prompt(f"  {name}", default="", show_default=False)
        if value:
            repos[name] = value

    agent = typer.prompt(
        "\nCoding agent to use",
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
    console.print(f"\n[green]OK[/green] Config saved to {config.config_path}")

    created = scaffold.ensure_structure(config)
    if created:
        console.print(f"[green]OK[/green] Structure created: {', '.join(p.name for p in created)}")
    else:
        console.print("[dim]The specs/current, active, archive structure already existed.[/dim]")

    if agent == "claude-code":
        written = claude_code.install(config)
        console.print(f"[green]OK[/green] Claude Code commands generated in .claude/commands/:")
        for p in written:
            console.print(f"  - /{p.stem}")

    console.print(
        "\n[bold]Done.[/bold] Next step: in Claude Code, run "
        "[cyan]/pyspec-explore <ticket-id>[/cyan] to start a ticket."
    )


@app.command()
def fetch(ticket_id: str) -> None:
    """Fetches a normalized ticket from the configured source and prints it."""
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
    title: str = typer.Option("", "--title", help="Ticket title (if not passed, it's fetched from the configured source)."),
    modulo: str = typer.Option("<modulo>", "--modulo", help="Main module/domain the ticket touches."),
    overwrite: bool = typer.Option(False, "--overwrite", help="Overwrite the active spec if it already exists."),
) -> None:
    """Creates specs/active/sc-<id>.spec from the template."""
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

    console.print(f"[green]OK[/green] Spec created at {path}")


@app.command()
def archive(ticket_id: str) -> None:
    """Moves specs/active/sc-<id>.spec to specs/archive/."""
    config = _load_or_exit()
    try:
        dst = scaffold.move_to_archive(config, ticket_id)
    except scaffold.SpecError as exc:
        err_console.print(str(exc))
        raise typer.Exit(code=1) from exc
    console.print(f"[green]OK[/green] Spec archived at {dst}")


@app.command()
def status() -> None:
    """Lists active tickets and documented modules in current/."""
    config = _load_or_exit()

    active = scaffold.list_active(config)
    table = Table(title="Active tickets")
    table.add_column("Ticket")
    table.add_column("File")
    for path in active:
        table.add_row(path.stem.removeprefix("sc-"), str(path))
    console.print(table)

    modules = scaffold.list_current_modules(config)
    console.print(f"\n[bold]Modules documented in current/:[/bold] {len(modules)}")
    for path in modules:
        console.print(f"  - {path.stem}")


if __name__ == "__main__":
    app()
