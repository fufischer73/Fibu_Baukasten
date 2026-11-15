# Moodle am BBZ Rendsburg-Eckernförde (Moodle 4.5.12 mit Unterabschnitt-Plugin)

Erfahrungen aus dem Pfad „Buchungen im Beschaffungsprozess“. Die allgemeine Moodle-Referenz des Baukastens steht in `moodle.md`.

## Was die Schule hat

- **Moodle 4.5.12+** (Build 20260624). **Unterabschnitt** gibt es als Plugin: Im Plus-Menü eines Abschnitts steht neben „Aktivität oder Material“ der Eintrag **„Unterabschnitt“**. Unterabschnitte sind Aktivitäten (`mod_subsection`), die einen eigenen Abschnitt tragen.
- **Keine Kurs-ID sichtbar.** Links lauten `…/course/section.php?id=…` mit der internen Abschnitts-ID, nicht mit der Abschnittsnummer. Darum nimmt man **keine Abschnittsnummer** (`moodle.abschnitt`).
- Kurse sind je Lernfeld aufgebaut, Pfade als Unterabschnitte („Übungs-Lernpfad Umsatzsteuer“, „Übungs-Lernpfad Beschaffung“).
- Fragetyp „Reihenfolge“ ist ab 4.4 im Standard. Keine H5P-Kurz-Checks.

## Einstellungen in kurs.yaml

```yaml
moodle:
  version: 4
  unterabschnitte: stufen        # ein Abschnitt, je Stufe ein Unterabschnitt; einer = alles in einem Unterabschnitt; true = je Modul einer
  unterabschnitt_name: Übungs-Lernpfad <Thema>
  start: false                   # kein Start-Lernpaket
  anordnung: true
  freischaltung: offen           # beide Stufen frei
  reihenfolge: frei
```

**Alle Aktivitäten in einem einzigen Unterabschnitt:** `unterabschnitte: flach`. Dann entsteht ein Abschnitt mit einem Unterabschnitt, darin alle Lernpakete und Tests hintereinander (Stufe für Stufe). Mit `trennbeschriftungen: true` (Standard) steht vor jeder Stufe ein Textfeld als Trenner („🌱 Schritt für Schritt“, „🎯 Überprüfung“ …), mit `false` entfällt es. Die Klickanleitung beschreibt genau diese Reihenfolge. Die Trenner (Aktivität „Text- und Medienfeld“, englisch *Label*) in der Kurssicherung sind am BBZ noch nicht getestet: im Testkurs prüfen, sonst `trennbeschriftungen: false` und die Trenner von Hand anlegen.

Mit `stufen` heißen die Unterabschnitte „Übungs-Lernpfad <Thema> – 🌱 Schritt für Schritt“ und „… – 🎯 Überprüfung“. Mit `einer` heißt der eine Unterabschnitt „Übungs-Lernpfad <Thema>“. Hat der Pfad nur eine Stufe, wird der Name nicht ergänzt.

## Empfohlener Weg: vorbereitete Unterabschnitte, nur Lernpakete einfügen

Seit dem Absatz-Pfad ist das der Hauptweg (die Klickanleitung `ausgabe/moodle/ANLEITUNG_moodle4.md` beschreibt ihn): Abschnitt und Unterabschnitte im Zielkurs selbst anlegen, dann die Lernpakete als Aktivitäten einfügen. Es muss nichts aus dem ersten Abschnitt verschoben und kein versteckter Unterabschnitt gezählt werden.

1. Das erste Lernpaket vollständig einrichten (Einstellungen in der Klickanleitung).
2. Im Kurs **duplizieren** und bei jedem Duplikat Namen ändern und die ZIP aus `download/lernpakete/` austauschen (Einstellungen › Paketdatei). Erst im Testkurs ausprobieren.
3. Den Abschlusstest von Hand einrichten (Fragen-XML) oder aus der Sicherung nur den Test wiederherstellen (Schritt „Schema“, nur den Test ankreuzen).
4. Änderungen später: nur die Paketdatei tauschen.

Die Kurssicherung (`…_moodle4.mbz`) bleibt als Alternative. Der folgende Ablauf gilt für sie.

## Ablauf der Übergabe mit der Kurssicherung

1. **Testkurs:** neuen, leeren Kurs anlegen. *Mehr › Wiederverwendung › Wiederherstellen*, `…_moodle4.mbz` hochladen, „In diesen Kurs, Inhalte hinzufügen“. Kontrollieren: Abschnitt mit den Unterabschnitten, Lernpakete öffnen sich, Test zeigt Belege und Buchungssätze als Tabelle.
2. **Echter Kurs:** vorher **Kurs sichern** (*Mehr › Wiederverwendung › Sichern*). Dann die Sicherung wiederherstellen (**einmal**).
3. Moodle legt den neuen Abschnitt bzw. den Unterabschnitt im **ersten Abschnitt** unter „Allgemeines“ an. Prüfen, ob sich sonst nichts verändert hat.
4. Unterabschnitt(e) über das Drei-Punkte-Menü (*Verschieben*) oder per Maus in den Ziel-Abschnitt schieben. Einen vorher angelegten leeren Unterabschnitt gleichen Namens **löschen**.
5. Ein Lernpaket und den Test als Schüler:in oder mit einem Testkonto ausprobieren.
6. **Änderungen später:** nur die **Lernpakete tauschen** (Lernpaket › Einstellungen › Paketdatei, neue ZIP aus `download/lernpakete/`). Der Fortschritt der Schüler:innen bleibt, solange die Modul-IDs gleich bleiben. **Nicht erneut wiederherstellen.**
7. Der Moodle-Test (Fragen) bleibt bei Änderungen an der Entwurfsmarkierung unverändert. Ändern sich Fragen selbst, den Test neu einspielen (XML-Import der Fragensammlung) und mit der Lehrkraft absprechen.

## Verhalten im Lernpaket

- Der **Kursindex** (linke Moodle-Leiste) wird beim Start geschlossen, damit die Belege Platz haben. Moodle merkt sich das Schließen als persönliche Einstellung.
- Zusatzseiten (Unternehmen, Kontenübersicht, Schemata) erscheinen als aufklappbare Kästen im Modul (`:::hilfe`) und in der Seitenleiste oben. Die Leiste scrollt mit dem Kurs; im Modul sind die Hilfen besser aufgehoben.
- Der Knopf „⤢ Mehr Platz“ im Lernpaket blendet die Moodle-Kopfzeile aus.

## Stolpersteine

- Eine Abschnittsnummer, die nicht stimmt, erzeugt leere Zusatzabschnitte (Umsatzsteuer-Pfad: 43 war falsch). Besser ohne Nummer arbeiten.
- Unterabschnitte haben eigene, versteckte Nummern (hinter den normalen Abschnitten). In Kursen mit vielen Abschnitten deshalb zuerst sichern oder eine Kurskopie testen.
- Die Web-Version bleibt der Weg zum Testen ohne Moodle. Die Moodle-Version speichert den Stand selbst.
