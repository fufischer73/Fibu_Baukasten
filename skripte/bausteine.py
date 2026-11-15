"""Markdown mit Lernpfad-Bausteinen → HTML im Design der Vorlage.

Bausteine (Container, geöffnet mit ::: name …, geschlossen mit :::; verschachtelt: außen mehr Doppelpunkte):
    :::ziele [Titel]            Lernziele-Kasten (sonst automatisch aus „lernziele“ im Modulkopf)
    :::tipp [Titel]             Tipp          :::achtung [Titel]   typischer Fehler, Warnung
    :::notiz [Titel]            Hinweis       :::gestaltung [Titel] Gestaltungsregeln
    :::kasten [Titel]           neutraler Kasten (z. B. um mehrere Checklisten)
    :::aufgabe basis 10 Titel   Aufgabe (Niveau basis|plus|kreativ|pflicht, Minuten optional, Titel)
    :::checkliste [Titel]       Liste zum Abhaken (Markdown-Liste darin)
    :::loesung [Titel]          aufklappbare Lösung
    :::schritte                 nummerierte Schrittfolge (Markdown-Liste 1. 2. 3. darin)
    ::::varianten               Anleitungen nebeneinander (bei „beide“), darin:
    :::variante <id> [Label]    Anleitung nur für eine Variante des Umschalters (z. B. ppt, oo)
    :::material <datei> Titel   Download-Kasten mit Knopf, Text darin = Beschreibung
    :::menueband <variante> <Registerkarte>   Schema eines Menübands (Zeilen: gruppen:, menue:, text:)
    :::seitenleiste <variante> <Titel>        Schema einer Seitenleiste (Zeilen: zeilen:, text:)
    :::screenshot <datei>       Bild (bzw. Platzhalter, solange die Datei fehlt); Text darin = Beschreibung
    :::schluessel <stufe|modul> Code zum Freischalten (zugang: in kurs.yaml); erscheint, sobald das Modul als
                                erledigt markiert ist. Text darin = eigener Hinweis (optional)
    :::raum [braucht=<schloss>] Titel   Raum eines Online-Breakouts; bleibt zu, bis das Schloss mit dieser id geöffnet ist
    :::schloss                  digitales Schloss (YAML: id, titel, code, hinweis, oeffnet) – öffnet einen Raum
    :::uebung                   interaktive Übung (YAML im Block): typ rechnen | buchung | konten | luecken –
                                Eingabe, Prüfen, Hinweis, Lösung mit Rechenweg (siehe referenzen/bausteine.md)
    :::kurzcheck / :::abgabe / :::raster / :::medien   Platzhalter: hier erscheinen Kurz-Check, Abgabe,
                                Bewertungsraster, Videos aus dem Modulkopf (sonst am Ende des Moduls)
Jeder Baustein kann am Ende der Kopfzeile {id} bekommen, z. B. ":::notiz Nur für PowerPoint {ppt}" – dann erscheint
er nur bei dieser Variante des Umschalters.
Kurzschreibweisen im Text:
    {{Start › Schriftart}}      Menüpfad          ++Strg+C++ oder ++Enter++   Tasten
    [Text](modul:e2)            Link auf ein anderes Modul
    <span class="ppt">…</span>  Text nur für eine Variante (HTML ist erlaubt)
"""
import ast
import html
import json
import math
import random
import re

import yaml

from gemeinsam import Fehler, beleg_pruefen, buchungssatz_html
from markdown_it import MarkdownIt
from mdit_py_plugins.container import container_plugin

NIVEAU = {"basis": ("basis", "Basis"), "plus": ("plus", "Plus"), "kreativ": ("kreativ", "Kreativ"),
          "pflicht": ("basis", "Pflicht")}
KAESTEN = {  # name: (CSS-Klasse, Standardtitel)
    "ziele": ("goals", "🎯 Das kannst du nach diesem Modul"),
    "tipp": ("tip", "💡 Tipp"),
    "achtung": ("warn", "⚠️ Achtung"),
    "notiz": ("note", ""),
    "gestaltung": ("design", "✏️ Gestaltungsregeln"),
    "kasten": ("plain", ""),
}
ROH = ("menueband", "seitenleiste", "screenshot", "kurzcheck", "abgabe", "raster", "medien", "schluessel", "uebung", "schloss", "hilfe")
ALLE = set(KAESTEN) | {"aufgabe", "checkliste", "loesung", "schritte", "varianten", "variante", "material", "raum"} | set(ROH)

esc = lambda s: html.escape(str(s), quote=True)


