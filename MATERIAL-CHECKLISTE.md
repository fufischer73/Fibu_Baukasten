# Material-Checkliste: Was Claude vor einem neuen Übungspfad braucht

Bevor ein neuer Übungspfad entsteht, bitte dieses Material bereitstellen (im Chat hochladen oder im Repository ablegen). **Je mehr davon vorliegt, desto weniger muss Claude raten und desto weniger muss später korrigiert werden.** Beim Beschaffungs-Pfad hat sich gezeigt: Die **Lösungen** waren das Wichtigste, denn erst sie belegen, dass die Buchungssätze stimmen.

Nicht alles ist Pflicht. Die Spalte „Pflicht“ sagt, ohne was Claude **nicht** startet.

| Nr. | Material | Pflicht? | Wofür Claude es braucht |
| --- | --- | --- | --- |
| 1 | **Kannliste** oder Lernziele zum Themengebiet (Lehrplan, Lernfeld, Kompetenzen) | ja | Legt fest, was am Ende können soll. Daraus entstehen Module und Testfragen. |
| 2 | **Lehrbuchseiten** zum Thema (PDF oder gut lesbare Fotos, alle Seiten des Kapitels) | ja | Fachliche Grundlage und Begriffe, die die Schüler:innen schon kennen. Die Aufgaben im Pfad werden eigene Aufgaben, das Buch dient als Maßstab. |
| 3 | **Lernsituationen und Arbeitsblätter** (Aufgabenblätter, die im Unterricht gemacht wurden) | ja | Zeigt, welche Geschäftsfälle und Aufgabenarten schon vorkommen, und womit die Schüler:innen vertraut sind. |
| 4 | **Lösungen** zu den Lernsituationen, Arbeitsblättern und Aufgaben (Lösungsvorschläge des Verlags oder eigene) | ja | Belegt die richtigen Buchungssätze und Beträge. **Ohne Lösungen markiert Claude alle Buchungssätze als „nicht bestätigt“.** |
| 5 | **Prüfungsnahe Aufgaben** (alte Klassenarbeiten, Kammer- oder Abschlussprüfungsaufgaben, Probearbeiten), möglichst mit Lösungen | ja | Zeigt, wie abgefragt wird (Konten ankreuzen, Sachverhalt beurteilen, Beträge berechnen). Wird nicht nachgebaut, nur als Stilvorlage genutzt. |
| 6 | **Kontenplan / Kontenübersicht**, wie er im Unterricht gilt (auch Ergänzungen für das Thema) | ja | Alle Kontonummern und -bezeichnungen im Pfad stammen von hier. |
| 7 | **Hinweise zum Thema**: Was ist Gegenstand, was **nicht**? (zum Beispiel „HGB § 255 gehört in eine andere Lernsituation“) | ja | Vermeidet Aufgaben, die nicht zum Unterricht gehören. |
| 8 | **Broschüre, Skript, Folien oder Merkblätter** der Lehrkraft, falls vorhanden | nein | Formulierungen und Eselsbrücken der Lehrkraft werden übernommen. |
| 9 | **Hilfsmittel, die ihr im Unterricht nutzt** (Schemata, Tabellen, Merkzettel; zum Beispiel das Skonto-Schema) | nein | Kommen als Hilfsseite oder Hilfsblatt in den Pfad. |
| 10 | **Modellunternehmen**, falls es eines gibt (Beschreibung, Produkte, Konten) | nein | Standard ist die Wiesengrund Küchenmöbel GmbH. Andere Firma nur auf Wunsch. |
| 11 | **Hinweise zu schwachen Schüler:innen**: Welche Schritte fallen schwer? Wo scheitern sie meistens? | nein, aber hilfreich | Daraus entsteht die Stufe „Schritt für Schritt“ (siehe FOERDERBEREICH.md). |
| 12 | **Rahmen**: Unterrichtsstunden, Klasse/Bildungsgang, Vorwissen, Zeitpunkt (vor der Klassenarbeit?) | ja | Bestimmt den Umfang (Module und Minuten). |
| 13 | **Moodle**: Zielkurs, Abschnitt oder Unterabschnitt, in den der Pfad kommt; Testkurs vorhanden? | später | Wird erst vor der Übergabe geklärt, siehe `referenzen/moodle-bbz.md`. |

## So gibst du das Material weiter

- **Im Chat hochladen:** PDFs, Word-Dateien (DOCX) und Bilder können direkt in den Chat gezogen werden.
- **Lösungen getrennt kennzeichnen:** zum Beispiel Dateiname „LS52_Loesungen.pdf“.
- **Urheberrecht:** Lehrbuchseiten dienen nur der Vorbereitung. Im Pfad stehen **eigene** Aufgaben, Belege und Zahlen, keine Seiten oder Aufgaben aus dem Buch.
- **Keine Namen von Schüler:innen** und keine Notenlisten hochladen.

## Was Claude danach tut

1. Liest alles (auch Bilder und Tabellen) und fasst kurz zusammen, was er verstanden hat.
2. Prüft, **welche Buchungssätze durch Lösungen belegt sind** und welche nicht (Wissensspeicher `buchungsmuster.yaml`).
3. Fragt, was noch fehlt, **eine Frage pro Nachricht** mit Vorschlag.
4. Legt eine **Gliederung** vor (Module, Minuten, Aufgabenarten, Förderstufe, Test).
5. **Baut erst nach deiner Zusage.**
