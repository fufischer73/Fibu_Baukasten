#!/usr/bin/env python3
"""Erzeugt die Seite „Kontenübersicht“ eines Lernpfads aus den Konten, die er wirklich verwendet.

  python3 skripte/kontenuebersicht.py <ordner>              Vorschau auf dem Bildschirm
  python3 skripte/kontenuebersicht.py <ordner> --schreiben  seiten/kontenuebersicht.md schreiben (ersetzt die Datei!)

Die Bezeichnungen kommen aus dem zentralen Kontenplan (kontenplan.yaml). Die Spalte „Wofür?“ entsteht aus dem Eintrag
`konten_hinweise:` in der kurs.yaml (Kontonummer in Anführungszeichen → kurzer Satz). Gibt es keinen Hinweis, entfällt die
Spalte. Die Seite selbst zählt bei der Suche nicht mit.
"""
import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import konten as K  # noqa: E402

GRUPPEN = [("bestand", "Bestandskonten"), ("erfolg", "Erfolgskonten"), ("abschluss", "Abschlusskonten")]


def erzeuge(ordner, beschreibung="Die Konten, die du in den Aufgaben brauchst."):
    ordner = Path(ordner)
    kurs = yaml.safe_load((ordner / "kurs.yaml").read_text(encoding="utf-8")) or {}
    hinweise = {str(a): str(b) for a, b in (kurs.get("konten_hinweise") or {}).items()}
    index = K.plan_index()
    gesamt = {**{nr: k["name"] for nr, k in index.items()}, **{str(a): str(b) for a, b in (kurs.get("kontenplan") or {}).items()}}
    fund = K.finde_konten(ordner, gesamt, ohne=("kontenuebersicht.md",))
    unbekannt = sorted(nr for nr in fund if nr not in gesamt)
    benutzt = sorted(nr for nr in fund if nr in gesamt)
    zeilen = ["---", "titel: Kontenübersicht", 'icon: "📒"', f"beschreibung: {beschreibung}", "reihenfolge: 2", "---",
              "Diese Konten brauchst du in den Aufgaben. Der Auszug stammt aus dem Kontenplan deiner Lehrkraft.", ""]
    for art, titel in GRUPPEN:
        nrn = [nr for nr in benutzt if (index.get(nr, {}).get("art") or K.art_aus_nummer(nr)) == art]
        if not nrn:
            continue
        mit = any(nr in hinweise for nr in nrn)
        zeilen += [f"## {titel}", ""]
        zeilen += ["| Nr. | Bezeichnung | Wofür? |", "| --- | --- | --- |"] if mit else ["| Nr. | Bezeichnung |", "| --- | --- |"]
        for nr in nrn:
            name = gesamt[nr]
            zeilen.append(f"| {nr} | {name} | {hinweise.get(nr, '')} |" if mit else f"| {nr} | {name} |")
        zeilen.append("")
    return "\n".join(zeilen).rstrip() + "\n", unbekannt


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ordner")
    ap.add_argument("--schreiben", action="store_true")
    a = ap.parse_args(argv)
    text, unbekannt = erzeuge(a.ordner)
    if unbekannt:
        print(f"! Nicht im Kontenplan: {', '.join(unbekannt)} (zuerst kontenpruefung.py ausführen und aufnehmen)", file=sys.stderr)
    if a.schreiben:
        ziel = Path(a.ordner) / "seiten" / "kontenuebersicht.md"
        ziel.parent.mkdir(exist_ok=True)
        ziel.write_text(text, encoding="utf-8")
        print(f"✓ {ziel} geschrieben")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
