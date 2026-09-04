from pyspec.sources.base import SourceError, Ticket
from pyspec.sources.manual import ManualSource
from pyspec.sources.shortcut import ShortcutSource
from pyspec.sources.trello import TrelloSource

__all__ = [
    "Ticket",
    "SourceError",
    "ManualSource",
    "ShortcutSource",
    "TrelloSource",
    "get_source",
]


def get_source(config):
    """Devuelve la instancia de fuente de tickets configurada en pyspec.config.PyspecConfig."""
    ds = config.data_source
    if ds.type == "trello":
        return TrelloSource(ds.trello)
    if ds.type == "shortcut":
        return ShortcutSource(ds.shortcut)
    if ds.type == "manual":
        return ManualSource()
    raise SourceError(f"Fuente de datos desconocida: {ds.type!r}")
