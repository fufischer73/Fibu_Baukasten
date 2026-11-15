"""Gemeinsame Grundlage aller Skripte des Lernpfad-Baukastens: Kurs laden, Pfade, kleine Helfer.

Ein Lernpfad ist ein Ordner:
    kurs.yaml            Titel, Stufen (mit Modul-Reihenfolge), Varianten, Selbstcheck, Moodle-Einstellungen
    module/<id>.md       ein Modul: YAML-Kopf (Titel, Lernziele, Kurz-Check, Abgabe …) + Text mit Bausteinen
    seiten/<name>.md     Zusatzseiten (Spickzettel, Hinweise für Lehrkräfte …) – optional
    medien.yaml          Videos und Hilfeseiten (optional)
    quellen.yaml         Quellen mit Prüfstatus (optional, empfohlen)
    fragen/*.yaml        Fragen für Moodle-Tests (optional)
    material/            Bilder, Screenshots, Übungsdateien
    ausgabe/             wird erzeugt (nicht von Hand ändern)
"""
import re
import sys
import unicodedata
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("Es fehlt das Python-Paket „pyyaml“. Installieren mit:  pip install pyyaml markdown-it-py mdit-py-plugins")

SKILL = Path(__file__).resolve().parents[1]
VORLAGE = SKILL / "vorlage"
REVIEW = ("entwurf", "geprueft", "freigegeben")


class Fehler(Exception):
    """Inhaltsfehler, die das Bauen verhindern (mit verständlicher Meldung)."""


def slug(text):
    t = unicodedata.normalize("NFKD", str(text).lower())
    t = t.replace("ß", "ss")
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:48] or "seite"


def lies_md(datei):
    """Markdown mit YAML-Kopf (--- … ---) → (kopf: dict, text: str)."""
    s = Path(datei).read_text(encoding="utf-8").replace("\r\n", "\n")
    if s.startswith("---\n"):
        ende = s.find("\n---", 4)
        if ende < 0:
            raise Fehler(f"{datei}: YAML-Kopf ohne abschließendes ---")
        try:
            kopf = yaml.safe_load(s[4:ende]) or {}
        except yaml.YAMLError as e:
            raise Fehler(f"{datei}: YAML-Kopf fehlerhaft – {e}")
        return kopf, s[ende + 4:].lstrip("\n")
    return {}, s


def lies_yaml(datei, standard=None):
    p = Path(datei)
    if not p.exists():
        return standard
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8")) or standard
    except yaml.YAMLError as e:
        raise Fehler(f"{p.name}: YAML fehlerhaft – {e}")


class Kurs:
    """Der ganze Lernpfad, geladen aus seinem Ordner."""

    def __init__(self, ordner):
        self.ordner = Path(ordner).resolve()
        k = lies_yaml(self.ordner / "kurs.yaml")
        if not k:
            raise Fehler(f"Keine kurs.yaml in {self.ordner} gefunden.")
        self.k = k
        self.titel = k.get("titel", "Lernpfad")
        self.kurzname = k.get("kurzname") or slug(self.titel)
        self.stufen = k.get("stufen") or []
        self.module = {}      # id → dict(kopf…, text, datei, stufe)
        self.reihenfolge = []  # Modul-IDs in Pfad-Reihenfolge
        for st in self.stufen:
            for mid in st.get("module") or []:
                datei = self.ordner / "module" / f"{mid}.md"
                if not datei.exists():
                    raise Fehler(f"Modul „{mid}“ aus Stufe „{st.get('id')}“: Datei module/{mid}.md fehlt.")
                kopf, text = lies_md(datei)
                kopf.setdefault("id", mid)
                if kopf["id"] != mid:
                    raise Fehler(f"module/{mid}.md: id im Kopf („{kopf['id']}“) passt nicht zum Dateinamen.")
                kopf["text"] = text
                kopf["quelle"] = datei
                kopf["stufe"] = st["id"]
                kopf.setdefault("titel", mid)
                kopf.setdefault("review", "entwurf")
                kopf["datei"] = kopf.get("datei") or f"{mid}-{slug(kopf['titel'])}.html"
                self.module[mid] = kopf
                self.reihenfolge.append(mid)
        self.seiten = []
        for datei in sorted((self.ordner / "seiten").glob("*.md")):
            kopf, text = lies_md(datei)
            kopf["text"] = text
            kopf["quelle"] = datei
            kopf.setdefault("titel", datei.stem)
            kopf["datei"] = kopf.get("datei") or f"{slug(datei.stem)}.html"
            self.seiten.append(kopf)
        self.seiten.sort(key=lambda s: s.get("reihenfolge", 99))
        self.medien = lies_yaml(self.ordner / "medien.yaml", {}) or {}
        self.quellen = lies_yaml(self.ordner / "quellen.yaml", []) or []
        self.moodle = k.get("moodle") or {}

    # -- Abkürzungen
    def stufe(self, sid):
        return next(s for s in self.stufen if s["id"] == sid)

    def module_der_stufe(self, sid):
        return [self.module[m] for m in self.stufe(sid).get("module") or []]

    def freigegeben(self, mid):
        return self.module[mid].get("review") == "freigegeben"

    def einstufung_aktiv(self):
        return (self.moodle.get("freischaltung", "einstufung") == "einstufung") and len(self.stufen) > 1

    def einstufung_datei(self, sid):
        return f"einstufung-{slug(sid)}.html"

    @property
    def ausgabe(self):
        return self.ordner / "ausgabe"


