"""Comandi del CLI scadenze."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from . import data as dati
from .export import esporta_csv, esporta_ical

app = typer.Typer(
    help="Scadenze fiscali italiane 2026, dal terminale.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()

MESI = {
    "gennaio": 1,
    "febbraio": 2,
    "marzo": 3,
    "aprile": 4,
    "maggio": 5,
    "giugno": 6,
    "luglio": 7,
    "agosto": 8,
    "settembre": 9,
    "ottobre": 10,
    "novembre": 11,
    "dicembre": 12,
}


@app.callback()
def main(
    ctx: typer.Context,
    categoria: str | None = typer.Option(
        None, "--categoria", "-c", help="Filtra per categoria (iva, ritenute, inps, ...)"
    ),
) -> None:
    ctx.obj = {"categoria": categoria}


def _carica(ctx: typer.Context) -> list[dati.Scadenza]:
    scadenze = dati.carica_scadenze()
    categoria = (ctx.obj or {}).get("categoria")
    if categoria:
        scadenze = dati.filtra_categoria(scadenze, categoria)
    return scadenze


def _stampa_tabella(scadenze: list[dati.Scadenza], oggi: date, titolo: str) -> None:
    if not scadenze:
        console.print("[yellow]Nessuna scadenza trovata.[/yellow]")
        return
    tabella = Table(title=titolo, header_style="bold cyan")
    tabella.add_column("Data", style="bold", no_wrap=True)
    tabella.add_column("Scadenza")
    tabella.add_column("Categoria")
    tabella.add_column("Modello")
    tabella.add_column("Tra", justify="right", no_wrap=True)
    for s in scadenze:
        delta = (s.data - oggi).days
        if delta < 0:
            tra = "[dim]passata[/dim]"
        elif delta == 0:
            tra = "[bold red]oggi[/bold red]"
        elif delta <= 7:
            tra = f"[bold red]{delta} gg[/bold red]"
        else:
            tra = f"[green]{delta} gg[/green]"
        tabella.add_row(
            s.data.strftime("%d/%m/%Y"),
            f"{s.titolo}\n[dim]{s.descrizione}[/dim]",
            s.categoria,
            s.modello or "-",
            tra,
        )
    console.print(tabella)


@app.command()
def prossime(
    ctx: typer.Context,
    giorni: int = typer.Option(30, "--giorni", "-g", help="Orizzonte in giorni"),
) -> None:
    """Scadenze nei prossimi giorni (default: 30)."""
    oggi = date.today()
    trovate = dati.filtra_prossime(_carica(ctx), oggi, giorni)
    _stampa_tabella(trovate, oggi, f"Scadenze nei prossimi {giorni} giorni")


@app.command()
def mese(
    ctx: typer.Context,
    nome_mese: str = typer.Argument(..., metavar="MESE", help="Nome del mese (es. luglio) o numero 1-12"),
) -> None:
    """Scadenze di un mese del 2026."""
    chiave = nome_mese.strip().lower()
    if chiave.isdigit() and 1 <= int(chiave) <= 12:
        numero = int(chiave)
    elif chiave in MESI:
        numero = MESI[chiave]
    else:
        console.print(f"[red]Mese non riconosciuto:[/red] {nome_mese}")
        raise typer.Exit(code=1)
    trovate = dati.filtra_mese(_carica(ctx), numero)
    _stampa_tabella(trovate, date.today(), f"Scadenze di {chiave if not chiave.isdigit() else numero} 2026")


@app.command()
def cerca(ctx: typer.Context, testo: str = typer.Argument(..., help="Testo da cercare")) -> None:
    """Cerca nel titolo e nella descrizione delle scadenze."""
    trovate = dati.cerca(_carica(ctx), testo)
    _stampa_tabella(trovate, date.today(), f"Scadenze che contengono “{testo}”")


@app.command()
def export(
    ctx: typer.Context,
    ical: bool = typer.Option(False, "--ical", help="Esporta in formato iCalendar (.ics)"),
    csv: bool = typer.Option(False, "--csv", help="Esporta in CSV (separatore ';', apribile in Excel)"),
    output: Path | None = typer.Option(None, "--output", "-o", help="File di destinazione"),
) -> None:
    """Esporta le scadenze in formato iCalendar (--ical) o CSV (--csv)."""
    if ical == csv:
        console.print("[red]Specifica un formato: --ical oppure --csv[/red]")
        raise typer.Exit(code=1)
    scadenze = _carica(ctx)
    if ical:
        destinazione = output or Path("scadenze.ics")
        destinazione.write_bytes(esporta_ical(scadenze))
    else:
        destinazione = output or Path("scadenze.csv")
        # utf-8-sig: con il BOM Excel riconosce l'UTF-8 e mostra bene gli accenti
        destinazione.write_text(esporta_csv(scadenze), encoding="utf-8-sig")
    console.print(f"[green]Esportate {len(scadenze)} scadenze in[/green] {destinazione}")


if __name__ == "__main__":
    app()
