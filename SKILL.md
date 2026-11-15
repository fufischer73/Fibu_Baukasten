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
| `kontenplan.yaml`, `stammdaten.yaml`, `THEMEN.md` | Zentraler Kontenplan (Schulplan gilt), gemeinsame Kunden und Lieferanten, Stand aller Themen |
| `referenzen/bausteine.md` | Alle Bausteine: Belege, Übungen, Hilfen, Kästen |
| `referenzen/schema.md` | Alle Felder von `kurs.yaml`, Modulen, Fragen |
| `referenzen/moodle-bbz.md` | Moodle am BBZ: Unterabschnitte, Wiederherstellen, Lernpakete tauschen |
| `referenzen/qualitaet.md` | Faktencheck, Quellen, Urheberrecht, Datenschutz |
| `referenzen/didaktik.md` | Allgemeine Didaktik des Baukastens (Niveaus, Aufgaben, Sprache) |

## Grundstruktur eines Themas (so wie bei „Umsatzsteuer“ und „Beschaffung“)

- **Zwei Stufen:** 🌱 **Schritt für Schritt** (Förderbereich, 1 bis 3 Module) und 🎯 **Überprüfung** (3 bis 4 Module).
- **Abschlusstest** am Ende der Überprüfung: Moodle-Test aus `fragen/` und Web-Seite.
- **Seiten** (`seiten/`): Unternehmen, Kontenübersicht, Merkzettel, bei Bedarf Schemata. Sie kommen als `:::hilfe` in die Module.
- **Optional eine dritte Stufe 📚 Nachschlagen** (Modul `n1` ohne Aufgaben): alle Hilfsseiten als `:::hilfe` plus ein **DOCX-Hilfsblatt** zum Ausdrucken (Vorlage: `bibliothek/hilfsblatt_erzeugen_absatz.py`, Skript in `werkzeuge/` ablegen, nicht in `material/`). Die Hilfen bleiben zusätzlich in den Aufgabenmodulen.
- **`PRUEFUNGSBEZUG.md`** im Themenordner: welche Aufgabenart der prüfungsnahen Aufgaben wo im Pfad vorkommt und was bewusst fehlt.
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
| `python3 skripte/selbsttest.py <ordner>` | Browser-Automat löst alle lösbaren Aufgaben, auch mit Zahllast und Erfolg (Node und Playwright nötig) |
| `python3 skripte/kontenpruefung.py <ordner>` bzw. `--liste 5001 …` | Stehen alle Konten des Pfads oder des Materials im Kontenplan? `--aufnehmen` und `--bestaetigen` pflegen den Plan |
| `python3 skripte/kontenuebersicht.py <ordner> [--schreiben]` | Erzeugt die Seite „Kontenübersicht“ aus den verwendeten Konten |
| `python3 skripte/stammdaten.py --seite` / `--pruefen <ordner>` / `--naechste kreditor` | Tabellen für „Unternehmen“, Abgleich der Belege mit den Stammdaten, nächste freie Nummer |
| `python3 skripte/wissen_aufnehmen.py aufnahme.yaml [--eintragen]` | Buchungssätze aus Material in den Wissensspeicher aufnehmen (siehe unten) |
| `python3 skripte/themen.py --schreiben` | Themenübersicht `THEMEN.md` erzeugen |
| `python3 skripte/bauen.py`, `moodle_kurs.py`, `moodle_xml.py`, `durchklicken.py` | Einzelschritte |

Voraussetzungen einmal prüfen: `python3 -c "import yaml, markdown_it, mdit_py_plugins"`. Fehlt etwas: `pip install pyyaml markdown-it-py mdit-py-plugins`.

## Ablauf: 9 Schritte, Haltepunkte 🛑 bei der Lehrkraft

Sprich locker, ohne Fachjargon („Kursbeschreibung“, „Lernpaket“, nicht „YAML“, „SCORM“). **Eine Frage pro Nachricht**, möglichst mit Vorschlag („Ich würde … nehmen, passt das?“).

### 1 Material anfordern