def lade_klausur_modul():
    """Das Modul klausur.py des Klausur-Baukastens (Schwester-Skill) – für `tests: - klausur: <ordner>` in kurs.yaml."""
    try:
        import klausur
        return klausur
    except ImportError:
        pass
    for k in (SKILL / "klausur-baukasten" / "skripte", Path.home() / ".claude" / "skills" / "klausur-baukasten" / "skripte"):
        if (k / "klausur.py").exists():
            sys.path.insert(0, str(k))
            import klausur
            return klausur
    raise Fehler("Für „klausur:“ in tests: fehlt der Klausur-Baukasten (Ordner klausur-baukasten/ im Repo bzw. "
                 "~/.claude/skills/klausur-baukasten).")


def kurs_aus_argumenten(argv=None, beschreibung=""):
    """Ordner des Lernpfads aus der Kommandozeile (Standard: aktueller Ordner)."""
    import argparse
    ap = argparse.ArgumentParser(description=beschreibung)
    ap.add_argument("ordner", nargs="?", default=".", help="Ordner des Lernpfads (mit kurs.yaml)")
    return ap


def melde_fehler_und_ende(e):
    print(f"\n✗ {e}", file=sys.stderr)
    sys.exit(1)


# ---------- Buchungssätze als Tabelle (Soll | an | Haben) ----------
_BS_TEIL = re.compile(r"^(\d{4}) (.+?)(?: (\d{1,3}(?:\.\d{3})*,\d{2}) €)?$")


def buchungssatz_html(text):
    """„6000 Aufwendungen Rohstoffe 10.000,00 € und 2600 Vorsteuer 1.900,00 € an 4400 Verbindlichkeiten 11.900,00 €“
    → HTML-Tabelle mit Soll und Haben (für Antworten in Tests und Kurz-Checks). Passt der Text nicht, kommt None zurück.
    Nur Inline-Stile, damit es auch im Moodle-Test ohne eigenes Stylesheet aussieht."""
    import html as _h
    teile = re.split(r" an (?=\d{4} )", str(text).strip())
    if len(teile) != 2:
        return None

    def seite(s):
        out = []
        for p in re.split(r" und (?=\d{4} )", s.strip()):
            m = _BS_TEIL.match(p.strip())
            if not m:
                return None
            out.append((m.group(1), m.group(2).strip(), m.group(3) or ""))
        return out
    soll, haben = seite(teile[0]), seite(teile[1])
    if not soll or not haben:
        return None
    th = "padding:.15em .6em;border-bottom:1px solid #888;font-weight:600;text-align:left"
    td = "padding:.15em .6em;vertical-align:top"
    tb = td + ";text-align:right;white-space:nowrap"
    zeilen = []
    for i in range(max(len(soll), len(haben))):
        s_ = soll[i] if i < len(soll) else None
        h_ = haben[i] if i < len(haben) else None
        zeilen.append(
            "<tr>" +
            (f'<td style="{td}">{_h.escape(s_[0] + " " + s_[1])}</td><td style="{tb}">{_h.escape(s_[2] + (" €" if s_[2] else ""))}</td>'
             if s_ else f'<td style="{td}"></td><td style="{tb}"></td>') +
            f'<td style="{td};font-weight:600">{"an" if i == 0 else ""}</td>' +
            (f'<td style="{td}">{_h.escape(h_[0] + " " + h_[1])}</td><td style="{tb}">{_h.escape(h_[2] + (" €" if h_[2] else ""))}</td>'
             if h_ else f'<td style="{td}"></td><td style="{tb}"></td>') + "</tr>")
    return ('<table style="border-collapse:collapse;margin:.2em 0;font-size:.95em"><tr>'
            f'<th colspan="2" style="{th}">Soll</th><th style="{th}"></th><th colspan="2" style="{th}">Haben</th></tr>' +
            "".join(zeilen) + "</table>")

