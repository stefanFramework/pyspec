"""Genera los comandos de Claude Code (/pyspec-explore, execute, verify, archive)
a partir de las plantillas empaquetadas, parametrizados con la config del repo."""

from __future__ import annotations

import string
from importlib import resources
from pathlib import Path

from pyspec.config import PyspecConfig

COMMAND_NAMES = ("explore", "execute", "verify", "archive")


def _render(template_text: str, config: PyspecConfig) -> str:
    mapping = {
        "repo_backend": config.repos.get("backend") or "(no configurado)",
        "repo_frontend": config.repos.get("frontend") or "(no configurado)",
        "repo_infra": config.repos.get("infra") or "(no configurado)",
    }
    return string.Template(template_text).safe_substitute(mapping)


def install(config: PyspecConfig) -> list[Path]:
    """Escribe .claude/commands/pyspec-*.md en specs_root. Devuelve los paths creados."""
    commands_dir = config.specs_root / ".claude" / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)

    templates_root = resources.files("pyspec.templates.claude_commands")
    written: list[Path] = []
    for name in COMMAND_NAMES:
        template_text = (templates_root / f"{name}.md").read_text(encoding="utf-8")
        rendered = _render(template_text, config)
        out_path = commands_dir / f"pyspec-{name}.md"
        out_path.write_text(rendered, encoding="utf-8")
        written.append(out_path)
    return written
