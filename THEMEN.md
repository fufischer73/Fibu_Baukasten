# Themenübersicht

Welche Themen der Baukasten schon kennt und wie viel gesichertes Buchungswissen (`buchungsmuster.yaml`) dazugehört.
Diese Datei wird von `python3 skripte/themen.py --schreiben` erzeugt. Gepflegt wird `themen.yaml`.

| Thema | Lernfeld | Stand | Repository | Muster bestätigt | Muster offen | Hinweis |
| --- | --- | --- | --- | --- | --- | --- |
| Umsatzsteuer prüfen | – | gebaut (2026-11-06) | Umsatzsteuer- | 6 | 0 | Check-Pfad, erster Pfad des Baukastens. Lernfeld bitte ergänzen. |
| Buchungen im Beschaffungsprozess | 5 | freigegeben (2026-11-09) | Fibu_Beschaffung | 21 | 0 | aufwands- und bestandsorientiert, Skonto, Gutschriften, Abschluss |
| Absatzprozesse buchen | 5 | freigegeben (2026-11-15) | Absatz_Fibu | 7 | 0 | Förderstufe, Überprüfung, Abschlusstest, Nachschlagen, Hilfsblatt |
| Anlagenwirtschaft: Abschreibungen und Anlagenverkauf | 5 | im Bau (2026-11-15) | Anlagenwirtschaft_Fibu | 16 | 0 | Anschaffungskosten, lineare, Leistungs- und degressive Abschreibung, Anlagenverkauf, digitale Wirtschaftsgüter |

**Gesamt:** 50 bestätigte Buchungsmuster, 0 offene (Status „neu“).

## So kommt ein neues Thema dazu

1. Material sammeln (MATERIAL-CHECKLISTE.md). Eintrag in `themen.yaml` mit `stand: material`.
2. Konten prüfen: `python3 skripte/kontenpruefung.py --liste …`. Fehlende Konten der Lehrkraft vorlegen.
3. Buchungssätze aus den Lösungen aufnehmen (`skripte/wissen_aufnehmen.py`) und von der Lehrkraft bestätigen lassen.
4. Pfad bauen (SKILL.md). `stand: im_bau`, danach `gebaut` und nach der Freigabe `freigegeben`.
5. `python3 skripte/themen.py --schreiben`.
