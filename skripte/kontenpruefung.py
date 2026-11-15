#!/usr/bin/env python3
"""Kontenprüfung: Stehen alle Konten eines Lernpfads (oder eines Materials) im zentralen Kontenplan?

  python3 skripte/kontenpruefung.py <ordner>                       Konten im Lernpfad gegen kontenplan.yaml prüfen
  python3 skripte/kontenpruefung.py --liste 5001 5101="Erlösberichtigungen f. Waren" 6040
                                                                    Konten aus Material (Lehrbuch, Aufgaben, Lösungen) prüfen
  python3 skripte/kontenpruefung.py --aufnehmen 5001="Erlösberichtigungen" --quelle "LS 53" [--bestaetigt]
                                                                    neue Konten in kontenplan.yaml eintragen (Status „neu“)
  python3 skripte/kontenpruefung.py --bestaetigen 5001 5101        Status „neu“ → „verifiziert“ (nach Bestätigung der Lehrkraft)

Gemeldet wird:
  ✗ Konto fehlt im Plan   (Fehler: Rückgabewert 1)
  ! Bezeichnung weicht ab (Hinweis: Schulplan gilt, IKR ergänzt nur fehlende Konten)
  ! Konto hat Status „neu“ (noch nicht von der Lehrkraft bestätigt)
  ! Eintrag nur in kurs.yaml  (gehört in den zentralen Plan, wenn er allgemein gilt)

Beim Material gilt: Erst die Liste prüfen, dann der Lehrkraft die fehlenden Konten vorlegen („Fehlen in deinem Kontenplan: …,
Bezeichnung laut Lösungen: …. Soll ich sie aufnehmen?“), erst danach --aufnehmen und --bestaetigen.
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import konten as K  # noqa: E402


def _kurs_plan(ordner):
    p = Path(ordner) / "kurs.yaml"
    if not p.exists():
        return {}
    d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return {str(a): str(b) for a, b in (d.get("kontenplan") or {}).items()}


def pruefe_pfad(ordner):
    """→ (fehler, hinweise, benutzt)"""
    index = K.plan_index()
    plan = {nr: k["name"] for nr, k in index.items()}
    inline = _kurs_plan(ordner)
    gesamt = {**plan, **inline}
    fehler, hinweise = [], []
    if not index:
        return ["kontenplan.yaml fehlt oder ist leer"], [], {}
    fund = K.finde_konten(ordner, gesamt)
    for nr in sorted(fund):
        e = fund[nr]
        wo = ", ".join(sorted(e["dateien"]))
        if nr not in gesamt:
            fehler.append(f"Konto {nr} fehlt im Kontenplan (vorkommend in: {wo})")
            continue
        k = index.get(nr)
        if k is None:   # nur in kurs.yaml
            hinweise.append(f"Konto {nr} „{inline[nr]}“ steht nur in kurs.yaml, nicht im zentralen Plan (in: {wo})")
            continue
        if k.get("status") == "neu":
            hinweise.append(f"Konto {nr} „{k['name']}“ hat Status „neu“: noch nicht von der Lehrkraft bestätigt (in: {wo})")
        # Tabellen (zum Beispiel die Kontenübersicht) müssen die Bezeichnung genau tragen
        erlaubt = {n.lower() for n in K.namen(k)}
        falsch_tab = sorted(n for n in e["tabellen"] if n.strip().lower() not in erlaubt)
        if falsch_tab:
            hinweise.append(f"Konto {nr}: Bezeichnung in einer Tabelle weicht ab. Plan: „{k['name']}“, gefunden: „{falsch_tab[0]}“ (in: {wo})")
        # Im Fließtext reicht es, wenn die Bezeichnung irgendwo stimmt (dort stehen oft Kurzformen und Erklärungen)
        texte = [n for n in e["namen"] if n]
        if texte and not any(K.name_passt(n, k) for n in texte):
            hinweise.append(f"Konto {nr}: im Text keine passende Bezeichnung gefunden. Plan: „{k['name']}“, gefunden: „{texte[0][:40]}“ (in: {wo})")
    # Konten, die in Aufgaben vorkommen, aber auf der Seite „Kontenübersicht“ fehlen (Schüler:innen suchen sie dort)
    if (Path(ordner) / "seiten" / "kontenuebersicht.md").exists():
        auf_seite = {nr for nr, e in fund.items() if "kontenuebersicht.md" in e["dateien"]}
        fehlen = sorted(nr for nr, e in fund.items() if nr in gesamt and nr not in auf_seite and (e["dateien"] - {"kontenuebersicht.md"}))
        if fehlen:
            hinweise.append("Kontenübersicht: " + ", ".join(f"{nr} {gesamt[nr]}" for nr in fehlen) +
                            " kommt/kommen in Aufgaben vor, steht/stehen aber nicht auf der Seite "
                            "(kontenuebersicht.py erzeugt sie aus den verwendeten Konten)")
    for nr, name in inline.items():
        k = index.get(nr)
        if k and name != k["name"] and name not in k.get("alias", []):
            hinweise.append(f"kurs.yaml: Konto {nr} heißt dort „{name}“, im zentralen Plan „{k['name']}“")
    return fehler, hinweise, fund


def pruefe_liste(eintraege):
    """eintraege: ['5001', '5101=Erlösberichtigungen f. Waren', …] → (fehler, hinweise, ok, fehlende_roh)"""
    index = K.plan_index()
    fehler, hinweise, ok, fehlende = [], [], [], []
    for e in eintraege:
        nr, _, name = e.partition("=")
        nr = nr.strip()
        k = index.get(nr)
        if k is None:
            fehler.append(f"Konto {nr}" + (f" („{name}“)" if name else "") + " fehlt im Kontenplan")
            fehlende.append(e)
            continue
        text = f"{nr} {k['name']}"
        if k.get("status") == "neu":
            hinweise.append(f"Konto {nr} „{k['name']}“ hat Status „neu“ (noch nicht bestätigt)")
        if name and not K.name_passt(name, k):
            hinweise.append(f"Konto {nr}: Material nennt „{name}“, Plan: „{k['name']}“ (Schulplan gilt)")
        ok.append(text)
    return fehler, hinweise, ok, fehlende


def aufnehmen(eintraege, quelle, bestaetigt):
    index = K.plan_index()
    status = "verifiziert" if bestaetigt else "neu"
    zeilen, doppelt = [], []
    for e in eintraege:
        nr, _, name = e.partition("=")
        nr, name = nr.strip(), name.strip()
        if not re.fullmatch(r"\d{4}", nr) or not name:
            sys.exit(f"✗ „{e}“: erwartet Nummer=Bezeichnung (vierstellige Nummer)")
        if nr in index:
            doppelt.append(nr)
            continue
        zeilen.append(K.eintrag_zeile(nr, name, K.art_aus_nummer(nr), quelle, status))
    if doppelt:
        print(f"! schon im Plan, übersprungen: {', '.join(doppelt)}")
    if not zeilen:
        return
    text = K.PLAN_DATEI.read_text(encoding="utf-8").rstrip("\n")
    K.PLAN_DATEI.write_text(text + "\n" + "\n".join(zeilen) + "\n", encoding="utf-8")
    print(f"✓ {len(zeilen)} Konto/Konten in {K.PLAN_DATEI.name} eingetragen (Status {status}).")
    if not bestaetigt:
        print("  Bitte der Lehrkraft vorlegen und nach der Bestätigung:  python3 skripte/kontenpruefung.py --bestaetigen "
              + " ".join(e.partition("=")[0] for e in eintraege))


def bestaetigen(nummern):
    text = K.PLAN_DATEI.read_text(encoding="utf-8")
    geaendert = []
    for nr in nummern:
        muster = re.compile(r'^(  - \{nr: "' + re.escape(nr) + r'",.*?status: )neu(\}\s*)$', re.M)
        text, n = muster.subn(r"\1verifiziert\2", text)
        (geaendert if n else []).append(nr)
        if not n:
            print(f"! {nr}: kein Eintrag mit Status „neu“ gefunden")
    if geaendert:
        K.PLAN_DATEI.write_text(text, encoding="utf-8")
        print(f"✓ bestätigt (verifiziert, {date.today().isoformat()}): {', '.join(geaendert)}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ordner", nargs="?", help="Ordner des Lernpfads")
    ap.add_argument("--liste", nargs="+", metavar="NR[=NAME]", help="Konten aus Material prüfen")
    ap.add_argument("--aufnehmen", nargs="+", metavar="NR=NAME", help="neue Konten in den Plan eintragen")
    ap.add_argument("--quelle", default="Material der Lehrkraft", help="Quelle für --aufnehmen")
    ap.add_argument("--bestaetigt", action="store_true", help="--aufnehmen: sofort als verifiziert eintragen (Lehrkraft hat bestätigt)")
    ap.add_argument("--bestaetigen", nargs="+", metavar="NR", help="Status „neu“ → „verifiziert“")
    a = ap.parse_args(argv)

    if a.aufnehmen:
        return aufnehmen(a.aufnehmen, a.quelle, a.bestaetigt) or 0
    if a.bestaetigen:
        return bestaetigen(a.bestaetigen) or 0
    if a.liste:
        fehler, hinweise, ok, fehlende = pruefe_liste(a.liste)
        for o in ok:
            print(f"  ✓ {o}")
        for h in hinweise:
            print(f"  ! {h}")
        for f in fehler:
            print(f"  ✗ {f}")
        if fehler:
            print(f"\n{len(fehler)} Konto/Konten fehlen. Der Lehrkraft vorlegen, dann:\n"
                  f"  python3 skripte/kontenpruefung.py --aufnehmen {' '.join(chr(34) + e + chr(34) if '=' in e else e for e in fehlende)} --quelle \"…\"")
        else:
            print("\n✓ Alle Konten stehen im Kontenplan.")
        return 1 if fehler else 0
    if not a.ordner:
        ap.error("Ordner des Lernpfads oder --liste angeben")
    fehler, hinweise, fund = pruefe_pfad(a.ordner)
    for h in hinweise:
        print(f"  ! {h}")
    for f in fehler:
        print(f"  ✗ {f}")
    if fehler:
        print(f"✗ {len(fehler)} Konto/Konten fehlen im Plan ({len(fund)} verwendet), {len(hinweise)} Hinweis(e).")
    else:
        print(f"✓ Alle {len(fund)} verwendeten Konten stehen im Kontenplan" + (f", {len(hinweise)} Hinweis(e)." if hinweise else "."))
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
