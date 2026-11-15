#!/usr/bin/env python3
"""Selbsttest im Browser: Ein Automat füllt alle Rechen- und Buchungsaufgaben der Web-Version mit der Musterlösung aus
und klickt „Prüfen“. Jede Aufgabe muss „richtig“ melden. Fängt Fehler, die die reine Rechnung nicht sieht.

  python3 skripte/selbsttest.py <ordner>     (vorher alles.py oder bauen.py laufen lassen)

Voraussetzung: Node.js mit Playwright (npm i -g playwright; ein vorhandener Chrome oder Chromium reicht).
Nicht abgedeckt: Aufgaben mit Zahllast, Erfolg oder Steuerart, T-Konten, Auswahl, Zuordnung, Lückentext, Moodle selbst.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

hier = Path(__file__).resolve().parent / "selbsttest"
if len(sys.argv) < 2:
    sys.exit(__doc__)
ordner = Path(sys.argv[1]).resolve()
if not (ordner / "ausgabe" / "web").is_dir():
    sys.exit("✗ Erst bauen: python3 skripte/alles.py " + str(ordner))
plan = Path(tempfile.mkdtemp()) / "plans.json"
subprocess.run([sys.executable, str(hier / "plan.py"), str(ordner), str(plan)], check=True)
env = dict(os.environ)
try:
    env["NODE_PATH"] = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
except FileNotFoundError:
    sys.exit("✗ Node.js/npm fehlt")
r = subprocess.run(["node", str(hier / "solve.js"), str(plan)], env=env, capture_output=True, text=True)
print(r.stdout)
if r.returncode != 0:
    print(r.stderr[:800])
if r.returncode != 0:
    sys.exit("✗ Der Browser-Test ist abgebrochen (siehe Meldung oben).")
nok = [z for z in r.stdout.splitlines() if " NOK " in z]
print(f"✗ {len(nok)} Aufgabe(n) wurden nicht als richtig erkannt" if nok else "✓ Alle automatisch lösbaren Aufgaben nehmen ihre Musterlösung an")
sys.exit(1 if nok else 0)
