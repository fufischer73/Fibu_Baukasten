#!/usr/bin/env python3
"""Erzeugt material/hilfsblatt-absatz.docx (Hilfsblatt zum Ausdrucken, ONLYOFFICE-tauglich).
Aufruf:  python3 werkzeuge/hilfsblatt_erzeugen.py   (im Ordner des Lernpfads). Inhalte spiegeln die Seiten in seiten/.
Dieses Skript liegt bewusst nicht in material/, damit es nicht in die Lernpakete gelangt."""
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

SCHRIFT = "Arial"
BLAU = RGBColor(0x1F, 0x4E, 0x79)
ROT = RGBColor(0xC0, 0x39, 0x2B)


def font(run, groesse=10, fett=False, farbe=None, kursiv=False):
    run.font.name = SCHRIFT
    run._element.rPr.rFonts.set(qn("w:eastAsia"), SCHRIFT)
    run.font.size = Pt(groesse)
    run.bold = fett
    run.italic = kursiv
    if farbe is not None:
        run.font.color.rgb = farbe


def absatz(doc, text="", groesse=10, fett=False, farbe=None, vor=0, nach=3, ausrichtung=None, kursiv=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(vor)
    p.paragraph_format.space_after = Pt(nach)
    if ausrichtung:
        p.alignment = ausrichtung
    if text:
        font(p.add_run(text), groesse, fett, farbe, kursiv)
    return p


def ueberschrift(doc, text):
    p = absatz(doc, text, 12, True, BLAU, vor=9, nach=3)
    pPr = p._p.get_or_add_pPr()
    rand = OxmlElement("w:pBdr")
    unten = OxmlElement("w:bottom")
    for k, v in (("val", "single"), ("sz", "6"), ("space", "1"), ("color", "1F4E79")):
        unten.set(qn(f"w:{k}"), v)
    rand.append(unten)
    pPr.append(rand)
    p.paragraph_format.keep_with_next = True
    return p


def fuellung(zelle, farbe):
    tcPr = zelle._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), farbe)
    tcPr.append(shd)


def zellrand(tabelle):
    tblPr = tabelle._tbl.tblPr
    raender = OxmlElement("w:tblBorders")
    for seite in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{seite}")
        for k, v in (("val", "single"), ("sz", "4"), ("space", "0"), ("color", "9AA5B1")):
            e.set(qn(f"w:{k}"), v)
        raender.append(e)
    tblPr.append(raender)
    mar = OxmlElement("w:tblCellMar")
    for seite, w in (("top", 40), ("left", 80), ("bottom", 40), ("right", 80)):
        e = OxmlElement(f"w:{seite}")
        e.set(qn("w:w"), str(w))
        e.set(qn("w:type"), "dxa")
        mar.append(e)
    tblPr.append(mar)


def tabelle(doc, kopf, zeilen, breiten, groesse=9, fett_erste=False, hoehe=None):
    t = doc.add_table(rows=1, cols=len(kopf))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    zellrand(t)
    for i, k in enumerate(kopf):
        z = t.rows[0].cells[i]
        z.text = ""
        font(z.paragraphs[0].add_run(k), groesse, True)
        fuellung(z, "DCE6F1")
    # Kopfzeile nicht über Seiten trennen
    trPr = t.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    trPr.append(th)
    for zeile in zeilen:
        r = t.add_row()
        cs = OxmlElement("w:cantSplit")
        r._tr.get_or_add_trPr().append(cs)
        if hoehe:
            r.height = Cm(hoehe)
        for i, text in enumerate(zeile):
            z = r.cells[i]
            z.text = ""
            p = z.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            font(p.add_run(str(text)), groesse, fett_erste and i == 0)
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    t._tbl.tblPr.append(lay)
    for i, b in enumerate(breiten):
        t.columns[i].width = Cm(b)
    for r in t.rows:
        for i, b in enumerate(breiten):
            r.cells[i].width = Cm(b)
    absatz(doc, "", 3, nach=0)   # kleiner Abstand unter der Tabelle
    return t


def liste(doc, eintraege, nummeriert=False, groesse=10):
    for i, e in enumerate(eintraege, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.6)
        p.paragraph_format.first_line_indent = Cm(-0.6)
        p.paragraph_format.space_after = Pt(2)
        marke = f"{i}." if nummeriert else "•"
        font(p.add_run(marke + "\t"), groesse, True)
        if isinstance(e, tuple):
            font(p.add_run(e[0]), groesse, True)
            font(p.add_run(e[1]), groesse)
        else:
            font(p.add_run(e), groesse)
        p.paragraph_format.tab_stops.add_tab_stop(Cm(0.6))


