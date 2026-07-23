# Changelog

Tutte le modifiche rilevanti di questo progetto sono documentate qui.
Il formato segue [Keep a Changelog](https://keepachangelog.com/it/1.1.0/)
e il versionamento segue il [Semantic Versioning](https://semver.org/lang/it/).

## [0.1.2] - 2026-07-23

### Aggiunto

- Export CSV (`scadenze export --csv`): separatore `;` e BOM UTF-8, così il
  file si apre correttamente in Excel in italiano

## [0.1.1] - 2026-07-23

### Corretto

- Scadenza dell'invio delle CU contenenti esclusivamente redditi di lavoro
  autonomo: 30 aprile 2026, non 31 marzo (regola in vigore dal 2026).
  Revisione completa delle date su scadenzario Agenzia delle Entrate,
  Fisco Oggi e Circolare INPS 14/2026: tutte le altre date confermate.

## [0.1.0] - 2026-07-23

### Aggiunto

- Comandi `prossime`, `mese`, `cerca` ed `export --ical`, con flag globale
  `--categoria`
- Dataset di 54 scadenze fiscali italiane 2026 con slittamenti per weekend,
  festivi e differimento feriale già applicati
- Tabelle rich con evidenza delle scadenze imminenti (≤ 7 giorni)
- Export iCalendar importabile in Google Calendar, Outlook e Apple Calendar
- README con GIF animata del terminale e pubblicazione automatica su PyPI
  via trusted publishing

[0.1.2]: https://github.com/nimesh-bothalage/scadenze/releases/tag/v0.1.2
[0.1.1]: https://github.com/nimesh-bothalage/scadenze/releases/tag/v0.1.1
[0.1.0]: https://github.com/nimesh-bothalage/scadenze/releases/tag/v0.1.0
