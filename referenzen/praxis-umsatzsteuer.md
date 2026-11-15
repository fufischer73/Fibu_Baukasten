# Praxis: Übungspfad „Umsatzsteuer prüfen“ (Industriekaufleute, BBZ)

Erfahrungen aus dem ersten fertigen Übungs- und Überprüfungspfad. Lies das **vor dem Interview**, wenn ein weiterer Übungspfad für diese Lehrkraft entsteht.
Das Beispiel liegt im Repository `Umsatzsteuer-` (kurs.yaml, module/, fragen/, seiten/).

## 1 Arbeitsweise mit dieser Lehrkraft

- Sprache: Deutsch mit Umlauten und korrekter Rechtschreibung. Dateien für Lehrkräfte als **DOCX/XLSX** (ONLYOFFICE). Schüler:innen duzen (Gruppenarbeit: „ihr“).
- **Erst fragen, dann bauen.** Bei größeren Vorhaben zuerst Gliederung/Rückfragen mit Vorschlägen, Zusage abwarten. Sagt die Lehrkraft „wir diskutieren nur“, wird nichts gebaut.
- Wünsche der Lehrkraft vollständig abarbeiten und danach kurz bestätigen, was umgesetzt ist und was bewusst nicht. Nichts stillschweigend ändern.
- Eigene Beispiele und Zahlen, nie Schulbuchaufgaben nachbauen. Beispielfirma erfinden (hier: Wiesengrund Küchenmöbel GmbH).
- Die Lehrkraft testet selbst durch und meldet Änderungen. Danach neu bauen, testen, pushen, Downloads aktualisieren.
- Freigabe (`review: freigegeben`) nur auf ausdrückliche Aussage („es ist freigegeben“).

## 2 Didaktik, die sich bewährt hat

- **Check-Pfad statt Lernpfad:** Die Schüler:innen haben das Thema schon erarbeitet. Keine neuen Lerntexte, sondern Überprüfung: 3 kurze Module (Verstehen, Berechnen, Buchen) plus Abschlusstest. Stark reduzieren, wenn die Lehrkraft „deutlich reduzieren“ sagt.
- **Aufgaben klassenarbeitsnah:** Berechnungen, Buchungssätze, **Auswirkung auf bestehende Zahllast und Erfolg**, Steuerart (Umsatzsteuer oder Vorsteuer), Abschluss der Konten (Verrechnung, Zahllast passivieren, Überhang aktivieren).
- **Interaktiv zum Selbstkontrollieren** (`:::uebung`): Tipps nur auf Klick und gestuft (Ansatz, halber Rechenweg), zwei Versuche, falsche Felder rot markiert, Hinweis ohne Lösung, danach Lösung mit Rechenweg, danach **Parallelaufgabe mit anderen Zahlen** (`parameter:`, Formeln). Nicht nur „Lösung per Klick“.
- Buchungssätze: Konten aus Liste (inkl. Ablenker, Umsatzsteuer- und Vorsteuerkonto immer dabei) plus Betrag. Lösung und Testantworten als **Tabelle Soll | an | Haben**.
- Lückentext: je Lücke 3 Optionen, falsche Optionen möglichst als **Gegenstück** der richtigen (Steuerträger/Steuerschuldner, Forderung/Verbindlichkeit).
- Kurz-Check: Antworten werden beim Bauen gemischt (die richtige Antwort stand anfangs immer an Position 1!).
- Abschlusstest in **beiden** Welten: Moodle-Test aus `fragen/` und automatisch erzeugte Web-Seite (ein Versuch, Zwischenstand). Offene Fragen bewertet die Lehrkraft.
- Kontenplan der Lehrkraft verwenden (`kontenplan:` in kurs.yaml, Nummern **in Anführungszeichen**), nicht den eigenen.
- Zwischenstand als Datei sichern/laden nur in der Web-Version (Moodle speichert selbst).
- Escape-/Breakout-Idee: gebaut und getestet (Räume, Schlösser, Tresor), von der Lehrkraft für den Unterricht wieder entfernt. Wiederherstellbar aus Commit `1e96d96` im Repository `Umsatzsteuer-`.

## 3 Technische Stolpersteine