Frage nach dem Material aus `MATERIAL-CHECKLISTE.md`: Kannliste, Lehrbuchseiten, Lernsituationen und Arbeitsblätter, **Lösungen**, prüfungsnahe Aufgaben (mit Lösungen), Kontenplan, Hinweise zu Gegenstand und Nicht-Gegenstand, Broschüre oder Folien, Hilfsschemata, Rahmen (Stunden, Klasse). **Ohne Lösungen startest du nicht:** Frage nach ihnen. Fehlen sie, sag offen, dass die Buchungssätze „nicht bestätigt“ sind.

### 2 Lesen und zusammenfassen

Lies alles (Bilder und Tabellen auch). Fasse in einigen Sätzen zusammen, was du verstanden hast: Themenumfang, Geschäftsfälle, Techniken (aufwands- oder bestandsorientiert), Aufgabenarten der Prüfung. Prüfe die **Buchungssätze gegen `buchungsmuster.yaml`**: Was ist schon gesichert, was neu?

**Kontenabgleich (neu):** Sammle alle Kontonummern aus Lehrbuch, Aufgaben, Lösungen und Kontenrahmen und prüfe sie mit `python3 skripte/kontenpruefung.py --liste 5001 5101="Erlösberichtigungen f. Waren" …`. Es gilt die Bezeichnung des **Schulplans**, der Industriekontenrahmen ergänzt nur fehlende Konten. Fehlende Konten und abweichende Bezeichnungen legst du der Lehrkraft vor („Diese Konten fehlen in deinem Plan: … Soll ich sie aufnehmen?“). Erst nach der Bestätigung: `--aufnehmen … --quelle …`, dann `--bestaetigen …`. Scans (Bild-PDFs) mit `pdftoppm -r 80 -png` in Bilder umwandeln und ansehen.

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
- `seiten/` anpassen, `:::hilfe` in die Module. Die Kontenübersicht kommt aus `kontenuebersicht.py` (Hinweise je Konto in `konten_hinweise:` der kurs.yaml), die Tabellen für „Unternehmen“ aus `stammdaten.yaml`. **Neue Kunden, Lieferanten oder Dienstleister zuerst in `stammdaten.yaml` eintragen**, dann in die Belege.
- `fragen/test-<kurzname>.yaml`: 12 bis 17 Fragen, 20 Punkte, eine offene Frage.
- `quellen.yaml`: jede Fachaussage, Status ehrlich.
- Neue Konten in `kurs.yaml` (`kontenplan:`) und `seiten/kontenuebersicht.md`.
- Alles `review: entwurf`.

### 6 Prüfen

1. `pruefen.py <ordner>` bis keine ✗ mehr (prüft jetzt auch, ob alle Konten im Kontenplan stehen, ob die Belege zu den Stammdaten passen und ob ein Beleg mehr als 4 Spalten hat).
2. `buchungspruefung.py <ordner> --lernen`: Rechenfehler beheben, **neue Muster** der Lehrkraft vorlegen (Lösungsvorschlag?), bestätigte Muster auf `verifiziert` setzen.
3. `alles.py <ordner> --entwuerfe`.
4. `selbsttest.py <ordner>`.
5. Screenshots der Seiten ansehen (Playwright), Fehler beheben.

### 7 Review 🛑 Haltepunkt 2

Die Lehrkraft testet die Web-Version und die Moodle-Datei im Testkurs. Gib ihr eine Liste, was sie besonders prüfen soll (erfundene Angaben, unbestätigte Muster, fehlende Quellen). Änderungen in der Quelle umsetzen, neu bauen, neu hochladen. **Freigeben nur auf ausdrückliche Aussage** („alles freigegeben“).

### 8 Moodle übergeben

Siehe `referenzen/moodle-bbz.md`. **Hauptweg:** Abschnitt und Unterabschnitte im Zielkurs selbst anlegen, Lernpakete einfügen (erstes einrichten, dann duplizieren), bei Änderungen nur die Paketdatei tauschen. **Alternative:** Kurssicherung wiederherstellen und Unterabschnitte verschieben. **Nie zweimal wiederherstellen.**

### 9 Wissen sichern

