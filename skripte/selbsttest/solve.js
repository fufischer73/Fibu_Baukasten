const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const plans = JSON.parse(fs.readFileSync(process.argv[2]));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1000, height: 900 } });
  const fmt = n => String(n).replace('.', ',');
  for (const f of Object.keys(plans)) {
    await p.goto('file://' + f);
    await p.waitForTimeout(500);
    const cards = await p.$$('.uebung');
    for (let i = 0; i < plans[f].length; i++) {
      const pl = plans[f][i];
      if (!pl) continue;
      const c = cards[i];
      if (pl.typ === 'rechnen') {
        const ins = await c.$$('input.ue-betrag');
        for (let k = 0; k < pl.werte.length; k++) await ins[k].fill(fmt(pl.werte[k]));
      } else {
        const sats = await c.$$('.ue-satz');
        for (let s = 0; s < pl.saetze.length; s++) {
          const seiten = await sats[s].$$('.ue-seite');
          for (let side = 0; side < 2; side++) {
            const rows = pl.saetze[s][side === 0 ? 'soll' : 'haben'];
            for (let r = 1; r < rows.length; r++) await (await seiten[side].$('.ue-plus')).click();
            const sels = await seiten[side].$$('select.ue-konto');
            const ins = await seiten[side].$$('input.ue-betrag');
            for (let r = 0; r < rows.length; r++) {
              await sels[r].selectOption(rows[r][0]);
              await ins[r].fill(fmt(rows[r][1]));
            }
          }
        }
      }
      const btns = await c.$$('button');
      let pr = null;
      for (const bt of btns) if ((await bt.innerText()).trim() === 'Prüfen') pr = bt;
      if (!pr) { console.log(f.split('/').pop().slice(0, 3), i, 'NOK  kein Prüfen-Knopf gefunden'); continue; }
      await pr.click();
      await p.waitForTimeout(150);
      const fb = await c.$('.ue-fb');
      const cls = fb ? await fb.getAttribute('class') : 'kein Feedback';
      const titel = await c.$eval('h3', e => e.textContent);
      console.log(f.split('/').pop().slice(0, 3), i, cls.includes('richtig') ? 'OK ' : 'NOK', titel, '|', cls);
    }
  }
  await b.close();
})();
