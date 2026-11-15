/* Interaktive Übungen (:::uebung): Rechnen, Buchungssätze, T-Konten, Lückentext, Auswahl, Zuordnung, Reihenfolge, offene Frage.
   Ablauf: Tipps nur auf Klick (gestuft) -> Eingabe -> „Prüfen“ -> bei Fehler Markierung und Hinweis (ohne Lösung)
   -> nach dem letzten Versuch oder bei richtiger Lösung: Lösung mit Rechenweg -> Parallelaufgabe mit anderen Zahlen.
   Parameter und Formeln (parameter:, formel:, {{n}}, {{=n*0.19:eur}}) erzeugen die Parallelaufgabe automatisch.
   Läuft ohne Server (Web-Version und Moodle-Lernpaket). Keine externen Abhängigkeiten. */
(function () {
  "use strict";
  var MAX_VERSUCHE = 2;
  var TOL = 0.005;

  /* ---------- Helfer ---------- */
  function h(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function fmt(s) {
    return esc(s == null ? "" : s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/\n/g, "<br>");
  }
  function zahl(s) {
    s = String(s == null ? "" : s).replace(/EUR/gi, "").replace(/[€\s ]/g, "");
    if (!s) return NaN;
    if (/^[+-]?\d{1,3}(\.\d{3})+(,\d+)?$/.test(s)) s = s.replace(/\./g, "").replace(",", ".");
    else if (s.indexOf(",") >= 0) s = s.replace(/\./g, "").replace(",", ".");
    if (!/^[+-]?\d+(\.\d+)?$/.test(s)) return NaN;
    return parseFloat(s);
  }
  function runde(x, d) {
    var m = Math.pow(10, d == null ? 2 : d);
    return (x < 0 ? -1 : 1) * Math.round(Math.abs(x) * m + 1e-7) / m;
  }
  function euro(n) { return n.toLocaleString("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " €"; }
  function zahlText(n, art) {
    if (art === "eur") return euro(n);
    return Math.abs(n - Math.round(n)) < 1e-9 ? Math.round(n).toLocaleString("de-DE")
      : n.toLocaleString("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  function gleich(a, b, tol) { return !isNaN(a) && !isNaN(b) && Math.abs(a - b) <= (tol == null ? TOL : tol) + 1e-9; }
  function mische(liste, saat) {
    var x = 2166136261;
    String(saat).split("").forEach(function (c) { x = Math.imul(x ^ c.charCodeAt(0), 16777619) >>> 0; });
    var a = liste.slice();
    for (var i = a.length - 1; i > 0; i--) {
      x = (Math.imul(x, 1664525) + 1013904223) >>> 0;
      var j = x % (i + 1), t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }
  function markiere(el, ok) {
    el.classList.remove("ue-ok", "ue-bad");
    if (ok === true) el.classList.add("ue-ok");
    if (ok === false) el.classList.add("ue-bad");
  }
  function entmarkiere(el) { el.classList.remove("ue-ok", "ue-bad"); }
  function norm(s) { return String(s == null ? "" : s).trim().toLowerCase().replace(/\s+/g, " "); }

  /* ---------- Formeln: + - * / ^ ( ) und round floor ceil abs min max sqrt ---------- */
  var FUNK = { round: runde, floor: Math.floor, ceil: Math.ceil, abs: Math.abs, min: Math.min, max: Math.max, sqrt: Math.sqrt };
  function kompiliere(src) {
    var tok = [], re = /\s*(?:(\d+(?:\.\d+)?)|([A-Za-z_]\w*)|(.))/g, m;
    while ((m = re.exec(src)) !== null) {
      if (m[1] != null) tok.push({ t: "n", v: parseFloat(m[1]) });
      else if (m[2] != null) tok.push({ t: "i", v: m[2] });
      else if (m[3] != null && m[3].trim()) tok.push({ t: "o", v: m[3] });
      if (re.lastIndex >= src.length) break;
    }
    var p = 0;
    function peek() { return tok[p]; }
    function nimm() { return tok[p++]; }
    function ausdruck() {
      var l = term();
      while (peek() && peek().t === "o" && (peek().v === "+" || peek().v === "-")) {
        var o = nimm().v, r = term(), a = l;
        l = (function (a, r, o) { return function (v) { return o === "+" ? a(v) + r(v) : a(v) - r(v); }; })(a, r, o);
      }
      return l;
    }
    function term() {
      var l = potenz();
      while (peek() && peek().t === "o" && (peek().v === "*" || peek().v === "/")) {
        var o = nimm().v, r = potenz(), a = l;
        l = (function (a, r, o) { return function (v) { return o === "*" ? a(v) * r(v) : a(v) / r(v); }; })(a, r, o);
      }
      return l;
    }
    function potenz() {
      var b = unaer();
      if (peek() && peek().t === "o" && peek().v === "^") {
        nimm();
        var e = potenz();
        return function (v) { return Math.pow(b(v), e(v)); };
      }
      return b;
    }
    function unaer() {
      if (peek() && peek().t === "o" && (peek().v === "-" || peek().v === "+")) {
        var o = nimm().v, a = unaer();
        return function (v) { return o === "-" ? -a(v) : a(v); };
      }
      return primaer();
    }
    function primaer() {
      var t = nimm();
      if (!t) throw new Error("Formel unvollständig: " + src);
      if (t.t === "n") return function () { return t.v; };
      if (t.t === "o" && t.v === "(") {
        var e = ausdruck();
        var z = nimm();
        if (!z || z.v !== ")") throw new Error("Klammer fehlt: " + src);
        return e;
      }
      if (t.t === "i") {
        if (peek() && peek().v === "(") {
          nimm();
          var args = [];
          if (!(peek() && peek().v === ")")) {
            args.push(ausdruck());
            while (peek() && peek().v === ",") { nimm(); args.push(ausdruck()); }
          }
          var z2 = nimm();
          if (!z2 || z2.v !== ")") throw new Error("Klammer fehlt: " + src);
          var f = FUNK[t.v];
          if (!f) throw new Error("Unbekannte Funktion " + t.v);
          return function (v) { return f.apply(null, args.map(function (a) { return a(v); })); };
        }
        return function (v) {
          if (!(t.v in v)) throw new Error("Unbekannte Variable " + t.v);
          return v[t.v];
        };
      }
      throw new Error("Unerwartet: " + t.v);
    }
    // „,“ als Trenner zulassen (in Funktionsaufrufen)
    var fn = ausdruck();
    if (p < tok.length) throw new Error("Unerwartetes Zeichen in Formel: " + src);
    return fn;
  }
  var CACHE = {};
  function wert(expr, vars) {
    var f = CACHE[expr] || (CACHE[expr] = kompiliere(String(expr).replace(/,(?!\s*[\d(A-Za-z_])/g, ",")));
    return f(vars || {});
  }
  function vorlage(s, vars) {
    return String(s).replace(/\{\{\s*(=)?\s*([^}:]+?)\s*(?::\s*(\w+))?\s*\}\}/g, function (m, ist, name, art) {
      var v;
      try { v = ist ? wert(name, vars) : vars[name]; } catch (e) { return m; }
      if (typeof v !== "number" || !isFinite(v)) return m;
      return zahlText(runde(v, 2), art);
    });
  }
  function zufall1(p) {
    var von = p.von != null ? p.von : p.min, bis = p.bis != null ? p.bis : p.max, st = p.schritt || 1;
    var n = Math.floor((bis - von) / st + 1e-9) + 1;
    return runde(von + st * Math.floor(Math.random() * n), 4);
  }
  function startWerte(par) {
    var v = {};
    Object.keys(par || {}).forEach(function (k) { v[k] = par[k].start != null ? par[k].start : zufall1(par[k]); });
    return v;
  }
  function zufallsWerte(par, ausser) {
    var v;
    for (var i = 0; i < 40; i++) {
      v = {};
      Object.keys(par || {}).forEach(function (k) { v[k] = zufall1(par[k]); });
      if (JSON.stringify(v) !== JSON.stringify(ausser)) break;
    }
    return v;
  }
  /* Parameter einsetzen: Formeln auswerten, Platzhalter {{…}} in Texten ersetzen. */
  function loese(d, vars) {
    var c = JSON.parse(JSON.stringify(d));
    var v = {};
    Object.keys(vars || {}).forEach(function (k) { v[k] = vars[k]; });
    if (c.typ === "rechnen") {
      (c.felder || []).forEach(function (f) {
        if (f.formel != null) f.antwort = runde(wert(f.formel, v), f.runden != null ? f.runden : 2);
        if (f.id) v[f.id] = f.antwort;
      });
    }
    function geh(o, schluessel) {
      if (Array.isArray(o)) return o.map(function (x) { return geh(x, schluessel); });
      if (o && typeof o === "object") {
        var r = {};
        Object.keys(o).forEach(function (k) { r[k] = k === "formel" || k === "parameter" ? o[k] : geh(o[k], k); });
        return r;
      }
      if (typeof o === "string") {
        if ((schluessel === "betrag" || schluessel === "antwort") && /^[\s\d.+\-*\/^()A-Za-z_,]+$/.test(o) && isNaN(Number(o)))
          return runde(wert(o, v), 2);
        return o.indexOf("{{") >= 0 ? vorlage(o, v) : o;
      }
      return o;
    }
    return geh(c, "");
  }


  /* ---------- Belege (Rechnung, Gutschrift, Kontoauszug …) ---------- */
  function belegRechts(t) { return /^[+\-–−]?\s*[\d.,\s]+\s*(€|%|EUR|Stück|m|l|kg|Liter|Meter)?$/.test(String(t).trim()); }
  function belegEl(b) {
    var stil = String(b.stil || "rechnung").replace(/[^a-z]/g, "");
    var w = h("div", "beleg beleg-" + stil);
    w.setAttribute("role", "group");
    w.setAttribute("aria-label", "Beleg: " + (b.art || ""));
    var kopf = h("div", "beleg-kopf");
    var firma = h("div", "beleg-firma");
    firma.appendChild(h("div", "beleg-firmenname", b.firma || ""));
    if (b.firma_zeile) firma.appendChild(h("div", "beleg-firmazeile", b.firma_zeile));
    kopf.appendChild(firma);
    kopf.appendChild(h("div", "beleg-art", String(b.art || "").toUpperCase()));
    w.appendChild(kopf);
    if ((b.empfaenger && b.empfaenger.length) || (b.info && b.info.length)) {
      var mitte = h("div", "beleg-mitte");
      var an = h("div", "beleg-anschrift");
      if (b.absender_zeile) an.appendChild(h("div", "beleg-absenderzeile", b.absender_zeile));
      (b.empfaenger || []).forEach(function (z) { an.appendChild(h("div", "", z)); });
      mitte.appendChild(an);
      var info = h("table", "beleg-info");
      (b.info || []).forEach(function (r) {
        var tr = h("tr"); tr.appendChild(h("td", "beleg-k", r[0])); tr.appendChild(h("td", "beleg-v", r[1])); info.appendChild(tr);
      });
      mitte.appendChild(info);
      w.appendChild(mitte);
    }
    if (b.spalten && b.spalten.length) {
      var rechts = b.spalten.map(function (_, i) {
        var leer = function (x) { return String(x == null ? "" : x).trim() === ""; };
        return (b.zeilen || []).some(function (z) { return !leer(z[i]); }) && b.zeilen.every(function (z) { return leer(z[i]) || belegRechts(z[i]); });
      });
      var wrap = h("div", "beleg-tabelle");
      var t = h("table", "beleg-pos");
      var tr = h("tr");
      b.spalten.forEach(function (sp, i) { tr.appendChild(h("th", rechts[i] ? "re" : "", sp)); });
      var th = h("thead"); th.appendChild(tr); t.appendChild(th);
      var tb = h("tbody");
      (b.zeilen || []).forEach(function (z) {
        var r = h("tr");
        z.forEach(function (c, i) { r.appendChild(h("td", rechts[i] ? "re" : "", c)); });
        tb.appendChild(r);
      });
      t.appendChild(tb); wrap.appendChild(t); w.appendChild(wrap);
    }
    if (b.summen && b.summen.length) {
      var sw = h("div", "beleg-tabelle");
      var st = h("table", "beleg-summen");
      b.summen.forEach(function (z) {
        var r = h("tr", z[2] ? "fett" : "");
        r.appendChild(h("td", "", z[0])); r.appendChild(h("td", "re", z[1])); st.appendChild(r);
      });
      sw.appendChild(st); w.appendChild(sw);
    }
    if (b.text) { var tx = h("div", "beleg-text"); tx.innerHTML = fmt(b.text); w.appendChild(tx); }
    if (b.bedingungen) { var bd = h("div", "beleg-bedingungen"); bd.innerHTML = fmt(b.bedingungen); w.appendChild(bd); }
    if (b.fuss) w.appendChild(h("div", "beleg-fuss", b.fuss));
    if (b.stempel) { var sp = h("div", "beleg-stempel"); sp.innerHTML = fmt(b.stempel); w.appendChild(sp); }
    return w;
  }
  function belegeEl(b) {
    var liste = Array.isArray(b) ? b : [b];
    var box = h("div", "beleg-gruppe");
    liste.forEach(function (x) { box.appendChild(belegEl(x)); });
    return box;
  }

  /* ---------- Konto-Auswahl und Buchungszeilen ---------- */
  function kontoSelect(d) {
    var s = h("select", "ue-konto");
    s.setAttribute("aria-label", "Konto");
    var o = h("option", "", "Konto wählen …");
    o.value = "";
    s.appendChild(o);
    (d.konten || []).forEach(function (k) {
      var op = h("option", "", k.nr + " " + k.name);
      op.value = k.nr;
      s.appendChild(op);
    });
    return s;
  }
  function betragInput() {
    var i = h("input", "ue-betrag");
    i.type = "text";
    i.inputMode = "decimal";
    i.placeholder = "Betrag";
    i.setAttribute("aria-label", "Betrag in Euro");
    i.autocomplete = "off";
    return i;
  }
  function kontoName(d, nr) { return nr + " " + ((d.namen || {})[nr] || ""); }

  function zeilenBlock(d, start, max, onChange) {
    var wrap = h("div", "ue-zeilen");
    var liste = h("div", "ue-zeilenliste");
    var plus = h("button", "btn secondary ue-plus", "+ Zeile");
    plus.type = "button";
    var zeilen = [];
    function neu() {
      var z = { el: h("div", "ue-zeile"), konto: kontoSelect(d), betrag: betragInput() };
      z.el.appendChild(z.konto);
      z.el.appendChild(z.betrag);
      var weg = h("button", "ue-weg", "✕");
      weg.type = "button";
      weg.setAttribute("aria-label", "Zeile entfernen");
      weg.onclick = function () {
        if (zeilen.length <= 1) { z.konto.value = ""; z.betrag.value = ""; entmarkiere(z.konto); entmarkiere(z.betrag); onChange(); return; }
        liste.removeChild(z.el);
        zeilen.splice(zeilen.indexOf(z), 1);
        plus.disabled = false;
        onChange();
      };
      z.weg = weg;
      z.el.appendChild(weg);
      z.konto.onchange = z.betrag.oninput = function () { entmarkiere(z.konto); entmarkiere(z.betrag); onChange(); };
      zeilen.push(z);
      liste.appendChild(z.el);
      if (zeilen.length >= max) plus.disabled = true;
      return z;
    }
    plus.onclick = function () { if (zeilen.length < max) { neu().konto.focus(); onChange(); } };
    for (var i = 0; i < start; i++) neu();
    wrap.appendChild(liste);
    wrap.appendChild(plus);
    return {
      el: wrap,
      zeilen: zeilen,
      aktiv: function () { return zeilen.filter(function (z) { return z.konto.value || String(z.betrag.value).trim(); }); },
      sperren: function (b) {
        zeilen.forEach(function (z) { z.konto.disabled = b; z.betrag.disabled = b; z.weg.disabled = b; });
        plus.disabled = b || zeilen.length >= max;
      },
      zuruecksetzen: function () {
        while (zeilen.length > start) liste.removeChild(zeilen.pop().el);
        zeilen.forEach(function (z) { z.konto.value = ""; z.betrag.value = ""; entmarkiere(z.konto); entmarkiere(z.betrag); });
        this.sperren(false);
      },
      zustand: function () { return zeilen.map(function (z) { return [z.konto.value, z.betrag.value]; }); },
      laden: function (arr) {
        this.zuruecksetzen();
        arr = Array.isArray(arr) ? arr : [];
        while (zeilen.length < arr.length && zeilen.length < max) neu();
        arr.forEach(function (v, i) {
          if (!zeilen[i] || !Array.isArray(v)) return;
          var ok = Array.prototype.some.call(zeilen[i].konto.options, function (o) { return o.value === String(v[0]); });
          if (ok) zeilen[i].konto.value = String(v[0]);
          zeilen[i].betrag.value = String(v[1] == null ? "" : v[1]).slice(0, 20);
        });
      }
    };
  }

  function vergleiche(block, erwartet) {
    var frei = erwartet.map(function (e) { return { konto: String(e.konto), betrag: Number(e.betrag) }; });
    var zeilen = block.aktiv();
    var res = zeilen.map(function () { return { konto: false, betrag: false, voll: false }; });
    zeilen.forEach(function (z, i) {
      var b = zahl(z.betrag.value);
      for (var j = 0; j < frei.length; j++) {
        if (frei[j] && frei[j].konto === z.konto.value && gleich(frei[j].betrag, b)) {
          res[i] = { konto: true, betrag: true, voll: true };
          frei[j] = null;
          return;
        }
      }
    });
    zeilen.forEach(function (z, i) {
      if (res[i].voll) return;
      for (var j = 0; j < frei.length; j++) {
        if (frei[j] && frei[j].konto === z.konto.value) { res[i].konto = true; frei[j] = null; return; }
      }
    });
    var fehlend = frei.filter(Boolean).length;
    zeilen.forEach(function (z, i) { markiere(z.konto, res[i].konto); markiere(z.betrag, res[i].betrag); });
    block.zeilen.forEach(function (z) { if (zeilen.indexOf(z) < 0) { entmarkiere(z.konto); entmarkiere(z.betrag); } });
    return {
      ok: fehlend === 0 && res.length === erwartet.length && res.every(function (r) { return r.voll; }),
      fehlend: fehlend,
      kontoFalsch: res.some(function (r) { return !r.konto; }),
      betragFalsch: res.some(function (r) { return r.konto && !r.betrag; }),
      summe: zeilen.reduce(function (s, z) { var b = zahl(z.betrag.value); return s + (isNaN(b) ? 0 : b); }, 0)
    };
  }
  function satzTabelle(d, soll, haben) {
    function zeile(z) { return [esc(kontoName(d, String(z.konto))).trim(), euro(Number(z.betrag))]; }
    var n = Math.max(soll.length, haben.length), rows = "";
    for (var i = 0; i < n; i++) {
      var a = soll[i] ? zeile(soll[i]) : ["", ""], b = haben[i] ? zeile(haben[i]) : ["", ""];
      rows += "<tr><td>" + a[0] + "</td><td class=\"zahl\">" + (soll[i] ? a[1] : "") + "</td><td class=\"an\">" + (i === 0 ? "an" : "") +
        "</td><td>" + b[0] + "</td><td class=\"zahl\">" + (haben[i] ? b[1] : "") + "</td></tr>";
    }
    return "<table class=\"ue-bs\"><tr><th colspan=\"2\">Soll</th><th></th><th colspan=\"2\">Haben</th></tr>" + rows + "</table>";
  }
  function satzText(d, soll, haben) {
    function teil(zl) { return zl.map(function (z) { return kontoName(d, String(z.konto)) + " " + euro(Number(z.betrag)); }).join(" und "); }
    return teil(soll) + " an " + teil(haben);
  }

  /* ---------- Typ: rechnen ---------- */
  function euroOderZahl(f) {
    var n = Number(f.antwort);
    if (f.einheit === "€") return euro(n);
    return zahlText(n) + (f.einheit ? " " + f.einheit : "");
  }
  function tRechnen(d, body) {
    var felder = d.felder.map(function (f) {
      var zeile = h("label", "ue-feld");
      zeile.appendChild(h("span", "ue-label", f.label));
      var i = h("input", "ue-betrag");
      i.type = "text"; i.inputMode = "decimal"; i.autocomplete = "off";
      i.placeholder = "Ergebnis";
      i.oninput = function () { entmarkiere(i); };
      zeile.appendChild(i);
      if (f.einheit) zeile.appendChild(h("span", "ue-einheit", f.einheit));
      body.appendChild(zeile);
      return { f: f, i: i };
    });
    return {
      leer: function () { return felder.every(function (x) { return !x.i.value.trim(); }); },
      bewerte: function () {
        var ok = true, hinweise = [];
        felder.forEach(function (x) {
          var gut = gleich(zahl(x.i.value), Number(x.f.antwort), d.toleranz);
          markiere(x.i, gut);
          if (!gut) { ok = false; if (x.f.hinweis) hinweise.push(x.f.label + ": " + x.f.hinweis); }
        });
        return { ok: ok, hinweise: hinweise };
      },
      loesung: function () { return felder.map(function (x) { return "**" + x.f.label + ":** " + euroOderZahl(x.f); }).join("\n"); },
      sperren: function (b) { felder.forEach(function (x) { x.i.disabled = b; }); },
      zuruecksetzen: function () { felder.forEach(function (x) { x.i.value = ""; entmarkiere(x.i); x.i.disabled = false; }); },
      zustand: function () { return felder.map(function (x) { return x.i.value; }); },
      laden: function (a) { (Array.isArray(a) ? a : []).forEach(function (v, i) { if (felder[i]) felder[i].i.value = String(v).slice(0, 20); }); }
    };
  }

  /* ---------- Auswirkung (Steuerart, Zahllast, Erfolg) ---------- */
  var RICHT_ZAHLLAST = [["steigt", "Die Zahllast steigt"], ["sinkt", "Die Zahllast sinkt"], ["gleich", "Die Zahllast bleibt unverändert"]];
  var RICHT_ERFOLG = [["steigt", "Der Gewinn steigt"], ["sinkt", "Der Gewinn sinkt"], ["gleich", "Keine Auswirkung auf den Erfolg"]];
  var ART_STEUER = [["vorsteuer", "Vorsteuer (Forderung gegenüber dem Finanzamt)"], ["umsatzsteuer", "Umsatzsteuer (Verbindlichkeit gegenüber dem Finanzamt)"], ["keine", "Keine Steuer im Betrag"]];
  function auswirkung(titel, optionen, soll, neutral, platzhalter) {
    neutral = neutral || "gleich";
    var wrap = h("div", "ue-auswirkung");
    wrap.appendChild(h("div", "ue-auswirkung-titel", titel));
    var zeile = h("div", "ue-zeile");
    var s = h("select", "ue-konto");
    s.setAttribute("aria-label", titel);
    var o0 = h("option", "", "bitte wählen …"); o0.value = ""; s.appendChild(o0);
    optionen.forEach(function (o) { var op = h("option", "", o[1]); op.value = o[0]; s.appendChild(op); });
    var b = betragInput(); b.placeholder = platzhalter || "um … €";
    b.setAttribute("aria-label", "Betrag der Veränderung in Euro");
    s.onchange = b.oninput = function () { entmarkiere(s); entmarkiere(b); };
    zeile.appendChild(s); zeile.appendChild(b);
    wrap.appendChild(zeile);
    return {
      el: wrap,
      leer: function () { return !s.value && !b.value.trim(); },
      bewerte: function () {
        var rOk = s.value === soll.richtung;
        var bOk;
        if (soll.richtung === neutral) bOk = !b.value.trim() || gleich(zahl(b.value), 0);
        else bOk = gleich(zahl(b.value), Number(soll.betrag));
        markiere(s, rOk); markiere(b, rOk && bOk ? true : (soll.richtung === neutral && !b.value.trim() ? null : bOk));
        return rOk && bOk;
      },
      text: function () {
        var l = optionen.filter(function (o) { return o[0] === soll.richtung; })[0][1];
        if (soll.richtung === neutral) return l;
        return optionen === ART_STEUER ? l.split(" (")[0] + " " + euro(Number(soll.betrag)) : l + " um " + euro(Number(soll.betrag));
      },
      sperren: function (x) { s.disabled = x; b.disabled = x; },
      zuruecksetzen: function () { s.value = ""; b.value = ""; entmarkiere(s); entmarkiere(b); s.disabled = false; b.disabled = false; },
      zustand: function () { return [s.value, b.value]; },
      laden: function (a) {
        if (!Array.isArray(a)) return;
        if (Array.prototype.some.call(s.options, function (o) { return o.value === String(a[0]); })) s.value = String(a[0]);
        b.value = String(a[1] == null ? "" : a[1]).slice(0, 20);
      }
    };
  }

  /* ---------- Typ: buchung ---------- */
  function tBuchung(d, body, onChange) {
    onChange = onChange || function () {};
    var saetze = d.saetze && d.saetze.length ? d.saetze : [{ soll: d.soll, haben: d.haben }];
    var teile = saetze.map(function (s) {
      var box = h("div", "ue-satz");
      if (s.text) box.appendChild(h("div", "ue-satz-titel", s.text));
      var grid = h("div", "ue-buchung");
      var cs = h("div", "ue-seite"), ch = h("div", "ue-seite");
      cs.appendChild(h("div", "ue-seite-titel", "Soll"));
      ch.appendChild(h("div", "ue-seite-titel", "Haben"));
      var soll = zeilenBlock(d, 1, s.soll.length + 2, onChange);
      var haben = zeilenBlock(d, 1, s.haben.length + 2, onChange);
      cs.appendChild(soll.el); ch.appendChild(haben.el);
      grid.appendChild(cs);
      grid.appendChild(h("div", "ue-an", "an"));
      grid.appendChild(ch);
      box.appendChild(grid);
      body.appendChild(box);
      return { s: s, soll: soll, haben: haben };
    });
    var st = d.steuerart ? auswirkung("Handelt es sich um Umsatzsteuer oder Vorsteuer?", ART_STEUER,
      { richtung: d.steuerart.art, betrag: d.steuerart.betrag }, "keine", "Steuerbetrag in €") : null;
    var zl = d.zahllast ? auswirkung("Auswirkung auf die Umsatzsteuer-Zahllast", RICHT_ZAHLLAST, d.zahllast) : null;
    var er = d.erfolg ? auswirkung("Auswirkung auf den Erfolg des Unternehmens", RICHT_ERFOLG, d.erfolg) : null;
    if (st) body.appendChild(st.el);
    if (zl) body.appendChild(zl.el);
    if (er) body.appendChild(er.el);
    return {
      leer: function () {
        return teile.every(function (t) { return !t.soll.aktiv().length && !t.haben.aktiv().length; }) &&
          (!st || st.leer()) && (!zl || zl.leer()) && (!er || er.leer());
      },
      bewerte: function () {
        var ok = true, hinweise = {};
        teile.forEach(function (t) {
          var a = vergleiche(t.soll, t.s.soll), b = vergleiche(t.haben, t.s.haben);
          if (!a.ok || !b.ok) ok = false;
          if (a.kontoFalsch || b.kontoFalsch) hinweise["Mindestens ein Konto ist falsch gewählt oder steht auf der falschen Seite."] = 1;
          if (a.betragFalsch || b.betragFalsch) hinweise["Bei mindestens einem Konto stimmt der Betrag nicht."] = 1;
          if (a.fehlend) hinweise["Auf der Soll-Seite fehlt noch mindestens ein Konto."] = 1;
          if (b.fehlend) hinweise["Auf der Haben-Seite fehlt noch mindestens ein Konto."] = 1;
          if (t.soll.aktiv().length && t.haben.aktiv().length && Math.abs(a.summe - b.summe) > TOL)
            hinweise["Die Summe im Soll muss genauso hoch sein wie die Summe im Haben."] = 1;
        });
        if (st && !st.bewerte()) { ok = false; hinweise["Prüfe, ob im Betrag Umsatzsteuer oder Vorsteuer steckt."] = 1; }
        if (zl && !zl.bewerte()) { ok = false; hinweise["Prüfe die Auswirkung auf die Zahllast."] = 1; }
        if (er && !er.bewerte()) { ok = false; hinweise["Prüfe die Auswirkung auf den Erfolg."] = 1; }
        return { ok: ok, hinweise: Object.keys(hinweise) };
      },
      loesung: function () {
        var z = teile.map(function (t) { return (t.s.text ? "**" + t.s.text + "**\n" : "") + satzText(d, t.s.soll, t.s.haben); });
        if (st) z.push("**Steuer:** " + st.text() + ".");
        if (zl) z.push("**Zahllast:** " + zl.text() + ".");
        if (er) z.push("**Erfolg:** " + er.text() + ".");
        return z.join("\n");
      },
      loesungHtml: function () {
        var z = teile.map(function (t) {
          return (t.s.text ? "<strong>" + esc(t.s.text) + "</strong>" : "") + satzTabelle(d, t.s.soll, t.s.haben);
        });
        var extra = [];
        if (st) extra.push("**Steuer:** " + st.text() + ".");
        if (zl) extra.push("**Zahllast:** " + zl.text() + ".");
        if (er) extra.push("**Erfolg:** " + er.text() + ".");
        return z.join("") + (extra.length ? "<div>" + fmt(extra.join("\n")) + "</div>" : "");
      },
      sperren: function (b) {
        teile.forEach(function (t) { t.soll.sperren(b); t.haben.sperren(b); });
        if (st) st.sperren(b);
        if (zl) zl.sperren(b);
        if (er) er.sperren(b);
      },
      zuruecksetzen: function () {
        teile.forEach(function (t) { t.soll.zuruecksetzen(); t.haben.zuruecksetzen(); });
        if (st) st.zuruecksetzen();
        if (zl) zl.zuruecksetzen();
        if (er) er.zuruecksetzen();
      },
      zustand: function () {
        return { t: teile.map(function (t) { return { s: t.soll.zustand(), h: t.haben.zustand() }; }),
          st: st ? st.zustand() : null, zl: zl ? zl.zustand() : null, er: er ? er.zustand() : null };
      },
      laden: function (z) {
        if (!z || !Array.isArray(z.t)) return;
        teile.forEach(function (t, i) { if (z.t[i]) { t.soll.laden(z.t[i].s); t.haben.laden(z.t[i].h); } });
        if (st) st.laden(z.st);
        if (zl) zl.laden(z.zl);
        if (er) er.laden(z.er);
      }
    };
  }

  function kombiniere(a, b) {
    return {
      leer: function () { return a.leer() && b.leer(); },
      bewerte: function () {
        var x = a.bewerte(), y = b.bewerte();
        return { ok: x.ok && y.ok, hinweise: (x.hinweise || []).concat(y.hinweise || []) };
      },
      loesung: function () { return a.loesung() + "\n" + b.loesung(); },
      loesungHtml: function () {
        return (a.loesungHtml ? a.loesungHtml() : fmt(a.loesung())) + (b.loesungHtml ? b.loesungHtml() : fmt(b.loesung()));
      },
      sperren: function (v) { a.sperren(v); b.sperren(v); },
      zuruecksetzen: function () { a.zuruecksetzen(); b.zuruecksetzen(); },
      zustand: function () { return { a: a.zustand(), b: b.zustand() }; },
      laden: function (z) { a.laden(z && z.a); b.laden(z && z.b); }
    };
  }

  /* ---------- Typ: konten (T-Konten, optional mit Abschlussbuchungen) ---------- */
  function tKonten(d, body) {
    var aktualisieren = function () {};
    var konten = d.t_konten.map(function (tk) {
      var box = h("div", "ue-tkonto");
      var kopf = h("div", "ue-tkopf");
      kopf.appendChild(h("span", "", "S"));
      kopf.appendChild(h("strong", "", kontoName(d, String(tk.konto))));
      kopf.appendChild(h("span", "", "H"));
      box.appendChild(kopf);
      var gitter = h("div", "ue-tgitter");
      var links = h("div", "ue-tseite"), rechts = h("div", "ue-tseite");
      var seite = tk.ausgleich.seite;
      var summeGegeben = { soll: 0, haben: 0 };
      ["soll", "haben"].forEach(function (s) {
        var ziel = s === "soll" ? links : rechts;
        (tk[s] || []).forEach(function (e) {
          var p = h("div", "ue-gegeben");
          p.appendChild(h("span", "", e.text || ""));
          p.appendChild(h("span", "ue-gb", euro(Number(e.betrag))));
          ziel.appendChild(p);
          summeGegeben[s] += Number(e.betrag);
        });
      });
      var block = zeilenBlock(d, 1, tk.ausgleich.zeilen.length + 2, function () { aktualisieren(); });
      (seite === "soll" ? links : rechts).appendChild(block.el);
      gitter.appendChild(links); gitter.appendChild(rechts);
      box.appendChild(gitter);
      var summe = h("div", "ue-tsumme");
      var sl = h("span", "", ""), sr = h("span", "", "");
      summe.appendChild(sl); summe.appendChild(h("strong", "", "Summe")); summe.appendChild(sr);
      box.appendChild(summe);
      body.appendChild(box);
      var obj = { tk: tk, block: block };
      obj.rechne = function () {
        var s = block.aktiv().reduce(function (a, z) { var b = zahl(z.betrag.value); return a + (isNaN(b) ? 0 : b); }, 0);
        var soll = summeGegeben.soll + (seite === "soll" ? s : 0), haben = summeGegeben.haben + (seite === "haben" ? s : 0);
        sl.textContent = soll ? euro(soll) : "–";
        sr.textContent = haben ? euro(haben) : "–";
        summe.classList.toggle("ue-gleich", soll > 0 && Math.abs(soll - haben) <= TOL);
      };
      return obj;
    });
    aktualisieren = function () { konten.forEach(function (k) { k.rechne(); }); };
    aktualisieren();
    var t1 = {
      leer: function () { return konten.every(function (k) { return !k.block.aktiv().length; }); },
      bewerte: function () {
        var ok = true, hinweise = {};
        konten.forEach(function (k) {
          var r = vergleiche(k.block, k.tk.ausgleich.zeilen);
          if (!r.ok) ok = false;
          if (r.kontoFalsch) hinweise["Bei einem Konto stimmt das Gegenkonto nicht."] = 1;
          if (r.betragFalsch) hinweise["Bei einem Konto stimmt der Betrag nicht."] = 1;
          if (r.fehlend) hinweise["Bei einem Konto fehlt noch mindestens eine Buchung."] = 1;
        });
        return { ok: ok, hinweise: Object.keys(hinweise) };
      },
      loesung: function () {
        return d.t_konten.map(function (tk) {
          return "**" + kontoName(d, String(tk.konto)) + "** (" + (tk.ausgleich.seite === "soll" ? "Soll" : "Haben") + "-Seite): " +
            tk.ausgleich.zeilen.map(function (z) { return kontoName(d, String(z.konto)) + " " + euro(Number(z.betrag)); }).join(", ");
        }).join("\n");
      },
      loesungHtml: function () {
        var rows = "";
        d.t_konten.forEach(function (tk) {
          tk.ausgleich.zeilen.forEach(function (z, i) {
            rows += "<tr><td>" + (i === 0 ? esc(kontoName(d, String(tk.konto))).trim() : "") + "</td><td>" + (i === 0 ? (tk.ausgleich.seite === "soll" ? "Soll" : "Haben") : "") +
              "</td><td>" + esc(kontoName(d, String(z.konto))).trim() + "</td><td class=\"zahl\">" + euro(Number(z.betrag)) + "</td></tr>";
          });
        });
        return "<table class=\"ue-bs\"><tr><th>Konto</th><th>Seite</th><th>Gegenkonto</th><th>Betrag</th></tr>" + rows + "</table>";
      },
      sperren: function (b) { konten.forEach(function (k) { k.block.sperren(b); }); },
      zuruecksetzen: function () { konten.forEach(function (k) { k.block.zuruecksetzen(); k.rechne(); }); },
      zustand: function () { return konten.map(function (k) { return k.block.zustand(); }); },
      laden: function (a) { konten.forEach(function (k, i) { k.block.laden(Array.isArray(a) ? a[i] : []); k.rechne(); }); }
    };
    if (d.saetze && d.saetze.length) {
      body.appendChild(h("div", "ue-abschnitt", "Abschlussbuchungen"));
      return kombiniere(t1, tBuchung(d, body));
    }
    return t1;
  }

  /* ---------- Typ: luecken (Auswahl je Lücke) ---------- */
  function tLuecken(d, body) {
    var woerter = (d.woerter || []).slice().sort(function (a, b) { return a.localeCompare(b, "de"); });
    function optionenFuer(k) {
      if (d.ablenker && d.ablenker[k]) return mische([d.loesung[k]].concat(d.ablenker[k]), d.titel + "|" + k);
      return woerter;
    }
    var p = h("div", "ue-luecken");
    var selects = {};
    String(d.lueckentext).split(/\[\[(\w+)\]\]/).forEach(function (t, i) {
      if (i % 2 === 0) {
        var span = h("span");
        span.innerHTML = fmt(t);
        p.appendChild(span);
      } else {
        var s = h("select", "ue-luecke");
        s.setAttribute("aria-label", "Lücke " + t);
        var o = h("option", "", "…"); o.value = ""; s.appendChild(o);
        optionenFuer(t).forEach(function (w) { var op = h("option", "", w); op.value = w; s.appendChild(op); });
        s.onchange = function () { entmarkiere(s); };
        selects[t] = s;
        p.appendChild(s);
      }
    });
    body.appendChild(p);
    var ids = Object.keys(selects);
    return {
      leer: function () { return ids.every(function (k) { return !selects[k].value; }); },
      bewerte: function () {
        var richtig = 0;
        ids.forEach(function (k) {
          var gut = selects[k].value === d.loesung[k];
          markiere(selects[k], gut);
          if (gut) richtig++;
        });
        return { ok: richtig === ids.length, hinweise: ["Richtig sind " + richtig + " von " + ids.length + " Lücken."] };
      },
      loesung: function () { return String(d.lueckentext).replace(/\[\[(\w+)\]\]/g, function (_, k) { return "**" + d.loesung[k] + "**"; }); },
      sperren: function (b) { ids.forEach(function (k) { selects[k].disabled = b; }); },
      zuruecksetzen: function () { ids.forEach(function (k) { selects[k].value = ""; entmarkiere(selects[k]); selects[k].disabled = false; }); },
      zustand: function () { var o = {}; ids.forEach(function (k) { o[k] = selects[k].value; }); return o; },
      laden: function (o) {
        if (!o || typeof o !== "object") return;
        ids.forEach(function (k) {
          var v = String(o[k] == null ? "" : o[k]);
          if (Array.prototype.some.call(selects[k].options, function (op) { return op.value === v; })) selects[k].value = v;
        });
      }
    };
  }

  /* ---------- Typ: lueckentext (Freitext, Test) ---------- */
  function tFreitextLuecken(d, body) {
    var p = h("div", "ue-luecken");
    var felder = {};
    String(d.lueckentext).split(/\[\[(\w+)\]\]/).forEach(function (t, i) {
      if (i % 2 === 0) { var span = h("span"); span.innerHTML = fmt(t); p.appendChild(span); }
      else {
        var inp = h("input", "ue-betrag ue-text-input");
        inp.type = "text"; inp.autocomplete = "off"; inp.setAttribute("aria-label", "Lücke " + t);
        inp.oninput = function () { entmarkiere(inp); };
        felder[t] = inp;
        p.appendChild(inp);
      }
    });
    body.appendChild(p);
    var ids = Object.keys(felder);
    function akz(k) { return (d.luecken[k].akzeptiert || []).map(String); }
    return {
      leer: function () { return ids.every(function (k) { return !felder[k].value.trim(); }); },
      bewerte: function () {
        var ok = true, hinweise = [];
        ids.forEach(function (k) {
          var v = norm(felder[k].value);
          var gut = akz(k).some(function (a) { return norm(a) === v || (!isNaN(zahl(a)) && gleich(zahl(a), zahl(v), 0)); });
          markiere(felder[k], gut);
          if (!gut) { ok = false; if (d.luecken[k].hinweis) hinweise.push(d.luecken[k].hinweis); }
        });
        return { ok: ok, hinweise: hinweise };
      },
      loesung: function () { return String(d.lueckentext).replace(/\[\[(\w+)\]\]/g, function (_, k) { return "**" + akz(k)[0] + "**"; }); },
      sperren: function (b) { ids.forEach(function (k) { felder[k].disabled = b; }); },
      zuruecksetzen: function () { ids.forEach(function (k) { felder[k].value = ""; entmarkiere(felder[k]); felder[k].disabled = false; }); },
      zustand: function () { var o = {}; ids.forEach(function (k) { o[k] = felder[k].value; }); return o; },
      laden: function (o) { if (o && typeof o === "object") ids.forEach(function (k) { if (o[k] != null) felder[k].value = String(o[k]).slice(0, 60); }); }
    };
  }

  /* ---------- Typ: auswahl (Single/Multiple Choice) ---------- */
  function tAuswahl(d, body) {
    var mehr = !!d.mehrfach;
    var name = "ue" + Math.random().toString(36).slice(2, 8);
    var reihe = d.optionen.map(function (o, i) { return i; });
    if (d.mischen !== false) reihe = mische(reihe, d.titel);
    var eintraege = reihe.map(function (i) {
      var o = d.optionen[i];
      var lab = h("label", "ue-opt");
      var inp = h("input"); inp.type = mehr ? "checkbox" : "radio"; inp.name = name;
      lab.appendChild(inp);
      var sp = h("span"); sp.innerHTML = o.html ? o.html : fmt(o.text);  // o.html: vom Baukasten erzeugte Buchungssatz-Tabelle
      lab.appendChild(sp);
      lab.addEventListener("change", function () { entmarkiere(lab); });
      body.appendChild(lab);
      return { o: o, inp: inp, lab: lab };
    });
    return {
      leer: function () { return eintraege.every(function (e) { return !e.inp.checked; }); },
      bewerte: function () {
        var ok = true, hinweise = [];
        eintraege.forEach(function (e) {
          var gew = e.inp.checked, rich = !!e.o.korrekt;
          if (gew !== rich) ok = false;
          if (gew) markiere(e.lab, rich);
          else entmarkiere(e.lab);
          if (gew && !rich && e.o.feedback) hinweise.push(e.o.feedback);
        });
        if (!ok && !hinweise.length) hinweise.push(mehr ? "Mindestens eine Auswahl stimmt nicht, oder es fehlt eine richtige Antwort." : "Diese Antwort stimmt nicht.");
        return { ok: ok, hinweise: hinweise };
      },
      loesung: function () {
        var r = eintraege.filter(function (e) { return e.o.korrekt; }).map(function (e) { return e.o.text; });
        return "**Richtig:** " + r.join(" | ") + (d.erklaerung ? "\n" + d.erklaerung : "");
      },
      sperren: function (b) { eintraege.forEach(function (e) { e.inp.disabled = b; }); },
      zuruecksetzen: function () { eintraege.forEach(function (e) { e.inp.checked = false; e.inp.disabled = false; entmarkiere(e.lab); }); },
      zustand: function () { return eintraege.map(function (e) { return e.inp.checked ? 1 : 0; }); },
      laden: function (a) { (Array.isArray(a) ? a : []).forEach(function (v, i) { if (eintraege[i]) eintraege[i].inp.checked = !!v; }); }
    };
  }

  /* ---------- Typ: zuordnung ---------- */
  function tZuordnung(d, body) {
    var reihe = mische(d.elemente.map(function (e, i) { return i; }), d.titel);
    var zeilen = reihe.map(function (i) {
      var e = d.elemente[i];
      var z = h("label", "ue-feld");
      z.appendChild(h("span", "ue-label ue-zu-text", e.text));
      var s = h("select", "ue-konto");
      var o0 = h("option", "", "Kategorie wählen …"); o0.value = ""; s.appendChild(o0);
      d.kategorien.forEach(function (k) { var op = h("option", "", k); op.value = k; s.appendChild(op); });
      s.onchange = function () { entmarkiere(s); };
      z.appendChild(s);
      body.appendChild(z);
      return { e: e, s: s };
    });
    return {
      leer: function () { return zeilen.every(function (z) { return !z.s.value; }); },
      bewerte: function () {
        var ok = true, hinweise = [];
        zeilen.forEach(function (z) {
          var gut = z.s.value === z.e.kategorie;
          markiere(z.s, gut);
          if (!gut) { ok = false; if (z.s.value && z.e.feedback) hinweise.push(z.e.text + ": " + z.e.feedback); }
        });
        if (!ok && !hinweise.length) hinweise.push("Nicht alle Zuordnungen stimmen, prüfe die rot markierten.");
        return { ok: ok, hinweise: hinweise };
      },
      loesung: function () { return d.elemente.map(function (e) { return e.text + " → **" + e.kategorie + "**"; }).join("\n"); },
      sperren: function (b) { zeilen.forEach(function (z) { z.s.disabled = b; }); },
      zuruecksetzen: function () { zeilen.forEach(function (z) { z.s.value = ""; entmarkiere(z.s); z.s.disabled = false; }); },
      zustand: function () { return zeilen.map(function (z) { return z.s.value; }); },
      laden: function (a) {
        (Array.isArray(a) ? a : []).forEach(function (v, i) {
          if (zeilen[i] && Array.prototype.some.call(zeilen[i].s.options, function (o) { return o.value === String(v); })) zeilen[i].s.value = String(v);
        });
      }
    };
  }

  /* ---------- Typ: reihenfolge (Position wählen) ---------- */
  function tReihenfolge(d, body) {
    var n = d.elemente.length;
    var reihe = mische(d.elemente.map(function (e, i) { return i; }), d.titel);
    if (reihe.every(function (v, i) { return v === i; })) reihe.push(reihe.shift());
    var zeilen = reihe.map(function (i) {
      var z = h("label", "ue-feld");
      var s = h("select", "ue-konto ue-pos");
      var o0 = h("option", "", "Platz …"); o0.value = ""; s.appendChild(o0);
      for (var k = 1; k <= n; k++) { var op = h("option", "", String(k)); op.value = String(k); s.appendChild(op); }
      s.onchange = function () { entmarkiere(s); };
      z.appendChild(s);
      z.appendChild(h("span", "ue-label ue-zu-text", d.elemente[i]));
      body.appendChild(z);
      return { i: i, s: s };
    });
    return {
      leer: function () { return zeilen.every(function (z) { return !z.s.value; }); },
      bewerte: function () {
        var ok = true;
        zeilen.forEach(function (z) {
          var gut = z.s.value === String(z.i + 1);
          markiere(z.s, gut);
          if (!gut) ok = false;
        });
        return { ok: ok, hinweise: ok ? [] : [d.feedback_falsch || "Die Reihenfolge stimmt noch nicht. Jede Zahl darf nur einmal vorkommen."] };
      },
      loesung: function () { return d.elemente.map(function (e, i) { return (i + 1) + ". " + e; }).join("\n") + (d.feedback_richtig ? "\n" + d.feedback_richtig : ""); },
      sperren: function (b) { zeilen.forEach(function (z) { z.s.disabled = b; }); },
      zuruecksetzen: function () { zeilen.forEach(function (z) { z.s.value = ""; entmarkiere(z.s); z.s.disabled = false; }); },
      zustand: function () { return zeilen.map(function (z) { return z.s.value; }); },
      laden: function (a) {
        (Array.isArray(a) ? a : []).forEach(function (v, i) {
          if (zeilen[i] && Array.prototype.some.call(zeilen[i].s.options, function (o) { return o.value === String(v); })) zeilen[i].s.value = String(v);
        });
      }
    };
  }

  /* ---------- Typ: offen (Freitext, Musterlösung zum Vergleichen) ---------- */
  function tOffen(d, body) {
    var ta = h("textarea", "ue-offen");
    ta.rows = d.zeilen || 6;
    ta.setAttribute("aria-label", "Deine Antwort");
    ta.placeholder = "Schreibe deine Antwort in zwei bis drei Sätzen …";
    body.appendChild(ta);
    return {
      selbst: true,
      leer: function () { return ta.value.trim().length < 15; },
      bewerte: function () { return { ok: null, hinweise: [] }; },
      loesung: function () {
        var z = ["**Musterlösung:** " + (d.musterloesung || "")];
        if (d.checkliste && d.checkliste.length) z.push("**Hast du das genannt?**\n" + d.checkliste.map(function (c) { return "☐ " + c; }).join("\n"));
        return z.join("\n");
      },
      sperren: function (b) { ta.readOnly = b; },
      zuruecksetzen: function () { ta.value = ""; ta.readOnly = false; },
      zustand: function () { return ta.value; },
      laden: function (v) { if (typeof v === "string") ta.value = v.slice(0, 4000); }
    };
  }

  var TYPEN = { rechnen: tRechnen, buchung: tBuchung, konten: tKonten, luecken: tLuecken, lueckentext: tFreitextLuecken,
                auswahl: tAuswahl, zuordnung: tZuordnung, reihenfolge: tReihenfolge, offen: tOffen };

  /* ---------- Karte ---------- */
  var NIVEAU = { basis: "Basis", plus: "Plus", kreativ: "Kreativ" };
  function lpState() { return window.LP && window.LP.state ? window.LP.state : null; }

  function karte(host, dRoh, kartenId, opt) {
    opt = opt || {};
    var istTest = !!dRoh.test || !!opt.test;
    var maxV = Number(dRoh.versuche) || (istTest ? 1 : MAX_VERSUCHE);
    var alt = lpState() && lpState().ue && kartenId ? lpState().ue[kartenId] : null;

    // Zahlen festlegen (Startwerte, Zufall oder gespeicherte Werte)
    var vars = null;
    if (dRoh.parameter) {
      if (alt && alt.p) vars = alt.p;
      else if (opt.parallel) vars = zufallsWerte(dRoh.parameter, startWerte(dRoh.parameter));
      else if (dRoh.zufall || istTest) vars = zufallsWerte(dRoh.parameter, null);
      else vars = startWerte(dRoh.parameter);
    }
    var d;
    try { d = vars ? loese(dRoh, vars) : loese(dRoh, {}); }
    catch (e) { var f = h("p", "box warn", "Diese Übung konnte nicht geladen werden."); host.appendChild(f); if (window.console) console.error(e); return f; }

    var niveau = NIVEAU[d.niveau] ? d.niveau : "basis";
    var card = h("section", "box task uebung " + niveau + (opt.parallel ? " ue-parallelkarte" : ""));
    if (istTest) card.setAttribute("data-test", "1");
    var kopf = h("div", "task-head");
    kopf.appendChild(h("span", "lvl " + niveau, opt.parallel ? "Parallelaufgabe" : (istTest ? "Frage" : NIVEAU[niveau])));
    kopf.appendChild(h("h3", "", d.titel));
    if (d.minuten && !istTest) kopf.appendChild(h("span", "lvl time", d.minuten + " min"));
    card.appendChild(kopf);
    if (opt.parallel) card.appendChild(h("p", "ue-hinweis-parallel", "Gleiche Aufgabe, andere Zahlen. Zeig, dass du den Rechenweg verstanden hast."));
    if (d.text) { var tx = h("div", "ue-text"); tx.innerHTML = fmt(d.text); card.appendChild(tx); }
    if (d.beleg) card.appendChild(belegeEl(d.beleg));

    var body = h("div", "ue-body");
    card.appendChild(body);

    var typ = (TYPEN[d.typ] || tLuecken)(d, body);

    // Gestufte Tipps
    var tippListe = d.tipps && d.tipps.length ? d.tipps : (d.tipp ? [d.tipp] : []);
    if (istTest) tippListe = [];
    var tippZahl = 0, tipp = null, tippBtn = null;
    if (tippListe.length) {
      tipp = h("div", "ue-tipp");
      tipp.hidden = true;
      tippBtn = h("button", "btn secondary");
      tippBtn.type = "button";
      tippBtn.setAttribute("aria-expanded", "false");
      var tippKnopf = function () {
        if (tippZahl >= tippListe.length) { tippBtn.hidden = true; return; }
        tippBtn.textContent = tippListe.length === 1 ? "💡 Tipp anzeigen" :
          (tippZahl === 0 ? "💡 Tipp 1 von " + tippListe.length + " anzeigen" : "💡 Nächster Tipp (" + (tippZahl + 1) + " von " + tippListe.length + ")");
      };
      var tippZeigen = function (bis) {
        while (tippZahl < bis && tippZahl < tippListe.length) {
          var p = h("p");
          p.innerHTML = "<strong>💡 Tipp" + (tippListe.length > 1 ? " " + (tippZahl + 1) : "") + ":</strong> " + fmt(tippListe[tippZahl]);
          tipp.appendChild(p);
          tippZahl++;
        }
        tipp.hidden = tippZahl === 0;
        tippBtn.setAttribute("aria-expanded", String(tippZahl > 0));
        tippKnopf();
      };
      tippBtn.onclick = function () { tippZeigen(tippZahl + 1); speichern(); };
      tippKnopf();
    }

    var fb = h("div", "ue-fb");
    fb.setAttribute("role", "status");
    fb.setAttribute("aria-live", "polite");
    var lsg = h("div", "ue-loesung");
    lsg.hidden = true;
    var parBox = h("div", "ue-parallel");
    parBox.hidden = true;
    var versuche = 0, fertig = false, okFlag = null, parCard = null, parStart = false;

    function setStatus(s) {
      card.setAttribute("data-status", s || "");
      document.dispatchEvent(new CustomEvent("lp-uebung"));
    }
    function speichern() {
      var stt = lpState();
      if (!stt || !kartenId) return;
      stt.ue = stt.ue || {};
      stt.ue[kartenId] = { v: versuche, f: fertig, ok: okFlag, z: typ.zustand(), p: vars, t: tippZahl, par: parStart };
      try { window.LP.save(); } catch (e) { /* ignorieren */ }
    }
    var timer = null;
    function spaeter() { if (!fertig) { clearTimeout(timer); timer = setTimeout(speichern, 500); } }
    card.addEventListener("input", spaeter);
    card.addEventListener("change", spaeter);

    var pruef = h("button", "btn", istTest ? "Antwort prüfen" : "Prüfen");
    pruef.type = "button";
    var neu = h("button", "btn secondary", istTest ? "Frage nochmal versuchen" : "Nochmal von vorn");
    neu.type = "button";
    neu.hidden = true;

    function meld(art, html) { fb.className = "ue-fb " + art; fb.innerHTML = html; }
    function zeigeLoesung(ok) {
      var teile = [];
      if (ok === null) {
        teile.push("<div>" + fmt(typ.loesung()) + "</div>");
      } else {
        if (d.loesungsweg) teile.push("<div class=\"ue-weg-titel\">Rechenweg</div><div>" + fmt(d.loesungsweg) + "</div>");
        var lh = typ.loesungHtml ? typ.loesungHtml() : fmt(typ.loesung());
        if (!ok) teile.push("<div class=\"ue-weg-titel\">Lösung</div><div>" + lh + "</div>");
        else if (!d.loesungsweg) teile.push("<div>" + lh + "</div>");
        if (ok && d.erklaerung) teile.push("<div class=\"ue-weg-titel\">Erklärung</div><div>" + fmt(d.erklaerung) + "</div>");
        else if (!ok && d.erklaerung && typ.loesung().indexOf(d.erklaerung) < 0) teile.push("<div>" + fmt(d.erklaerung) + "</div>");
      }
      if (ok === true && d.code) {
        teile.push("<div class=\"ue-code\"><strong>🔑 Code-Teil: " + esc(d.code.teil) + "</strong>" + (d.code.text ? "<br>" + fmt(d.code.text) : "") + "</div>");
      }
      lsg.innerHTML = teile.join("");
      lsg.hidden = false;
      zeigeParallelAngebot(ok);
    }

    // Parallelaufgabe mit anderen Zahlen
    function zeigeParallelAngebot(ok) {
      if (!dRoh.parameter || opt.parallel || istTest || dRoh.parallel === false) return;
      parBox.innerHTML = "";
      parBox.hidden = false;
      var t = h("p");
      t.innerHTML = ok ? "<strong>Zum Festigen:</strong> Löse die gleiche Aufgabe noch einmal mit anderen Zahlen (freiwillig)."
        : "<strong>Jetzt du:</strong> Du hast die Lösung gesehen. Zeig jetzt, dass du den Rechenweg verstanden hast, und löse eine Parallelaufgabe mit anderen Zahlen.";
      parBox.appendChild(t);
      if (!parStart) {
        var b = h("button", "btn", "Parallelaufgabe starten");
        b.type = "button";
        b.onclick = function () { starteParallel(); b.hidden = true; speichern(); };
        parBox.appendChild(b);
      }
    }
    function starteParallel() {
      if (parCard) return;
      parStart = true;
      parCard = karte(host, dRoh, kartenId + "~p", { parallel: true });
      if (parCard && parCard.scrollIntoView && !opt.laden) { try { parCard.scrollIntoView({ block: "nearest", behavior: "smooth" }); } catch (e) { /* ignorieren */ } }
    }
    function entferneParallel() {
      if (parCard && parCard.parentNode) parCard.parentNode.removeChild(parCard);
      parCard = null; parStart = false;
      var stt = lpState();
      if (stt && stt.ue) delete stt.ue[kartenId + "~p"];
      document.dispatchEvent(new CustomEvent("lp-uebung"));
    }

    pruef.onclick = function () {
      if (fertig) return;
      if (typ.leer()) { meld("hinweis", typ.selbst ? "Schreibe zuerst deine Antwort auf (mindestens ein bis zwei Sätze)." : "Trage zuerst etwas ein, dann kannst du prüfen."); return; }
      var r = typ.bewerte();
      versuche++;
      if (r.ok === null) {
        fertig = true; okFlag = null; typ.sperren(true);
        meld("hinweis", "Vergleiche deine Antwort mit der Musterlösung. Diese Frage bewertet deine Lehrkraft.");
        zeigeLoesung(null);
        setStatus("offen");
      } else if (r.ok) {
        fertig = true; okFlag = true; typ.sperren(true);
        meld("richtig", "<strong>Richtig!</strong>" + (d.loesungsweg ? " Unten siehst du den Rechenweg zum Vergleichen." : ""));
        zeigeLoesung(true);
        setStatus("richtig");
      } else if (versuche >= maxV) {
        fertig = true; okFlag = false; typ.sperren(true);
        meld("falsch", "Das war " + (maxV > 1 ? "noch " : "") + "nicht richtig. Vergleiche deine Eingabe (rot markiert) mit der Lösung.");
        zeigeLoesung(false);
        setStatus("falsch");
      } else {
        var li = (r.hinweise || []).map(function (x) { return "<li>" + fmt(x) + "</li>"; }).join("");
        meld("falsch", "<strong>Noch nicht ganz richtig.</strong> Prüfe die rot markierten Felder und versuche es noch einmal." + (li ? "<ul>" + li + "</ul>" : ""));
      }
      pruef.hidden = fertig;
      neu.hidden = !fertig || (istTest && false);
      speichern();
    };
    neu.onclick = function () {
      versuche = 0; fertig = false; okFlag = null;
      typ.zuruecksetzen();
      fb.className = "ue-fb"; fb.innerHTML = "";
      lsg.hidden = true; parBox.hidden = true;
      entferneParallel();
      pruef.hidden = false; neu.hidden = true;
      setStatus("");
      speichern();
    };

    // gespeicherten Zwischenstand wiederherstellen
    if (alt && alt.z != null) {
      try {
        typ.laden(alt.z);
        versuche = Number(alt.v) || 0;
        if (tippListe.length && alt.t) tippZeigen(Number(alt.t));
        if (alt.f) {
          fertig = true; okFlag = alt.ok === undefined ? null : alt.ok;
          if (okFlag !== null) typ.bewerte();
          typ.sperren(true);
          if (okFlag === null) meld("hinweis", "Vergleiche deine Antwort mit der Musterlösung. Diese Frage bewertet deine Lehrkraft.");
          else if (okFlag) meld("richtig", "<strong>Richtig!</strong>" + (d.loesungsweg ? " Unten siehst du den Rechenweg zum Vergleichen." : ""));
          else meld("falsch", "Das war " + (maxV > 1 ? "noch " : "") + "nicht richtig. Vergleiche deine Eingabe (rot markiert) mit der Lösung.");
          parStart = !!alt.par;
          zeigeLoesung(okFlag);
          pruef.hidden = true; neu.hidden = false;
          card.setAttribute("data-status", okFlag === null ? "offen" : (okFlag ? "richtig" : "falsch"));
        }
      } catch (e) { if (window.console) console.error(e); }
    }

    var aktionen = h("div", "ue-aktionen");
    if (tippBtn) aktionen.appendChild(tippBtn);
    aktionen.appendChild(pruef);
    aktionen.appendChild(neu);
    if (tipp) card.appendChild(tipp);
    card.appendChild(aktionen);
    card.appendChild(fb);
    card.appendChild(lsg);
    card.appendChild(parBox);
    host.appendChild(card);

    // bei neuen Test-Zufallswerten sofort merken, damit ein Neuladen dieselben Zahlen zeigt
    if (vars && (dRoh.zufall || istTest || opt.parallel) && !(alt && alt.p)) speichern();
    if (alt && alt.par && !opt.parallel) { parStart = false; opt.laden = true; starteParallel(); }
    if (alt && alt.f) document.dispatchEvent(new CustomEvent("lp-uebung"));
    return card;
  }

  /* ---------- Zusammenfassung für Tests ---------- */
  function ergebnis() {
    var boxen = document.querySelectorAll(".ue-ergebnis");
    if (!boxen.length) return;
    var karten = document.querySelectorAll("section.uebung[data-test]");
    var n = karten.length, r = 0, f = 0, o = 0;
    Array.prototype.forEach.call(karten, function (k) {
      var s = k.getAttribute("data-status");
      if (s === "richtig") r++; else if (s === "falsch") f++; else if (s === "offen") o++;
    });
    var bearbeitet = r + f + o;
    var seite = (document.body && document.body.dataset && document.body.dataset.module) || location.pathname.split("/").pop() || "seite";
    Array.prototype.forEach.call(boxen, function (box) {
      var t = "<strong>Dein Stand:</strong> " + bearbeitet + " von " + n + " Fragen bearbeitet – " + r + " richtig, " + f + " nicht richtig" +
        (o ? ", " + o + " offen (bewertet deine Lehrkraft)" : "") + ".";
      var bewertbar = n - o;
      if (bearbeitet === n && bewertbar > 0) t += " <strong>Ergebnis: " + r + " von " + bewertbar + " (" + Math.round(r / bewertbar * 100) + " %).</strong>";
      box.className = "ue-ergebnis box note";
      box.innerHTML = "<p>" + t + "</p>";
      if (bearbeitet > 0) {
        var b = h("button", "btn secondary", "Test neu starten");
        b.type = "button";
        b.onclick = function () {
          if (!confirm("Alle Antworten dieses Tests löschen und neu beginnen?")) return;
          var st = lpState();
          if (st && st.ue) Object.keys(st.ue).forEach(function (k) { if (k.indexOf(seite + "#") === 0) delete st.ue[k]; });
          try { window.LP.save(); } catch (e) { /* ignorieren */ }
          location.reload();
        };
        box.appendChild(b);
      }
    });
  }

  /* ---------- Breakout: Schlösser und Räume ---------- */
  function seitenId() {
    return (document.body && document.body.dataset && document.body.dataset.module) || location.pathname.split("/").pop() || "seite";
  }
  function schlossOffen(id) {
    var st = lpState(), e = st && st.ue && st.ue["lock:" + seitenId() + ":" + id];
    return !!(e && e.o);
  }
  function schloss(host, d) {
    var key = "lock:" + seitenId() + ":" + d.id;
    var card = h("section", "box schloss");
    card.setAttribute("data-id", d.id);
    var kopf = h("div", "task-head");
    var icon = h("span", "schloss-icon", "🔒");
    kopf.appendChild(icon);
    kopf.appendChild(h("h3", "", d.titel));
    card.appendChild(kopf);
    if (d.text) { var tx = h("div", "ue-text"); tx.innerHTML = fmt(d.text); card.appendChild(tx); }
    var zeile = h("div", "ue-zeile");
    var inp = h("input", "ue-betrag schloss-eingabe");
    inp.type = "text"; inp.autocomplete = "off"; inp.placeholder = "Code";
    inp.setAttribute("aria-label", "Code für " + d.titel);
    if (d.ziffern) inp.inputMode = "numeric";
    var btn = h("button", "btn", "Schloss öffnen");
    btn.type = "button";
    zeile.appendChild(inp); zeile.appendChild(btn);
    card.appendChild(zeile);
    var fb = h("div", "ue-fb");
    fb.setAttribute("role", "status"); fb.setAttribute("aria-live", "polite");
    card.appendChild(fb);
    var offen = h("div", "schloss-offen");
    offen.hidden = true;
    card.appendChild(offen);
    var fehler = 0;
    function klar(t) { return String(t).toLowerCase().replace(/[\s\-.]/g, ""); }
    function zeigeOffen(laden) {
      icon.textContent = "🔓";
      card.classList.add("schloss-auf");
      inp.value = d.code; inp.disabled = true; btn.hidden = true;
      fb.className = "ue-fb richtig"; fb.innerHTML = "<strong>Das Schloss springt auf!</strong>";
      if (d.oeffnet) { offen.innerHTML = fmt(d.oeffnet); offen.hidden = false; }
    }
    btn.onclick = function () {
      if (!inp.value.trim()) { fb.className = "ue-fb hinweis"; fb.textContent = "Gib zuerst einen Code ein."; return; }
      if (klar(inp.value) === klar(d.code)) {
        var st = lpState();
        if (st) { st.ue = st.ue || {}; st.ue[key] = { o: 1 }; try { window.LP.save(); } catch (e) { /* ignorieren */ } }
        zeigeOffen();
        document.dispatchEvent(new CustomEvent("lp-schloss"));
      } else {
        fehler++;
        fb.className = "ue-fb falsch";
        fb.innerHTML = "Das Schloss bleibt zu. Prüft eure Code-Teile und ihre Reihenfolge." +
          (fehler >= 3 && d.hinweis ? "<p><strong>Hinweis:</strong> " + fmt(d.hinweis) + "</p>" : "");
        inp.select();
      }
    };
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") btn.click(); });
    host.appendChild(card);
    if (schlossOffen(d.id)) zeigeOffen(true);
  }
  function raeume() {
    Array.prototype.forEach.call(document.querySelectorAll(".raum[data-braucht]"), function (r) {
      var b = r.getAttribute("data-braucht");
      if (!b) return;
      var auf = schlossOffen(b);
      r.classList.toggle("raum-zu", !auf);
      var ph = r.querySelector(":scope > .raum-platzhalter");
      if (!auf && !ph) {
        ph = h("p", "raum-platzhalter", "🔒 Dieser Raum ist noch verschlossen. Öffnet zuerst das Schloss davor.");
        var t = r.querySelector(":scope > .raum-titel");
        if (t && t.nextSibling) r.insertBefore(ph, t.nextSibling); else r.appendChild(ph);
      }
      if (auf && ph) ph.parentNode.removeChild(ph);
    });
  }
  function spielNeu() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-lp-reset]"), function (b) {
      b.addEventListener("click", function () {
        if (!confirm("Alle Antworten und geöffneten Schlösser dieser Seite löschen und das Spiel neu starten?")) return;
        var st = lpState(), id = seitenId();
        if (st && st.ue) Object.keys(st.ue).forEach(function (k) { if (k.indexOf(id + "#") === 0 || k.indexOf("lock:" + id + ":") === 0) delete st.ue[k]; });
        try { window.LP.save(); } catch (e) { /* ignorieren */ }
        location.reload();
      });
    });
  }

  function start() {
    var hosts = document.querySelectorAll("section.uebung-host");
    var seite = (document.body && document.body.dataset && document.body.dataset.module) || location.pathname.split("/").pop() || "seite";
    Array.prototype.forEach.call(hosts, function (host, nr) {
      var s = host.querySelector("script[type='application/json']");
      if (!s) return;
      try {
        var d = JSON.parse(s.textContent);
        host.innerHTML = "";
        karte(host, d, seite + "#" + nr);
        host.classList.add("ue-bereit");
      } catch (e) {
        host.innerHTML = "<p class=\"box warn\">Diese Übung konnte nicht geladen werden.</p>";
        if (window.console) console.error(e);
      }
    });
    Array.prototype.forEach.call(document.querySelectorAll("section.schloss-host"), function (host) {
      var s = host.querySelector("script[type='application/json']");
      if (!s) return;
      try { var d = JSON.parse(s.textContent); host.innerHTML = ""; schloss(host, d); host.classList.add("ue-bereit"); }
      catch (e) { host.innerHTML = "<p class=\"box warn\">Dieses Schloss konnte nicht geladen werden.</p>"; if (window.console) console.error(e); }
    });
    raeume();
    document.addEventListener("lp-schloss", raeume);
    spielNeu();
    document.addEventListener("lp-uebung", ergebnis);
    ergebnis();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
