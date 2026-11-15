#!/usr/bin/env python3
"""Buchungsprüfung für einen Fibu-Übungspfad – das „Gedächtnis“ des Baukastens für Buchungstechnik.

  python3 skripte/buchungspruefung.py <ordner> [--muster buchungsmuster.yaml] [--lernen] [--proben 40]

Was geprüft wird (jede Aufgabe mit mehreren zufälligen Zahlen, nicht nur mit den Startwerten):
  1. Soll = Haben in jedem Buchungssatz (typ buchung, saetze, T-Konten mit Ausgleich) – Fehler (✗)
  2. Beträge: höchstens zwei Nachkommastellen, nie null oder negativ – Fehler (✗)
  3. Buchungssätze der richtigen Testantworten (single/multiple choice) gehen auf – Fehler (✗)
  4. Jeder Buchungssatz wird mit dem Wissensspeicher `buchungsmuster.yaml` verglichen: Kennt der Baukasten dieses Muster
     aus früheren, geprüften Themen? Unbekannte Muster stehen als „NEU“ in der Liste (!). Sie müssen gegen Lösungsvorschläge
     der Lehrkraft geprüft werden. Mit --lernen kommen sie als status: neu in die Musterdatei; erst nach der Bestätigung durch
     die Lehrkraft setzt man status: verifiziert und trägt Namen und Quelle ein.
  5. Muster mit status: neu in der Aufgabe stehen im Bericht als offen, bis sie bestätigt sind.

Die Musterdatei wächst mit jedem Thema. So lernt der Baukasten die Buchungstechnik immer besser: Was einmal geprüft ist,
wird nie wieder angezweifelt, und was neu ist, fällt sofort auf.
"""
import argparse
import glob
import random
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bausteine as B  # noqa: E402

ROLLEN = [  # Kontonummer-Muster → Rolle im Buchungssatz (IKR, Werkstoffkonten mit Unterkonten)
    (r"2(000|010|020|030|280)", "BESTAND"), (r"2(001|011|021|031|281)", "BEZUG_B"), (r"2(002|012|022|032|282)", "NACHL_B"),
    (r"6(000|010|020|030|080)", "AUFW"), (r"6(001|011|021|031|081)", "BEZUG_A"), (r"6(002|012|022|032|082)", "NACHL_A"),
    (r"2600", "VST"), (r"4800", "UST"), (r"4400", "VERB"), (r"2400", "FORD"), (r"2800", "BANK"), (r"2880", "KASSE"),
    (r"8000", "EBK"), (r"8010", "SBK"), (r"8020", "GUV"), (r"5(001|101)", "ERLBER"), (r"5[01]\d\d", "ERLOES"),
    (r"6040", "VERPACK"), (r"6140", "FRACHT"), (r"6150", "PROVISION"),
]


def rolle(nr):
    nr = str(nr)
    for muster, name in ROLLEN:
        if re.fullmatch(muster, nr):
            return name
    return nr


def schluessel(soll, haben):
    """Buchungssatz → Mustername wie 'S:AUFW+VST > H:VERB' (Rollen statt Kontonummern, sortiert)."""
    return "S:" + "+".join(sorted(rolle(k) for k in soll)) + " > H:" + "+".join(sorted(rolle(k) for k in haben))


def proben(par, n):
    for i in range(n):
        v = {}
        for k, x in par.items():
            if i == 0 and x.get("start") is not None:
                v[k] = x["start"]
                continue
            lo, hi, st = x["von"], x["bis"], x.get("schritt", 1)
            v[k] = lo + st * random.randint(0, int(round((hi - lo) / st)))
        yield v


def wert(f, v):
    return B.formel_wert(str(f), v)


class Bericht:
    def __init__(self):
        self.fehler, self.neu, self.offen, self.geprueft, self.saetze = [], {}, {}, 0, 0

    def f(self, text):
        if text not in self.fehler:
            self.fehler.append(text)


