"""Web-Version der Tests: aus den fragen/*.yaml eines Tests (tests: in kurs.yaml) wird eine Seite mit interaktiven Fragen.

Jede Frage bekommt sofort Rückmeldung (ein Versuch, dann Lösung); oben und unten steht der Zwischenstand
(„x von y richtig“). Der Moodle-Test bleibt davon unberührt. Mit  web: false  am Test lässt sich die Seite abschalten.
Die Seite erscheint unter „Immer griffbereit“ und gehört nicht in die Moodle-Lernpakete.
"""
import yaml

from gemeinsam import Fehler, buchungssatz_html, lies_yaml, slug


def _text(x):
    return "" if x is None else str(x)


def frage_zu_block(a):
    """Eine Frage aus fragen/*.yaml → Daten für :::uebung (oder None, wenn der Typ nicht passt)."""
    typ = a.get("typ")
    basis = {"titel": a.get("titel") or a.get("id", ""), "niveau": "basis", "text": _text(a.get("aufgabe")), "test": True}
    if a.get("beleg"):
        basis["beleg"] = a["beleg"]
    if typ in ("single_choice", "multiple_choice"):
        optionen = []
        for o in a.get("optionen") or []:
            e = {"text": _text(o.get("text")).replace("`", ""), "korrekt": bool(o.get("korrekt"))}
            if o.get("feedback"):
                e["feedback"] = _text(o["feedback"])
            tabelle = buchungssatz_html(e["text"])
            if tabelle:
                e["html"] = tabelle   # Buchungssatz als Tabelle (Soll | an | Haben)
            optionen.append(e)
        return {**basis, "typ": "auswahl", "mehrfach": typ == "multiple_choice", "optionen": optionen,
                "erklaerung": _text(a.get("erklaerung"))}
    if typ == "zuordnung":
        el = [{"text": _text(e.get("text")), "kategorie": _text(e.get("kategorie")),
               **({"feedback": _text(e["feedback"])} if e.get("feedback") else {})} for e in a.get("elemente") or []]
        return {**basis, "typ": "zuordnung", "kategorien": [str(k) for k in a.get("kategorien") or []], "elemente": el,
                "erklaerung": _text(a.get("erklaerung"))}
    if typ == "reihenfolge":
        return {**basis, "typ": "reihenfolge", "elemente": [str(e) for e in a.get("elemente") or []],
                "feedback_richtig": _text(a.get("feedback_richtig")), "feedback_falsch": _text(a.get("feedback_falsch"))}
    if typ == "lueckentext":
        text = _text(a.get("text")).replace("{{", "[[").replace("}}", "]]")
        luecken = {str(k): {"akzeptiert": [str(x) for x in (v.get("akzeptiert") or [])], **({"hinweis": _text(v["hinweis"])} if v.get("hinweis") else {})}
                   for k, v in (a.get("luecken") or {}).items()}
        return {**basis, "typ": "lueckentext", "lueckentext": text, "luecken": luecken}
    if typ == "zahl":
        par = {k: {"von": v["min"], "bis": v["max"], "schritt": v.get("schritt", 1)} for k, v in (a.get("parameter") or {}).items()}
        felder = []
        for x in a.get("antworten") or []:
            f = {"id": x.get("id"), "label": x.get("label") or "Ergebnis", "formel": str(x.get("formel")), "runden": x.get("runden", 2),
                 "hinweis": ""}
            if x.get("einheit"):
                f["einheit"] = x["einheit"]
            felder.append(f)
        d = {**basis, "typ": "rechnen", "felder": felder, "loesungsweg": _text(a.get("loesungsweg"))}
        if par:
            d["parameter"] = par
            d["zufall"] = True
        if a["antworten"] and a["antworten"][0].get("toleranz") is not None:
            d["toleranz"] = max(float(a["antworten"][0]["toleranz"]), 0.0) or 0.01
        return d
    if typ == "offen":
        return {**basis, "typ": "offen", "musterloesung": _text(a.get("musterloesung")),
                "checkliste": [str(x) for x in a.get("checkliste") or []], "zeilen": a.get("zeilen") or 6}
    return None


def testseiten(kurs):
    """Pseudo-Zusatzseiten (Web) für alle Tests ohne klausur: in kurs.yaml."""
    seiten = []
    for t in kurs.k.get("tests") or []:
        if t.get("klausur") or t.get("web") is False:
            continue
        dateien = t.get("fragen")
        if not dateien:
            continue
        dateien = [dateien] if isinstance(dateien, str) else dateien
        alle = {}
        for d in dateien:
            p = kurs.ordner / "fragen" / f"{d}.yaml"
            if not p.exists():
                raise Fehler(f"Test {t.get('id')}: fragen/{d}.yaml gibt es nicht")
            for a in lies_yaml(p, []) or []:
                a.setdefault("titel", a.get("id", ""))
                alle[a["id"]] = a
        ids = list(t.get("auswahl") or alle)
        ohne = set(t.get("ohne") or [])
        bloecke, entwurf = [], False
        for qid in ids:
            a = alle.get(qid)
            if a is None or qid in ohne:
                continue
            daten = frage_zu_block(a)
            if daten is None:
                continue
            entwurf = entwurf or a.get("review", "entwurf") != "freigegeben"
            bloecke.append(":::uebung\n" + yaml.safe_dump(daten, allow_unicode=True, sort_keys=False, width=1000).rstrip() + "\n:::\n")
        if not bloecke:
            continue
        titel = t.get("titel") or t["id"]
        anrede = (kurs.k.get("anrede") or "du") == "sie"
        intro = (("Hier können Sie sich selbst prüfen: Jede Frage wird sofort ausgewertet. " if anrede else
                  "Hier prüfst du dich selbst: Jede Frage wird sofort ausgewertet. ") +
                 "Pro Frage gibt es einen Versuch, danach erscheint die Lösung. Der Test kann beliebig oft neu gestartet werden. "
                 "Im Moodle-Kurs gibt es denselben Test mit Bewertung durch die Lehrkraft.")
        text = ((f":::notiz\n{t['text'].strip()}\n:::\n\n" if t.get("text") else "") + intro + "\n\n" +
                '<div class="ue-ergebnis"></div>\n\n' + "\n".join(bloecke) + '\n<div class="ue-ergebnis"></div>\n')
        tid = slug(t["id"])
        seiten.append({"titel": titel, "icon": "📝", "beschreibung": f"{len(bloecke)} Fragen zum Selbsttest, sofort ausgewertet.",
                       "reihenfolge": 90, "text": text, "datei": f"{tid if tid.startswith('test') else 'test-' + tid}.html",
                       "nur_web": True, "quelle": None, "entwurf": entwurf})
    return seiten
