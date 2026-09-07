"""Generates the Claude Code commands (/pyspec-explore, execute, verify, archive)
from the packaged templates, parametrized with the repo's config."""

from __future__ import annotations

import string
from importlib import resources
from pathlib import Path

from pyspec.config import PyspecConfig

COMMAND_NAMES = ("explore", "execute", "verify", "archive")


def _render(template_text: str, config: PyspecConfig) -> str:
    mapping = {
        "repo_backend": config.repos.get("backend") or "(not configured)",
        "repo_frontend": config.repos.get("frontend") or "(not configured)",
        "repo_infra": config.repos.get("infra") or "(not configured)",
        "data_source": config.data_source.type,
    }
    return string.Template(template_text).safe_substitute(mapping)


def install(config: PyspecConfig) -> list[Path]:
    """Writes .claude/commands/pyspec-*.md under specs_root. Returns the created paths."""
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
