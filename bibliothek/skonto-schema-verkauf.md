---
titel: Skonto-Schema (Verkauf)
icon: "🧮"
beschreibung: Hilfsblatt für Skonto, Umsatzsteuer und Buchungssatz beim Zahlungseingang.
reihenfolge: 5
---
Das Schema hilft dir, wenn ein Kunde **unter Abzug von Skonto** zahlt. **Waagerecht** denkst du an den Skontosatz, **senkrecht** an die Umsatzsteuer (netto und brutto).

## So sieht das Schema aus

| | Rechnung | abzüglich ___ % Skonto | = Zahlungsbetrag | Anteil in % |
| --- | --- | --- | --- | --- |
| **Warenwert** | | <sup style="color:#c0392b;font-weight:700;font-size:.7em">3</sup> | | 100 % |
| **Umsatzsteuer** | | <sup style="color:#c0392b;font-weight:700;font-size:.7em">2</sup> | | 19 % |
| **Rechnungsbetrag** | <sup style="color:#c0392b;font-weight:700;font-size:.7em">1</sup> | <sup style="color:#c0392b;font-weight:700;font-size:.7em">5</sup> | <sup style="color:#c0392b;font-weight:700;font-size:.7em">4</sup> | 119 % |
| **Anteil in %** | 100 % | Skontosatz | 100 % minus Skontosatz | |

:::tipp Für den Buchungssatz brauchst du nur die Felder 1 bis 4
- **Feld 1** (Rechnungsbetrag): die **Forderung** im Haben, **2400**.
- **Feld 4** (Zahlungsbetrag): die **Bank** im Soll, **2800**.
- **Feld 3** (Skonto auf den Warenwert): die **Erlösberichtigung** im Soll, **5001** (Erzeugnisse) oder **5101** (Waren).
- **Feld 2** (Skonto auf die Umsatzsteuer): die **Umsatzsteuer-Berichtigung** im Soll, **4800**.

**Feld 5** (Skonto vom Rechnungsbetrag) brauchst du beim **Rechnen**. Du rechnest es zuerst aus und teilst es dann mit der Brutto-Netto-Rechnung in Warenwert (Feld 3) und Umsatzsteuer (Feld 2) auf.
:::

## Beispiel mit Zahlen

Ein Kunde bezahlt eine Rechnung der Wiesengrund GmbH über **11.900,00 €** (netto 10.000,00 € plus 19 % Umsatzsteuer) unter Abzug von **2 % Skonto**.

| | Rechnung | abzüglich 2 % Skonto | = Zahlungsbetrag | Anteil in % |
| --- | --- | --- | --- | --- |
| **Warenwert** | 10.000,00 € | <sup style="color:#c0392b;font-weight:700;font-size:.7em">3</sup> 200,00 € | 9.800,00 € | 100 % |
| **Umsatzsteuer** | 1.900,00 € | <sup style="color:#c0392b;font-weight:700;font-size:.7em">2</sup> 38,00 € | 1.862,00 € | 19 % |
| **Rechnungsbetrag** | <sup style="color:#c0392b;font-weight:700;font-size:.7em">1</sup> 11.900,00 € | <sup style="color:#c0392b;font-weight:700;font-size:.7em">5</sup> 238,00 € | <sup style="color:#c0392b;font-weight:700;font-size:.7em">4</sup> 11.662,00 € | 119 % |
| **Anteil in %** | 100 % | 2 % | 98 % | |

So rechnest du:
1. **Feld 5:** 2 % von 11.900,00 € = **238,00 €**.
2. **Feld 3:** 238,00 € : 1,19 = **200,00 €** (der Skonto netto, 100 %).
3. **Feld 2:** 238,00 € minus 200,00 € = **38,00 €** (die Umsatzsteuer darin, 19 %).
4. **Feld 4:** 11.900,00 € minus 238,00 € = **11.662,00 €**.

**Buchungssatz (Erzeugnisse):**

| Soll | Betrag | | Haben | Betrag |
| --- | --- | --- | --- | --- |
| 2800 Bank | 11.662,00 € | an | 2400 Forderungen a. L. L. | 11.900,00 € |
| 5001 Erlösberichtigungen f. eigene Erzeugnisse | 200,00 € | | | |
| 4800 Umsatzsteuer | 38,00 € | | | |

:::achtung Typische Fehler
- Die Felder **3** und **2** sind **nicht** die Beträge der Rechnung, sondern der **Skonto** darauf.
- Der Skonto gilt nur für das, was der Beleg nennt. Steht dort „**Fracht ist nicht skontierbar**“, rechnest du den Skonto nur vom **Warenwert** (und der darauf entfallenden Umsatzsteuer).
:::
