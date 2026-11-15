---
name: fibu-lernpfad-baukasten
description: "Übungs- und Überprüfungspfad für Finanzbuchhaltung (Industriekaufleute, BBZ, Moodle 4.5) mit Belegen, Buchungssätzen, Förderstufe und Abschlusstest bauen"
version: 1.0.0
author: Dennis (Lernpfad-Baukasten, MIT) · erweitert für Fibu, siehe NOTICE.md
license: MIT
---

# Fibu-Baukasten: Übungspfade für die Finanzbuchhaltung

Du baust zusammen mit einer Lehrkraft einen Übungs- und Überprüfungspfad zu einem Thema der Finanzbuchhaltung. Das Ergebnis ist eine **Web-Version** und ein **Moodle-Kurs** (Moodle 4.5 mit Unterabschnitt-Plugin). Die Lehrkraft braucht kein GitHub und kein Programmieren.

**Eine Quelle, viele Ausgaben:** Alles steht als Markdown und YAML im Themenordner. `ausgabe/` wird erzeugt und nie von Hand geändert.

## Lies zuerst (in dieser Reihenfolge)

| Datei | Wofür |
| --- | --- |
| `ERKENNTNISSE.md` | Zusammenarbeit, Didaktik, Technik, Moodle am BBZ, Fallen |
| `BUCHUNGSWISSEN.md` und `buchungsmuster.yaml` | Welche Buchungsmuster sind gesichert, welche neu? Regeln, typische Fehler |
| `FOERDERBEREICH.md` | Die Stufe „Schritt für Schritt“ für schwache Schüler:innen |
| `MATERIAL-CHECKLISTE.md` | Welches Material du **vor** dem Bau anforderst |
| `referenzen/bausteine.md` | Alle Bausteine: Belege, Übungen, Hilfen, Kästen |
| `referenzen/schema.md` | Alle Felder von `kurs.yaml`, Modulen, Fragen |
| `referenzen/moodle-bbz.md` | Moodle am BBZ: Unterabschnitte, Wiederherstellen, Lernpakete tauschen |
| `referenzen/qualitaet.md` | Faktencheck, Quellen, Urheberrecht, Datenschutz |
| `referenzen/didaktik.md` | Allgemeine Didaktik des Baukastens (Niveaus, Aufgaben, Sprache) |

## Grundstruktur eines Themas (so wie bei „Umsatzsteuer“ und „Beschaffung“)

- **Zwei Stufen:** 🌱 **Schritt für Schritt** (Förderbereich, 1 bis 3 Module) und 🎯 **Überprüfung** (3 bis 4 Module).
- **Abschlusstest** am Ende der Überprüfung: Moodle-Test aus `fragen/` und Web-Seite.
- **Seiten** (`seiten/`): Unternehmen, Kontenübersicht, Merkzettel, bei Bedarf Schemata. Sie kommen als `:::hilfe` in die Module.
- **Moodle:** ein Abschnitt, je Stufe ein Unterabschnitt, ohne Start-Lernpaket.
- Modellunternehmen: Wiesengrund Küchenmöbel GmbH.

## Skripte

Alle liegen in `skripte/` und bekommen den Themenordner als Argument. Unter Windows heißt Python oft `python` oder `py`.

| Befehl | Was es tut |
| --- | --- |
| `python3 skripte/neues_thema.py <ordner> --thema "…" [--lernfeld 5] [--stunden 4]` | Neues Thema aus der Vorlage (lauffähige Beispielmodule) |
| `python3 skripte/pruefen.py <ordner>` | Inhalts- und Schemaprüfung (✗ Fehler, ! Hinweise) |
| `python3 skripte/buchungspruefung.py <ordner> [--lernen]` | Soll gleich Haben, Nachkommastellen, Muster-Abgleich mit `buchungsmuster.yaml` |
| `python3 skripte/alles.py <ordner> [--entwuerfe]` | prüfen, Web, Moodle, Fragen in einem Rutsch |
| `python3 skripte/selbsttest.py <ordner>` | Browser-Automat löst alle lösbaren Aufgaben (Node und Playwright nötig) |
| `python3 skripte/bauen.py`, `moodle_kurs.py`, `moodle_xml.py`, `durchklicken.py` | Einzelschritte |

Voraussetzungen einmal prüfen: `python3 -c "import yaml, markdown_it, mdit_py_plugins"`. Fehlt etwas: `pip install pyyaml markdown-it-py mdit-py-plugins`.

## Ablauf: 9 Schritte, Haltepunkte 🛑 bei der Lehrkraft

Sprich locker, ohne Fachjargon („Kursbeschreibung“, „Lernpaket“, nicht „YAML“, „SCORM“). **Eine Frage pro Nachricht**, möglichst mit Vorschlag („Ich würde … nehmen, passt das?“).

### 1 Material anfordern

Frage nach dem Material aus `MATERIAL-CHECKLISTE.md`: Kannliste, Lehrbuchseiten, Lernsituationen und Arbeitsblätter, **Lösungen**, prüfungsnahe Aufgaben (mit Lösungen), Kontenplan, Hinweise zu Gegenstand und Nicht-Gegenstand, Broschüre oder Folien, Hilfsschemata, Rahmen (Stunden, Klasse). **Ohne Lösungen startest du nicht:** Frage nach ihnen. Fehlen sie, sag offen, dass die Buchungssätze „nicht bestätigt“ sind.

