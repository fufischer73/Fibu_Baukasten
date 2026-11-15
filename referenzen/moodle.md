# Moodle: Kursaufbau, Freischaltung, Übergabe

Getestet mit Moodle 5.2.3 (Standard) und 4.2.3. Standard ist seit Oktober 2026 **Moodle 5**.

## Was im Kurs landet

| Im Kurs | Woher | Moodle 4 | Moodle 5 |
| --- | --- | --- | --- |
| **🧭 Mein Lernpfad** (Abschnitt „Allgemeines“) | Startseite: Weitermachen, Fortschritt je Stufe, Einstufungstests, Selbstcheck | ✓ | ✓ |
| **🎯 Einstufungstests** (Allgemeines) | Kurz-Checks der vorigen Stufe; bewertet, kein Aktivitätsabschluss | ✓ | ✓ |
| Abschnitt je **Stufe** | `stufen` in kurs.yaml | ✓ | ✓ |
| **Lernpaket** je freigegebenem Modul | Modulseite + Zusatzseiten, speichert Häkchen, Notizen, Kurz-Check, „erledigt“ | untereinander im Abschnitt | Modul mit Abgabe/H5P als Unterabschnitt, sonst direkt |
| **📤 Aufgabe** (Datei-Abgabe) | `abgabe:` im Modulkopf; Meilenstein mit Rubrik aus `raster:` | ✓ | ✓ |
| **H5P-Kurz-Check** | `h5p: true` + `h5p.py` | – | ✓ |

Im Lernpaket steckt die Navigation des ganzen Kurses (links, mit Häkchen und 🔒), „Weiter“ führt auch zu
Aufgaben. In Aufgaben und H5P steht oben ⬅️ Zurück / ➡️ Weiter im Lernpfad. Der Knopf ⤢ oben blendet die
Moodle-Kopfzeile aus (Kompaktmodus, gut fürs Handy).

## Freischaltung

**Innerhalb einer Stufe** (`moodle.reihenfolge`):
- `nacheinander` (Standard): Ein Modul wird frei, wenn das Lernpaket davor als erledigt markiert ist.
  Abgaben blockieren nicht – sie laufen parallel weiter.
- `frei`: alle Module der Stufe sofort offen.

**Zwischen den Stufen** (`moodle.freischaltung`):
- **Modell A `einstufung` (Standard):** Stufe 2 öffnet sich, wenn der Meilenstein von Stufe 1 **abgegeben**
  ist (Abgabe reicht, Bewertung nicht nötig) **oder** der Einstufungstest mit mindestens `einstufung.bestehen`
  Prozent bestanden ist. Hat eine Stufe keinen Meilenstein mit Abgabe, zählt das letzte Lernpaket.
- **Modell B `offen`:** alle Stufen sofort offen, keine Einstufungstests.

Einstufungstests laufen im Browser der Schüler:innen – für die Freischaltung gut, als Prüfung nicht sicher.
Für bewertete Tests: `fragen/` + `tests:` in kurs.yaml → echter Moodle-Test in der Kurssicherung.

## Moodle-Tests (tests: in kurs.yaml)

- Der Test steht hinter dem Modul aus `nach:` (bzw. am Ende der Stufe aus `stufe:`) und übernimmt dessen
  Freischaltung. Mit `bestehen:` gilt er erst ab dieser Bewertung als abgeschlossen.
- Fragen: Moodle 4 legt sie im Kurs-Fragenpool ab (Kategorie `<Kurs>/<Testtitel>`), Moodle 5 in einer eigenen
  Fragensammlung „Fragensammlung: <Kurs>“ (erscheint nicht als Aktivität auf der Kursseite).
- Rechenaufgaben mit Varianten → Zufallsfrage aus ihrer Unterkategorie: Jede:r bekommt andere Zahlen.
- Offene Fragen bewertet die Lehrkraft unter **Test › Ergebnisse › Manuelle Bewertung**.
- Getestet mit Moodle 4.2.3 und 5.2.3: wiederherstellen, Versuch starten, richtige Antworten → volle Punkte.
- Eine fertige Klausur aus dem Klausur-Baukasten lässt sich mit `klausur: <ordner>` in `tests:` als Test in den Kurs
  einbauen (siehe `schema.md`). Für **Klausuren** (Punkte je Aufgabe, Teile mit Überschrift, Essay-Wortgrenzen, Zeitfenster, Kennwort, keine Einsicht,
  Notenschlüssel) gibt es den Skill `klausur-baukasten/`. Er nutzt dieselben Bausteine (`moodle_test.py`) mit zusätzlichen
  Testschlüsseln `oeffnen`, `schliessen`, `kennwort`, `navigation`, `abschnitte` und `feedback: punkte|keine`.
  Die Klausur-Ausgabe ist im **BBZ-Moodle 4.5.12+** wiederhergestellt und im Testkurs als Schüler:in durchgespielt
  worden (verifiziert 04.10.2026) – inklusive Notenschlüssel, Zeitlimit und Freitext. Andere Moodle-Versionen und
  andere Schulen trotzdem immer erst im Testkurs prüfen.

## Moodle 4 oder 5?