- `buchungsmuster.yaml` und `BUCHUNGSWISSEN.md` (Lernprotokoll) ergänzen.
- `ERKENNTNISSE.md` um neue Erfahrungen erweitern.
- Quellen, Downloads (`download/`: Sicherung, Web-Zip, Lernpakete) und Quelltext im Repository ablegen.

## Wissen aufnehmen (ohne einen Pfad zu bauen)

Die Lehrkraft kann dem Baukasten jederzeit weiteres Buchungswissen geben, zum Beispiel Lösungen zu einem neuen Thema. Der Baukasten „lernt“, weil das Wissen in Dateien steht, die jeder neue Chat zuerst liest. Du behältst nichts von einem Chat zum nächsten. Jedes neue Muster und jedes neue Konto braucht die **Bestätigung der Lehrkraft**.

1. **Material anfordern** (Lösungen sind das Wichtigste) und lesen. Eintrag in `themen.yaml` mit `stand: material`.
2. **Konten abgleichen:** `kontenpruefung.py --liste …`. Fehlende Konten der Lehrkraft vorlegen, nach der Bestätigung aufnehmen.
3. **Buchungssätze in `aufnahme.yaml` schreiben** (Vorlage: `vorlage-aufnahme.yaml`): Vorgang in Worten, Technik, Konten im Soll und Haben, wenn möglich Beträge für die Probe Soll = Haben, Quelle (zum Beispiel „Aufgabe 3a“). Derselbe Vorgang heißt immer gleich.
4. **Prüfen:** `python3 skripte/wissen_aufnehmen.py aufnahme.yaml`. Das Skript meldet je Satz: ✓ bekannt, ! neu, ✗ **Widerspruch** (derselbe Vorgang ist schon anders bestätigt), ✗ fehlendes Konto, ✗ Soll ≠ Haben, und weist auf Umkehrungen bekannter Muster hin (Gutschrift zur Rechnung). Bei Widersprüchen oder Fehlern wird nichts eingetragen: **Die Lehrkraft entscheidet.** Fehler im Material sind möglich, melde sie offen.
5. **Neue Muster der Lehrkraft vorlegen** („Stimmt das so? Gibt es einen Lösungsvorschlag dazu?“).
6. **Eintragen:** `python3 skripte/wissen_aufnehmen.py aufnahme.yaml --eintragen [--bestaetigt]`. Später `--bestaetigen "S:… > H:…"`.
7. **Wissen sichern:** Regeltabelle und Lernprotokoll in `BUCHUNGSWISSEN.md` ergänzen, `themen.yaml` nachziehen, `python3 skripte/themen.py --schreiben`.

Die Grenze: „Profi“ heißt hier „durch das Material und die Bestätigung der Lehrkraft abgesichert“. Gesetze und Fachbücher prüfst du nur, wenn sie im Material stehen. Nicht Belegtes bleibt „nicht bestätigt“.

## Regeln

- **Nichts erfinden:** keine Konten, Paragrafen, Zahlen, Menüpfade ohne Beleg. Lieber „nicht bestätigt“.
- **Lösungen sind die Wahrheit:** Weicht ein Buchungssatz von Lösungsvorschlag oder Muster ab, gilt die Lösung.
- **Eigene Aufgaben:** keine Buchaufgaben und keine Prüfungsaufgaben nachbauen.
- **Schulplan gilt:** Bezeichnungen und Kontonummern der Lehrkraft gehen vor. Der Industriekontenrahmen ergänzt nur fehlende Konten (nach Bestätigung).
- **Stammdaten zuerst:** Kunden, Lieferanten und Dienstleister des Modellunternehmens stehen in `stammdaten.yaml` und gelten für alle Pfade.
- **Gegenstand bestimmt die Lehrkraft.** Rechtsgrundlagen stehen als Nachweis in `quellen.yaml`, werden aber nur abgefragt, wenn die Lehrkraft es will.
- Keine personenbezogenen Daten, keine Namen von Schüler:innen.
- **Fremde Repositories nicht verändern** (siehe NOTICE.md).
- Du-Form, kurze Sätze, gendern mit Doppelpunkt. Deutsch mit Umlauten und korrekter Rechtschreibung.
- Die Lehrkraft arbeitet mit ONLYOFFICE: Dateien als DOCX oder XLSX liefern.