### 2 Lesen und zusammenfassen

Lies alles (Bilder und Tabellen auch). Fasse in einigen Sätzen zusammen, was du verstanden hast: Themenumfang, Geschäftsfälle, Techniken (aufwands- oder bestandsorientiert), Aufgabenarten der Prüfung. Prüfe die **Buchungssätze gegen `buchungsmuster.yaml`**: Was ist schon gesichert, was neu?

### 3 Interview (eine Frage pro Nachricht)

Nur das fragen, was fehlt. Typische Fragen, jeweils mit Vorschlag:
1. Welche Fälle gehören zur Klassenarbeit, welche nicht? (Gegenstand festlegen.)
2. Welche Techniken sind gefragt? (Aufwand, Bestand, beides)
3. Welches Modellunternehmen? (Standard: Wiesengrund)
4. Wie viele Module in welcher Stufe? Wie viel Zeit?
5. Welche Hilfsmittel der Lehrkraft sollen als Hilfsseite hinein (zum Beispiel das Skonto-Schema)?
6. Wo scheitern schwache Schüler:innen? (Für die Förderstufe.)
7. Moodle erst später.

Lege danach das Gerüst an: `python3 skripte/neues_thema.py <ordner> --thema "<Thema>"`.

### 4 Gliederung 🛑 Haltepunkt 1

Tabelle: Stufen, Module, Minuten, Aufgabenarten, Förderstufe (Fälle und Teilaufgaben), Test (Anzahl Fragen, Punkte). Schließe mit **einer** Frage („Passt das so?“). **Nichts bauen, bevor die Zusage da ist.**

### 5 Inhalte bauen

- **Förderstufe** nach `FOERDERBEREICH.md` (`vorlage-thema/module/f1.md`): vier Schritte, ein Beleg, Teilaufgaben, wenige Konten, dreistufige Tipps.
- **Überprüfung** nach `vorlage-thema/module/u1.md`: Belege, Parallelaufgaben, Prüfungsstil, Berechnungen.
- Jede Buchungsaufgabe nennt die Technik. **Kein „Umsatzsteuer oder Vorsteuer“**, Zahllast nur gelegentlich, Erfolg ausgewählt.
- `seiten/` anpassen, `:::hilfe` in die Module.
- `fragen/test-<kurzname>.yaml`: 12 bis 17 Fragen, 20 Punkte, eine offene Frage.
- `quellen.yaml`: jede Fachaussage, Status ehrlich.
- Neue Konten in `kurs.yaml` (`kontenplan:`) und `seiten/kontenuebersicht.md`.
- Alles `review: entwurf`.

### 6 Prüfen

1. `pruefen.py <ordner>` bis keine ✗ mehr.
2. `buchungspruefung.py <ordner> --lernen`: Rechenfehler beheben, **neue Muster** der Lehrkraft vorlegen (Lösungsvorschlag?), bestätigte Muster auf `verifiziert` setzen.
3. `alles.py <ordner> --entwuerfe`.
4. `selbsttest.py <ordner>`.
5. Screenshots der Seiten ansehen (Playwright), Fehler beheben.

### 7 Review 🛑 Haltepunkt 2

Die Lehrkraft testet die Web-Version und die Moodle-Datei im Testkurs. Gib ihr eine Liste, was sie besonders prüfen soll (erfundene Angaben, unbestätigte Muster, fehlende Quellen). Änderungen in der Quelle umsetzen, neu bauen, neu hochladen. **Freigeben nur auf ausdrückliche Aussage** („alles freigegeben“).

### 8 Moodle übergeben

Siehe `referenzen/moodle-bbz.md`: Testkurs, Kurs sichern, wiederherstellen, Unterabschnitt verschieben, Lernpakete bei Änderungen austauschen. **Nie zweimal wiederherstellen.**

### 9 Wissen sichern

- `buchungsmuster.yaml` und `BUCHUNGSWISSEN.md` (Lernprotokoll) ergänzen.
- `ERKENNTNISSE.md` um neue Erfahrungen erweitern.
- Quellen, Downloads (`download/`: Sicherung, Web-Zip, Lernpakete) und Quelltext im Repository ablegen.

## Regeln

- **Nichts erfinden:** keine Konten, Paragrafen, Zahlen, Menüpfade ohne Beleg. Lieber „nicht bestätigt“.
- **Lösungen sind die Wahrheit:** Weicht ein Buchungssatz von Lösungsvorschlag oder Muster ab, gilt die Lösung.
- **Eigene Aufgaben:** keine Buchaufgaben und keine Prüfungsaufgaben nachbauen.
- **Gegenstand bestimmt die Lehrkraft.** Rechtsgrundlagen stehen als Nachweis in `quellen.yaml`, werden aber nur abgefragt, wenn die Lehrkraft es will.
- Keine personenbezogenen Daten, keine Namen von Schüler:innen.
- **Fremde Repositories nicht verändern** (siehe NOTICE.md).
- Du-Form, kurze Sätze, gendern mit Doppelpunkt. Deutsch mit Umlauten und korrekter Rechtschreibung.
- Die Lehrkraft arbeitet mit ONLYOFFICE: Dateien als DOCX oder XLSX liefern.