def betraege(text):
    return [float(x.replace(".", "").replace(",", ".")) for x in re.findall(r"(\d{1,3}(?:\.\d{3})*,\d{2}) €", text)]


def kontos_aus_text(teil):
    return re.findall(r"(?:^|\bund )(\d{4}) ", teil.strip())


def pruefe_uebung(d, wo, kurs, bekannt, b, n):
    par = d.get("parameter") or {}
    for idx, v in enumerate(proben(par, n)):
        b.geprueft += 1
        def s(z):
            return round(sum(wert(x["betrag"], v) for x in z), 2)
        paare = []
        if d["typ"] == "buchung":
            paare = [(d["titel"], d.get("soll"), d.get("haben"))] if not d.get("saetze") else \
                [(x.get("text", d["titel"]), x["soll"], x["haben"]) for x in d["saetze"]]
        elif d["typ"] == "konten":
            for tk in d["t_konten"]:
                so = sum(wert(x["betrag"], v) for x in tk.get("soll") or [])
                ha = sum(wert(x["betrag"], v) for x in tk.get("haben") or [])
                au = sum(wert(x["betrag"], v) for x in tk["ausgleich"]["zeilen"])
                if tk["ausgleich"]["seite"] == "soll":
                    so += au
                else:
                    ha += au
                if round(so, 2) != round(ha, 2):
                    b.f(f"{wo} „{d['titel']}“: T-Konto {tk['konto']} geht nicht auf bei {v} (Soll {so:.2f}, Haben {ha:.2f})")
            paare = [(x.get("text", d["titel"]), x["soll"], x["haben"]) for x in d.get("saetze") or []]
        elif d["typ"] == "rechnen":
            vv = dict(v)
            for fl in d["felder"]:
                if fl.get("formel") is None:
                    continue
                r = wert(fl["formel"], vv)
                if fl.get("runden") is None and abs(r * 100 - round(r * 100)) > 1e-6:
                    b.f(f"{wo} „{d['titel']}“: {fl['label']} hat bei {v} mehr als zwei Nachkommastellen ({r})")
                if r <= 0:
                    b.f(f"{wo} „{d['titel']}“: {fl['label']} ist bei {v} nicht positiv ({r})")
                if fl.get("id"):
                    vv[fl["id"]] = round(r, int(fl["runden"]) if fl.get("runden") is not None else 2)
        for ti, so, ha in paare:
            if s(so) != s(ha):
                b.f(f"{wo} „{d['titel']}“ – {ti}: Soll {s(so):.2f} ≠ Haben {s(ha):.2f} bei {v}")
            for z in list(so) + list(ha):
                if wert(z["betrag"], v) <= 0:
                    b.f(f"{wo} „{d['titel']}“ – {ti}: Betrag {z['betrag']} ist bei {v} nicht positiv")
            if idx == 0:
                key = schluessel([z["konto"] for z in so], [z["konto"] for z in ha])
                b.saetze += 1
                merke(key, f"{wo} „{d['titel']}“ – {ti}", bekannt, b)


def merke(key, wo, bekannt, b):
    m = bekannt.get(key)
    if not m:
        b.neu.setdefault(key, []).append(wo)
    elif m.get("status") != "verifiziert":
        b.offen.setdefault(key, []).append(wo)


def lies_module(ordner, kurs):
    for datei in sorted(glob.glob(str(ordner / "module" / "*.md"))):
        t = open(datei, encoding="utf-8").read()
        for m in re.finditer(r"^:::uebung\n(.*?)^:::\n", t, re.S | re.M):
            d, fehler = B.lies_uebung(m.group(1), kurs.get("kontenplan"))
            yield Path(datei).name, d, fehler


