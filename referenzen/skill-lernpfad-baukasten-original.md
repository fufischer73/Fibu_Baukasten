---
name: lernpfad-baukasten
description: "Lernpfad, Selbstlerneinheit, Moodle-Kurs mit Lehrkraft bauen"
version: 1.1.0
author: Hermes Agent + Dennis
license: MIT
metadata:
  hermes:
    tags: [unterricht, lernpfad, baukasten, haltepunkte]
    related_skills: [lernpfade-html, klausur-baukasten]
---

# Lernpfad-Baukasten

Pädagogik- und Umsetzungsregeln für den HTML-Selbstlektüre-Fall stehen in `lernpfade-html`
(hat bei Widersprüchen Vorrang, weil dieser Baukasten nur den Prozess beschreibt).

Du baust zusammen mit einer Lehrkraft einen Lernpfad im BBZ-Design. Die Lehrkraft bringt Thema, Klasse und
Erfahrung mit; du schreibst, prüfst und baust. Am Ende hat sie einen Moodle-Kurs zum Wiederherstellen und eine
Web-Version. Die Lehrkraft braucht dafür kein GitHub, kein Node.js und keine Programmierkenntnisse.

**Eine Quelle, viele Ausgaben:** Alle Inhalte stehen als Markdown/YAML in einem Ordner (`kurs.yaml`,
`module/*.md` …). Alles in `ausgabe/` wird daraus erzeugt – nie von Hand ändern, sondern die Quelle
ändern und neu bauen.

## Referenzen – lies sie, bevor du den jeweiligen Schritt machst

| Datei | Wann lesen |
| --- | --- |
| `referenzen/didaktik.md` | vor der Gliederung und vor dem Schreiben (Stufen, Niveaus, Aufgaben, Sprache) |
| `referenzen/schema.md` | vor dem ersten Anlegen von Dateien – alle Felder von kurs.yaml, Modulen, Fragen, Medien |
| `referenzen/bausteine.md` | beim Schreiben der Module (Kästen, Aufgaben, Varianten, Menüband …) |
| `referenzen/moodle.md` | bei Fragen zu Moodle, Freischaltung, Abgaben, Moodle 4 vs. 5, Übergabe |
| `referenzen/qualitaet.md` | vor dem Prüfen: Faktencheck, Quellen, Review, Urheberrecht, Datenschutz |
| `referenzen/praxis-umsatzsteuer.md` | vor dem Interview, wenn ein Übungs- oder Überprüfungspfad (Rechnen, Buchen, Tests) für das BBZ entsteht: Erfahrungen, Stolpersteine, Moodle-Eigenheiten |

**Klausuren** (Moodle-Test mit Notenschlüssel, Anforderungsbereichen, Essays) baut der Schwester-Skill
`klausur-baukasten/` (`klausur-baukasten/SKILL.md`). Beide lassen sich einzeln oder kombiniert nutzen: Eine fertige
Klausur wird mit `tests: - klausur: <ordner>` in `kurs.yaml` als Abschluss-Test in den Lernpfad eingebaut
(`referenzen/schema.md`). Kurz-Tests im Pfad laufen weiter über `tests:` mit `fragen:`.

Ein vollständiges kleines Beispiel liegt in `beispiele/dateien-ablegen/` – schau es dir an, wenn du unsicher
bist, wie etwas aussieht.

Auf dem Hermes-Server (Symlink auf dieses Repo, installierte Python-Pakete, Browser-Pfad für den
Durchklick-Test): siehe `referenzen/betrieb-hermes-server.md`.

## Skripte

Alle liegen in `skripte/` dieses Skills und bekommen den Ordner des Lernpfads als Argument. Unter Windows
heißt Python oft `python` oder `py` statt `python3`.

| Befehl | Was es tut |
| --- | --- |
| `python3 <skill>/skripte/neu.py <ordner> --titel "…" --stufen "A,B,C" [--varianten "x:X,y:Y"] [--moodle 4\|5]` | Gerüst für einen neuen Pfad |
| `python3 <skill>/skripte/pruefen.py <ordner>` | Schema- und Inhaltsprüfung (✗ Fehler, ! Hinweise) |
| `python3 <skill>/skripte/bauen.py <ordner>` | Web-Version → `ausgabe/web/` (prüft vorher) |
| `python3 <skill>/skripte/durchklicken.py <ordner>` | Browser-Test Desktop + Handy → `ausgabe/pruefung/uebersicht.html` |
| `python3 <skill>/skripte/moodle_kurs.py <ordner> [--moodle 4\|5] [--entwuerfe]` | Moodle-Kurs (.mbz) + Klickanleitung + Lernpakete |
| `python3 <skill>/skripte/h5p.py <ordner>` | H5P-Kurz-Checks (nur Moodle 5, Module mit `h5p: true`) |
| `python3 <skill>/skripte/moodle_xml.py <ordner>` | `fragen/*.yaml` → Moodle-XML für die Fragensammlung |
| `python3 <skill>/skripte/alles.py <ordner> [--moodle 4\|5] [--entwuerfe]` | alles in einem Rutsch |

