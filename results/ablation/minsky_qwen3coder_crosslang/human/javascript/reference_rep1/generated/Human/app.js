// Runnable Express server. Auto-discovers every feature module under controllers/ and views/
// and mounts each exported function as POST /{layer}/{module}. Mirrors FastAPI router
// auto-discovery so no per-feature wiring is written (Code/Test isolation preserved).
'use strict';
const express = require('express');
const fs = require('fs');
const path = require('path');

function createApp() {
  const app = express();
  app.use(express.json());
  app.get('/health', (_req, res) => res.json({ status: 'ok' }));
  for (const layer of ['controllers', 'views', 'models']) {
    const dir = path.join(__dirname, layer);
    if (!fs.existsSync(dir)) continue;
    for (const file of fs.readdirSync(dir).filter((f) => f.endsWith('.js'))) {
      const mod = require(path.join(dir, file));
      const fn = Object.values(mod).find((v) => typeof v === 'function');
      if (!fn) continue;
      const route = `/${layer}/${file.replace(/\.js$/, '')}`;
      app.post(route, (req, res) => {
        try {
          res.json(fn(req.body));
        } catch (err) {
          res.status(400).json({ error: String(err && err.message || err) });
        }
      });
    }
  }
  return app;
}

if (require.main === module) {
  const port = process.env.PORT || 3000;
  createApp().listen(port, () => console.log(`listening on ${port}`));
}
module.exports = { createApp };