def pruefe_fragen(ordner, bekannt, b):
    for datei in sorted(glob.glob(str(ordner / "fragen" / "*.yaml"))):
        for a in yaml.safe_load(open(datei, encoding="utf-8")) or []:
            if a.get("typ") in ("single_choice", "multiple_choice"):
                for o in a.get("optionen") or []:
                    teile = re.split(r" an (?=\d{4} )", str(o["text"]))
                    if len(teile) != 2:
                        continue
                    s_, h_ = betraege(teile[0]), betraege(teile[1])
                    if s_ and h_ and abs(sum(s_) - sum(h_)) > 0.005 and o.get("korrekt"):   # Antworten ohne Beträge auf einer Seite überspringen
                        b.f(f"Frage {a.get('id')}: richtige Antwort geht nicht auf (Soll {sum(s_):.2f}, Haben {sum(h_):.2f})")
                    if o.get("korrekt"):
                        key = schluessel(kontos_aus_text(teile[0]), kontos_aus_text(teile[1]))
                        merke(key, f"Test {a.get('id')} – richtige Antwort", bekannt, b)
            elif a.get("typ") == "zahl":
                par = {k: {"von": x["min"], "bis": x["max"], "schritt": x.get("schritt", 1)} for k, x in (a.get("parameter") or {}).items()}
                for v in proben(par, 20):
                    for an in a.get("antworten") or []:
                        r = wert(an["formel"], v)
                        if an.get("runden") is None and abs(r * 100 - round(r * 100)) > 1e-6:
                            b.f(f"Frage {a.get('id')}: {an.get('label')} hat bei {v} mehr als zwei Nachkommastellen")
                        if r <= 0:
                            b.f(f"Frage {a.get('id')}: {an.get('label')} ist bei {v} nicht positiv")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ordner")
    ap.add_argument("--muster", default=str(Path(__file__).resolve().parent.parent / "buchungsmuster.yaml"))
    ap.add_argument("--lernen", action="store_true", help="unbekannte Muster als status: neu in die Musterdatei schreiben")
    ap.add_argument("--proben", type=int, default=40)
    a = ap.parse_args(argv)
    ordner = Path(a.ordner)
    kurs = yaml.safe_load(open(ordner / "kurs.yaml", encoding="utf-8"))
    mfile = Path(a.muster)
    muster = yaml.safe_load(open(mfile, encoding="utf-8")) if mfile.exists() else []
    bekannt = {m["muster"]: m for m in muster or []}
    b = Bericht()
    for name, d, fehler in lies_module(ordner, kurs):
        if fehler:
            b.f(f"{name}: Übung fehlerhaft – {'; '.join(fehler)}")
            continue
        pruefe_uebung(d, name, kurs, bekannt, b, a.proben)
    pruefe_fragen(ordner, bekannt, b)
    print(f"Buchungsprüfung: {b.geprueft} Belegungen, {b.saetze} Buchungssätze, {len(bekannt)} bekannte Muster")
    for f in b.fehler:
        print("  ✗", f)
    for k, w in sorted(b.neu.items()):
        print(f"  ! NEU {k}  ({w[0]}{' …' if len(w) > 1 else ''}) – bitte gegen Lösungsvorschlag prüfen")
    for k, w in sorted(b.offen.items()):
        print(f"  · offen (status: neu) {k}  ({w[0]})")
    if a.lernen and b.neu:
        muster = list(muster or []) + [{"muster": k, "name": "", "quelle": w[0], "status": "neu", "thema": ordner.name}
                                       for k, w in sorted(b.neu.items())]
        mfile.write_text(yaml.safe_dump(muster, allow_unicode=True, sort_keys=False), encoding="utf-8")
        print(f"  → {len(b.neu)} neue Muster in {mfile} eingetragen (status: neu)")
    if b.fehler:
        print(f"✗ {len(b.fehler)} Fehler")
        return 1
    print("✓ Keine Rechenfehler" + (f", {len(b.neu)} neue Muster zu prüfen" if b.neu else ", alle Muster bekannt"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
