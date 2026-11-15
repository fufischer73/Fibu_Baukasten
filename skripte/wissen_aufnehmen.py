#!/usr/bin/env python3
"""Wissen aufnehmen: Buchungssätze aus Material (Lösungen, Aufgaben, Lehrbuch) in den Wissensspeicher übernehmen,
auch ohne einen Lernpfad zu bauen.

Ablauf (siehe SKILL.md, „Wissen aufnehmen“):
  1. Claude liest das Material und schreibt die Buchungssätze in eine Datei `aufnahme.yaml` (Vorlage: vorlage-aufnahme.yaml).
  2. python3 skripte/wissen_aufnehmen.py aufnahme.yaml          Prüfen: bekannt, neu, Widerspruch, fehlende Konten, Soll = Haben
  3. Die Lehrkraft bestätigt die neuen Muster (anhand der Lösungen).
  4. python3 skripte/wissen_aufnehmen.py aufnahme.yaml --eintragen [--bestaetigt]
     trägt neue Muster in buchungsmuster.yaml ein (Status „neu“, mit --bestaetigt sofort „verifiziert“).
  5. python3 skripte/wissen_aufnehmen.py --bestaetigen "S:… > H:…" [--name "…"]   Status „neu“ → „verifiziert“.
  6. Lernprotokoll in BUCHUNGSWISSEN.md ergänzen.

Was geprüft wird:
  ✗ Konto fehlt im Kontenplan   → vorher python3 skripte/kontenpruefung.py --aufnehmen …
  ✗ Soll ≠ Haben                → nur wenn `betraege` angegeben ist
  ✗ Widerspruch                 → derselbe Vorgang (Name und Technik) ist als bestätigtes Muster schon anders gespeichert.
                                  Dann gilt, was die Lehrkraft entscheidet; bis dahin wird nichts eingetragen.
  i Umkehrung von …             → der Satz ist das Gegenstück zu einem bekannten Muster (zum Beispiel Gutschrift zur Rechnung)
  · bekannt / offen             → schon gespeichert (bestätigt bzw. Status „neu“)
"""
import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import konten as K  # noqa: E402
from buchungspruefung import schluessel  # noqa: E402

MUSTER_DATEI = Path(os.environ.get("FIBU_MUSTER") or Path(__file__).resolve().parent.parent / "buchungsmuster.yaml")   # Umgebungsvariable nur für Tests


def lade_muster(datei=None):
    p = Path(datei or MUSTER_DATEI)
    return (yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else None) or []


def umkehrung(key):
    m = re.fullmatch(r"S:(.*) > H:(.*)", key)
    return f"S:{m.group(2)} > H:{m.group(1)}" if m else key


def pruefe(aufnahme, muster):
    """→ Liste von Ergebnissen (dict: satz, key, art ('bekannt'|'offen'|'neu'|'widerspruch'|'fehler'), text)"""
    plan = K.plan_dict()
    bekannt = {m["muster"]: m for m in muster}
    ergebnisse = []
    gesehen = {}
    for i, s in enumerate(aufnahme.get("saetze") or [], 1):
        name = str(s.get("name") or f"Satz {i}")
        soll = [str(x) for x in s.get("soll") or []]
        haben = [str(x) for x in s.get("haben") or []]
        r = {"satz": s, "name": name, "key": None, "art": None, "meldungen": []}
        ergebnisse.append(r)
        if not soll or not haben:
            r["art"] = "fehler"
            r["meldungen"].append("✗ Soll und Haben müssen Konten enthalten")
            continue
        fehlend = [k for k in soll + haben if k not in plan]
        if fehlend:
            r["art"] = "fehler"
            r["meldungen"].append(f"✗ Konto fehlt im Kontenplan: {', '.join(sorted(set(fehlend)))} "
                                  "(vorher kontenpruefung.py --aufnehmen)")
            continue
        bt = s.get("betraege")
        if bt:
            bs, bh = bt.get("soll") or [], bt.get("haben") or []
            if len(bs) != len(soll) or len(bh) != len(haben):
                r["art"] = "fehler"
                r["meldungen"].append("✗ betraege: je Konto ein Betrag (gleiche Anzahl wie soll und haben)")
                continue
            if round(sum(float(x) for x in bs), 2) != round(sum(float(x) for x in bh), 2):
                r["art"] = "fehler"
                r["meldungen"].append(f"✗ Soll ≠ Haben: {sum(float(x) for x in bs):.2f} ≠ {sum(float(x) for x in bh):.2f}")
                continue
        key = schluessel(soll, haben)
        r["key"] = key
        technik = str(s.get("technik") or "-")
        # Widerspruch: gleicher Vorgang (Name + Technik), aber ein anderes bestätigtes Muster
        for m in muster:
            if (m.get("status") == "verifiziert" and str(m.get("name", "")).strip().lower() == name.strip().lower()
                    and str(m.get("technik", "-")) == technik and m["muster"] != key):
                r["art"] = "widerspruch"
                r["meldungen"].append(f"✗ Widerspruch: „{name}“ ({technik}) ist bestätigt als {m['muster']} gespeichert, "
                                      f"das Material sagt {key}")
                break
        if r["art"]:
            continue
        if key in gesehen and gesehen[key] != name:
            r["meldungen"].append(f"i gleiches Muster wie „{gesehen[key]}“ in dieser Aufnahme")
        gesehen.setdefault(key, name)
        if key in bekannt:
            st = bekannt[key].get("status")
            r["art"] = "bekannt" if st == "verifiziert" else "offen"
            r["meldungen"].append(f"· {'bekannt' if st == 'verifiziert' else 'offen (Status neu)'}: {bekannt[key].get('name') or key}")
        else:
            r["art"] = "neu"
            u = umkehrung(key)
            if u in bekannt and bekannt[u].get("status") == "verifiziert":
                r["meldungen"].append(f"i Umkehrung von „{bekannt[u].get('name') or u}“ (zum Beispiel Gutschrift, Storno)")
    return ergebnisse


