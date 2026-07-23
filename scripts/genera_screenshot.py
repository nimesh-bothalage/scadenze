"""Genera docs/demo.svg: screenshot dell'output di `scadenze prossime`."""

from datetime import date
from pathlib import Path

from rich.console import Console

from scadenze import cli
from scadenze.data import carica_scadenze, filtra_prossime

console = Console(record=True, width=88, force_terminal=True)
cli.console = console

oggi = date.today()
giorni = 40
console.print(f"[bold]$ scadenze prossime --giorni {giorni}[/bold]\n")
cli._stampa_tabella(
    filtra_prossime(carica_scadenze(), oggi, giorni),
    oggi,
    f"Scadenze nei prossimi {giorni} giorni",
)

dest = Path(__file__).resolve().parent.parent / "docs" / "demo.svg"
dest.parent.mkdir(exist_ok=True)
console.save_svg(str(dest), title="scadenze")
print(f"Salvato {dest}")
