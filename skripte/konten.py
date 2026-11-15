"""Zentraler Kontenplan: laden, Konten in einem Lernpfad finden, mit dem Plan vergleichen.

Wird von gemeinsam.py (Kurs lädt den Plan), kontenpruefung.py und kontenuebersicht.py benutzt.
Die Datei kontenplan.yaml liegt im Hauptordner des Baukastens (siehe dort für die Regeln).
"""
import json
import os
import re
from pathlib import Path

import yaml

BAUKASTEN = Path(__file__).resolve().parent.parent
PLAN_DATEI = Path(os.environ.get("FIBU_KONTENPLAN") or BAUKASTEN / "kontenplan.yaml")   # Umgebungsvariable nur für Tests

# Kontonummer + Bezeichnung in Fließtext, Tabellen und Buchungssätzen: „5001 Erlösberichtigungen …“
RE_TEXT = re.compile(r"(?<![\w\-./,€])(\d{4})(?= [A-ZÄÖÜ][^\s|]*)")
# Tabellenzeile: | 2400 | Forderungen a. L. L. | …
RE_TABELLE = re.compile(r"^\|\s*(\d{4})\s*\|\s*([^|]+?)\s*\|")
# YAML: konto: "2400"  und  konten: ["2400", "4800"]
RE_KONTO_ZEILE = re.compile(r"\bkonto:\s*[\"']?(\d{4})[\"']?")
RE_KONTEN_LISTE = re.compile(r"^\s*(?:-\s*)?konten:\s*\[(.*)\]\s*$")


def lade_plan(datei=None):
    """Liste aller Konten (Dicts: nr, name, art, alias, quelle, status). Leere Liste, wenn die Datei fehlt."""
    p = Path(datei or PLAN_DATEI)
    if not p.exists():
        return []
    daten = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    out = []
    for k in daten.get("konten") or []:
        k = dict(k)
        k["nr"] = str(k["nr"])
        k["name"] = str(k["name"])
        k["alias"] = [str(a) for a in k.get("alias") or []]
        out.append(k)
    return out


def plan_dict(datei=None):
    """Kontonummer → Name (so, wie es kurs.yaml: kontenplan erwartet)."""
    return {k["nr"]: k["name"] for k in lade_plan(datei)}


def plan_index(datei=None):
    return {k["nr"]: k for k in lade_plan(datei)}


def namen(k):
    return [k["name"]] + list(k.get("alias") or [])


_RAND = ",.;:()\"'„“‚‘[]{}*`"


def name_passt(gefunden, konto):
    """Passt die gefundene Bezeichnung (Anfang eines Buchungssatz-Teils) zur Bezeichnung des Plans oder einem Alias?
    Großzügig: Es genügt, wenn das erste Wort zum Anfang einer erlaubten Bezeichnung passt (oder umgekehrt, wie bei
    „Umsatzsteuerberichtigung“ für „Umsatzsteuer“). Satzzeichen und Anführungszeichen werden ignoriert."""
    woerter = [w.strip(_RAND) for w in gefunden.split()[:6]]
    woerter = [w for w in woerter if w]
    if not woerter:
        return True
    erlaubt = [n.lower() for n in namen(konto)]
    for n in range(1, len(woerter) + 1):
        kandidat = " ".join(woerter[:n]).lower()
        if any(e.startswith(kandidat) for e in erlaubt):
            return True
    erstes = woerter[0].lower()
    return any(erstes.startswith(e.split()[0].strip(_RAND)) for e in erlaubt if e.split())


def _quelltexte(ordner):
    """(Datei, Text) aller Dateien eines Lernpfads, in denen Konten vorkommen können (ohne kurs.yaml und ausgabe/)."""
    ordner = Path(ordner)
    for sub, muster in (("module", "*.md"), ("seiten", "*.md"), ("fragen", "*.yaml")):
        for f in sorted((ordner / sub).glob(muster)):
            yield f, f.read_text(encoding="utf-8")


def finde_konten(ordner, plan=None, ohne=()):
    """Alle Konten, die ein Lernpfad verwendet.
    Ergebnis: {nr: {"dateien": set, "namen": set (aus Fließtext), "tabellen": set (aus Tabellenzeilen)}}. Jahreszahlen (1900 bis 2099), die nicht im Plan stehen, werden ignoriert."""
    plan = plan if plan is not None else plan_dict()
    fund = {}

    def merke(nr, datei, name=None, tabelle=False):
        if re.fullmatch(r"(19|20)\d\d", nr) and nr not in plan:
            return   # vermutlich eine Jahreszahl
        e = fund.setdefault(nr, {"dateien": set(), "namen": set(), "tabellen": set()})
        e["dateien"].add(datei.name)
        if name:
            e["tabellen" if tabelle else "namen"].add(name)

    for f, text in _quelltexte(ordner):
        if f.name in ohne:
            continue
        for zeile in text.split("\n"):
            m = RE_TABELLE.match(zeile)
            if m:
                merke(m.group(1), f, m.group(2), tabelle=True)
                continue
            m = RE_KONTEN_LISTE.match(zeile)
            if m:
                for nr in re.findall(r"[\"']?(\d{4})[\"']?", m.group(1)):
                    merke(nr, f)
            for nr in RE_KONTO_ZEILE.findall(zeile):
                merke(nr, f)
            for m in RE_TEXT.finditer(zeile):
                rest = zeile[m.end():].strip()
                merke(m.group(1), f, rest[:60])
    return fund


def eintrag_zeile(nr, name, art, quelle, status, alias=None):
    """Eine Zeile für kontenplan.yaml (gleiches Format wie die vorhandenen)."""
    q = lambda s: json.dumps(s, ensure_ascii=False)
    teile = [f"nr: {q(nr)}", f"name: {q(name)}", f"art: {art}"]
    if alias:
        teile.append("alias: [" + ", ".join(q(a) for a in alias) + "]")
    teile += [f"quelle: {q(quelle)}", f"status: {status}"]
    return "  - {" + ", ".join(teile) + "}"


def art_aus_nummer(nr):
    return {"0": "bestand", "2": "bestand", "3": "bestand", "4": "bestand", "5": "erfolg", "6": "erfolg",
            "7": "erfolg", "8": "abschluss"}.get(str(nr)[:1], "erfolg")
