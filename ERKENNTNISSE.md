# Erkenntnisse aus den bisherigen Fibu-Pfaden

Zusammengeführt aus „Umsatzsteuer prüfen“ (06.11.2026) und „Buchungen im Beschaffungsprozess“ (09.11.2026). Lies das **vor dem Interview** zu einem neuen Thema und ergänze es **nach** jedem Thema.

## 1 Zusammenarbeit mit der Lehrkraft

- **Sprache:** Deutsch mit Umlauten und korrekter Rechtschreibung. Schüler:innen duzen (Gruppenarbeit: „ihr“). Dateien für Lehrkräfte als **DOCX/XLSX** (ONLYOFFICE, die Schule stellt darauf um).
- **Erst fragen, dann bauen.** Material anfordern, lesen, **eine Frage pro Nachricht mit Vorschlag**, Gliederung vorlegen, auf Zusage warten. Sagt die Lehrkraft „wir diskutieren nur“ oder „prüfe erst und antworte, bevor du umbaust“, wird **nichts** gebaut.
- **Lösungen anfordern.** Aufgabenblätter ohne Lösungen reichen nicht. Die Lösungsvorschläge der Lehrkraft machen aus „vermutlich richtig“ „belegt“. Ohne Lösung offen sagen: „nicht bestätigt“.
- **Ehrlich berichten:** Was geprüft ist, was nicht (zum Beispiel nicht im echten Moodle getestet). Fehler sofort zugeben, auch eigene (ein YAML-Fehler im Repository wurde sofort korrigiert).
- **Wünsche vollständig abarbeiten** und danach kurz sagen, was umgesetzt ist und was bewusst nicht. Nichts stillschweigend ändern.
- **Freigabe** (`review: freigegeben`) nur auf ausdrückliche Aussage („alles freigegeben“). Danach neu bauen ohne `--entwuerfe`.
- **Was Gegenstand ist, bestimmt die Lehrkraft.** Beispiel: HGB § 255 gehört in eine andere Lernsituation und wird nicht abgefragt, UStG § 17 ist Hintergrund für die Vorsteuer-Korrekturen. Rechtsgrundlagen stehen in `quellen.yaml` nur als Nachweis.
- **Eigene Beispiele und Zahlen**, nie Schulbuchaufgaben nachbauen. Beispielfirma: **Wiesengrund Küchenmöbel GmbH** (nur Name und Produkte sind festgelegt, die übrigen Angaben der Seite „Unternehmen“ sind frei erfunden und müssen angepasst werden, wenn das Unterrichts-Modellunternehmen anders aussieht).
- **Fremde Repositories nicht verändern.** Der Baukasten von `dclausen01` bleibt unberührt; dieses Paket ist eine eigene Kopie (siehe NOTICE.md).

## 2 Didaktik

### Zwei Stufen

- **🌱 Schritt für Schritt** (Förderbereich, siehe FOERDERBEREICH.md) und **🎯 Überprüfung** mit Abschlusstest. Beide sofort frei.
- Überprüfung = **Check-Pfad**: Die Schüler:innen haben das Thema schon erarbeitet. Keine neuen Lerntexte, sondern Aufgaben. 3 bis 4 Module plus Abschlusstest. Stark reduzieren, wenn die Lehrkraft es sagt.

### Aufgaben

- **Belege als echte Belege** (`beleg:`: Rechnung, Gutschrift, Bonusabrechnung, Kontoauszug), nicht als Textaufgabe. Mit Parametern, damit die Parallelaufgabe andere Zahlen hat.
- **Jede Buchungsaufgabe nennt die Technik** (aufwands- oder bestandsorientiert), wenn das Thema beides kennt. Schwerpunkt: das, was die Prüfung verlangt.
- **Aufgabenarten** nach den prüfungsnahen Aufgaben der Lehrkraft: Buchungssatz bilden, Konten ankreuzen (Auswahl mit Tabelle Soll | an | Haben), Sachverhalt beurteilen (Multiple Choice), Beträge berechnen, T-Konten abschließen.
- **Steuerart-Frage** („Umsatzsteuer oder Vorsteuer?“) gibt es nicht mehr. **Zahllast** nur **gelegentlich**, **Erfolg** in ausgewählten Aufgaben. Im Förderbereich gar nicht.
- **Variation:** Gleiche Fälle mit verschiedenen Belegen (Fracht, Transport, Verpackung, Montage). Besonderheiten wie „nicht skontierbar“ in 1 bis 2 Aufgaben aufnehmen.
- **Interaktiv:** Tipps nur auf Klick und gestuft, zwei Versuche, falsche Felder rot, Lösung mit Rechenweg, Parallelaufgabe. Nicht nur „Lösung per Klick“.
- **Hilfen im Modul, nicht am Rand:** `:::hilfe <seite>` bettet Unternehmen, Kontenübersicht und Schemata als aufklappbare Kästen vor der ersten Aufgabe ein. Die Seitenleiste von Moodle ist lang und wird nicht gefunden.
- **Kurz-Check** mit 3 bis 4 Fragen je Modul, falsche Antworten sind typische Fehlvorstellungen. Beim Bauen werden die Antworten gemischt.
- **Abschlusstest** in beiden Welten (Moodle-Test aus `fragen/` und Web-Seite): 12 bis 17 Fragen, 20 Punkte, eine offene Frage zur Handbewertung.
- **Kontenplan der Lehrkraft** in `kurs.yaml` (`kontenplan:`, Nummern **in Anführungszeichen**). Ergänzungen aus der Übersicht der Lehrkraft einarbeiten.
- **Prüfungsaufgaben** der Lehrkraft nur als Stilvorlage. Keine Kammeraufgaben nachbauen.