| | Moodle 4.x | Moodle 5.x |
| --- | --- | --- |
| Unterabschnitte | gibt es nicht – alles untereinander | Modul mit Abgabe/H5P bekommt einen Unterabschnitt |
| H5P-Kurz-Checks | nein (H5P-Kern zu alt für aktuelle Bibliotheken) | ja |
| Fragetyp Anordnung | ab 4.4 im Standard, in 4.2 nur als Plugin – fällt im Test weg, außer `moodle: {version: 4, anordnung: true}` (Moodle 4.4 und neuer) | ja |
| Fragen eines Tests | im Kurs-Fragenpool | in einer Fragensammlung (Aktivität, unsichtbar) |
| Standard im Skill | nur noch für ältere Installationen (`moodle.version: 4`) | **Standard** (`moodle.version: 5`) |

Die Kurssicherung trägt die niedrigste passende Version, damit Moodle beim Wiederherstellen nicht warnt.

## Übergabe: Kurs wiederherstellen

1. Kurs in Moodle öffnen (leer oder vorhanden – vorhandene Inhalte bleiben).
2. **Mehr › Wiederverwendung** (4.2: **Mehr › Kurswiederverwendung**), oben im Auswahlmenü **Wiederherstellen**.
3. Datei `ausgabe/moodle/<kurzname>_moodle5.mbz` (bzw. `_moodle4`) hochladen → **Wiederherstellen**.
4. **In diesen Kurs wiederherstellen › Inhalte zu diesem Kurs hinzufügen** → Weiter, Weiter, Wiederherstellen.
5. Kurs ansehen: Abschnitt „Allgemeines“ mit 🧭 Mein Lernpfad, darunter die Stufen.

**Wohin kommt es?** Beim Wiederherstellen mit „Inhalte zu diesem Kurs hinzufügen“ ordnet Moodle Abschnitte nach ihrer **Nummer** zu (Allgemeines = 0, darunter 1, 2 …); ein vorhandener Abschnitt mit derselben Nummer bekommt die Aktivitäten dazu. Mit `moodle.abschnitt: N` in kurs.yaml trägt die Sicherung die Stufen ab Abschnitt N ein (Start-Lernpaket am Anfang des Abschnitts, `start_im_abschnitt: false` lässt es in „Allgemeines“). Legen Sie den Zielabschnitt (bzw. Unterabschnitt) vorher im Kurs leer an und prüfen Sie die Zuordnung im Testkurs.

Nur **einmal** wiederherstellen – ein zweites Mal legt alles doppelt an. Für Änderungen siehe unten.
Klappt das Wiederherstellen nicht (Rechte, Dateigröße): `ANLEITUNG_moodle5.md` (bzw. `_moodle4`) beschreibt denselben Kurs zum
Nachklicken, mit allen Einstellungen. Lernpakete liegen einzeln in `ausgabe/moodle/lernpakete/`.

## Gut zu wissen (häufige Fragen)

- **Lehrkräfte sehen vor dem Lernpaket eine Zwischenseite „Vorschau/Start“** – das ist Moodle-Absicht
  (Rolle mit Berichtsrecht). Schüler:innen landen direkt im Paket.
- **Lehrkräften zeigt Moodle keine eigenen Abschlüsse.** Testen immer mit einem Schüler:innen-Testkonto,
  nicht mit „Rolle wechseln“. Das Paket weist darauf hin.
- **Fortschritt** (Häkchen, Notizen, Kurz-Check, erledigt) speichert Moodle je Lernpaket. Sichtbar für die
  Lehrkraft unter Lernpaket › Berichte und im Abschlussbericht des Kurses.
- **Punkte**: Lernpakete melden die Kurz-Check-Punkte als Bewertung (Bewertungen-Übersicht). Wer das nicht
  will, stellt beim Lernpaket die Bewertung auf 0 – oder blendet die Spalte aus.
- **H5P**: Sind die H5P-Inhaltstypen im Moodle noch nicht installiert, muss das erste Paket jemand mit
  Admin-/Manager-Rechten hochladen (danach geht es für alle).
- **Handy**: läuft im Handy-Browser (getestet). Die Moodle-App ist nicht getestet – dort fehlt vermutlich die
  Kursnavigation im Paket.

## Änderungen an einem laufenden Kurs

- **Inhalt eines Moduls korrigiert:** neu bauen, dann in Moodle beim Lernpaket › Einstellungen › Paket die
  neue ZIP aus `ausgabe/moodle/lernpakete/` hochladen und speichern. Fortschritt bleibt (gleiche Modul-ID).
- **Neues Modul:** Lernpaket einzeln anlegen, Einstellungen aus der Klickanleitung übernehmen, Voraussetzung
  „vorheriges Lernpaket abgeschlossen“ setzen. Im nächsten Schuljahr einfach den ganzen Kurs neu wiederherstellen.
- **Abgabe/Raster geändert:** direkt in Moodle an der Aufgabe ändern (und in der Quelle nachziehen).

## Einstellungen, die die Kurssicherung setzt (für Handarbeit)

Lernpaket: Anzeige im aktuellen Fenster, Breite 100 %, Höhe 500; Kursstruktur deaktiviert; Navigation nein;
Struktur-Seite überspringen: immer; Versuchsstatus nicht anzeigen; Bewertung: höchste, max. 100;
Aktivitätsabschluss: Status „abgeschlossen“ erforderlich. Startseite ohne Abschluss und Bewertung 0,
Einstufungstests ohne Abschluss (zählen über die Bewertung).
Aufgabe: Dateiabgabe, Dateitypen und Anzahl laut Modulkopf, Abschluss „Abgabe erforderlich“, Meilenstein mit
Bewertungsraster (nicht erreicht / erreicht / besonders gut = 0 / 2 / 3 Punkte je Kriterium).
Kurs: Abschlussverfolgung an, Themenformat.
