# Förderbereich: „Schritt für Schritt“ für schwache Schüler:innen

Manche Schüler:innen verstehen Buchungen nur in sehr kleinen Schritten. Für sie gibt es in **jedem Pfad eine eigene Stufe** vor der Überprüfung: **🌱 Schritt für Schritt**. Sie ist kein Strafraum, sondern ein Angebot. Beide Stufen sind sofort frei (`freischaltung: offen`), niemand wird eingestuft. Die Einleitung sagt: „Fällt dir das Thema schwer? Beginne hier. Fühlst du dich sicher? Geh direkt zur Überprüfung.“

## Warum eine eigene Stufe?

Die Überprüfung ist für Schüler:innen gedacht, die das Thema schon können. Wer noch nicht sicher ist, braucht
- **kleinere Schritte** (nicht „buche die Rechnung“, sondern vier Teilaufgaben),
- ein **Beispiel zum Mitgehen**, bevor die eigene Aufgabe kommt,
- **weniger Auswahl** (4 statt 12 Konten),
- **mehr Hilfe** (drei Tipps statt zwei, ein Merkzettel, Erklärungen in einfacher Sprache) und
- **keinen Druck** (keine Zeitgrenze, unbegrenzte Versuche, kein Notenbezug).

## Der feste Ablauf in jedem Förder-Modul

Immer die gleichen **vier Schritte**. Sie stehen auf dem Merkzettel und in jedem Förder-Modul:

1. **Beleg lesen:** Wer kauft, wer verkauft? Was? Welche Beträge?
2. **Was ist passiert?** Welche Konten sind betroffen?
3. **Soll oder Haben?** Links oder rechts?
4. **Beträge eintragen** und prüfen: Soll gleich Haben.

## Aufbau eines Förder-Moduls (Vorlage: `vorlage-thema/module/f1.md`)

| Teil | Inhalt | Baustein |
| --- | --- | --- |
| Kopf | 3 bis 4 einfache Lernziele („Ich kann …“), Kurz-Check mit 3 sehr leichten Fragen | `lernziele`, `kurzcheck` |
| **So gehst du immer vor** | die vier Schritte | `:::schritte` |
| **Hilfen zum Aufklappen** | Merkzettel, Kontenübersicht | `:::hilfe merkzettel`, `:::hilfe kontenuebersicht` |
| **1. Gemeinsam** | **ein** Beleg, **vier Teilaufgaben**: (1) Was ist passiert? (`auswahl`), (2) Welche Konten, Soll oder Haben? (`zuordnung`), (3) Beträge ausrechnen (`rechnen`), (4) Buchungssatz bilden (`buchung` mit wenigen Konten, dreistufigen Tipps) | `:::uebung` mit `beleg:` |
| **2. Jetzt du** | ein ähnlicher Fall mit anderen Zahlen und Parallelaufgabe, noch mit reduzierter Kontenauswahl | `:::uebung` mit `parameter:` |
| **3. Mein Merkzettel** | Checkliste „Das kann ich jetzt“, Hinweis auf die Überprüfung | `:::checkliste` |

## Regeln für Autor:innen

- **Ein Fall pro Förder-Modul**, nicht mehrere Themen.
- **Feste Zahlen in den Teilaufgaben**, damit Schritt 1 bis 4 zusammenpassen. Erst im Teil „Jetzt du“ gibt es `parameter:`.
- **Kontenauswahl klein:** 4 bis 6 Konten (richtige plus 1 bis 2 Ablenker). In der Überprüfung dagegen 8 bis 12.
- **Tipps dreistufig:** 1. Was ist zu tun? 2. Welche Konten, welcher Betrag? 3. Fast die Lösung.
- **Einfache Sprache:** kurze Sätze, Alltagsbilder, Fachwörter erklären („Forderung = der Kunde schuldet uns Geld“).
- **Keine neuen Techniken mischen:** Aufwands- und bestandsorientiert nicht im gleichen Förder-Modul.
- **Keine Zahllast-, Erfolgs- oder Steuerart-Fragen** im Förderbereich. Erst in der Überprüfung, und auch dort nur gelegentlich.
- **Das Skonto-Schema** (und ähnliche Schemata der Lehrkraft) kommt als `:::hilfe` in die Förder-Module, wenn das Thema es braucht (Bibliothek: `bibliothek/`).
- **Übergang:** Am Ende steht immer „Du bist sicher? Geh zur Überprüfung.“

## Wie viel?

Pro Pfad **1 bis 3 Förder-Module** (je 30 bis 40 Minuten): eines je Hauptfall (zum Beispiel Einkauf, Gutschrift, Zahlung). Mehr nicht, sonst wird die Stufe zum zweiten Pfad.

## In Moodle

Die Stufe erscheint als eigener Unterabschnitt neben der Überprüfung (`unterabschnitte: stufen`). Aktivitätsabschluss ist freiwillig. Der Abschlusstest gehört zur Überprüfung, nicht zur Förderstufe.

## Was noch kommen könnte (nicht gebaut)

- Eine Übungsart, bei der ein Teil des Buchungssatzes **vorgegeben** ist (nur die Haben-Seite ausfüllen). Bisher lässt sich das mit kleinen Teilaufgaben nachbilden.
- Eine kurze Wiederholung der Grundlagen (aktive/passive Konten, Soll und Haben) als eigener Förder-Baustein für alle Themen. Der Merkzettel (`seiten/merkzettel.md`) deckt das schon in Kurzform ab.
