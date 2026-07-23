from datetime import date

from scadenze.data import (
    Scadenza,
    carica_scadenze,
    cerca,
    filtra_categoria,
    filtra_mese,
    filtra_prossime,
)


def _esempio() -> list[Scadenza]:
    return [
        Scadenza(
            id="iva-1",
            data=date(2026, 7, 16),
            titolo="Liquidazione IVA mensile",
            descrizione="Versamento IVA di giugno",
            categoria="iva",
        ),
        Scadenza(
            id="ritenute-1",
            data=date(2026, 8, 20),
            titolo="Versamento ritenute",
            descrizione="Ritenute su redditi di lavoro dipendente",
            categoria="ritenute",
        ),
        Scadenza(
            id="lipe-q2",
            data=date(2026, 9, 30),
            titolo="LIPE 2° trimestre",
            descrizione="Comunicazione liquidazioni periodiche IVA",
            categoria="iva",
        ),
    ]


def test_carica_scadenze_ordina_per_data():
    scadenze = carica_scadenze()
    assert len(scadenze) >= 3
    assert all(a.data <= b.data for a, b in zip(scadenze, scadenze[1:]))


def test_filtra_prossime_esclude_passate_e_lontane():
    oggi = date(2026, 7, 23)
    trovate = filtra_prossime(_esempio(), oggi, giorni=30)
    assert [s.id for s in trovate] == ["ritenute-1"]


def test_filtra_prossime_include_oggi():
    oggi = date(2026, 8, 20)
    trovate = filtra_prossime(_esempio(), oggi, giorni=30)
    assert "ritenute-1" in [s.id for s in trovate]


def test_filtra_mese():
    trovate = filtra_mese(_esempio(), 9)
    assert [s.id for s in trovate] == ["lipe-q2"]


def test_filtra_categoria_case_insensitive():
    trovate = filtra_categoria(_esempio(), "IVA")
    assert [s.id for s in trovate] == ["iva-1", "lipe-q2"]


def test_cerca_su_titolo_e_descrizione():
    assert [s.id for s in cerca(_esempio(), "lipe")] == ["lipe-q2"]
    assert [s.id for s in cerca(_esempio(), "dipendente")] == ["ritenute-1"]
    assert cerca(_esempio(), "bollo auto") == []
