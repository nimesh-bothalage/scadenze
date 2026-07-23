from typer.testing import CliRunner

from scadenze.cli import app

runner = CliRunner()


def test_prossime_esce_bene():
    esito = runner.invoke(app, ["prossime", "--giorni", "400"])
    assert esito.exit_code == 0
    assert "Scadenze" in esito.output


def test_mese_dicembre_contiene_imu():
    esito = runner.invoke(app, ["mese", "dicembre"])
    assert esito.exit_code == 0
    assert "IMU" in esito.output


def test_mese_numerico():
    esito = runner.invoke(app, ["mese", "12"])
    assert esito.exit_code == 0
    assert "IMU" in esito.output


def test_mese_non_valido():
    esito = runner.invoke(app, ["mese", "tredicesimo"])
    assert esito.exit_code == 1


def test_categoria_filtra():
    esito = runner.invoke(app, ["--categoria", "imu", "mese", "12"])
    assert esito.exit_code == 0
    assert "IMU" in esito.output
    assert "Liquidazione IVA" not in esito.output


def test_cerca():
    esito = runner.invoke(app, ["cerca", "acconto IVA"])
    assert esito.exit_code == 0
    assert "28/12/2026" in esito.output


def test_export_ical(tmp_path):
    destinazione = tmp_path / "scadenze.ics"
    esito = runner.invoke(app, ["export", "--ical", "-o", str(destinazione)])
    assert esito.exit_code == 0
    assert destinazione.read_bytes().startswith(b"BEGIN:VCALENDAR")


def test_export_senza_formato():
    esito = runner.invoke(app, ["export"])
    assert esito.exit_code == 1
