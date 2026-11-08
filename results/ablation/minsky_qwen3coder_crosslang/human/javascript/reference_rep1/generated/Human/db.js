// Thin SQLite-backed key/value store (the project's "SQL DB"). Stores each feature's
// state blob as JSON in a single table — the JS analog of the Python adapter's AppState.
'use strict';
let _db = null;
function db() {
  if (_db) return _db;
  const Database = require('better-sqlite3');
  _db = new Database(process.env.APP_DB || 'app.db');
  _db.exec('CREATE TABLE IF NOT EXISTS app_state (key TEXT PRIMARY KEY, value TEXT NOT NULL)');
  return _db;
}
function load(key, fallback) {
  const row = db().prepare('SELECT value FROM app_state WHERE key = ?').get(key);
  return row ? JSON.parse(row.value) : fallback;
}
function save(key, value) {
  db().prepare('INSERT INTO app_state (key, value) VALUES (?, ?) '
    + 'ON CONFLICT(key) DO UPDATE SET value = excluded.value').run(key, JSON.stringify(value));
}
module.exports = { db, load, save };
