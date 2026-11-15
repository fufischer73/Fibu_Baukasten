#!/usr/bin/env python3
"""Legt ein neues Fibu-Thema aus der Vorlage an (zwei Stufen: „Schritt für Schritt“ und „Überprüfung“).

  python3 skripte/neues_thema.py <ordner> --thema "Buchungen im Absatzprozess" [--lernfeld 5] [--stunden 4]

Was passiert:
  1. Die Vorlage `vorlage-thema/` wird nach <ordner> kopiert.
  2. Die Platzhalter @@THEMA@@, @@KURZNAME@@, @@LERNFELD@@, @@STUNDEN@@ werden ersetzt.
  3. Danach läuft alles.py auf dem Ordner sofort durch (die Beispielinhalte sind lauffähig).

Die Beispielmodule (f1 = Schritt für Schritt, u1 = Überprüfung) zeigen den Aufbau. Claude ersetzt sie mit der Lehrkraft durch
den echten Inhalt – erst nach der Materialabfrage (MATERIAL-CHECKLISTE.md) und der Zusage zur Gliederung (SKILL.md).
"""
import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gemeinsam import slug  # noqa: E402

TEXT = {".yaml", ".yml", ".md", ".txt"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ordner", help="Zielordner (darf nicht existieren)")
    ap.add_argument("--thema", required=True, help='Titel, z. B. "Buchungen im Absatzprozess"')
    ap.add_argument("--kurzname", help="a-z, 0-9, Bindestrich (Standard: aus dem Titel)")
    ap.add_argument("--lernfeld", default="5")
    ap.add_argument("--stunden", default="4")
    a = ap.parse_args(argv)
    ziel = Path(a.ordner)
    if ziel.exists():
        sys.exit(f"✗ {ziel} gibt es schon. Bitte einen neuen Ordner angeben.")
    vorlage = Path(__file__).resolve().parent.parent / "vorlage-thema"
    if not vorlage.is_dir():
        sys.exit("✗ vorlage-thema/ fehlt.")
    kurz = a.kurzname or slug(a.thema)
    ersatz = {"@@THEMA@@": a.thema, "@@KURZNAME@@": kurz, "@@LERNFELD@@": str(a.lernfeld), "@@STUNDEN@@": str(a.stunden)}
    shutil.copytree(vorlage, ziel)
    for p in sorted(ziel.rglob("*")):
        if p.is_file() and p.suffix in TEXT:
            t = p.read_text(encoding="utf-8")
            for k, v in ersatz.items():
                if p.suffix in (".yaml", ".yml"):   # in Anführungszeichen stehende Werte: \\ und \" maskieren
                    v = v.replace("\\", "\\\\").replace('"', '\\"')
                t = t.replace(k, v)
            p.write_text(t, encoding="utf-8")
        if "@@KURZNAME@@" in p.name:
            p.rename(p.with_name(p.name.replace("@@KURZNAME@@", kurz)))
    print(f"✓ Neues Thema „{a.thema}“ angelegt: {ziel}  (kurzname: {kurz})")
    print("  Nächste Schritte:")
    print(f"   1. Material abfragen und lesen (MATERIAL-CHECKLISTE.md), Interview, Gliederung mit Zusage der Lehrkraft")
    print(f"   2. Beispielmodule ersetzen: {ziel}/module/f1.md (Schritt für Schritt) und u1.md (Überprüfung), Fragen in fragen/")
    print(f"   3. python3 skripte/pruefen.py {ziel}  und  python3 skripte/buchungspruefung.py {ziel}")
    print(f"   4. python3 skripte/alles.py {ziel} --entwuerfe")


if __name__ == "__main__":
    main()
