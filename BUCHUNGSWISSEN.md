# Buchungswissen des Fibu-Baukastens

Hier steht, was der Baukasten über Buchungstechnik **sicher** weiß, und wie er **immer besser** wird. Die maschinenlesbare Fassung ist `buchungsmuster.yaml`. `skripte/buchungspruefung.py` vergleicht jeden Buchungssatz eines Pfads damit.

## So lernt der Baukasten dazu

1. **Vor dem Bauen:** `buchungsmuster.yaml` und diese Datei lesen. Was dort `verifiziert` steht, gilt als gesichert.
2. **Beim Bauen:** Für jeden neuen Buchungssatz Lösungsvorschläge der Lehrkraft suchen. Ohne Lösung bleibt er „neu“.
3. **Prüfen:** `python3 skripte/buchungspruefung.py <ordner>`. Das Skript
   - rechnet jede Aufgabe mit vielen Zufallszahlen durch (Soll gleich Haben, höchstens zwei Nachkommastellen, nie null oder negativ),
   - prüft die richtigen Testantworten,
   - meldet **NEUE Muster**, die noch nicht in `buchungsmuster.yaml` stehen.
4. **Neue Muster eintragen:** `--lernen` schreibt sie mit `status: neu` in die Musterdatei.
5. **Bestätigen lassen:** Die Lehrkraft bestätigt anhand von Lösungsvorschlag, Buch oder Klassenarbeit. Dann setzt Claude `status: verifiziert` und trägt Name, Technik und Quelle ein.
6. **Nach dem Thema:** Neue Erkenntnisse in den Abschnitt „Lernprotokoll“ unten schreiben (Fehler, die aufgefallen sind, Regeln, Besonderheiten der Lehrkraft).

Das Ziel: **Was einmal geprüft ist, wird nie wieder angezweifelt. Was neu ist, fällt sofort auf.**

## Regeln, die sich bewährt haben

### Grundmuster

| Merke | Regel |
| --- | --- |
| Soll gleich Haben | Jeder Buchungssatz geht auf. Die Probe steht in jeder Lösung. |
| Verbindlichkeit 4400 | Immer **brutto**. Einkauf: Haben. Gutschrift, Zahlung: Soll. |
| Vorsteuer 2600 | Einkauf: **Soll**. Gutschrift, Skonto: **Haben** (Berichtigung). |
| Umsatzsteuer 4800 | Verkauf: **Haben**. |
| Forderung 2400 | Verkauf: Soll (brutto). Zahlungseingang: Haben. |
| Rabatt in der Rechnung (Sofortrabatt) | Wird **nicht gebucht**. Gebucht wird der Nettobetrag danach. |
| Gutschrift | Ändert immer auch die Vorsteuer. Rücksendung: Menge und Wert sinken. Mängelrüge, Bonus: nur der Wert. |
| Skonto (Nettomethode) | Skonto **netto** auf das Nachlasskonto, Umsatzsteuer darauf als Vorsteuer-Berichtigung (Haben 2600). Bank bekommt Brutto minus Skonto brutto. |
| „Nicht skontierbar“ | Fracht, Transport, Verpackung, Montage stehen in der Rechnung, aber der Skonto gilt nur für den Warenwert, wenn der Beleg es sagt. |

### Werkstoffe: aufwands- und bestandsorientiert (Werkstoffkonten mit Unterkonten)

| Vorgang | bestandsorientiert | aufwandsorientiert |
| --- | --- | --- |
| Anfangsbestand | 2000 an 8000 | 2000 an 8000 |
| Einkauf | 2000, 2600 an 4400 | 6000, 2600 an 4400 |
| mit Bezugskosten | 2000, 2001, 2600 an 4400 | 6000, 6001, 2600 an 4400 |
| Bezugskosten einzeln | 2001, 2600 an 4400 | 6001, 2600 an 4400 |
| Rücksendung (Gutschrift) | 4400 an 2000, 2600 | 4400 an 6000, 2600 |
| Mängelrüge, Bonus | 4400 an 2002, 2600 | 4400 an 6002, 2600 |
| Zahlung mit Skonto | 4400 an 2800, 2002, 2600 | 4400 an 2800, 6002, 2600 |
| Umbuchung Bezugskosten | 2000 an 2001 | 6000 an 6001 |
| Umbuchung Nachlässe | 2002 an 2000 | 6002 an 6000 |
| Verbrauch | 6000 an 2000 | – |
| Inventurbestand | 8010 an 2000 | 8010 an 2000 |
| Bestandsmehrung | – | 2000 an 6000 |

(Für Fremdbauteile 201x/601x, Hilfsstoffe 202x/602x, Betriebsstoffe 203x/603x, Handelswaren 228x/608x gelten dieselben Muster.)
Quelle: Lösungsvorschläge der Lehrkraft (Cornelsen, Industriekaufleute 1, Lernfeld 5, Lernsituation 52). Belegt in `buchungsmuster.yaml`.

### Umsatzsteuer

| Vorgang | Buchung |
| --- | --- |
| Verkauf auf Ziel | 2400 an 5000, 4800 |
| Einkauf auf Ziel | 6000, 2600 an 4400 |
| Kauf einer Maschine | 0700, 2600 an 4400 |
| Verrechnung am Jahresende | 4800 an 2600 |
| Zahllast passivieren | 4800 an 8010 |
| Vorsteuerüberhang aktivieren | 8010 an 2600 |

## Typische Fehler (aus der Praxis)

- **Brutto und Netto verwechseln.** Die Verbindlichkeit und die Forderung stehen brutto, Aufwand, Erlöse und Bestand netto.
- **Vorsteuer bei der Gutschrift vergessen.** Auch beim Skonto muss sie berichtigt werden.
- **Skonto brutto auf das Nachlasskonto buchen** statt netto.
- **Zahllast-Frage** (steigt oder sinkt?): Gutschrift und Skonto **erhöhen** die Zahllast, weil die Vorsteuer sinkt.
- **Hauptkonto und Unterkonto vertauschen** bei der Umbuchung (Hauptkonto im Soll, Unterkonto im Haben).
- **Technik mischen:** Klasse-2-Konten gehören zur bestandsorientierten, Klasse-6-Konten zur aufwandsorientierten Buchung.
- **Parameter-Raster:** Prozentsätze wie 2 % Skonto mit Umsatzsteuer führen zu Beträgen mit drei Nachkommastellen, wenn die Zahlen nicht auf ein passendes Raster gelegt werden (zum Beispiel Vielfache von 500). Das prüft `buchungspruefung.py`.

## Lernprotokoll

| Datum | Thema | Was wir gelernt haben |
| --- | --- | --- |
| 2026-11-06 | Umsatzsteuer | Aufbau Check-Pfad, Buchungsaufgaben mit Zahllast und Erfolg, Tipps in zwei Stufen. |
| 2026-11-09 | Beschaffung | 20 Muster gegen Lösungsvorschläge bestätigt, auch Abschluss (Verbrauch, Inventurbestand, Bestandsmehrung, Anfangsbestand über 8000). Steuerart-Frage entfällt, Zahllast nur gelegentlich. Skonto nur auf den Warenwert, wenn der Beleg es sagt. Gutschrift kann Rücksendung, Preisnachlass und gekürzte Bezugskosten enthalten. |
| _(neues Thema)_ | | |
