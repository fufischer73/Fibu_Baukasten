#!/usr/bin/env python3
"""Gemeinsame Stammdaten (stammdaten.yaml): Tabellen für die Seite „Unternehmen“, nächste freie Nummer, Abgleich mit den Belegen.

  python3 skripte/stammdaten.py --seite [--gruppen einkauf vertrieb kunden]   Markdown-Tabellen für seiten/unternehmen.md
  python3 skripte/stammdaten.py --naechste kreditor|debitor                    nächste freie Nummer
  python3 skripte/stammdaten.py --pruefen <ordner>                             Belege eines Lernpfads mit den Stammdaten vergleichen

--pruefen meldet (Hinweise, kein Fehler):
  ! Name nicht in den Stammdaten    (neue Firma? zuerst in stammdaten.yaml eintragen)
  ! Anschrift weicht ab             (zum Beispiel andere Straße als in einem früheren Pfad)
"""
import argparse
import os
import re
import sys
from pathlib import Path

import yaml

DATEI = Path(os.environ.get("FIBU_STAMMDATEN") or Path(__file__).resolve().parent.parent / "stammdaten.yaml")   # Umgebungsvariable nur für Tests

GRUPPEN = {
    "einkauf": ("Lieferanten in den Aufgaben", "lieferanten", "Lieferant", "Liefert", "Kreditor"),
    "vertrieb": ("Dienstleister für den Vertrieb", "lieferanten", "Dienstleister", "Leistung", "Kreditor"),
    "kunden": ("Kunden in den Aufgaben", "kunden", "Kunde", "Kauft", "Debitor"),
    "anlagen": ("Lieferanten für Anlagegüter", "lieferanten", "Lieferant", "Liefert", "Kreditor"),
    "anlagenkaeufer": ("Käufer gebrauchter Anlagegüter", "kunden", "Käufer", "Kauft", "Debitor"),
}


def lade(datei=None):
    p = Path(datei or DATEI)
    return (yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else None) or {}


def tabellen(gruppen=("einkauf", "vertrieb", "kunden"), daten=None):
    """Markdown für die Seite „Unternehmen“ (Abschnitte mit Tabellen und Hinweis zu den Sammelkonten)."""
    d = daten or lade()
    z = []
    for g in gruppen:
        titel, schluessel, spalte1, spalte2, nummer = GRUPPEN[g]
        if g == "kunden":
            eintraege = [e for e in d.get("kunden") or [] if e.get("gruppe") != "anlagen"]
        elif g == "anlagenkaeufer":
            eintraege = [e for e in d.get("kunden") or [] if e.get("gruppe") == "anlagen"]
        else:
            eintraege = [e for e in d.get(schluessel) or [] if e.get("gruppe") == g]
        if not eintraege:
            continue
        z += [f"## {titel}", "", f"| {spalte1} | {spalte2} | {nummer} |", "| --- | --- | --- |"]
        for e in eintraege:
            ort = str(e.get("plz_ort", "")).split(" ", 1)[-1] if e.get("plz_ort") else ""
            nr = e.get("kreditor") or e.get("debitor") or ""
            was = e.get("liefert") or e.get("kauft") or ""
            z.append(f"| {e['name']}, {ort} | {was} | {nr} |" if ort else f"| {e['name']} | {was} | {nr} |")
        z.append("")
        if g in ("kunden", "anlagenkaeufer"):
            z += ["Die Debitorennummern stehen nur auf den Belegen. Gebucht wird in den Aufgaben auf dem Sammelkonto "
                  "**2400 Forderungen a. L. L.**", ""]
        elif g == "anlagen" or g == "vertrieb" or (g == "einkauf" and "vertrieb" not in gruppen):
            z += ["Die Kreditorennummern stehen nur auf den Belegen. Gebucht wird in den Aufgaben auf dem Sammelkonto "
                  "**4400 Verbindlichkeiten a. L. L.**", ""]
    return "\n".join(z).rstrip() + "\n"


def naechste(art, daten=None):
    d = daten or lade()
    feld, liste = ("kreditor", d.get("lieferanten")) if art == "kreditor" else ("debitor", d.get("kunden"))
    nummern = [int(e[feld]) for e in liste or [] if e.get(feld)]
    return str(max(nummern) + 10 if nummern else (44010 if art == "kreditor" else 20010))


def pruefe_pfad(ordner, daten=None):
    """Hinweise zu Firmennamen und Anschriften in den Belegen (module/, fragen/)."""
    d = daten or lade()
    firmen = {}
    for e in (d.get("lieferanten") or []) + (d.get("kunden") or []):
        firmen[e["name"]] = e
    u = d.get("unternehmen") or {}
    eigene = {u.get("name", ""), u.get("bank", "")} - {""}
    hinweise = []
    ordner = Path(ordner)
    for sub, muster in (("module", "*.md"), ("fragen", "*.yaml")):
        for f in sorted((ordner / sub).glob(muster)):
            text = f.read_text(encoding="utf-8")
            # absender_zeile: Name · Straße · PLZ Ort
            for m in re.finditer(r"absender_zeile:\s*(.+)", text):
                teile = [t.strip().strip("\"'") for t in m.group(1).split("·")]
                hinweise += _vergleiche(f.name, teile, firmen, eigene)
            # empfaenger: [Name, Straße, PLZ Ort]
            for m in re.finditer(r"empfaenger:\s*\[([^\]]+)\]", text):
                teile = [t.strip().strip("\"'") for t in m.group(1).split(",")]
                hinweise += _vergleiche(f.name, teile, firmen, eigene)
    return sorted(set(hinweise))


def _vergleiche(datei, teile, firmen, eigene):
    name = teile[0] if teile else ""
    if not name or name in eigene or any(name.startswith(e) for e in eigene if e):
        return []
    e = firmen.get(name) or next((v for k, v in firmen.items() if k in name), None)
    if e is None:
        return [f"{datei}: „{name}“ steht nicht in stammdaten.yaml (neue Firma? zuerst dort eintragen)"]
    out = []
    if e.get("strasse") and len(teile) > 1 and teile[1] != e["strasse"] and not teile[1][:1].isdigit():
        out.append(f"{datei}: Anschrift von „{e['name']}“ weicht ab: Beleg „{teile[1]}“, Stammdaten „{e['strasse']}“")
    if e.get("plz_ort") and len(teile) > 2 and teile[2] != e["plz_ort"]:
        out.append(f"{datei}: Ort von „{e['name']}“ weicht ab: Beleg „{teile[2]}“, Stammdaten „{e['plz_ort']}“")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seite", action="store_true")
    ap.add_argument("--gruppen", nargs="+", choices=list(GRUPPEN), default=["einkauf", "vertrieb", "kunden"])
    ap.add_argument("--naechste", choices=["kreditor", "debitor"])
    ap.add_argument("--pruefen", metavar="ORDNER")
    a = ap.parse_args(argv)
    if a.naechste:
        print(naechste(a.naechste))
        return 0
    if a.pruefen:
        h = pruefe_pfad(a.pruefen)
        for x in h:
            print("  !", x)
        print(f"✓ Stammdaten-Abgleich: {len(h)} Hinweis(e)." if h else "✓ Alle Firmen und Anschriften in den Belegen passen zu den Stammdaten.")
        return 0
    if a.seite:
        print(tabellen(a.gruppen))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