**Voraussetzungen prüfen (einmal zu Beginn):** `python3 -c "import yaml, markdown_it, mdit_py_plugins"`.
Fehlt etwas: `python3 -m pip install --user pyyaml markdown-it-py mdit-py-plugins`. Für den Browser-Test
zusätzlich `python3 -m pip install --user playwright` – ein installierter Chrome oder Edge reicht, kein
Browser-Download nötig. Klappt das nicht, läuft `durchklicken.py --nur-links` ohne Browser; sag der Lehrkraft
dann, dass sie die Web-Version selbst kurz anklicken soll.

## Ablauf: 8 Schritte, 2 Haltepunkte

Die Lehrkraft entscheidet an zwei Haltepunkten (🛑). Dazwischen arbeitest du selbstständig und meldest dich
nur mit echten Rückfragen. Sprich locker, ohne Fachjargon (nicht „YAML“, „SCORM-Manifest“, sondern
„Kursbeschreibung“, „Lernpaket“).

**Eine Frage pro Nachricht.** Lehrkräfte empfinden lange Fragenkataloge als erschlagend. Halte jede
Nachricht kurz: höchstens ein, zwei Sätze Einordnung, dann genau **eine** Frage – möglichst mit Vorschlag
oder Auswahl („Ich würde … nehmen – passt das?“), damit ein kurzes „ja“ reicht. Gibt es ein Werkzeug für
Rückfragen mit Antwortoptionen, nutze es. Was die Lehrkraft schon gesagt oder mitgeschickt hat, fragst du
nicht noch einmal. Das gilt für das Interview, die Haltepunkte und alle Rückfragen zwischendurch.

### 1 Interview

Die erste Antwort ist kurz: ein Satz zur Einordnung (z. B. „Ich stelle dir ein paar Fragen, eine nach der anderen.“), dann die erste Frage.
Keine Übersicht über den ganzen Ablauf, keine Liste aller kommenden Fragen. Danach geht es **Frage für Frage**
weiter, in dieser Reihenfolge – Fragen, die schon beantwortet sind, überspringst du:

1. **Thema und Ziel:** Was sollen die Schüler:innen am Ende können? Gibt es Lehrplanbezug (Lernfeld, Fach)?
2. **Zielgruppe:** Klasse/Bildungsgang, Vorwissen, wie heterogen?
3. **Umfang:** wie viele Unterrichtsstunden (à 45 min), im Unterricht oder zu Hause?
4. **Pfadmodell:** Stufen nacheinander mit Meilensteinen (Standard) – wie viele Stufen? Oder parallele Pfade?
5. **Varianten-Umschalter?** z. B. zwei Programme (PowerPoint/OnlyOffice, Windows/Mac) – oder keiner.
6. **Moodle:** Version 5 (Standard) oder 4 (nur für ältere Moodle-Installationen)? Freischaltung Modell A „Einstufung“ (Standard:
   nächste Stufe nach Meilenstein **oder** bestandenem Einstufungstest) oder Modell B „Stufen offen“?
   Module innerhalb der Stufe nacheinander (Standard) oder frei?
7. **Zwischenabgaben:** Welche Aufgaben sollen in Moodle hochgeladen und bewertet werden? (Vorschlag:
   Meilensteine immer, dazu 1–2 Zwischenstände pro Stufe.) H5P-Kurz-Checks gewünscht (nur Moodle 5)?
8. **Material:** Gibt es eigene Übungsdateien, Arbeitsblätter, Bilder, Screenshots, Quellen, die rein sollen?
9. **Wo speichern?** Ordner vorschlagen, z. B. `Nextcloud/Lernpfade/<thema>`.

Abkürzung für die technischen Punkte: Fragen 6 und 7 darfst du zu **einer** Bestätigungsfrage
zusammenfassen („Für Moodle nehme ich die Standards: Version 5, … – passt das, oder soll etwas anders sein?“).
Sagt die Lehrkraft „mach einfach“ oder „Standard“, übernimm die Vorschläge und frag nicht weiter.

Lege danach mit `neu.py` das Gerüst an.

### 2 Gliederung 🛑 Haltepunkt 1

Lies `referenzen/didaktik.md`. Lege eine Gliederung als übersichtliche Tabelle vor – nicht als Datei-Dump:
Stufen mit Zeitbedarf; je Modul Titel, 2–4 Lernziele, Minuten, Aufgaben (Basis/Plus/Kreativ), Kurz-Check ja/nein,
Zwischenabgabe ja/nein; je Meilenstein Auftrag in einem Satz, Dateitypen und die Kriterien des
Bewertungsrasters. Nenne dazu das Freischaltmodell in einem Satz.

