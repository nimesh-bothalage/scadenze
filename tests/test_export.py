from datetime import date

from icalendar import Calendar

from scadenze.data import Scadenza, carica_scadenze
from scadenze.export import esporta_ical


def test_esporta_ical_un_evento_per_scadenza():
    scadenze = carica_scadenze()
    cal = Calendar.from_ical(esporta_ical(scadenze))
    eventi = [c for c in cal.walk("VEVENT")]
    assert len(eventi) == len(scadenze)


def test_esporta_ical_campi_evento():
    scadenza = Scadenza(
        id="test-1",
        data=date(2026, 8, 20),
        titolo="Liquidazione IVA mensile",
        descrizione="Versamento IVA di luglio",
        categoria="iva",
    )
    cal = Calendar.from_ical(esporta_ical([scadenza]))
    evento = next(iter(cal.walk("VEVENT")))
    assert str(evento["UID"]) == "test-1@scadenze"
    assert str(evento["SUMMARY"]) == "Liquidazione IVA mensile"
    assert evento["DTSTART"].dt == date(2026, 8, 20)
    assert evento["DTEND"].dt == date(2026, 8, 21)
