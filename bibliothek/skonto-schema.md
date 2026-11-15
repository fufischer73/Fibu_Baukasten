---
titel: Skonto-Schema
icon: "🧮"
beschreibung: Hilfsblatt für Skonto, Umsatzsteuer und Buchungssatz.
reihenfolge: 3
---
Das Schema hilft dir bei jeder Zahlung unter Abzug von Skonto. **Waagerecht** denkst du an den Skontosatz, **senkrecht** an die Umsatzsteuer (netto und brutto).

## So sieht das Schema aus

| | Rechnung | abzüglich ___ % Skonto | = Zahlungsbetrag | Anteil in % |
| --- | --- | --- | --- | --- |
| **Warenwert** | | <sup style="color:#c0392b;font-weight:700;font-size:.7em">3</sup> | | 100 % |
| **Umsatzsteuer** | | <sup style="color:#c0392b;font-weight:700;font-size:.7em">2</sup> | | 19 % |
| **Rechnungsbetrag** | <sup style="color:#c0392b;font-weight:700;font-size:.7em">1</sup> | <sup style="color:#c0392b;font-weight:700;font-size:.7em">5</sup> | <sup style="color:#c0392b;font-weight:700;font-size:.7em">4</sup> | 119 % |
| **Anteil in %** | 100 % | Skontosatz | 100 % minus Skontosatz | |

**Was bedeuten die kleinen roten Nummern?** Sie nummerieren die fünf wichtigen Felder des Schemas. Die Nummern **1 bis 4** sind die Felder, die du für den **Buchungssatz** brauchst. Die **5** ist das Feld, mit dem du beim **Rechnen** beginnst. Alle anderen Felder sind Zwischenergebnisse.

:::tipp Für den Buchungssatz brauchst du nur die Felder 1 bis 4
- **Feld 1** (Rechnungsbetrag): die **Verbindlichkeit** im Soll, **4400**.
- **Feld 4** (Zahlungsbetrag): die **Bank** im Haben, **2800**.
- **Feld 3** (Skonto auf den Warenwert): der **Nachlass** im Haben, zum Beispiel **6002** oder **2002**.
- **Feld 2** (Skonto auf die Umsatzsteuer): die **Vorsteuerberichtigung** im Haben, **2600**.

Das **Feld 5** (Skonto vom Rechnungsbetrag) brauchst du beim **Rechnen**: Du rechnest es zuerst aus und teilst es dann mit der Brutto-Netto-Rechnung in Warenwert (Feld 3) und Umsatzsteuer (Feld 2) auf.
:::

## Beispiel mit Zahlen

Die Wiesengrund Küchenmöbel GmbH bezahlt eine Rechnung über **2.856,00 €** (netto 2.400,00 € plus 19 % Umsatzsteuer) unter Abzug von **2 % Skonto**.

| | Rechnung | abzüglich 2 % Skonto | = Zahlungsbetrag | Anteil in % |
| --- | --- | --- | --- | --- |
| **Warenwert** | 2.400,00 € | <sup style="color:#c0392b;font-weight:700;font-size:.7em">3</sup> 48,00 € | 2.352,00 € | 100 % |
| **Umsatzsteuer** | 456,00 € | <sup style="color:#c0392b;font-weight:700;font-size:.7em">2</sup> 9,12 € | 446,88 € | 19 % |
| **Rechnungsbetrag** | <sup style="color:#c0392b;font-weight:700;font-size:.7em">1</sup> 2.856,00 € | <sup style="color:#c0392b;font-weight:700;font-size:.7em">5</sup> 57,12 € | <sup style="color:#c0392b;font-weight:700;font-size:.7em">4</sup> 2.798,88 € | 119 % |
| **Anteil in %** | 100 % | 2 % | 98 % | |

So rechnest du:
1. **Feld 5:** 2 % von 2.856,00 € = **57,12 €**.
2. **Feld 3:** 57,12 € : 1,19 = **48,00 €** (der Skonto netto, 100 %).
3. **Feld 2:** 57,12 € minus 48,00 € = **9,12 €** (die Umsatzsteuer darin, 19 %).
4. **Feld 4:** 2.856,00 € minus 57,12 € = **2.798,88 €**.

**Buchungssatz (aufwandsorientiert, Hilfsstoffe):**

| Soll | Betrag | | Haben | Betrag |
| --- | --- | --- | --- | --- |
| 4400 Verbindlichkeiten a. L. L. | 2.856,00 € | an | 2800 Bank | 2.798,88 € |
| | | | 6022 Nachlässe Hilfsstoffe | 48,00 € |
| | | | 2600 Vorsteuer | 9,12 € |

:::achtung Typischer Fehler
Die Zahlen **3** und **2** sind **keine** Beträge aus der Rechnung, sondern der **Skonto** darauf. Wer die Spalte „Rechnung“ mit der Spalte „Skonto“ verwechselt, bucht den vollen Betrag auf das Nachlasskonto.
:::

:::material material/skonto-schema.docx Hilfsblatt zum Ausdrucken
Das Schema leer zum Ausfüllen und mit dem Beispiel von dieser Seite. Du kannst es in ONLYOFFICE öffnen.
:::
