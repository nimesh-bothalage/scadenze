"""Genera docs/demo.gif: sessione animata del terminale.

Ogni frame è un SVG di rich convertito in PNG con Edge headless,
poi i PNG vengono assemblati in GIF con Pillow.
"""

import re
import subprocess
import tempfile
from datetime import date
from pathlib import Path

from PIL import Image
from rich.console import Console

from scadenze import cli
from scadenze.data import carica_scadenze, filtra_categoria, filtra_mese, filtra_prossime

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
LARGHEZZA_CONSOLE = 88
ALTEZZA_RIGHE = 28  # altezza fissa della finestra, in righe di testo
SFONDO = "0d0d0d"
PASSO_DIGITAZIONE = 3          # caratteri digitati per frame
DURATA_DIGITAZIONE = 70        # ms
DURATA_COMANDO_COMPLETO = 600  # ms
DURATA_OUTPUT = 3500           # ms

OGGI = date.today()
SCADENZE = carica_scadenze()


def output_prossime() -> None:
    cli._stampa_tabella(filtra_prossime(SCADENZE, OGGI, 40), OGGI, "Scadenze nei prossimi 40 giorni")


def output_mese() -> None:
    cli._stampa_tabella(filtra_mese(SCADENZE, 12), OGGI, "Scadenze di dicembre 2026")


def output_categoria() -> None:
    trovate = filtra_prossime(filtra_categoria(SCADENZE, "inps"), OGGI, 120)
    cli._stampa_tabella(trovate, OGGI, "Scadenze nei prossimi 120 giorni")


COMANDI = [
    ("scadenze prossime --giorni 40", output_prossime),
    ("scadenze mese dicembre", output_mese),
    ("scadenze --categoria inps prossime --giorni 120", output_categoria),
]


def rendi_frame(percorso_svg: Path, digitato: str, output=None) -> None:
    console = Console(record=True, width=LARGHEZZA_CONSOLE, force_terminal=True)
    cli.console = console
    console.print(f"[bold green]❯[/bold green] [bold]{digitato}[/bold]")
    if output is not None:
        console.print()
        output()
    righe = len(console.export_text(clear=False).splitlines())
    assert righe <= ALTEZZA_RIGHE, f"output di {righe} righe, alza ALTEZZA_RIGHE"
    for _ in range(ALTEZZA_RIGHE - righe):
        console.print()
    console.save_svg(str(percorso_svg), title="scadenze")


def dimensioni_svg(percorso: Path) -> tuple[int, int]:
    vista = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', percorso.read_text(encoding="utf-8"))
    return int(float(vista.group(1))) + 1, int(float(vista.group(2))) + 1


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        cartella = Path(tmp)
        frame_svg: list[tuple[Path, int]] = []  # (svg, durata ms)

        for comando, output in COMANDI:
            for fine in range(PASSO_DIGITAZIONE, len(comando), PASSO_DIGITAZIONE):
                svg = cartella / f"frame_{len(frame_svg):03d}.svg"
                rendi_frame(svg, comando[:fine] + "▌")
                frame_svg.append((svg, DURATA_DIGITAZIONE))
            svg = cartella / f"frame_{len(frame_svg):03d}.svg"
            rendi_frame(svg, comando)
            frame_svg.append((svg, DURATA_COMANDO_COMPLETO))
            svg = cartella / f"frame_{len(frame_svg):03d}.svg"
            rendi_frame(svg, comando, output)
            frame_svg.append((svg, DURATA_OUTPUT))

        larghezza = max(dimensioni_svg(svg)[0] for svg, _ in frame_svg)
        altezza = max(dimensioni_svg(svg)[1] for svg, _ in frame_svg)
        print(f"{len(frame_svg)} frame, finestra {larghezza}x{altezza}")

        immagini, durate = [], []
        for svg, durata in frame_svg:
            html = svg.with_suffix(".html")
            html.write_text(
                f'<!DOCTYPE html><html><body style="margin:0;background:#{SFONDO}">'
                f'<img src="{svg.name}" style="display:block"></body></html>',
                encoding="utf-8",
            )
            png = svg.with_suffix(".png")
            subprocess.run(
                [
                    EDGE,
                    "--headless=new",
                    "--disable-gpu",
                    f"--user-data-dir={cartella / 'profilo-edge'}",
                    f"--screenshot={png}",
                    f"--window-size={larghezza},{altezza}",
                    f"--default-background-color={SFONDO}FF",
                    html.as_uri(),
                ],
                check=True,
                capture_output=True,
                timeout=60,
            )
            immagini.append(Image.open(png).convert("RGB"))
            durate.append(durata)
            print(".", end="", flush=True)
        print()

        dest = Path(__file__).resolve().parent.parent / "docs" / "demo.gif"
        dest.parent.mkdir(exist_ok=True)
        prima, *resto = [im.quantize(colors=64) for im in immagini]
        prima.save(
            str(dest),
            save_all=True,
            append_images=resto,
            duration=durate,
            loop=0,
            optimize=True,
        )
        print(f"Salvato {dest} ({dest.stat().st_size // 1024} KiB)")


if __name__ == "__main__":
    main()