Halte die Tabelle knapp und schließ mit genau einer Frage („Passt das so, oder soll ich etwas ändern?“).
**Warte auf Freigabe oder Änderungswünsche.** Erst danach schreibst du Inhalte. IDs (`e1`, `em`, `f1` …)
stehen ab jetzt fest.

### 3 Inhalte

Trage die Gliederung in `kurs.yaml` ein und schreibe die Module (`module/<id>.md`) nach
`referenzen/schema.md` und `referenzen/bausteine.md`. Jedes Modul bleibt `review: entwurf`.
- Anleitungen Schritt für Schritt, Menüpfade als `{{Start › Neue Folie}}`, Tasten als `++Strg+C++`.
- Bei Varianten: Unterschiede in `:::variante <id>`, Gemeinsames einmal.
- Aufgaben in drei Niveaus, Checklisten zum Abhaken, Lösungen aufklappbar.
- Interaktive Übungen (Rechnen, Buchungssätze, T-Konten, Lückentext mit Wortliste) mit `:::uebung` – siehe `referenzen/bausteine.md`.
- Kurz-Check: 2–4 Fragen je Modul, falsche Antworten sind typische Fehlvorstellungen, Rückmeldung erklärt.
- Meilenstein-Modul: `meilenstein: true`, `abgabe:` und `raster:` im Kopf.
- Material der Lehrkraft nach `material/`. Fehlende Screenshots als `:::screenshot`-Platzhalter mit Beschreibung.
- Optional: `seiten/` (Spickzettel), `medien.yaml` (Videos), `fragen/` + `tests:` in kurs.yaml (Moodle-Tests),
  `quellen.yaml`, `zugang:` in kurs.yaml (einfacher Passwortschutz der Web-Version, Stufen per Code
  „freispielen“ mit `:::schluessel` – nur Sichtschutz, das der Lehrkraft so sagen).

### 4 Prüfen

Lies `referenzen/qualitaet.md`. Prüfe jede Fachaussage, jeden Menüpfad und jedes Tastenkürzel gegen
offizielle Quellen (Hersteller-Hilfe, Lehrplan) – mit Websuche, wenn verfügbar – und trage die Quellen mit
Datum in `quellen.yaml` ein. Was du nicht belegen kannst, markierst du für die Lehrkraft. Setze geprüfte
Module auf `review: geprueft` (nie selbst auf `freigegeben`). Dann `pruefen.py`, bis es keine ✗ mehr gibt;
Hinweise (!) bewerten und beheben oder begründen.

### 5 Review 🛑 Haltepunkt 2

`bauen.py` und `durchklicken.py` laufen lassen. Gib der Lehrkraft:
- den Pfad zu `ausgabe/web/index.html` (im Browser öffnen; Entwürfe sind dort markiert),
- `ausgabe/pruefung/uebersicht.html` (alle Seiten auf einen Blick, Desktop und Handy),
- eine kurze Liste, was sie besonders prüfen sollte (unsichere Stellen, fehlende Screenshots, Quellen).

Hast du zu einzelnen Stellen Rückfragen, stell sie danach nacheinander, nicht als Block.

Änderungswünsche setzt du in der Quelle um und baust neu. **Nur die Lehrkraft gibt frei.** Sagt sie
„Modul X ist freigegeben“ (oder „alles“), setzt du `review: freigegeben`.

### 6 Ausgaben bauen

`alles.py <ordner>` (Moodle-Version aus `kurs.yaml`). Nur freigegebene Module kommen in den Moodle-Kurs.
Für einen Testkurs vorab geht `--entwuerfe` – dann ausdrücklich dazusagen, dass es kein Kurs für
Schüler:innen ist.

### 7 Durchklicken

`alles.py` klickt die Web-Version durch. Schau dir die Übersicht selbst an (Screenshots öffnen), behebe
Probleme und baue neu. Melde, was du nicht beheben konntest.

### 8 Übergabe

Erkläre der Lehrkraft in wenigen Schritten (Details: `referenzen/moodle.md` › Übergabe):
1. Leeren Moodle-Kurs anlegen lassen oder eigenen nehmen → **Mehr › Wiederverwendung › Wiederherstellen**
   → `ausgabe/moodle/<kurzname>_moodle5.mbz` hochladen → „In diesen Kurs, Inhalte hinzufügen“ → durchklicken.
2. Als Schüler:in testen („Rolle wechseln“ zeigt keine Abschlüsse – besser ein Testkonto).
3. Klappt Wiederherstellen nicht (Rechte): `ANLEITUNG_moodle5.md` beschreibt denselben Kurs zum Nachklicken.
4. Moodle-Tests aus `tests:` in kurs.yaml sind schon in der Kurssicherung – mit allen Fragen. Offene Fragen
   bewertet die Lehrkraft von Hand. Die Moodle-XML in `ausgabe/moodle/fragen/` ist nur noch für eigene
   Tests nötig (Fragensammlung › Import › Moodle-XML).

