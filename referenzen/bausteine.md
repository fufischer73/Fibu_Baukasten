# Bausteine für Module und Seiten

Der Text eines Moduls ist Markdown (Überschriften `##`, Listen, **fett**, Tabellen, Links, Bilder). Dazu kommen
Bausteine: Sie beginnen mit `:::name …` und enden mit einer Zeile `:::`. Bausteine dürfen ineinander stecken –
einfach immer `:::` schreiben, die Verschachtelung erkennt `bauen.py` selbst. Unbekannte Namen meldet `pruefen.py`.

Überschriften: `##` für Abschnitte (nummeriert: „## 1. Schrift ändern“), `###` darunter. Die Modul-Überschrift
(`#`) erzeugt `bauen.py` aus dem Titel – nicht selbst schreiben.

## Kästen

```markdown
:::tipp
So sortieren sich Dateien automatisch nach Datum.
:::

:::achtung Typischer Fehler
Nicht auf dem Desktop speichern – da findet man nichts wieder.
:::

:::notiz 👉 Bevor du startest
Hinweis ohne Standardtitel.
:::

:::gestaltung
- Höchstens drei Farben
- Mindestens 24 pt Schrift
:::

:::ziele
- nur nötig, wenn die Lernziele nicht im Modulkopf stehen
:::
```

`tipp` 💡, `achtung` ⚠️, `notiz` (neutral), `gestaltung` ✏️ Gestaltungsregeln, `ziele` 🎯, `kasten` (schlicht,
z. B. um mehrere Checklisten). Ein Titel hinter dem Namen ersetzt den Standardtitel.

**Nur für eine Variante:** Jeder Baustein kann am Ende der Kopfzeile `{id}` bekommen –
`:::notiz Nur in PowerPoint {ppt}`, `:::schritte {oo}`, `:::screenshot material/x.png {ppt}`. Er erscheint dann
nur, wenn diese Variante gewählt ist.

## Aufgaben

```markdown
:::aufgabe basis 10 1 · Dein Schulordner
Lege einen Ordner **Schule** an und darin je einen Ordner pro Fach.

:::checkliste Selbstcheck
- Der Ordner „Schule“ existiert.
- Für jedes Fach gibt es einen Unterordner.
:::

:::loesung
So könnte es aussehen: …
:::
:::
```

`:::aufgabe <niveau> [minuten] Titel` – Niveau `basis` (alle), `plus` (weiterführend), `kreativ` (offen,
eigene Ideen), `pflicht` (grün wie Basis, heißt „Pflicht“). Minuten optional, `10+` heißt „10 min oder länger“.
`:::checkliste [Titel]` macht aus der Liste darin Häkchen, die gespeichert werden (Web: Browser, Moodle: im Kurs).
`:::loesung [Titel]` ist aufklappbar.

## Interaktive Übungen (:::uebung)

Übungen zum Selbstkontrollieren: Die Schüler:innen tragen etwas ein, klicken „Prüfen“ und bekommen sofort
Rückmeldung – ohne Server, in der Web-Version und im Moodle-Lernpaket. Ablauf in allen Typen:

1. **Tipps** bleiben zu, bis sie angeklickt werden. `tipps:` ist eine Liste (Tipp 1 = Ansatz, Tipp 2 = halber Rechenweg), jeder Klick zeigt den nächsten; `tipp:` (ein Text) geht weiter.
2. Erst nach einer **Eingabe** lässt sich prüfen. Falsche Felder werden rot, richtige grün markiert.
3. Beim **ersten falschen Versuch** gibt es nur Hinweise (`hinweis:` je Feld, allgemeine Hinweise zu Konten),
   keine Lösung. Nach dem **zweiten falschen Versuch** (oder bei richtiger Lösung) erscheinen Lösung und
   **Rechenweg** (`loesungsweg:`). „Nochmal von vorn“ setzt die Aufgabe zurück.
4. Bei Übungen mit `parameter:` folgt danach die **Parallelaufgabe**: dieselbe Aufgabe mit anderen, zufälligen Zahlen
   (wer die Lösung gesehen hat, soll sie selbst lösen; bei richtiger Lösung ist sie freiwillig). Abschalten mit `parallel: false`.

Der Block enthält YAML und steht allein (nicht in `:::aufgabe`). Gemeinsame Felder: `typ`, `titel`, `niveau`
(basis | plus | kreativ), `minuten`, `text` (Aufgabentext, `**fett**` und Zeilenumbrüche erlaubt), `tipp`, `loesungsweg`.
Zahlen immer als Zahl schreiben (`921.5`), Kontonummern **immer in Anführungszeichen** (`"0700"`, sonst liest YAML
eine Oktalzahl).

```markdown
:::uebung
typ: rechnen
titel: Von netto zu brutto
text: Nettobetrag 4.850,00 €, Steuersatz 19 %.
felder:
  - {label: Umsatzsteuer, antwort: 921.5, einheit: "€", hinweis: "19 % vom Nettobetrag."}
  - {label: Bruttobetrag, antwort: 5771.5, einheit: "€"}
toleranz: 0.01          # optional, Standard 0,01
tipp: Netto sind 100 %.
loesungsweg: |
  4.850,00 € · 0,19 = 921,50 €
:::
```

| typ | Was die Schüler:innen tun | Wichtige Felder |
| --- | --- | --- |
| `rechnen` | Zahlen eintragen (Komma, Punkt, Tausenderpunkt und „€“ werden verstanden) | `felder` (label, antwort, einheit, hinweis) |
| `buchung` | Buchungssatz aus Konto-Auswahllisten und Beträgen bilden (Reihenfolge egal, „+ Zeile“ für zusammengesetzte Sätze); optional Auswirkung auf Zahllast und Erfolg | `konten` (wählbare Konten inkl. Ablenker), `soll`, `haben` (oder `saetze` mit mehreren Buchungssätzen), `steuerart` (`art: vorsteuer\|umsatzsteuer\|keine`, `betrag`), `zahllast`, `erfolg` (je `richtung: steigt\|sinkt\|gleich`, `betrag`) |
| `konten` | T-Konten abschließen: Gegenkonto wählen, Betrag eintragen, Summen werden live gebildet | `konten`, `t_konten` (konto, `soll`/`haben` vorgegeben, `ausgleich`: seite, zeilen) |
| `luecken` | Lückentext mit Auswahl je Lücke | `lueckentext` (Lücken als `[[a]]`), `loesung` (a: Wort), `ablenker` (je Lücke 1–2 falsche Wörter, am besten das Gegenstück; alternativ `woerter` = gemeinsame Liste für alle Lücken) |

**Zwischenstand:** Eingaben und Ergebnisse jeder Übung werden mit dem Fortschritt gespeichert (Browser bzw. Moodle). Auf jeder Modulseite und der Übersicht gibt es „💾 Zwischenstand speichern“ (Datei) und „📂 Zwischenstand laden“ – so lassen sich Stände sichern und auf andere Geräte übertragen. Die Datei gehört zu genau einem Lernpfad (`kurzname`). Nur in der Web-Version: In Moodle-Lernpaketen fehlt die Sicherung, weil Moodle den Stand (auch der Übungen) selbst speichert.

**Parameter und Formeln:** Mit `parameter:` entstehen Zahlen, die sich für die Parallelaufgabe ändern. Jede Zahl hat `start` (Wert der ersten Aufgabe),
`von`, `bis` und `schritt`; Beträge und Antworten schreibt man als Formel (`+ - * / ^`, Klammern, `round floor ceil abs min max sqrt`).
In Texten stehen Platzhalter: `{{n}}` (Zahl), `{{n:eur}}` (als Euro), `{{=n*0.19:eur}}` (berechnet). `pruefen.py` rechnet alle Formeln mit
Start- und Zufallswerten durch und meldet mehr als zwei Nachkommastellen (Schrittweite anpassen) oder negative Beträge.

```markdown
:::uebung
typ: rechnen
titel: Von netto zu brutto
parameter:
  n: {start: 4850, von: 1200, bis: 9800, schritt: 50}
text: Nettopreis **{{n:eur}}**, Steuersatz 19 %.
felder:
  - {label: Umsatzsteuer, formel: "n*0.19", einheit: "€", hinweis: "19 % vom Nettobetrag."}
tipps: ["Netto sind 100 %.", "Rechne {{n:eur}} · 0,19."]
loesungsweg: "{{n:eur}} · 0,19 = {{=n*0.19:eur}}"
:::
```

Weitere Typen (vor allem für Tests, siehe unten): `auswahl` (`optionen` mit `korrekt`, `feedback`, `erklaerung`), `zuordnung` (`kategorien`, `elemente`),
`reihenfolge` (`elemente` in richtiger Reihenfolge), `lueckentext` (Freitext, Lücken `[[a]]`, `luecken` mit `akzeptiert`), `offen` (`musterloesung`, `checkliste`).
Ein `konten`-Block kann zusätzlich `saetze:` (Abschlussbuchungssätze) enthalten und wird dann in einer Karte geprüft.

**Web-Version der Tests:** Jeder Test aus `tests:` (ohne `klausur:`) erscheint auch in der Web-Version als Seite „📝 Titel“ unter „Immer griffbereit“.
Sie wird aus `fragen/` erzeugt: sofort ausgewertet, ein Versuch je Frage, Zwischenstand „x von y richtig“, „Test neu starten“. Zufallsrechnungen
(`zahl` mit `parameter`) bekommen beim Öffnen zufällige Werte. Die Seite gehört nicht in die Moodle-Lernpakete; dort gibt es den Moodle-Test. `web: false` am Test schaltet sie ab.

**Online-Breakout (Räume, Schlösser, Code-Teile):** Aus Übungen lässt sich ein Breakout bauen (Beispiel: `seiten/breakout.md` im Lernpfad Umsatzsteuer).
- `code: {teil: "4", text: "…"}` in einer Übung: Nach **richtiger** Lösung erscheint der Code-Teil (🔑), nach falscher Lösung nicht.
- `:::schloss` (YAML: `id`, `titel`, `code`, `text`, `hinweis` nach drei Fehlversuchen, `oeffnet` = Text beim Öffnen): digitales Schloss. Leerzeichen und Groß-/Kleinschreibung im Code sind egal.
- `:::raum braucht=<schloss-id> Titel`: Raum, dessen Inhalt erst sichtbar wird, wenn das Schloss geöffnet ist (merkt sich der Browser, steckt auch im Zwischenstand).
- `<button data-lp-reset>`: „Spiel neu starten“ löscht Antworten und Schlösser der Seite.
- Für Gruppen feste Zahlen nehmen: `parameter: {n: {start: 4200}}` (nur `start` = feste Zahl) und `parallel: false`.
- **Die Codes stehen im Quelltext der Seite** – nur Sichtschutz, nichts für Bewertung. Mit `nur_web: true` im Kopf der Seite bleibt der Breakout aus den Moodle-Lernpaketen heraus.

Konten stammen aus `kontenplan:` in kurs.yaml (Nummer → Name); `pruefen.py` meldet Konten, die dort fehlen.

**Kurz-Check:** Die Antworten werden beim Bauen stabil gemischt, die richtige steht nicht immer an erster Stelle. `mischen: false` an einer Frage schaltet das ab (z. B. bei „alle genannten“).

## Schritte

```markdown
:::schritte
1. Gehe in den Ordner.
2. Drücke ++Strg+Umschalt+N++.
3. Tippe den Namen und bestätige mit ++Enter++.
:::
```

Nummerierte Schrittfolge mit großen Ziffern – für Anleitungen immer diese statt einer normalen Liste.

## Varianten (mit Umschalter aus kurs.yaml)

```markdown
:::varianten
:::variante win
Öffne den **Explorer** mit ++Windows++ + ++E++.
:::
:::variante mac
Öffne den **Finder**.
:::
:::
```

Jede `:::variante <id>` erscheint nur, wenn oben diese Variante gewählt ist; bei „beide“ stehen sie im
`:::varianten`-Rahmen nebeneinander. Kurze Unterschiede im Fließtext: `<span class="win">Strg</span><span class="mac">Befehl</span>`.
Was für alle gleich ist, steht außerhalb – nicht doppelt schreiben. Eigene Beschriftung statt des Namens aus
kurs.yaml: `:::variante oo OnlyOffice (Browser)`.

## Menüpfade, Tasten, Links

| Schreibweise | Ergebnis |
| --- | --- |
| `{{Start › Schriftart › Fett}}` | Menüpfad als Kästchen (Trennzeichen ›, auf dem Mac: Alt+Umschalt+3 – oder einfach kopieren) |
| `++Strg+C++`, `++Enter++` | Tasten bzw. Tastenkombination |
| `[zum Modul E2](modul:e2)` | Link auf ein anderes Modul (Dateiname egal, in Moodle wird daraus Text) |
| `[Vorlage](material/vorlage.pptx)` | Link auf eine Datei in `material/` |
| `![Beschreibung](material/bild.png)` | Bild – Beschreibung = Alternativtext, immer ausfüllen |

## Material zum Herunterladen

```markdown
:::material material/uebung-e3.pptx Übungsdatei: Text gestalten
Enthält fünf Folien mit ungestaltetem Text.
:::
```

## Menüband und Seitenleiste (Schema-Grafiken statt Screenshots)

```markdown
:::menueband ppt Start
gruppen: Folien: Neue Folie, Layout | Schriftart: *1 Schriftart, *2 Größe, Fett | Absatz: Aufzählung
text: Die Gruppe „Schriftart“ auf der Registerkarte Start
:::

:::menueband oo Start
gruppen: Schriftart, *Größe, Fett
menue: Aufzählung|Punkte|*Zahlen
:::

:::seitenleiste ppt Hintergrund formatieren
zeilen: #Füllung|Einfarbig|*Farbverlauf|Bild- oder Texturfüllung
text: Aufgabenbereich rechts
:::
```

- `:::menueband <variante> <Registerkarte>`: Registerkarten aus `menueband:` in kurs.yaml, die genannte ist aktiv.
  Nicht aufgelistete Registerkarte = Kontext-Registerkarte (wird so beschriftet).
- `gruppen:` Gruppen mit `|` trennen, `Name: Knopf, Knopf`; `*` markiert, `*1` markiert mit Nummer.
- `menue:` aufgeklapptes Menü: erster Eintrag = Kopf, dann Einträge mit `|`.
- `zeilen:` bei der Seitenleiste: `#` = Zwischenüberschrift, `*` = markiert.
- Ohne Varianten in kurs.yaml gibt es diese beiden Bausteine nicht.

## Code zum Freischalten (zugang: in kurs.yaml)

```markdown
:::schluessel vertiefung
Damit öffnest du auf der Übersicht die nächste Stufe.
:::
```

- `:::schluessel <stufe|modul>` zeigt den Code aus `zugang.stufen` bzw. `zugang.module` – aber erst, wenn das
  Modul als erledigt markiert ist (vorher: „Der Code erscheint, sobald …“). Text darin ist optional.
- Typisch: am Ende des Meilensteins der vorigen Stufe, hinter der letzten Aufgabe. Der Code wird auf der
  Übersicht (Feld unter der gesperrten Stufe) oder direkt im gesperrten Modul eingegeben.
- Strenger geht es ohne Baustein: Code nur in der Rückmeldung der Lehrkraft (Moodle-Abgabe) oder als Lösung
  einer Aufgabe („Das Lösungswort ist der Code“).
- In Moodle-Lernpaketen erscheint der Kasten nicht.

## Screenshots

```markdown
:::screenshot material/e3-schrift.png
Registerkarte Start, Gruppe Schriftart markiert.
:::
```

Solange die Datei fehlt, erscheint ein Platzhalter mit der Beschreibung – so sieht die Lehrkraft, welche Bilder
noch fehlen (`pruefen.py` listet sie als Hinweis). Screenshots nimmt die Lehrkraft selbst auf (keine
personenbezogenen Daten im Bild).

## Platzhalter für Kopf-Inhalte

`:::kurzcheck`, `:::abgabe`, `:::raster`, `:::medien` (jeweils sofort mit `:::` schließen) setzen Kurz-Check,
Abgabe-Kasten, Bewertungsraster und Videos aus dem Modulkopf an diese Stelle. Ohne Platzhalter stehen sie am Ende.

```markdown
## Zum Schluss

:::kurzcheck
:::
```

## Tabellen

Normale Markdown-Tabellen; auf dem Handy werden sie waagerecht scrollbar. Breite Tabellen (mehr als 4 Spalten)
möglichst vermeiden.

## HTML

HTML ist erlaubt, wenn ein Baustein nicht reicht (z. B. `<span class="win">`). Keine Skripte, keine
externen Einbettungen (iframes von YouTube usw.) – Videos gehören in `medien.yaml`.

## Belege (`beleg:` in :::uebung und in Testfragen)

Rechnungen, Gutschriften, Bonusabrechnungen und Kontoauszüge erscheinen als Beleg mit Briefkopf, Anschrift, Positionstabelle und Summen – nicht als Textaufgabe. Das Feld `beleg:` steht in einem `:::uebung`-Block (nach `text:`) oder in einer Frage in `fragen/*.yaml`. Eine Liste von Belegen zeigt mehrere Belege untereinander. Bei Übungen mit `parameter:` gelten die Platzhalter `{{n:eur}}`, `{{=n*0.19:eur}}` auch im Beleg (Werte in Anführungszeichen schreiben). Im Moodle-Test steht der Beleg mit Inline-Stilen hinter dem Fragetext (feste Zahlen).

```yaml
beleg:
  art: Rechnung                 # Rechnung | Gutschrift | Bonusabrechnung | Kontoauszug … (großer Titel rechts)
  stil: rechnung                # optional, Farbe: rechnung (blau) | gutschrift (grün) | bonus (braun) | bank | spedition
  firma: Holzwerk Nordmark GmbH
  firma_zeile: Spanplatten · Massivholz
  absender_zeile: Holzwerk Nordmark GmbH · Hafenstraße 14 · 24937 Flensburg
  empfaenger: [Wiesengrund Küchenmöbel GmbH, Am Wiesengrund 8, 24768 Rendsburg]
  info:                         # rechter Block, je [Beschriftung, Wert]
    - [Rechnungs-Nr., R-2026-1184]
  spalten: [Pos., Bezeichnung, Menge, Einzelpreis, Gesamtpreis]
  zeilen:                       # jede Zeile so viele Einträge wie Spalten; Zahlenspalten werden rechtsbündig
    - ["1", "Spanplatte roh", "{{q}} Stück", "{{p:eur}}", "{{=q*p:eur}}"]
  summen:                       # je [Beschriftung, Wert] oder [Beschriftung, Wert, fett]
    - ["Nettobetrag", "{{=q*p:eur}}"]
    - ["Bruttobetrag", "{{=q*p*1.19:eur}}", fett]
  text: Freitext über der Tabelle (optional)
  bedingungen: Zahlungsbedingungen im Rahmen (optional)
  fuss: Fußzeile (optional)
  stempel: "Eingegangen am 10.03.2026"   # optional
```

Keine Schlüssel namens `betrag` oder `antwort` im Beleg verwenden (sie werden als Formeln gelesen). Belege bleiben auch im Dunkelmodus helles Papier. Auswahlaufgaben (`typ: auswahl`) zeigen Buchungssätze in einer Zeile (`4400 … an 2800 …`) als Tabelle Soll | an | Haben.

## Hilfen im Modul (`:::hilfe`)

```markdown
:::hilfe kontenuebersicht
:::
```

Der Baustein bettet die Seite `seiten/<name>.md` als **aufklappbaren Kasten** in das Modul ein (Titel und Symbol der Seite stehen in der Zusammenfassung). Damit sind Unternehmen, Kontenübersicht und Schemata dort, wo man sie braucht, und nicht nur in der Seitenleiste. Der Seitenname ist der Dateiname ohne `.md`. Die Seite bleibt zusätzlich in der Seitenleiste und in der Web-Version. Typisch: ein Abschnitt „Hilfen zum Aufklappen“ vor der ersten Aufgabe.