def eintragen(ergebnisse, aufnahme, bestaetigt_alle):
    muster_text = MUSTER_DATEI.read_text(encoding="utf-8").rstrip("\n") + "\n" if MUSTER_DATEI.exists() else ""
    neue, gesehen = [], set()
    for r in ergebnisse:
        if r["art"] != "neu" or r["key"] in gesehen:
            continue
        gesehen.add(r["key"])
        s = r["satz"]
        bestaetigt = bestaetigt_alle or bool(s.get("bestaetigt"))
        eintrag = {"muster": r["key"], "name": r["name"], "technik": str(s.get("technik") or "-"),
                   "quelle": str(s.get("quelle") or aufnahme.get("quelle") or "Material der Lehrkraft"),
                   "status": "verifiziert" if bestaetigt else "neu"}
        if aufnahme.get("thema"):
            eintrag["thema"] = str(aufnahme["thema"])
        neue.append(eintrag)
    if not neue:
        print("Nichts Neues einzutragen.")
        return 0
    MUSTER_DATEI.write_text(muster_text + yaml.safe_dump(neue, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"✓ {len(neue)} neue Muster in {MUSTER_DATEI.name} eingetragen "
          f"({sum(1 for n in neue if n['status'] == 'verifiziert')} verifiziert, {sum(1 for n in neue if n['status'] == 'neu')} neu).")
    print("  Nicht vergessen: Lernprotokoll in BUCHUNGSWISSEN.md ergänzen und, falls nötig, die Regeltabelle dort.")
    return 0


def bestaetigen(key, name=None, quelle=None):
    text = MUSTER_DATEI.read_text(encoding="utf-8")
    bloecke = re.split(r"(?m)^(?=- muster: )", text)
    gefunden = False
    for i, b in enumerate(bloecke):
        if re.match(r"- muster: " + re.escape(key) + r"\s*$", b.split("\n", 1)[0]):
            gefunden = True
            if not re.search(r"(?m)^  status: neu\s*$", b):
                print("! Das Muster hat schon den Status „verifiziert“ oder ist unbekannt formatiert.")
                return 1
            b = re.sub(r"(?m)^  status: neu\s*$", "  status: verifiziert", b)
            if name:
                b = re.sub(r"(?m)^  name: .*$", "  name: " + json.dumps(name, ensure_ascii=False), b, count=1)
            if quelle:
                b = re.sub(r"(?m)^  quelle: .*$", "  quelle: " + json.dumps(quelle, ensure_ascii=False), b, count=1)
            bloecke[i] = b
    if not gefunden:
        print(f"✗ Muster „{key}“ nicht gefunden.")
        return 1
    MUSTER_DATEI.write_text("".join(bloecke), encoding="utf-8")
    print(f"✓ bestätigt ({date.today().isoformat()}): {key}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("aufnahme", nargs="?", help="aufnahme.yaml mit den Buchungssätzen aus dem Material")
    ap.add_argument("--eintragen", action="store_true", help="neue Muster in buchungsmuster.yaml eintragen")
    ap.add_argument("--bestaetigt", action="store_true", help="--eintragen: die Lehrkraft hat alles bestätigt (Status verifiziert)")
    ap.add_argument("--bestaetigen", metavar="MUSTER", help="Status eines vorhandenen Musters von „neu“ auf „verifiziert“")
    ap.add_argument("--name")
    ap.add_argument("--quelle")
    a = ap.parse_args(argv)
    if a.bestaetigen:
        return bestaetigen(a.bestaetigen, a.name, a.quelle)
    if not a.aufnahme:
        ap.error("aufnahme.yaml angeben (Vorlage: vorlage-aufnahme.yaml)")
    aufnahme = yaml.safe_load(Path(a.aufnahme).read_text(encoding="utf-8")) or {}
    muster = lade_muster()
    ergebnisse = pruefe(aufnahme, muster)
    zahl = {"bekannt": 0, "offen": 0, "neu": 0, "widerspruch": 0, "fehler": 0}
    for r in ergebnisse:
        zahl[r["art"]] += 1
        marke = {"bekannt": "✓", "offen": "·", "neu": "!", "widerspruch": "✗", "fehler": "✗"}[r["art"]]
        titel = f"{marke} {r['name']}" + (f"   [{r['key']}]" if r["key"] else "")
        if r["art"] == "neu":
            titel = f"{marke} NEU: {r['name']}   [{r['key']}]"
        print(titel)
        for m in r["meldungen"]:
            print(f"    {m}")
    print(f"\n{len(ergebnisse)} Sätze: {zahl['bekannt']} bekannt, {zahl['offen']} offen, {zahl['neu']} neu, "
          f"{zahl['widerspruch']} Widersprüche, {zahl['fehler']} Fehler.")
    if zahl["widerspruch"] or zahl["fehler"]:
        print("✗ Erst Widersprüche und Fehler klären (Lehrkraft fragen), dann erneut prüfen. Es wird nichts eingetragen.")
        return 1
    if a.eintragen:
        return eintragen(ergebnisse, aufnahme, a.bestaetigt)
    if zahl["neu"]:
        print("Neue Muster der Lehrkraft vorlegen (Lösungsvorschlag?). Danach:  python3 skripte/wissen_aufnehmen.py "
              f"{a.aufnahme} --eintragen [--bestaetigt]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
