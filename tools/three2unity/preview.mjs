#!/usr/bin/env node
// node preview.mjs <Assets/ThreeImport dir> [port]  — opens scene.glb + scene.json in a browser tab (plain three.js, no Unity).
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { exec } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const dir = path.resolve(process.argv[2] ?? ''), port = Number(process.argv[3] ?? 8770), here = path.dirname(fileURLToPath(import.meta.url));
if (!fs.existsSync(path.join(dir, 'scene.glb'))) { console.error('usage: node preview.mjs <path to Assets/ThreeImport> [port]'); process.exit(1); }
const TYPES = { '.html': 'text/html', '.json': 'application/json', '.glb': 'model/gltf-binary' };
http.createServer((req, res) => {
  const u = new URL(req.url, 'http://x').pathname, f = u === '/' ? path.join(here, 'preview.html') : path.join(dir, path.basename(u));
  if (!fs.existsSync(f)) { res.writeHead(404).end(); return; }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
}).listen(port, '127.0.0.1', () => {
  const url = `http://127.0.0.1:${port}/`; console.log('preview at', url, '(Ctrl+C to stop)');
  if (!process.env.NO_OPEN) exec(`${process.platform === 'win32' ? 'start ""' : process.platform === 'darwin' ? 'open' : 'xdg-open'} ${url}`);
});
