# Fibu-Baukasten

Baukasten für **Übungs- und Überprüfungspfade zur Finanzbuchhaltung** (Industriekaufleute, BBZ Rendsburg-Eckernförde). Aus Markdown und YAML entstehen eine **Web-Version** und ein **Moodle-Kurs** (Moodle 4.5 mit Unterabschnitt-Plugin) mit Belegen, Buchungssätzen, Förderstufe und Abschlusstest. Fertige Beispiele: „Umsatzsteuer prüfen“ und „Buchungen im Beschaffungsprozess“.

Das Paket ist eigenständig. Es enthält die Werkzeuge des Lernpfad-Baukastens von Dennis (`dclausen01`, MIT) als eigene Kopie mit Erweiterungen, **ohne das Original zu verändern** (siehe `NOTICE.md`).

## Für die Lehrkraft: So startet ein neues Thema

1. Neuen Chat öffnen, den Text aus `STARTPROMPT.md` einfügen und das Material hochladen (**Checkliste: `MATERIAL-CHECKLISTE.md`**): Kannliste, Lehrbuchseiten, Lernsituationen **mit Lösungen**, prüfungsnahe Aufgaben, Kontenplan, Hinweise zum Gegenstand.
2. Claude fragt, was fehlt (eine Frage pro Nachricht) und legt eine Gliederung vor. Gebaut wird erst nach deiner Zusage.
3. Du testest die Web-Version und den Moodle-Testkurs und sagst „freigegeben“, wenn alles passt.
4. Übergabe nach `referenzen/moodle-bbz.md`.

## Was jedes Thema bekommt

| Teil | Inhalt |
| --- | --- |
| 🌱 **Schritt für Schritt** | Förderbereich für schwache Schüler:innen: vier feste Schritte, ein Beleg, Teilaufgaben, wenig Konten, viele Tipps, Merkzettel (`FOERDERBEREICH.md`) |
| 🎯 **Überprüfung** | 3 bis 4 Module wie in der Klassenarbeit: Belege, Buchungssätze (aufwands- oder bestandsorientiert), Berechnungen, Sachverhalte, Parallelaufgaben |
| **Abschlusstest** | 12 bis 17 Fragen, 20 Punkte, als Moodle-Test und Web-Seite |
| **Hilfen** | Unternehmen, Kontenübersicht, Merkzettel und Schemata als aufklappbare Kästen im Modul |

## Das Gedächtnis des Baukastens

Der Baukasten **lernt die Buchungstechnik immer besser**:

- `buchungsmuster.yaml`: alle Buchungsmuster, die gegen Lösungsvorschläge der Lehrkraft **verifiziert** sind (derzeit 27 aus Beschaffung und Umsatzsteuer).
- `skripte/buchungspruefung.py <ordner> --lernen`: rechnet jede Aufgabe mit Zufallszahlen durch, meldet Rechenfehler und **neue Muster**, die noch bestätigt werden müssen.
- `BUCHUNGSWISSEN.md`: Regeln, typische Fehler, Lernprotokoll.
- `ERKENNTNISSE.md`: Zusammenarbeit, Didaktik, Technik, Moodle.

## Aufbau

```
SKILL.md                  Arbeitsanweisung für Claude (Ablauf, Haltepunkte, Regeln)
ERKENNTNISSE.md           Erfahrungen aus den bisherigen Pfaden
BUCHUNGSWISSEN.md         Buchungsregeln, Fehler, Lernprotokoll
buchungsmuster.yaml       geprüfte Buchungsmuster (maschinenlesbar)
FOERDERBEREICH.md         Konzept der Stufe „Schritt für Schritt“
MATERIAL-CHECKLISTE.md    Welches Material vor dem Bau gebraucht wird
STARTPROMPT.md            Erste Nachricht für einen neuen Chat
NOTICE.md                 Herkunft, Lizenz, Erweiterungen
vorlage-thema/            lauffähige Vorlage (Beispielmodule f1 und u1, Seiten, Test, kurs.yaml)
bibliothek/               wiederverwendbare Hilfen (zum Beispiel Skonto-Schema mit DOCX)
referenzen/               Baukasten-Dokumentation (Bausteine, Schema, Moodle, Qualität, Didaktik)
skripte/                  Werkzeuge: neues_thema, pruefen, buchungspruefung, alles, selbsttest …
vorlage/                  Web-Vorlage (Layout, Skripte der Lernpakete)
```

## Schnellstart (technisch)

```bash
pip install pyyaml markdown-it-py mdit-py-plugins
python3 skripte/neues_thema.py ../mein-thema --thema "Buchungen im Absatzprozess" --lernfeld 5
python3 skripte/pruefen.py ../mein-thema
python3 skripte/buchungspruefung.py ../mein-thema
python3 skripte/alles.py ../mein-thema --entwuerfe
python3 skripte/selbsttest.py ../mein-thema    # optional, braucht Node.js und Playwright
```

Die Vorlage baut sofort durch. Ihre Beispielinhalte (Ausgangsrechnung) werden mit der Lehrkraft durch den echten Inhalt ersetzt.

## Ein Thema pro Ordner

Jedes Thema bekommt ein eigenes Repository oder einen eigenen Ordner mit `kurs.yaml`, `module/`, `seiten/`, `fragen/`, `quellen.yaml`, `download/`. `buchungsmuster.yaml` und `BUCHUNGSWISSEN.md` bleiben **hier** im Baukasten und wachsen mit jedem Thema.