- YAML: Texte mit „: “ oder Kommas in `{…}` in Anführungszeichen; Kontonummern wie `0700` **immer quoten** (sonst Oktalzahl); in `:::uebung` Platzhalter als `{{n}}` (doppelte Klammern!). Einfache Klammern ließen in einer Zufallsfrage die Zahlen im Moodle-Test weg.
- Zahlen in Parametern so wählen, dass Ergebnisse höchstens zwei Nachkommastellen haben (pruefen.py meldet es).
- `hidden` an Knöpfen braucht `display: none !important`, sonst bleiben sie sichtbar.
- Browser-Tests mit Playwright (vorinstalliert) lohnen sich: Durchspielen aller Übungsarten, Neuladen, Datei speichern/laden.
- Eigene Prüfskripte (`pruefen.py`) vor jedem Bauen; Ausgabe nie von Hand ändern.

## 4 Moodle an dieser Schule (BBZ)

- Moodle **4.5.12**, Unterabschnitte über ein **Plugin**. In kurs.yaml: `moodle: {version: 4, anordnung: true}` (Reihenfolge-Frage ist ab 4.4 im Standard). Kein Moodle 5, keine H5P-Kurz-Checks.
- Wiederherstellen: „Inhalte zu diesem Kurs hinzufügen“, **zuerst im Testkurs**, nur **einmal**. Spätere Änderungen: nur das Lernpaket (SCORM-Datei) austauschen.
- `moodle.abschnitt: N` zielt auf eine Abschnittsnummer im Zielkurs. Beim ersten Versuch stimmte **43 nicht** (der Kurs hatte weniger Abschnitte; es entstanden leere Zusatzabschnitte). Die richtige Nummer vorher ermitteln: `…/course/view.php?id=KURS-ID&section=N` mit wechselndem N, bis der Zielabschnitt erscheint; im Testkurs prüfen. Der Kurs nutzt „ein Abschnitt pro Seite“ (Links `course/section.php?id=…` enthalten nur die interne ID, nicht die Nummer).
- Dateien der Lehrkraft liegen im Ordner `download/` des Themen-Repositorys (GitHub-Download), nicht im Chat.

## 5 Inhalt und Recht (Umsatzsteuer; vor Wiederverwendung neu prüfen)

- Steuersätze 19 %/7 %; Speisen in der Gastronomie ab 01.01.2026 7 %; Kleinunternehmer-Grenzen seit 2025: 25.000 € Vorjahr, 100.000 € laufendes Jahr; E-Rechnung: Empfang seit 2025, Ausstellen 2027 (über 800.000 € Vorjahresumsatz) bzw. 2028 (alle). Jahreserklärung regulär bis **31. Juli** des Folgejahres (nicht 31. Mai). Voranmeldung und Zahllast bis zum 10. des Folgemonats. Kleinbetragsrechnung bis 250 €.
- Wortwahl: Statt „Forderung/Verbindlichkeit gegenüber dem Finanzamt“ in Klassifizierungsfragen lieber **„erhöht/vermindert die Zahllast“**.
- Quellen sind in `quellen.yaml` noch als „zu prüfen“ markiert (Gesetz, Kontenrahmen): nicht als verifiziert ausgeben.

## 6 Ablauf für das nächste Thema

1. Material der Lehrkraft lesen (PDF als Bild, Arbeitsblätter, Kontenplan, eigene Broschüre); Rechtslage und Inhalt prüfen.
2. Rückfragen mit Vorschlägen stellen (Plattform, Umfang, Pfadform, Aufgabenstil, Kontenplan, Firma/Branche). Zusage abwarten.
3. Gliederung vorlegen (Module, Zeit, Tests), danach bauen: `neu.py`, Module mit `:::uebung`, `fragen/`, Kontenplan, Quellen.
4. `pruefen.py`, `alles.py --entwuerfe`, Browser-Test, Screenshots ansehen, Fehler beheben.
5. Lehrkraft testet; Änderungen einarbeiten; dann Freigabe und Bau ohne `--entwuerfe`.
6. Moodle: Testkurs, Zielabschnitt klären, wiederherstellen, Lehrkraft meldet Ergebnis. Downloads und Quelle im Repository ablegen und pushen.

## 7 Startprompt für einen neuen Chat

