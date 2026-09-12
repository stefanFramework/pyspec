"""Generates the Claude Code commands (/pyspec:explore, execute, verify, archive, run)
from the packaged templates, parametrized with the repo's config."""

from __future__ import annotations

import string
from importlib import resources
from pathlib import Path

from pyspec.config import PyspecConfig, RepoProfile

COMMAND_NAMES = ("explore", "execute", "verify", "archive", "run")

_REPO_NAMES = ("backend", "frontend", "infra")


def _repo_mapping(config: PyspecConfig) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for name in _REPO_NAMES:
        profile = config.repos.get(name) or RepoProfile()
        mapping[f"repo_{name}"] = profile.path or "(not configured)"
        mapping[f"repo_{name}_stack"] = profile.stack or "(not specified)"
        mapping[f"repo_{name}_test"] = profile.test_command or "(none configured)"
        mapping[f"repo_{name}_lint"] = profile.lint_command or "(none configured)"
        mapping[f"repo_{name}_base_branch"] = profile.base_branch or "(not configured)"
    return mapping


def _render(template_text: str, config: PyspecConfig) -> str:
    mapping = {
        "data_source": config.data_source.type,
        **_repo_mapping(config),
    }
    return string.Template(template_text).safe_substitute(mapping)


def install(config: PyspecConfig) -> list[Path]:
    """Writes .claude/commands/pyspec/*.md under specs_root (rendered as /pyspec:name
    commands by Claude Code's directory-based namespacing). Returns the created paths."""
    commands_dir = config.specs_root / ".claude" / "commands"
    namespace_dir = commands_dir / "pyspec"
    namespace_dir.mkdir(parents=True, exist_ok=True)

    _remove_legacy_flat_commands(commands_dir)

    templates_root = resources.files("pyspec.templates.claude_commands")
    written: list[Path] = []
    for name in COMMAND_NAMES:
        template_text = (templates_root / f"{name}.md").read_text(encoding="utf-8")
        rendered = _render(template_text, config)
        out_path = namespace_dir / f"{name}.md"
        out_path.write_text(rendered, encoding="utf-8")
        written.append(out_path)
    return written


def _remove_legacy_flat_commands(commands_dir: Path) -> None:
    """Removes .claude/commands/pyspec-*.md left over from before the /pyspec:name
    namespacing (moved to .claude/commands/pyspec/*.md)."""
    for name in COMMAND_NAMES:
        legacy_path = commands_dir / f"pyspec-{name}.md"
        if legacy_path.exists():
            legacy_path.unlink()
