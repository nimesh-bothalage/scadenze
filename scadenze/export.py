"""Export delle scadenze in formato iCalendar."""

from __future__ import annotations

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
