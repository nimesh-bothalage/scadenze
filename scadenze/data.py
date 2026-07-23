"""Caricamento del dataset e filtri sulle scadenze."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date
from importlib import resources
from pathlib import Path


@dataclass(frozen=True)
class Scadenza:
    id: str
    data: date
    titolo: str
    descrizione: str
    categoria: str
    soggetti: list[str] = field(default_factory=list)
    modello: str | None = None
    ricorrenza: str | None = None


def carica_scadenze(percorso: Path | None = None) -> list[Scadenza]:
    """Carica le scadenze dal JSON, ordinate per data.

    Senza argomenti legge il dataset incluso nel package.
    """
    if percorso is not None:
        testo = Path(percorso).read_text(encoding="utf-8")
    else:
        testo = (
            resources.files("scadenze").joinpath("data/scadenze_2026.json").read_text(encoding="utf-8")
        )
    voci = json.loads(testo)
    scadenze = [
        Scadenza(
            id=v["id"],
            data=date.fromisoformat(v["data"]),
            titolo=v["titolo"],
            descrizione=v["descrizione"],
            categoria=v["categoria"],
            soggetti=v.get("soggetti", []),
            modello=v.get("modello"),
            ricorrenza=v.get("ricorrenza"),
        )
        for v in voci
    ]
    return sorted(scadenze, key=lambda s: s.data)


def filtra_prossime(scadenze: list[Scadenza], oggi: date, giorni: int = 30) -> list[Scadenza]:
    """Scadenze da oggi (incluso) ai prossimi `giorni` giorni."""
    return [s for s in scadenze if 0 <= (s.data - oggi).days <= giorni]


def filtra_mese(scadenze: list[Scadenza], mese: int) -> list[Scadenza]:
    return [s for s in scadenze if s.data.month == mese]


def filtra_categoria(scadenze: list[Scadenza], categoria: str) -> list[Scadenza]:
    return [s for s in scadenze if s.categoria.lower() == categoria.lower()]


def cerca(scadenze: list[Scadenza], testo: str) -> list[Scadenza]:
    """Ricerca case-insensitive su titolo e descrizione."""
    t = testo.lower()
    return [s for s in scadenze if t in s.titolo.lower() or t in s.descrizione.lower()]
