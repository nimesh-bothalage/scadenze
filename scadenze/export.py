"""Export delle scadenze in formato iCalendar e CSV."""

from __future__ import annotations

import csv
import io
from datetime import timedelta

from icalendar import Calendar, Event

from .data import Scadenza


def esporta_ical(scadenze: list[Scadenza]) -> bytes:
    """Genera un calendario iCal con un evento intera-giornata per scadenza."""
    cal = Calendar()
    cal.add("prodid", "-//scadenze//IT")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", "Scadenze fiscali 2026")
    for s in scadenze:
        evento = Event()
        evento.add("uid", f"{s.id}@scadenze")
        evento.add("summary", s.titolo)
        evento.add("description", s.descrizione)
        evento.add("dtstart", s.data)
        evento.add("dtend", s.data + timedelta(days=1))
        evento.add("categories", [s.categoria])
        cal.add_component(evento)
    return cal.to_ical()


def esporta_csv(scadenze: list[Scadenza]) -> str:
    """Genera un CSV con separatore ';' (convenzione di Excel in italiano)."""
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=";", lineterminator="\n")
    writer.writerow(["data", "titolo", "descrizione", "categoria", "soggetti", "modello", "ricorrenza"])
    for s in scadenze:
        writer.writerow([
            s.data.isoformat(),
            s.titolo,
            s.descrizione,
            s.categoria,
            "|".join(s.soggetti),
            s.modello or "",
            s.ricorrenza or "",
        ])
    return buffer.getvalue()