# ---------------------------------------------------------------- Belege (Rechnung, Gutschrift, Kontoauszug …)
BELEG_SCHLUESSEL = ("art", "stil", "firma", "firma_zeile", "absender_zeile", "empfaenger", "info", "spalten", "zeilen",
                    "summen", "text", "bedingungen", "fuss", "stempel")
_BELEG_FARBE = {"rechnung": "#1f4e79", "gutschrift": "#2e6b3a", "bonus": "#7a4a14", "bank": "#0b5a8f", "spedition": "#444444"}


def beleg_pruefen(b, wo="beleg"):
    """Fehlermeldungen zu einem Beleg (Dict) oder einer Liste von Belegen."""
    fehler = []
    liste = b if isinstance(b, list) else [b]
    for i, x in enumerate(liste, 1):
        w = f"{wo} {i}" if isinstance(b, list) else wo
        if not isinstance(x, dict):
            fehler.append(f"{w}: muss ein Block mit art, firma, spalten … sein")
            continue
        for k in x:
            if k not in BELEG_SCHLUESSEL:
                fehler.append(f"{w}: Feld „{k}“ unbekannt (erlaubt: {', '.join(BELEG_SCHLUESSEL)})")
        if not x.get("art"):
            fehler.append(f"{w}: „art“ fehlt (z. B. Rechnung, Gutschrift, Kontoauszug)")
        for k in ("spalten", "zeilen", "summen", "info", "empfaenger"):
            if k in x and not isinstance(x[k], list):
                fehler.append(f"{w}: „{k}“ muss eine Liste sein")
        sp = x.get("spalten")
        if isinstance(sp, list) and isinstance(x.get("zeilen"), list):
            for z in x["zeilen"]:
                if not isinstance(z, list) or len(z) != len(sp):
                    fehler.append(f"{w}: jede Zeile braucht {len(sp)} Einträge (Zeile {z!r})")
                    break
        for z in x.get("summen") or []:
            if not isinstance(z, list) or len(z) not in (2, 3):
                fehler.append(f"{w}: summen: jede Zeile = [Beschriftung, Wert] oder [Beschriftung, Wert, fett]")
                break
        for z in x.get("info") or []:
            if not isinstance(z, list) or len(z) != 2:
                fehler.append(f"{w}: info: jede Zeile = [Beschriftung, Wert]")
                break
    return fehler


def _beleg_rechts(t):
    return bool(re.fullmatch(r"[+\-–−]?\s*[\d.,\s]+\s*(€|%|EUR|Stück|m|l|kg|Liter|Meter)?", str(t).strip()))


