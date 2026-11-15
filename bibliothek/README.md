# Bibliothek: wiederverwendbare Hilfen

Fertige Hilfsseiten und Hilfsblätter, die in mehreren Themen passen. So nutzt du sie in einem neuen Thema:

1. Datei aus `bibliothek/` nach `seiten/` des Themas kopieren (die DOCX nach `material/`).
2. Im Modul einbinden: `:::hilfe skonto-schema` (Abschnitt „Hilfen zum Aufklappen“).

| Datei | Inhalt | Wo sinnvoll |
| --- | --- | --- |
| `skonto-schema.md` und `.docx` | Skonto-Schema der Lehrkraft (waagerecht Skontosatz, senkrecht Umsatzsteuer, Felder 1 bis 5) mit Beispiel und Buchungssatz, Hilfsblatt zum Ausdrucken (ONLYOFFICE) | Beschaffung, Absatz (Kundenskonto), alles mit Skonto |
| `skonto-schema-verkauf.md` | Skonto-Schema für den **Verkauf** (Forderung, Erlösberichtigung 5001/5101, Umsatzsteuer 4800) mit Beispiel und Buchungssatz | Absatz, alles mit Kundenskonto |
| `hilfsblatt_erzeugen_absatz.py` | Erzeugt ein zweiseitiges DOCX-Hilfsblatt (A4) mit Merkzettel, Korrekturschema, Kontenübersicht und Skonto-Schema. Als Vorlage für weitere Themen kopieren und die Inhalte anpassen. | jedes Thema mit Nachschlagen-Stufe |

Neue Hilfsmittel der Lehrkraft (Schemata, Tabellen, Merkzettel) kommen hier hinein, wenn sie in mehr als einem Thema gebraucht werden.
Der **Merkzettel Buchen** liegt in `vorlage-thema/seiten/merkzettel.md` und gilt für alle Themen.
