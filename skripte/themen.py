#!/usr/bin/env python3
"""Themenübersicht: Welche Themen sind im Baukasten gebaut, wie viel gesichertes Buchungswissen gehört dazu?

  python3 skripte/themen.py               Übersicht auf dem Bildschirm
  python3 skripte/themen.py --schreiben   THEMEN.md neu erzeugen

Quellen: themen.yaml (von Hand gepflegt) und buchungsmuster.yaml (Muster je Thema, Feld `thema`).
Muster ohne passendes Thema werden am Ende gemeldet.
"""
import argparse
import sys
from collections import Counter
from pathlib import Path

import yaml

HAUPT = Path(__file__).resolve().parent.parent
STAND = {"offen": "offen", "material": "Material liegt vor", "im_bau": "im Bau", "gebaut": "gebaut", "freigegeben": "freigegeben"}


def lade(name):
    p = HAUPT / name
    return (yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else None) or ({} if name.endswith("yaml") and name == "themen.yaml" else [])


def tabelle():
    themen = (lade("themen.yaml") or {}).get("themen") or []
    muster = lade("buchungsmuster.yaml") or []
    ok, neu = Counter(), Counter()
    for m in muster:
        (ok if m.get("status") == "verifiziert" else neu)[str(m.get("thema") or "")] += 1
    zeilen = ["| Thema | Lernfeld | Stand | Repository | Muster bestätigt | Muster offen | Hinweis |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for t in themen:
        zeilen.append(f"| {t['titel']} | {t.get('lernfeld') or '–'} | {STAND.get(t.get('stand'), t.get('stand'))}"
                      f"{' (' + t['datum'] + ')' if t.get('datum') else ''} | {t.get('repository') or '–'} | "
                      f"{ok.get(t['id'], 0)} | {neu.get(t['id'], 0)} | {t.get('hinweis') or ''} |")
    ids = {t["id"] for t in themen}
    ohne = sorted({k for k in list(ok) + list(neu) if k not in ids})
    return "\n".join(zeilen), ohne, sum(ok.values()), sum(neu.values())


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--schreiben", action="store_true")
    a = ap.parse_args(argv)
    tab, ohne, ok, neu = tabelle()
    text = ("# Themenübersicht\n\n"
            "Welche Themen der Baukasten schon kennt und wie viel gesichertes Buchungswissen (`buchungsmuster.yaml`) dazugehört.\n"
            "Diese Datei wird von `python3 skripte/themen.py --schreiben` erzeugt. Gepflegt wird `themen.yaml`.\n\n"
            f"{tab}\n\n"
            f"**Gesamt:** {ok} bestätigte Buchungsmuster, {neu} offene (Status „neu“).\n\n"
            "## So kommt ein neues Thema dazu\n\n"
            "1. Material sammeln (MATERIAL-CHECKLISTE.md). Eintrag in `themen.yaml` mit `stand: material`.\n"
            "2. Konten prüfen: `python3 skripte/kontenpruefung.py --liste …`. Fehlende Konten der Lehrkraft vorlegen.\n"
            "3. Buchungssätze aus den Lösungen aufnehmen (`skripte/wissen_aufnehmen.py`) und von der Lehrkraft bestätigen lassen.\n"
            "4. Pfad bauen (SKILL.md). `stand: im_bau`, danach `gebaut` und nach der Freigabe `freigegeben`.\n"
            "5. `python3 skripte/themen.py --schreiben`.\n")
    if ohne:
        text += f"\n> Muster ohne Eintrag in `themen.yaml`: {', '.join(x or '(kein Thema)' for x in ohne)}\n"
    if a.schreiben:
        (HAUPT / "THEMEN.md").write_text(text, encoding="utf-8")
        print("✓ THEMEN.md geschrieben")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