## 3 Technik

- **YAML-Fallen:** Texte mit „: “ in Anführungszeichen (auch Titel!), Kommas in `{…}` quoten, Kontonummern wie `0700` immer als `"0700"`, in Übungen Platzhalter als `{{n}}` (doppelte Klammern), **Werte mit `{{` immer in Anführungszeichen**. `sed` auf Platzhalter kann `{{n}}` zu `{{{n}}}` machen. Danach immer `pruefen.py`.
- **Zahlenraster:** Prozent und Umsatzsteuer führen leicht zu drei Nachkommastellen. Zahlen auf passende Raster legen (zum Beispiel Vielfache von 500). `buchungspruefung.py` testet das mit vielen Zufallszahlen.
- **Belege (`beleg:`):** Felder siehe `referenzen/bausteine.md`. Keine Schlüssel `betrag` oder `antwort` im Beleg (sie werden als Formel gelesen). Beleg-Inhalt in Anführungszeichen.
- **Moodle-Test:** Der Beleg steht mit Inline-Stilen hinter dem Fragetext (feste Zahlen). Buchungssätze in einer Zeile (`4400 … an 2800 …`) werden zur Tabelle Soll | an | Haben, sobald die Konten vierstellig sind.
- **Prüfen vor jedem Bau:** `pruefen.py` (Inhalt), `buchungspruefung.py` (Rechnung und Muster), dann `alles.py`. Ausgabe in `ausgabe/` nie von Hand ändern.
- **Browser-Test** mit Playwright (Node): `skripte/selbsttest/` lässt einen Automaten alle lösbaren Aufgaben mit der Musterlösung ausfüllen. Das fängt Fehler, die die Rechnung nicht sieht.
- **Kursindex von Moodle:** Das Lernpaket schließt ihn beim Start (mehr Platz für Belege).

## 4 Moodle am BBZ

Siehe `referenzen/moodle-bbz.md`. Kurz:

- Moodle **4.5.12**, Unterabschnitt als **Plugin** (Eintrag „Unterabschnitt“ im Plus-Menü). Das Wiederherstellen aus der Sicherung legt Unterabschnitte richtig an.
- `moodle: {version: 4, unterabschnitte: stufen, unterabschnitt_name: …, start: false}`: ein Abschnitt, je Stufe ein Unterabschnitt.
- **Kurs-IDs sind am BBZ nicht sichtbar.** Darum **keine Abschnittsnummer** verwenden: Sicherung wiederherstellen, Unterabschnitt verschieben, leeren Unterabschnitt löschen. **Vorher den Kurs sichern.**
- Wiederherstellen nur **einmal**. Spätere Änderungen: nur die **Lernpakete (ZIP) austauschen**, nie neu wiederherstellen.

## 5 Quellen und Recht

- Jede Fachaussage in `quellen.yaml`. Status `verifiziert` nur, wenn Lösungsvorschläge, Buch oder amtlicher Text es belegen. Websuche bestätigt nur sekundär: Status bleibt „zu_pruefen“.
- Das Netzwerk der Arbeitsumgebung kann amtliche Seiten (zum Beispiel gesetze-im-internet.de) sperren. Dann ehrlich sagen und die Lehrkraft bitten, nachzulesen.
- Steuersätze, Fristen, Grenzen vor Wiederverwendung neu prüfen (Stand 2026: 19 % und 7 %, Kleinunternehmer 25.000 € und 100.000 €, Jahreserklärung bis 31. Juli, Voranmeldung bis zum 10., Kleinbetragsrechnung bis 250 €).

## 6 Ablauf (Kurzfassung, Details in SKILL.md)

1. Material anfordern (MATERIAL-CHECKLISTE.md), lesen, zusammenfassen.
2. Buchungswissen prüfen: Welche Muster sind gesichert, welche neu?
3. Interview (eine Frage pro Nachricht), Gliederung vorlegen, Zusage abwarten.
4. `neues_thema.py`, Module (Förder- und Überprüfungsstufe), Test, Quellen.
5. Prüfen, bauen, im Browser durchspielen.
6. Lehrkraft testet, Änderungen, Freigabe auf Ansage.
7. Moodle: Testkurs, echter Kurs, Lernpakete austauschen.
8. Wissen sichern: `buchungsmuster.yaml`, BUCHUNGSWISSEN.md (Lernprotokoll), ERKENNTNISSE.md ergänzen.
