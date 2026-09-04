"""Carga y guardado de la configuracion de pyspec (.pyspec/config.yaml)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

CONFIG_DIRNAME = ".pyspec"
CONFIG_FILENAME = "config.yaml"

SUPPORTED_SOURCES = ("trello", "shortcut", "manual")
SUPPORTED_AGENTS = ("claude-code",)


class ConfigNotFoundError(RuntimeError):
    """No se encontro .pyspec/config.yaml en el directorio actual ni en sus padres."""


@dataclass
class TrelloConfig:
    api_key_env: str = "TRELLO_API_KEY"
    token_env: str = "TRELLO_TOKEN"
    board_id: str = ""


@dataclass
class ShortcutConfig:
    token_env: str = "SHORTCUT_TOKEN"


@dataclass
class DataSourceConfig:
    type: str = "manual"
    trello: TrelloConfig = field(default_factory=TrelloConfig)
    shortcut: ShortcutConfig = field(default_factory=ShortcutConfig)


@dataclass
class PyspecConfig:
    specs_root: Path
    data_source: DataSourceConfig = field(default_factory=DataSourceConfig)
    repos: dict[str, str] = field(default_factory=dict)
    agent: str = "claude-code"

    @property
    def config_dir(self) -> Path:
        return self.specs_root / CONFIG_DIRNAME

    @property
    def config_path(self) -> Path:
        return self.config_dir / CONFIG_FILENAME

    def to_dict(self) -> dict:
        return {
            "version": 1,
            "data_source": {
                "type": self.data_source.type,
                "trello": {
                    "api_key_env": self.data_source.trello.api_key_env,
                    "token_env": self.data_source.trello.token_env,
                    "board_id": self.data_source.trello.board_id,
                },
                "shortcut": {
                    "token_env": self.data_source.shortcut.token_env,
                },
            },
            "repos": self.repos,
            "agent": self.agent,
        }

    def save(self) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with self.config_path.open("w", encoding="utf-8") as fh:
            yaml.safe_dump(self.to_dict(), fh, sort_keys=False, allow_unicode=True)

    @classmethod
    def load(cls, path: Path) -> "PyspecConfig":
        with path.open("r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh) or {}

        ds_raw = raw.get("data_source", {}) or {}
        trello_raw = ds_raw.get("trello", {}) or {}
        shortcut_raw = ds_raw.get("shortcut", {}) or {}

        data_source = DataSourceConfig(
            type=ds_raw.get("type", "manual"),
            trello=TrelloConfig(**trello_raw) if trello_raw else TrelloConfig(),
            shortcut=ShortcutConfig(**shortcut_raw) if shortcut_raw else ShortcutConfig(),
        )

        return cls(
            specs_root=path.parent.parent,
            data_source=data_source,
            repos=raw.get("repos", {}) or {},
            agent=raw.get("agent", "claude-code"),
        )


def find_config(start: Path | None = None) -> Path:
    """Busca .pyspec/config.yaml en start (o cwd) y sus directorios padres."""
    current = (start or Path.cwd()).resolve()
    for directory in (current, *current.parents):
        candidate = directory / CONFIG_DIRNAME / CONFIG_FILENAME
        if candidate.exists():
            return candidate
    raise ConfigNotFoundError(
        "No encontre .pyspec/config.yaml. Corre 'pyspec init' primero en la raiz del repo de specs."
    )


def load_config(start: Path | None = None) -> PyspecConfig:
    return PyspecConfig.load(find_config(start))