> Wir bauen einen weiteren Übungs- und Überprüfungspfad für Industriekaufleute zum Thema **<THEMA>**. Nutze den Skill `lernpfad-baukasten` (Repository `lernpfad-baukasten`, Branch `ccr-443b4e90-z3q3y7`) und lies zuerst `referenzen/praxis-umsatzsteuer.md`. Das fertige Beispiel liegt im Repository `Umsatzsteuer-`. Frage zuerst, was du wissen musst, und beginne erst nach meiner Zusage mit dem Bauen. Material: <PDF/Dateien hochladen>.

## 8 Nächstes Thema: Buchungen im Beschaffungsprozess (Vorbereitung)

Die Lehrkraft will als Nächstes einen entsprechenden Übungspfad zu **Buchungen im Beschaffungsprozess** (Industriekaufleute). Noch kein Material, noch keine Absprachen. Die folgenden Punkte sind meine Vermutungen, **nicht** Vorgaben – im Interview klären.

**Wahrscheinlich nötige Geschäftsfälle** (mit Lehrkraft abstimmen): Wareneingang und Eingangsrechnung (Vorsteuer, Konto 4400), Bezugskosten (Fracht, Verpackung), Rücksendung/Gutschrift, Preisnachlässe (Rabatt, Bonus), Skonto (Lieferantenskonto, Korrektur der Vorsteuer), Zahlung per Bank, Anlagenbeschaffung, Materialaufwand **aufwandsorientiert** (Konten 6000/6010/…) oder **bestandsorientiert** (2000/2010/…), Inventur und Bestandsveränderung.

**Rückfragen für das Interview** (jeweils mit Vorschlag): Welche Fälle gehören zur Klassenarbeit? Aufwands- oder bestandsorientiert (bisher beim Umsatzsteuer-Pfad: aufwandsorientiert)? Welche Skonto-Methode wird unterrichtet (Brutto- oder Nettomethode)? Wird Rabatt gebucht oder nur gerechnet? Kontenplan wie beim Umsatzsteuer-Pfad (Auszug der Lehrkraft)? Welches Material gibt es (Buchseiten, Arbeitsblätter, eigene Broschüre)? Wie viele Module und welche Zeit? Beispielfirma weiter **Wiesengrund Küchenmöbel GmbH**? Gleiche Plattform (Moodle 4.5.12, Web-Version), gleicher Zielkurs? Zielabschnitt: Nummer vorher klären (siehe Abschnitt 4).

**Wiederverwendbar aus dem Umsatzsteuer-Pfad:** `:::uebung` mit `buchung` (mehrere Soll- und Haben-Zeilen), `rechnen` mit Parametern (Skonto, Rabatt, Bezugskosten), Buchungssatz-Tabellen in Antworten, Abschlusstest in Web und Moodle, Kontenplan-Mechanik, Zwischenstand (Web), Zielabschnitt `moodle.abschnitt`. Auswirkung auf Zahllast/Erfolg lässt sich um „Auswirkung auf Verbindlichkeiten/Bestand/Erfolg“ erweitern.

**Fachlich zu prüfen** (Quellen in `quellen.yaml`, Status „zu_pruefen“, nicht erfinden): Skonto und Umsatzsteuerkorrektur, Behandlung von Bezugskosten und Nachlässen, Kontenbezeichnungen und -nummern nach dem Kontenplan der Lehrkraft.

**Anforderungen der Lehrkraft für den nächsten Pfad** (aus dem Chat zum Umsatzsteuer-Pfad):
- Aufbau wie beim Umsatzsteuer-Pfad (Module mit Kurz-Check und Übungen, Abschlusstest am Ende, Web-Version und Moodle).
- **Viel interaktiv**, vor allem **Buchungssätze bilden** (Konten wählen, Beträge eintragen, Tabelle Soll | an | Haben).
- **Ein Abschnitt mit Unterabschnitten** in Moodle. Achtung: Der Baukasten baut Unterabschnitte bisher nur im Moodle-5-Stil (`mod_subsection`). Das BBZ-Moodle ist 4.5.12 mit einem **Plugin** für Unterabschnitte. **Offen:** Name und Version des Plugins klären und in einem Testkurs prüfen, ob eine Sicherung im Plugin-Stil nötig ist oder ob die Unterabschnitte nach dem Wiederherstellen von Hand angelegt werden.
- Das Muster soll für **weitere Themen der Finanzbuchhaltung** taugen: Kontenplan, Übungsarten, Test und Moodle-Einstellungen bleiben gleich, nur Inhalte und Fragen wechseln.