def klassen(rest):
    """„Titel {ppt}“ → („Titel“, " ppt") – Varianten-Klasse am Ende der Kopfzeile."""
    m = re.search(r"\s*\{([\w -]+)\}\s*$", rest)
    if not m:
        return rest, ""
    return rest[:m.start()].strip(), " " + " ".join(m.group(1).split())


class Uebersetzer:
    def __init__(self, varianten=None, modul_datei=None, kontenplan=None):
        self.kontenplan = {str(k): str(v) for k, v in (kontenplan or {}).items()}  # Kontonummer → Name (kurs.yaml)
        self.varianten = varianten or {}           # id → Anzeigename
        self.modul_datei = modul_datei or {}       # Modul-ID → HTML-Datei
        self.md = MarkdownIt("commonmark", {"html": True, "typographer": False}).enable("table")
        ich = self

        def render(_renderer, tokens, idx, options, env):  # markdown-it bindet die Funktion an seinen Renderer
            return ich._container(tokens, idx, options, env)
        for name in ALLE - set(ROH):
            self.md.use(container_plugin, name=name, render=render)

        def link_open(renderer, tokens, idx, options, env):  # externe Links im neuen Tab (YouTube & Co. lassen sich nicht im Lernpaket anzeigen)
            if re.match(r"https?://", tokens[idx].attrGet("href") or ""):
                tokens[idx].attrSet("target", "_blank")
                tokens[idx].attrSet("rel", "noopener")
            return renderer.renderToken(tokens, idx, options, env)
        self.md.add_render_rule("link_open", link_open)
        self._stapel = []
        self.seiten = {}   # Seitenname → Seite (für :::hilfe); setzt bauen.py

    # -- Container
    def _container(self, tokens, idx, _opts, _env):
        t = tokens[idx]
        name = t.info.strip().split(" ", 1)[0]
        rest = t.info.strip()[len(name):].strip()
        if t.nesting == 1:
            self._stapel.append((name, rest))
            return self._auf(name, rest)
        name, rest = self._stapel.pop()
        return self._zu(name, rest)

    def _auf(self, name, rest):
        rest, extra = klassen(rest)
        if name in KAESTEN:
            cls, titel = KAESTEN[name]
            titel = rest or titel
            return f'<div class="box {cls}{extra}">' + (f'<div class="box-title">{self.inline(titel)}</div>' if titel else "")
        if name == "aufgabe":
            teile = rest.split()
            niveau = teile.pop(0).lower() if teile and teile[0].lower() in NIVEAU else "basis"
            minuten = teile.pop(0) if teile and re.fullmatch(r"\d+\+?", teile[0]) else ""
            cls, label = NIVEAU[niveau]
            return (f'<div class="box task {cls}{extra}"><div class="task-head"><span class="lvl {cls}">{label}</span>'
                    f'<h3>{self.inline(" ".join(teile))}</h3>' +
                    (f'<span class="lvl time">{minuten.rstrip("+")} min{" +" if minuten.endswith("+") else ""}</span>' if minuten else "") + "</div>")
        if name == "raum":
            m = re.search(r"\bbraucht=([\w-]+)", rest)
            titel = re.sub(r"\bbraucht=[\w-]+\s*", "", rest).strip()
            return (f'<div class="raum" data-braucht="{esc(m.group(1)) if m else ""}">' +
                    (f'<h2 class="raum-titel">{self.inline(titel)}</h2>' if titel else ""))
        if name == "checkliste":
            return f'<div class="checkliste{extra}">' + (f'<div class="check-title">{self.inline(rest)}</div>' if rest else "")
        if name == "loesung":
            return f"<details{' class=' + chr(34) + extra.strip() + chr(34) if extra else ''}><summary>{self.inline(rest or 'Lösung')}</summary>"
        if name == "schritte":
            return f'<div class="schritte{extra}">'
        if name == "varianten":
            return '<div class="both-grid">'
        if name == "variante":
            v, _, label = rest.partition(" ")
            return f'<div class="box how {esc(v)}"><span class="app-label">{self.inline(label.strip() or self.varianten.get(v, v))}</span>'
        if name == "material":
            datei, _, titel = rest.partition(" ")
            return f'<div class="box download{extra}"><div class="box-title">📥 {self.inline(titel or datei)}</div>'
        return "<div>"

    def _zu(self, name, rest):
        if name == "aufgabe" or name in KAESTEN or name in ("checkliste", "schritte", "varianten", "variante", "raum"):
            return "</div>"
        if name == "loesung":
            return "</details>"
        if name == "material":
            datei = klassen(rest)[0].partition(" ")[0]
            return (f'<p><a class="btn" href="{esc(datei)}" download>{esc(datei.rsplit("/", 1)[-1])} herunterladen</a></p></div>')
        return "</div>"

    # -- Verschachtelung: Doppelpunkte automatisch setzen, damit man immer ::: schreiben kann
    @staticmethod
    def _verschachtelung(text):
        zeilen = text.split("\n")
        paare, stapel, in_code = [], [], False
        for i, z in enumerate(zeilen):
            if z.lstrip().startswith("```"):
                in_code = not in_code
            if in_code:
                continue
            auf = re.match(r"^:{3,}\s*(\w+)", z)
            if auf and auf.group(1) in ALLE:
                stapel.append([i, None, []])
                if len(stapel) > 1:
                    stapel[-2][2].append(stapel[-1])
            elif re.match(r"^:{3,}\s*$", z) and stapel:
                knoten = stapel.pop()
                knoten[1] = i
                if not stapel:
                    paare.append(knoten)
        def hoehe(k):
            return 0 if not k[2] else 1 + max(hoehe(c) for c in k[2])
        def setze(k):
            n = 3 + hoehe(k)
            zeilen[k[0]] = re.sub(r"^:{3,}", ":" * n, zeilen[k[0]])
            if k[1] is not None:
                zeilen[k[1]] = ":" * n
            for c in k[2]:
                setze(c)
        for k in paare:
            setze(k)
        return "\n".join(zeilen)

    # -- Vorverarbeitung: Kurzschreibweisen und „rohe“ Bausteine (ohne Markdown darin)
    def _vor(self, text):
        text = self._verschachtelung(text)
        zeilen, out, i = text.split("\n"), [], 0
        in_code = False
        while i < len(zeilen):
            z = zeilen[i]
            if z.lstrip().startswith("```"):
                in_code = not in_code
            m = None if in_code else re.match(r"^(:{3,})\s*(\w+)\s*(.*)$", z)
            if m and m.group(2) in ROH:
                zu, name, rest = m.group(1), m.group(2), m.group(3).strip()
                inhalt = []
                i += 1
                while i < len(zeilen) and zeilen[i].strip() != zu:
                    inhalt.append(zeilen[i])
                    i += 1
                out.append("")
                out.append(self._roh(name, rest, "\n".join(inhalt).strip()))
                out.append("")
                i += 1
                continue
            out.append(z if in_code else self._kurz(z))
            i += 1
        return "\n".join(out)

    def _kurz(self, z):
        z = re.sub(r"\{\{\s*(.+?)\s*\}\}", lambda m: f'<span class="path">{esc(m.group(1))}</span>', z)
        z = re.sub(r"\+\+(.+?)\+\+", lambda m: self._tasten(m.group(1)), z)
        return z

    @staticmethod
    def _tasten(t):
        """++Strg+C++ → <kbd>Strg</kbd>+<kbd>C</kbd>; einzelne Taste wie gehabt."""
        teile = t.split("+")
        if len(teile) > 1 and all(x.strip() for x in teile):
            return "+".join(f"<kbd>{esc(x.strip())}</kbd>" for x in teile)
        return f"<kbd>{esc(t)}</kbd>"

    def _roh(self, name, rest, inhalt):
        rest, extra = klassen(rest)
        if name == "uebung":
            return self._uebung(inhalt)
        if name == "schloss":
            return self._schloss(inhalt)
        if name == "hilfe":
            return self._hilfe(rest)
        felder = {}
        for zeile in inhalt.split("\n"):
            k, sep, v = zeile.partition(":")
            if sep and re.fullmatch(r"[a-zäöü]+", k.strip()):
                felder[k.strip()] = v.strip()
        if name == "menueband":
            app, _, tab = rest.partition(" ")
            attrs = {"data-app": app, "data-tab": tab, "data-groups": felder.get("gruppen", ""),
                     "data-menu": felder.get("menue", ""), "data-caption": felder.get("text", "")}
            return '<figure class="rb" ' + " ".join(f'{k}="{esc(v)}"' for k, v in attrs.items() if v) + "></figure>"
        if name == "seitenleiste":
            app, _, titel = rest.partition(" ")
            attrs = {"data-app": app, "data-title": titel, "data-rows": felder.get("zeilen", ""),
                     "data-caption": felder.get("text", "")}
            return '<figure class="sp" ' + " ".join(f'{k}="{esc(v)}"' for k, v in attrs.items() if v) + "></figure>"
        if name == "schluessel":
            # Der Code selbst kommt von bauen.py (zugang: in kurs.yaml) – hier nur der Platzhalter
            return f'<div class="box lp-schluessel" data-ziel="{esc(rest)}" data-text="{esc(inhalt)}"></div>'
        if name == "screenshot":
            return f'<figure class="shot{extra}" data-src="{esc(rest)}" data-desc="{esc(inhalt)}"></figure>'
        return f'<div data-lp="{name}"></div>'

    def _hilfe(self, rest):
        """:::hilfe <seite> – der Inhalt einer Seite aus seiten/ als aufklappbarer Kasten mitten im Modul."""
        name = rest.split()[0] if rest.split() else ""
        seite = self.seiten.get(name)
        if not seite:
            raise Fehler(f":::hilfe {name}: Seite seiten/{name}.md gibt es nicht (vorhanden: {', '.join(sorted(self.seiten)) or 'keine'})")
        frisch = Uebersetzer(self.varianten, self.modul_datei, self.kontenplan)   # eigener Zustand, damit sich nichts verhakt
        inhalt = frisch.block(seite.get("text", ""))
        titel = f'{seite.get("icon", "")} {seite.get("titel", name)}'.strip()
        return f'<details class="hilfe"><summary>{esc(titel)}</summary><div class="hilfe-inhalt">{inhalt}</div></details>'

    def _schloss(self, inhalt):
        daten, fehler = lies_schloss(inhalt)
        if fehler:
            raise Fehler("Schloss fehlerhaft: " + "; ".join(fehler))
        js = json.dumps(daten, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
        return ('<section class="schloss-host"><script type="application/json">' + js + "</script>"
                '<noscript><p class="box warn">Für dieses Schloss wird JavaScript gebraucht.</p></noscript></section>')

    def _uebung(self, inhalt):
        daten, fehler = lies_uebung(inhalt, self.kontenplan)
        if fehler:
            raise Fehler("Übung fehlerhaft: " + "; ".join(fehler))
        js = json.dumps(daten, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
        return ('<section class="uebung-host"><script type="application/json">' + js + "</script>"
                '<noscript><p class="box warn">Für diese Übung wird JavaScript gebraucht.</p></noscript></section>')

    # -- Nachbearbeitung
    def _nach(self, h):
        h = re.sub(r"<table>", '<div class="table-wrap"><table>', h)
        h = re.sub(r"</table>", "</table></div>", h)
        h = re.sub(r'href="modul:([\w-]+)"', lambda m: f'href="{self.modul_datei.get(m.group(1), m.group(1) + ".html")}"', h)
        h = re.sub(r'(<div class="checkliste[^"]*">(?:<div class="check-title">.*?</div>)?\s*)<ul>', r'\1<ul class="check">', h)
        h = re.sub(r'(<div class="schritte[^"]*">\s*)<ol>', r'\1<ol class="steps">', h)
        return h

    def block(self, text):
        self._stapel = []
        return self._nach(self.md.render(self._vor(text or "")))

    def inline(self, text):
        return self.md.renderInline(self._kurz(str(text or "")))


def unbekannte_bausteine(text):
    """Für pruefen.py: Zeilen mit ::: name, die es nicht gibt (würden sonst als Text erscheinen)."""
    fehler = []
    for nr, z in enumerate(text.split("\n"), 1):
        m = re.match(r"^:{3,}\s*(\w+)", z)
        if m and m.group(1) not in ALLE:
            fehler.append((nr, m.group(1)))
    return fehler


# ---------- Interaktive Übungen (:::uebung) ----------
UEBUNG_TYPEN = ("rechnen", "buchung", "konten", "luecken", "lueckentext", "auswahl", "zuordnung", "reihenfolge", "offen")
RICHTUNGEN = ("steigt", "sinkt", "gleich")
_FUNK = {"round": lambda x, d=2: round(x, int(d)), "floor": math.floor, "ceil": math.ceil, "abs": abs,
         "min": min, "max": max, "sqrt": math.sqrt}


def _zahl(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def formel_baum(src):
    """Formel (+ - * / ^ Klammern, Funktionen) → geprüfter AST; sonst ValueError."""
    try:
        baum = ast.parse(str(src).replace("^", "**"), mode="eval")
    except SyntaxError:
        raise ValueError(f"Formel nicht lesbar: {src}")
    for n in ast.walk(baum):
        if isinstance(n, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Name, ast.Load, ast.Call,
                          ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd)):
            if isinstance(n, ast.Constant) and not _zahl(n.value):
                raise ValueError(f"Nur Zahlen erlaubt in der Formel: {src}")
            if isinstance(n, ast.Call) and not (isinstance(n.func, ast.Name) and n.func.id in _FUNK and not n.keywords):
                raise ValueError(f"Unbekannte Funktion in der Formel: {src}")
            continue
        raise ValueError(f"Nicht erlaubt in der Formel: {src}")
    return baum


def formel_namen(src):
    baum = formel_baum(src)
    funk = {n.func.id for n in ast.walk(baum) if isinstance(n, ast.Call)}
    return {n.id for n in ast.walk(baum) if isinstance(n, ast.Name)} - funk


def formel_wert(src, vars):
    baum = formel_baum(src)

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.Name):
            if n.id not in vars:
                raise ValueError(f"Unbekannte Variable „{n.id}“ in: {src}")
            return vars[n.id]
        if isinstance(n, ast.UnaryOp):
            return -ev(n.operand) if isinstance(n.op, ast.USub) else ev(n.operand)
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            return {ast.Add: lambda: a + b, ast.Sub: lambda: a - b, ast.Mult: lambda: a * b,
                    ast.Div: lambda: a / b, ast.Pow: lambda: a ** b}[type(n.op)]()
        if isinstance(n, ast.Call):
            return _FUNK[n.func.id](*[ev(a) for a in n.args])
        raise ValueError(src)
    return ev(baum)


def _parameter(d, fehler):
    """parameter: name → {start, von/bis oder min/max, schritt}; normalisiert zu von/bis/schritt."""
    par = d.get("parameter")
    if par is None:
        return {}
    if not isinstance(par, dict) or not par:
        fehler.append("parameter: Zuordnung name → {start, von, bis, schritt} nötig")
        return {}
    out = {}
    for k, p in par.items():
        von, bis = (p.get("von", p.get("min")), p.get("bis", p.get("max"))) if isinstance(p, dict) else (None, None)
        schritt = p.get("schritt", 1) if isinstance(p, dict) else None
        start = p.get("start")
        if start is not None and von is None and bis is None and _zahl(start):
            von = bis = start        # feste Zahl: nur „start“ angeben
            schritt = 1
        if not (_zahl(von) and _zahl(bis) and _zahl(schritt)) or schritt <= 0 or bis < von:
            fehler.append(f"parameter {k}: von, bis (oder min, max) und schritt als Zahlen nötig")
            continue
        if start is not None and not (_zahl(start) and von <= start <= bis):
            fehler.append(f"parameter {k}: start liegt nicht zwischen von und bis")
            continue
        out[str(k)] = {"von": von, "bis": bis, "schritt": schritt, **({"start": start} if start is not None else {})}
    return out


def _proben(par, n=40):
    """Start- und Zufallswerte, mit denen die Formeln geprüft werden."""
    rnd = random.Random(7)
    proben = []
    if par and all("start" in p for p in par.values()):
        proben.append({k: p["start"] for k, p in par.items()})
    for _ in range(n):
        v = {}
        for k, p in par.items():
            schritte = int((p["bis"] - p["von"]) / p["schritt"] + 1e-9) + 1
            v[k] = round(p["von"] + p["schritt"] * rnd.randrange(schritte), 4)
        proben.append(v)
    return proben or [{}]


def _walk_strings(o, schluessel=""):
    """Alle (Schlüssel, Text)-Paare eines Baums, ohne parameter."""
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("parameter",):
                continue
            yield from _walk_strings(v, k)
    elif isinstance(o, list):
        for v in o:
            yield from _walk_strings(v, schluessel)
    elif isinstance(o, str):
        yield schluessel, o


_PLATZ = re.compile(r"\{\{\s*(=)?\s*([^}:]+?)\s*(?::\s*(\w+))?\s*\}\}")


def _formeln_pruefen(d, par, fehler):
    """Formeln und Platzhalter mit Start- und Zufallswerten durchrechnen."""
    proben = _proben(par)
    felder_ids = [f.get("id") for f in (d.get("felder") or []) if isinstance(f, dict) and f.get("id")]
    gemeldet = set()

    def melde(text, schluessel=None):
        if (schluessel or text) not in gemeldet:
            gemeldet.add(schluessel or text)
            fehler.append(text)
    for v in proben:
        werte = dict(v)
        for f in d.get("felder") or []:
            if isinstance(f, dict) and isinstance(f.get("formel"), str):
                try:
                    r = formel_wert(f["formel"], werte)
                except (ValueError, ZeroDivisionError) as e:
                    melde(f"felder {f.get('label', '')}: {e}")
                    continue
                if f.get("runden") is None and abs(r * 100 - round(r * 100)) > 1e-6:
                    melde(f"Formel „{f['formel']}“ ergibt z. B. bei {v} mehr als zwei Nachkommastellen: Schrittweite der Parameter anpassen oder im Feld „runden:“ angeben", f["formel"])
                if f.get("id"):
                    werte[f["id"]] = round(r, int(f["runden"]) if f.get("runden") is not None else 2)
        for k, t in _walk_strings(d):
            if k in ("betrag", "antwort") and isinstance(t, str) and re.fullmatch(r"[\s\d.+\-*/^()A-Za-z_,]+", t):
                try:
                    r = formel_wert(t, werte)
                    if abs(r * 100 - round(r * 100)) > 1e-6:
                        melde(f"Formel „{t}“ ergibt z. B. bei {v} mehr als zwei Nachkommastellen: Schrittweite der Parameter anpassen", "dez:" + t)
                    if r < 0:
                        melde(f"Formel „{t}“ ergibt z. B. bei {v} einen negativen Betrag", "neg:" + t)
                except (ValueError, ZeroDivisionError) as e:
                    melde(f"{k}: {e}")
            elif "{{" in t:
                for m in _PLATZ.finditer(t):
                    try:
                        if m.group(1):
                            formel_wert(m.group(2), werte)
                        elif m.group(2) not in werte:
                            raise ValueError(f"Platzhalter {{{{{m.group(2)}}}}} ist kein Parameter und keine Antwort-id")
                    except (ValueError, ZeroDivisionError) as e:
                        melde(f"Platzhalter: {e}")


def lies_uebung(inhalt, kontenplan=None):
    """YAML eines :::uebung-Blocks lesen und prüfen → (daten für das Skript, Liste von Fehlermeldungen).
    Die Fehlermeldungen nutzt pruefen.py; bauen.py bricht bei Fehlern ab."""
    fehler = []
    try:
        d = yaml.safe_load(inhalt)
    except yaml.YAMLError as e:
        return None, [f"YAML fehlerhaft – {str(e).splitlines()[0] if str(e) else e}"]
    if not isinstance(d, dict):
        return None, ["Der Block braucht YAML mit „typ“ und „titel“"]
    typ = d.get("typ")
    if typ not in UEBUNG_TYPEN:
        return None, [f"typ „{typ}“ unbekannt (erlaubt: {', '.join(UEBUNG_TYPEN)})"]
    if not d.get("titel"):
        fehler.append("„titel“ fehlt")
    if d.get("niveau", "basis") not in ("basis", "plus", "kreativ"):
        fehler.append("niveau: basis | plus | kreativ")
    code = d.get("code")
    if code is not None and (not isinstance(code, dict) or not code.get("teil")):
        fehler.append("code: „teil“ nötig (der Code-Teil, der nach richtiger Lösung erscheint); „text“ optional")
    elif isinstance(code, dict):
        d["code"] = {"teil": str(code["teil"]), "text": str(code.get("text", ""))}
    if d.get("beleg") is not None:
        fehler += beleg_pruefen(d["beleg"])
    tipps = d.get("tipps")
    if tipps is not None and (not isinstance(tipps, list) or not all(isinstance(t, str) for t in tipps)):
        fehler.append("tipps: Liste mit Texten (Tipp 1, Tipp 2 …)")
    plan = kontenplan or {}
    namen = {}

    def konto(nr, wo):
        nr = str(nr)
        if plan and nr not in plan:
            fehler.append(f"{wo}: Konto {nr} steht nicht im kontenplan in kurs.yaml")
        namen[nr] = plan.get(nr, "")
        return nr

    def betrag_ok(x):
        return _zahl(x) or (isinstance(x, str) and bool(re.fullmatch(r"[\s\d.+\-*/^()A-Za-z_,]+", x)))

    def zeilen(liste, wo):
        if not isinstance(liste, list) or not liste:
            fehler.append(f"{wo}: Liste mit Zeilen nötig")
            return []
        out = []
        for z in liste:
            if not isinstance(z, dict) or "konto" not in z or not betrag_ok(z.get("betrag")):
                fehler.append(f"{wo}: jede Zeile braucht „konto“ und „betrag“ (Zahl oder Formel)")
                continue
            out.append({"konto": konto(z["konto"], wo), "betrag": z["betrag"]})
        return out

    d = dict(d)
    par = _parameter(d, fehler)
    if par:
        d["parameter"] = par
    if typ == "rechnen":
        f = d.get("felder")
        if not isinstance(f, list) or not f:
            fehler.append("rechnen: „felder“ (Liste mit label und antwort oder formel) fehlt")
        else:
            for x in f:
                if not isinstance(x, dict) or not x.get("label") or not (_zahl(x.get("antwort")) or isinstance(x.get("formel"), str)):
                    fehler.append("rechnen: jedes Feld braucht „label“ und „antwort“ (Zahl) oder „formel“")
                elif isinstance(x.get("formel"), str) and not par:
                    fehler.append("rechnen: „formel“ braucht „parameter“")
    elif typ in ("buchung", "konten"):
        liste = d.get("konten") or []
        if not liste:
            fehler.append("„konten“ fehlt (Liste der wählbaren Kontonummern)")
        d["konten"] = [{"nr": str(n), "name": plan.get(str(n), "")} for n in sorted(map(str, liste))]
        if plan:
            for n in liste:
                if str(n) not in plan:
                    fehler.append(f"konten: {n} steht nicht im kontenplan in kurs.yaml")
        wahl = {str(n) for n in liste}

        def saetze_lesen():
            saetze = d.get("saetze")
            if saetze:
                d["saetze"] = [{"text": x.get("text", ""), "soll": zeilen(x.get("soll"), "soll"), "haben": zeilen(x.get("haben"), "haben")}
                               for x in saetze if isinstance(x, dict)]
            return d.get("saetze")

        def konten_pruefen(alle):
            for z in alle:
                if z["konto"] not in wahl:
                    fehler.append(f"Konto {z['konto']} kommt in der Lösung vor, fehlt aber in „konten“")

        if typ == "buchung":
            if not saetze_lesen():
                d["soll"], d["haben"] = zeilen(d.get("soll"), "soll"), zeilen(d.get("haben"), "haben")
            for blk in ("zahllast", "erfolg"):
                a = d.get(blk)
                if a is not None and (not isinstance(a, dict) or a.get("richtung") not in RICHTUNGEN or
                                      (a.get("richtung") != "gleich" and not betrag_ok(a.get("betrag")))):
                    fehler.append(f"{blk}: richtung (steigt|sinkt|gleich) und betrag nötig")
            a = d.get("steuerart")
            if a is not None and (not isinstance(a, dict) or a.get("art") not in ("vorsteuer", "umsatzsteuer", "keine") or
                                  (a.get("art") != "keine" and not betrag_ok(a.get("betrag")))):
                fehler.append("steuerart: art (vorsteuer|umsatzsteuer|keine) und betrag nötig")
            alle = (d.get("soll") or []) + (d.get("haben") or [])
            for x in d.get("saetze") or []:
                alle += x["soll"] + x["haben"]
            konten_pruefen(alle)
        else:
            tk = d.get("t_konten")
            if not isinstance(tk, list) or not tk:
                fehler.append("konten: „t_konten“ fehlt")
            else:
                neu = []
                for t in tk:
                    if not isinstance(t, dict) or "konto" not in t or not isinstance(t.get("ausgleich"), dict):
                        fehler.append("t_konten: jedes Konto braucht „konto“ und „ausgleich“")
                        continue
                    a = t["ausgleich"]
                    if a.get("seite") not in ("soll", "haben"):
                        fehler.append("ausgleich: seite soll | haben")
                    t = dict(t)
                    t["konto"] = konto(t["konto"], "t_konten")
                    a = dict(a)
                    a["zeilen"] = zeilen(a.get("zeilen"), "ausgleich")
                    konten_pruefen(a["zeilen"])
                    t["ausgleich"] = a
                    for seite in ("soll", "haben"):
                        for e in t.get(seite) or []:
                            if not betrag_ok(e.get("betrag")):
                                fehler.append(f"t_konten {seite}: „betrag“ muss eine Zahl oder Formel sein")
                    neu.append(t)
                d["t_konten"] = neu
            if saetze_lesen():
                alle = []
                for x in d["saetze"]:
                    alle += x["soll"] + x["haben"]
                konten_pruefen(alle)
    elif typ == "luecken":
        text, loes, wort = d.get("lueckentext"), d.get("loesung"), d.get("woerter")
        if not isinstance(text, str) or "[[" not in text:
            fehler.append("luecken: „lueckentext“ mit Lücken in [[a]] fehlt")
        else:
            ids = re.findall(r"\[\[(\w+)\]\]", text)
            if not isinstance(loes, dict) or set(ids) - set(map(str, loes)):
                fehler.append("luecken: „loesung“ muss jede Lücke enthalten")
            abl = d.get("ablenker")
            if abl is not None:
                if not isinstance(abl, dict) or any(not isinstance(abl.get(i), list) or not abl.get(i) for i in ids):
                    fehler.append("luecken: „ablenker“ braucht für jede Lücke eine Liste mit falschen Wörtern")
                else:
                    d["ablenker"] = {str(k): [str(w) for w in v] for k, v in abl.items()}
                    if isinstance(loes, dict):
                        d["loesung"] = {str(k): str(v) for k, v in loes.items()}
            elif not isinstance(wort, list) or (isinstance(loes, dict) and set(map(str, loes.values())) - set(map(str, wort))):
                fehler.append("luecken: „ablenker“ je Lücke (empfohlen) oder „woerter“ mit allen Lösungswörtern nötig")
            else:
                d["woerter"] = [str(w) for w in wort]
                d["loesung"] = {str(k): str(v) for k, v in loes.items()}
    elif typ == "lueckentext":
        text, luecken = d.get("lueckentext"), d.get("luecken")
        ids = re.findall(r"\[\[(\w+)\]\]", text) if isinstance(text, str) else []
        if not ids:
            fehler.append("lueckentext: „lueckentext“ mit Lücken in [[a]] fehlt")
        elif not isinstance(luecken, dict) or any(not isinstance(luecken.get(i), dict) or not luecken[i].get("akzeptiert") for i in ids):
            fehler.append("lueckentext: „luecken“ braucht je Lücke „akzeptiert“ (Liste)")
        else:
            d["luecken"] = {str(k): {**v, "akzeptiert": [str(a) for a in v["akzeptiert"]]} for k, v in luecken.items()}
    elif typ == "auswahl":
        o = d.get("optionen")
        if not isinstance(o, list) or len(o) < 2 or not all(isinstance(x, dict) and x.get("text") for x in o):
            fehler.append("auswahl: „optionen“ (mind. zwei, je mit text und korrekt) fehlt")
        elif not any(x.get("korrekt") for x in o):
            fehler.append("auswahl: mindestens eine Option muss korrekt sein")
        else:
            d["optionen"] = [{**x, "text": str(x["text"]).replace("`", ""), "korrekt": bool(x.get("korrekt"))} for x in o]
            for x in d["optionen"]:   # Buchungssatz in einer Zeile → Tabelle Soll | an | Haben (wie im Test)
                if "html" not in x and "{{" not in x["text"]:
                    tabelle = buchungssatz_html(x["text"])
                    if tabelle:
                        x["html"] = tabelle
            d["mehrfach"] = bool(d.get("mehrfach")) or sum(bool(x.get("korrekt")) for x in o) > 1
    elif typ == "zuordnung":
        kat, el = d.get("kategorien"), d.get("elemente")
        if not isinstance(kat, list) or len(kat) < 2 or not isinstance(el, list) or not el:
            fehler.append("zuordnung: „kategorien“ (mind. zwei) und „elemente“ (text, kategorie) nötig")
        elif any(not isinstance(e, dict) or e.get("kategorie") not in kat for e in el):
            fehler.append("zuordnung: jedes Element braucht eine „kategorie“ aus der Liste")
    elif typ == "reihenfolge":
        el = d.get("elemente")
        if not isinstance(el, list) or len(el) < 2:
            fehler.append("reihenfolge: „elemente“ (mind. zwei, in richtiger Reihenfolge) fehlt")
        else:
            d["elemente"] = [str(e) for e in el]
    elif typ == "offen":
        if not d.get("musterloesung"):
            fehler.append("offen: „musterloesung“ fehlt")
    if par or any("{{" in t for _, t in _walk_strings(d)):
        if typ not in ("lueckentext", "luecken"):
            _formeln_pruefen(d, par, fehler)
    d["namen"] = {k: v for k, v in namen.items() if v}
    return d, fehler


def lies_schloss(inhalt):
    """YAML eines :::schloss-Blocks → (Daten, Fehler). Pflicht: id, titel, code."""
    try:
        d = yaml.safe_load(inhalt)
    except yaml.YAMLError as e:
        return None, [f"YAML fehlerhaft – {str(e).splitlines()[0] if str(e) else e}"]
    fehler = []
    if not isinstance(d, dict):
        return None, ["Der Block braucht YAML mit id, titel und code"]
    if not re.fullmatch(r"[a-z0-9-]+", str(d.get("id", ""))):
        fehler.append("„id“ nötig (a–z, 0–9, Bindestrich)")
    if not d.get("titel"):
        fehler.append("„titel“ fehlt")
    if not re.fullmatch(r"[A-Za-z0-9 -]+", str(d.get("code", ""))):
        fehler.append("„code“ nötig (Ziffern, Buchstaben)")
    if fehler:
        return None, fehler
    out = {"id": str(d["id"]), "titel": str(d["titel"]), "code": str(d["code"]),
           "text": str(d.get("text", "")), "hinweis": str(d.get("hinweis", "")), "oeffnet": str(d.get("oeffnet", "")),
           "ziffern": bool(d.get("ziffern", str(d["code"]).isdigit()))}
    return out, []