def fuss(doc):
    sec = doc.sections[0]
    p = sec.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    font(p.add_run("BBZ Rendsburg-Eckernförde · Hilfsblatt Absatzprozesse buchen · Wiesengrund Küchenmöbel GmbH ist frei erfunden"), 8, False, RGBColor(0x55, 0x55, 0x55))


def baue(ziel):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(1.8)
    sec.top_margin, sec.bottom_margin = Cm(1.5), Cm(1.5)
    st = doc.styles["Normal"]
    st.font.name = SCHRIFT
    st.font.size = Pt(10)

    absatz(doc, "Hilfsblatt: Absatzprozesse buchen", 18, True, BLAU, nach=0)
    absatz(doc, "Industriekaufleute · Lernfeld 5 · zum Ausdrucken und Beschriften", 10, False, RGBColor(0x55, 0x55, 0x55), nach=4)

    ueberschrift(doc, "1. Die vier Schritte")
    liste(doc, [("Beleg lesen: ", "Wer kauft, wer verkauft? Was? Welche Beträge?"),
                ("Was ist passiert? ", "Welche Konten sind betroffen?"),
                ("Soll oder Haben? ", "Links (Soll) oder rechts (Haben)?"),
                ("Beträge eintragen ", "und prüfen: Soll gleich Haben.")], nummeriert=True)

    ueberschrift(doc, "2. Die Grundmuster im Absatz")
    tabelle(doc, ["Was ist passiert?", "Buchungssatz"], [
        ["Wir verkaufen auf Ziel", "2400 Forderungen an 5000 Umsatzerlöse und 4800 Umsatzsteuer"],
        ["Der Kunde schickt Ware zurück (Gutschrift)", "5000 Umsatzerlöse und 4800 Umsatzsteuer an 2400 Forderungen"],
        ["Der Kunde behält die Ware und bekommt einen Nachlass (Mängelrüge, Bonus)", "5001 Erlösberichtigungen und 4800 Umsatzsteuer an 2400 Forderungen"],
        ["Der Kunde zahlt mit Skonto", "5001 Erlösberichtigungen, 4800 Umsatzsteuer und 2800 Bank an 2400 Forderungen"],
        ["Eingangsrechnung für Verpackung, Fracht, Provision", "6040, 6140 bzw. 6150 und 2600 Vorsteuer an 4400 Verbindlichkeiten"],
    ], [6.6, 10.8])
    absatz(doc, "Bei Handelswaren stehen statt 5000 und 5001 die Konten 5100 und 5101.", 9, False, None, vor=3, kursiv=True)

    ueberschrift(doc, "3. Welches Konto bei welcher Korrektur?")
    tabelle(doc, ["Was ist passiert?", "Wird gebucht?", "Erzeugnisse", "Handelswaren", "Gegenkonto"], [
        ["Sofortrabatt (steht in der Rechnung)", "nein, nur der Nettobetrag danach", "–", "–", "–"],
        ["Rücksendung (Ware kommt zurück)", "ja, Gutschrift", "5000", "5100", "2400"],
        ["Mängelrüge (Kunde behält die Ware)", "ja, Gutschrift", "5001", "5101", "2400"],
        ["Bonus", "ja, Gutschrift", "5001", "5101", "2400"],
        ["Skonto", "ja, beim Zahlungseingang", "5001", "5101", "2400, dazu 2800"],
        ["Umbuchung am Periodenende", "ja", "5000 an 5001", "5100 an 5101", "–"],
    ], [5.2, 4.2, 2.6, 2.6, 2.8], groesse=8.5)
    liste(doc, ["Steht der Rabatt schon in der Rechnung? Dann nichts buchen.",
                "Kommt Ware zurück? Dann 5000 oder 5100. Bleibt die Ware beim Kunden? Dann 5001 oder 5101.",
                "Immer: Die Umsatzsteuer sinkt mit und steht im Soll auf 4800."], groesse=9)

    ueberschrift(doc, "4. Kontenübersicht")
    tabelle(doc, ["Nr.", "Bezeichnung", "Nr.", "Bezeichnung"], [
        ["2200", "Fertigerzeugnisse", "5000", "Umsatzerlöse f. eigene Erzeugnisse"],
        ["2280", "Handelswaren", "5001", "Erlösberichtigungen f. eigene Erzeugnisse"],
        ["2400", "Forderungen a. L. L.", "5100", "Umsatzerlöse f. Waren"],
        ["2600", "Vorsteuer", "5101", "Erlösberichtigungen f. Waren"],
        ["2800", "Bank", "6040", "Aufwendungen für Verpackungsmaterial"],
        ["4400", "Verbindlichkeiten a. L. L.", "6140", "Frachten und Fremdlager"],
        ["4800", "Umsatzsteuer", "6150", "Vertriebsprovisionen"],
    ], [1.4, 6.2, 1.4, 8.4], groesse=8.5)

    doc.add_page_break()
    ueberschrift(doc, "5. Skonto-Schema (zum Ausfüllen)")
    absatz(doc, "Waagerecht denkst du an den Skontosatz, senkrecht an die Umsatzsteuer. Beginne mit dem Feld 5.", 9, nach=4)
    tabelle(doc, ["", "Rechnung", "abzüglich ___ % Skonto", "= Zahlungsbetrag", "Anteil in %"], [
        ["Warenwert", "", "(3)", "", "100 %"],
        ["Umsatzsteuer", "", "(2)", "", "19 %"],
        ["Rechnungsbetrag", "(1)", "(5)", "(4)", "119 %"],
        ["Anteil in %", "100 %", "Skontosatz", "100 % minus Skontosatz", ""],
    ], [3.4, 3.4, 4.0, 3.9, 2.7], groesse=9, fett_erste=True, hoehe=1.1)
    liste(doc, [("Feld 1 ", "Rechnungsbetrag: Forderung im Haben (2400)."),
                ("Feld 4 ", "Zahlungsbetrag: Bank im Soll (2800)."),
                ("Feld 3 ", "Skonto auf den Warenwert: Erlösberichtigung im Soll (5001 bzw. 5101)."),
                ("Feld 2 ", "Skonto auf die Umsatzsteuer: Berichtigung im Soll (4800)."),
                ("Feld 5 ", "Skonto vom Rechnungsbetrag: damit beginnst du beim Rechnen.")], groesse=9)

    ueberschrift(doc, "6. Beispiel mit Zahlen")
    absatz(doc, "Rechnung über 11.900,00 € (netto 10.000,00 € plus 19 % Umsatzsteuer), Zahlung unter Abzug von 2 % Skonto.", 9, nach=4)
    tabelle(doc, ["", "Rechnung", "abzüglich 2 % Skonto", "= Zahlungsbetrag", "Anteil in %"], [
        ["Warenwert", "10.000,00 €", "(3) 200,00 €", "9.800,00 €", "100 %"],
        ["Umsatzsteuer", "1.900,00 €", "(2) 38,00 €", "1.862,00 €", "19 %"],
        ["Rechnungsbetrag", "(1) 11.900,00 €", "(5) 238,00 €", "(4) 11.662,00 €", "119 %"],
        ["Anteil in %", "100 %", "2 %", "98 %", ""],
    ], [3.4, 3.4, 4.0, 3.9, 2.7], groesse=9, fett_erste=True)
    liste(doc, ["Feld 5: 2 % von 11.900,00 € = 238,00 €.",
                "Feld 3: 238,00 € : 1,19 = 200,00 € (Skonto netto).",
                "Feld 2: 238,00 € minus 200,00 € = 38,00 € (Umsatzsteuer darin).",
                "Feld 4: 11.900,00 € minus 238,00 € = 11.662,00 €."], nummeriert=True, groesse=9)
    absatz(doc, "Buchungssatz:", 9, True, vor=3, nach=2)
    tabelle(doc, ["Soll", "Betrag", "", "Haben", "Betrag"], [
        ["2800 Bank", "11.662,00 €", "an", "2400 Forderungen a. L. L.", "11.900,00 €"],
        ["5001 Erlösberichtigungen f. eigene Erzeugnisse", "200,00 €", "", "", ""],
        ["4800 Umsatzsteuer", "38,00 €", "", "", ""],
    ], [6.0, 2.6, 0.9, 5.0, 2.9], groesse=9)
    absatz(doc, "Gilt der Skonto nur für den Warenwert („Fracht nicht skontierbar“), rechne den Skonto nur vom Warenwert und der Umsatzsteuer darauf.", 9, False, ROT, vor=4, kursiv=True)

    ueberschrift(doc, "7. Typische Fehler")
    liste(doc, ["Brutto und Netto verwechseln: Die Forderung steht brutto, die Erlöse stehen netto.",
                "Bei der Gutschrift die Umsatzsteuer vergessen (sie steht im Soll auf 4800).",
                "Rücksendung auf 5001 oder Mängelrüge auf 5000 buchen.",
                "Weiterberechnete Verpackung und Transport auf ein Aufwandskonto buchen: Sie gehören in die Umsatzerlöse.",
                "Den Sofortrabatt buchen: Er steht schon in der Rechnung."], groesse=9)

    fuss(doc)
    doc.core_properties.title = "Hilfsblatt Absatzprozesse buchen"
    doc.core_properties.author = "BBZ Rendsburg-Eckernförde"
    doc.save(ziel)


if __name__ == "__main__":
    ziel = Path(__file__).resolve().parent.parent / "material" / "hilfsblatt-absatz.docx"
    baue(ziel)
    print("✓", ziel)