## Später: Korrekturen und Erweiterungen

- Immer in der Quelle ändern, dann neu bauen. Nie Dateien in `ausgabe/` bearbeiten.
- **Ein Modul korrigieren, Kurs läuft schon:** nur das Lernpaket austauschen – in Moodle beim Lernpaket
  › Einstellungen › Paketdatei die neue ZIP aus `ausgabe/moodle/lernpakete/` hochladen. Der Fortschritt
  der Schüler:innen bleibt, solange die Modul-ID gleich bleibt. Den Kurs nicht neu wiederherstellen
  (sonst doppelte Aktivitäten).
- **Neues Modul in laufendem Kurs:** Lernpaket einzeln anlegen (Einstellungen wie in der Klickanleitung),
  Voraussetzung setzen.
- IDs von Modulen, Stufen und Fragen nach der Freigabe nie ändern.

## Mit einem Coding-Agenten bauen (bewährt bei großen Pfaden)

Bei 15+ Modulen schreibt nicht der Agent selbst, sondern ein Coding-Agent (Skill `developer-workflow`) –
Hermes spezifiziert und prüft:

- **Spezifikation als Datei** in `docs/SPEC.md` (Quellen, Didaktik, technische Vorgaben, Arbeitsteilung,
  Abnahme), nicht als Chat-Text. Dazu `docs/GLIEDERUNG.md` mit Modul-IDs, Lernzielen, Minuten, Aufgaben.
- **Ein Kickoff pro Stufe** (`docs/KICKOFF-STUFE1.md` …): Quellen mit Dateipfaden, je Modul Inhalt,
  Aufgabenniveaus, Kurz-Check-Anforderungen, Abschluss „`pruefen.py` bis fehlerfrei". Danach `/clear` und der
  nächste Kickoff – 4–6 Module je Anlauf halten den Kontext frisch und die Qualität gleichmäßig.
- Der Agent liest den Baukasten über `~/.claude/skills/lernpfad-baukasten` (siehe `betrieb-hermes-server.md`).
- **Selbstberichte nachmessen:** `pruefen.py`, `bauen.py`, `durchklicken.py` selbst laufen lassen und die
  Aussagen zu Quellen und Zahlen stichprobenartig gegenlesen. Trägt man ihm im Kickoff auf, Unsicheres als
  `:::notiz Zu prüfen` zu markieren, statt zu behaupten, funktioniert das zuverlässig.

## Zeitkalkulation (vor der Freigabe)

- Modulminuten allein sagen nichts: **Aufgabenminuten aus den `:::aufgabe`-Blöcken addieren** und getrennt
  ausweisen (Basis = Pflicht, Plus = Differenzierung, Kreativ = freiwillig).
- Meilensteine realistisch ansetzen: ein 2–4-seitiges Dokument sind **150 min**, eine vollständige
  Schutzbedarfs-/Risikoanalyse **240 min** – nicht 60/90.
- **Duales System: keine Hausaufgaben.** Alles muss in der Schule passieren, der Pfad also ohne
  Hausarbeitsanteil in die vorgegebene Stundenzahl passen. Kalkulation: Modulminuten + Tests + Klausur +
  Feedbackrunden, geteilt durch 45.

## Material aus einem Vault übernehmen

Vor dem Kopieren ins Repo **auf personenbezogene Daten prüfen** – besonders Excalidraw-Ergebnisdateien aus
Unterrichtsstunden enthalten Namen von Schüler:innen (`grep -ril "<Name>"`) und Notenlisten. Nicht kopieren
und im Quellen-README begründen. Ist es schon committet: Dateien entfernen **und** die Historie neu aufsetzen
(orphan branch + force push), sonst bleiben die Daten in alten Commits.

## Regeln

- Nichts erfinden: keine Menüpfade, Tastenkürzel, Paragrafen, Zahlen ohne Beleg. Lieber als offen markieren.
- Keine personenbezogenen Daten, keine Namen von Schüler:innen, keine Kammer-Prüfungsaufgaben nachbauen,
  nur eigene oder frei lizenzierte Materialien (Quelle angeben).
- Keine externen Dienste zur Laufzeit: keine CDN-Schriften, keine eingebetteten Fremd-Skripte. Videos nur
  als Link auf offizielle Quellen (`medien.yaml`).
- Die Vorlage (`vorlage/`) nicht pro Kurs ändern. Farben kommen automatisch aus den Stufen.
- Sprache für Schüler:innen: du-Form, kurze Sätze, aktiv, konkrete Handlungsanweisungen, gendern mit Doppelpunkt.