def beleg_html(b):
    """Ein Beleg oder eine Liste von Belegen → HTML mit Inline-Stilen (für Moodle-Fragen ohne eigenes Stylesheet).
    Aufbau und Felder wie bei :::uebung → beleg: (siehe referenzen/bausteine.md)."""
    import html as _h
    if isinstance(b, list):
        return "".join(beleg_html(x) for x in b)
    e = lambda x: _h.escape(str(x if x is not None else ""))
    farbe = _BELEG_FARBE.get(str(b.get("stil") or "rechnung"), "#1f4e79")
    papier = "background:#fff;color:#222;border:1px solid #bbb;box-shadow:0 1px 4px rgba(0,0,0,.25);"
    out = [f'<div style="{papier}max-width:46em;margin:.8em 0;padding:1em 1.2em;font-family:Arial,Helvetica,sans-serif;font-size:.9em;line-height:1.35;position:relative">']
    out.append(f'<div style="display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid {farbe};padding-bottom:.4em;margin-bottom:.6em">'
               f'<div><div style="font-size:1.35em;font-weight:700;color:{farbe}">{e(b.get("firma"))}</div>'
               f'<div style="font-size:.8em;color:#555">{e(b.get("firma_zeile"))}</div></div>'
               f'<div style="font-size:1.1em;letter-spacing:.2em;font-weight:700;color:{farbe}">{e(str(b.get("art")).upper())}</div></div>')
    anschrift = "".join(f"<div>{e(z)}</div>" for z in b.get("empfaenger") or [])
    info = "".join(f'<tr><td style="color:#555;padding:0 .8em 0 0;white-space:nowrap">{e(k)}</td><td style="font-weight:600">{e(v)}</td></tr>' for k, v in b.get("info") or [])
    if anschrift or info:
        out.append('<table style="width:100%;border-collapse:collapse;margin-bottom:.7em"><tr>'
                   f'<td style="vertical-align:top;width:50%"><div style="font-size:.7em;color:#666;text-decoration:underline;margin-bottom:.3em">{e(b.get("absender_zeile"))}</div>{anschrift}</td>'
                   f'<td style="vertical-align:top"><table style="border-collapse:collapse;font-size:.9em">{info}</table></td></tr></table>')
    sp = b.get("spalten") or []
    if sp:
        zl_ = b.get("zeilen") or []
        rechts = [any(str(z[i]).strip() for z in zl_) and all(not str(z[i]).strip() or _beleg_rechts(z[i]) for z in zl_) for i in range(len(sp))]
        head = "".join(f'<th style="text-align:{"right" if rechts[i] else "left"};padding:.25em .5em;border:1px solid #999;background:#eef1f4;font-size:.85em">{e(s)}</th>' for i, s in enumerate(sp))
        rows = "".join("<tr>" + "".join(f'<td style="padding:.25em .5em;border:1px solid #ccc;text-align:{"right" if rechts[i] else "left"};{"white-space:nowrap;" if rechts[i] else ""}">{e(c)}</td>' for i, c in enumerate(z)) + "</tr>" for z in b.get("zeilen") or [])
        out.append(f'<table style="width:100%;border-collapse:collapse;margin-bottom:.6em"><tr>{head}</tr>{rows}</table>')
    if b.get("summen"):
        zl = "".join(f'<tr><td style="padding:.15em .6em;{"font-weight:700;border-top:1px solid #222;border-bottom:3px double #222;" if len(z) > 2 and z[2] else ""}">{e(z[0])}</td>'
                     f'<td style="padding:.15em .6em;text-align:right;white-space:nowrap;{"font-weight:700;border-top:1px solid #222;border-bottom:3px double #222;" if len(z) > 2 and z[2] else ""}">{e(z[1])}</td></tr>' for z in b["summen"])
        out.append(f'<table style="margin-left:auto;border-collapse:collapse;margin-bottom:.6em">{zl}</table>')
    for k in ("text", "bedingungen"):
        if b.get(k):
            out.append(f'<div style="margin:.3em 0;{"border:1px solid #999;padding:.3em .6em;font-size:.9em" if k == "bedingungen" else ""}">' + e(b[k]).replace("\n", "<br>") + "</div>")
    if b.get("fuss"):
        out.append(f'<div style="border-top:2px solid {farbe};margin-top:.7em;padding-top:.3em;font-size:.72em;color:#555">{e(b["fuss"])}</div>')
    if b.get("stempel"):
        out.append(f'<div style="position:absolute;top:5.2em;left:30%;border:2px solid #c0392b;color:#c0392b;padding:.2em .6em;transform:rotate(-6deg);font-weight:700;font-size:.8em;background:rgba(255,255,255,.7)">{e(b["stempel"]).replace(chr(10), "<br>")}</div>')
    out.append("</div>")
    return "".join(out)
