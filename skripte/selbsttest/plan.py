"""Plan für den Selbsttest: liest die gebauten Seiten (ausgabe/web) und berechnet für jede Rechen- und Buchungsaufgabe die
Musterlösung mit den Startwerten. Aufgaben mit Zahllast, Erfolg oder Steuerart werden ausgelassen.
  python3 plan.py <ordner> <plans.json>"""
import re, json, sys, glob
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bausteine as B

ordner = Path(sys.argv[1]).resolve()
plans = {}
for f in sorted(glob.glob(str(ordner / 'ausgabe' / 'web' / '*.html'))):
    if Path(f).name.startswith('test-'):   # Testseite: Zufallszahlen beim Öffnen, kein fester Startwert
        continue
    t = open(f, encoding='utf-8').read()
    blocks = re.findall(r'<section class="uebung-host"><script type="application/json">(.*?)</script>', t, re.S)
    pl = []
    for b in blocks:
        d = json.loads(b.replace('\\u003c', '<'))
        v = {k: (x.get('start') if x.get('start') is not None else x['von']) for k, x in (d.get('parameter') or {}).items()}
        item = None
        if d['typ'] == 'buchung' and not any(d.get(k) for k in ('steuerart', 'zahllast', 'erfolg')):
            sat = d.get('saetze') or [{'soll': d['soll'], 'haben': d['haben']}]
            item = {'typ': 'buchung', 'saetze': [
                {'soll': [(z['konto'], round(B.formel_wert(str(z['betrag']), v), 2)) for z in s['soll']],
                 'haben': [(z['konto'], round(B.formel_wert(str(z['betrag']), v), 2)) for z in s['haben']]} for s in sat]}
        elif d['typ'] == 'rechnen':
            res = []
            vv = dict(v)
            for fl in d['felder']:
                r = B.formel_wert(str(fl['formel']), vv) if fl.get('formel') is not None else fl['antwort']
                r = round(r, 2)
                res.append(r)
                if fl.get('id'):
                    vv[fl['id']] = r
            item = {'typ': 'rechnen', 'werte': res}
        pl.append(item)
    plans[f] = pl
json.dump(plans, open(sys.argv[2], 'w'))
print({k.split('/')[-1][:12]: sum(1 for x in v if x) for k, v in plans.items() if any(v)})
