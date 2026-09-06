"""Management of the specs/current, specs/active, specs/archive structure."""

from __future__ import annotations

import string
from importlib import resources
from pathlib import Path

from pyspec.config import PyspecConfig
from pyspec.sources.base import Ticket

SPECS_DIRS = ("current", "active", "archive")


class SpecError(RuntimeError):
    pass


def specs_root(config: PyspecConfig) -> Path:
    return config.specs_root / "specs"


def ensure_structure(config: PyspecConfig) -> list[Path]:
    """Creates specs/current, specs/active, specs/archive if they don't exist."""
    created: list[Path] = []
    root = specs_root(config)
    for name in SPECS_DIRS:
        d = root / name
        if not d.exists():
            d.mkdir(parents=True)
            created.append(d)
            (d / ".gitkeep").touch()
    return created


def _read_template(name: str) -> str:
    return (
        resources.files("pyspec.templates") / name
    ).read_text(encoding="utf-8")


def active_spec_path(config: PyspecConfig, ticket_id: str) -> Path:
    return specs_root(config) / "active" / f"sc-{ticket_id}.spec"


def archive_spec_path(config: PyspecConfig, ticket_id: str) -> Path:
    return specs_root(config) / "archive" / f"sc-{ticket_id}.spec"


def current_module_path(config: PyspecConfig, modulo: str) -> Path:
    return specs_root(config) / "current" / f"{modulo}.md"


def new_active_spec(
    config: PyspecConfig,
    ticket: Ticket,
    modulo: str = "<modulo>",
    overwrite: bool = False,
) -> Path:
    path = active_spec_path(config, ticket.id)
    if path.exists() and not overwrite:
        raise SpecError(
            f"{path} already exists. Pass --overwrite if you want to regenerate it."
        )

    template = _read_template("spec_template.md")
    content = string.Template(template).safe_substitute(
        ticket_id=ticket.id,
        title=ticket.title,
        url=ticket.url,
        modulo=modulo,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def new_current_module(config: PyspecConfig, modulo: str) -> Path:
    path = current_module_path(config, modulo)
    if path.exists():
        return path

    template = _read_template("current_module_template.md")
    content = string.Template(template).safe_substitute(modulo=modulo)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def move_to_archive(config: PyspecConfig, ticket_id: str) -> Path:
    src = active_spec_path(config, ticket_id)
    if not src.exists():
        raise SpecError(f"Could not find {src}. Is the ticket active?")

    dst = archive_spec_path(config, ticket_id)
    dst.parent.mkdir(parents=True, exist_ok=True)
    src.rename(dst)
    return dst


def list_active(config: PyspecConfig) -> list[Path]:
    d = specs_root(config) / "active"
    if not d.exists():
        return []
    return sorted(p for p in d.glob("sc-*.spec"))


def list_current_modules(config: PyspecConfig) -> list[Path]:
    d = specs_root(config) / "current"
    if not d.exists():
        return []
    return sorted(p for p in d.glob("*.md"))
