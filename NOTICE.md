# Herkunft und Lizenz

Dieses Paket ist eine **eigene Kopie** der Werkzeuge des **Lernpfad-Baukastens** von Dennis (GitHub: `dclausen01/lernpfad-baukasten`). Der Skill-Kopf des Originals nennt die Lizenz **MIT**; die Originaldatei liegt als `referenzen/skill-lernpfad-baukasten-original.md` bei. Die Werkzeuge in `skripte/` und `vorlage/` stammen daraus. Der Urheber bleibt genannt.

**Der Baukasten des Originals wird hier nicht verändert und nicht benötigt.** Dieses Paket enthält alles, was für die Fibu-Pfade gebraucht wird, inklusive der folgenden eigenen Erweiterungen:

- **Belege** (`beleg:` in Übungen und Testfragen): Rechnung, Gutschrift, Bonusabrechnung, Kontoauszug mit Parametern.
- **Moodle 4.5 mit Unterabschnitt-Plugin:** `moodle.unterabschnitte: einer | stufen | true`, `unterabschnitt_name`, `start: false`.
- **Baustein `:::hilfe <seite>`:** Seite als aufklappbarer Kasten im Modul.
- **Auswahlaufgaben** zeigen Buchungssätze als Tabelle Soll | an | Haben.
- **Lernpaket:** schließt den Kursindex von Moodle beim Start, Hilfsseiten oben in der Seitenleiste.
- **Neue Werkzeuge:** `buchungspruefung.py` (Rechnung und Wissensspeicher `buchungsmuster.yaml`), `selbsttest.py` (Browser-Automat), `neues_thema.py` (Vorlage `vorlage-thema/`).
- **Neue Anleitungen:** SKILL.md, ERKENNTNISSE.md, BUCHUNGSWISSEN.md, FOERDERBEREICH.md, MATERIAL-CHECKLISTE.md, STARTPROMPT.md.

**Hinweis zum Stand:** Während der Entwicklung des Beschaffungs-Pfads wurden die ersten Erweiterungen (Belege, Moodle-4.5-Unterabschnitte, Hilfen) auf einen Zweig `claude/ecstatic-lovelace-lilfd1` im Repository `dclausen01/lernpfad-baukasten` hochgeladen. Der Hauptzweig dort ist unverändert. Mit diesem Paket ist das Original nicht mehr nötig; der Zweig kann dort gelöscht werden.

Bei Weitergabe des Pakets: Lizenzhinweis des Originals beibehalten.
