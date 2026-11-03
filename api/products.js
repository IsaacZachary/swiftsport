import { put, list, del } from '@vercel/blob';

// The shop's products and settings are saved as JSON files in Vercel Blob.
// Each save writes a new file; the newest one is the live version, and the
// 5 most recent are kept as backups.
const PREFIX = 'data/shop-';

function authed(req) {
  const key = process.env.ADMIN_PASSWORD;
  return Boolean(key) && req.headers['x-admin-key'] === key;
}

async function newestFirst() {
  const { blobs } = await list({ prefix: PREFIX });
  return blobs.sort((a, b) => new Date(b.uploadedAt) - new Date(a.uploadedAt));
}

async function readJson(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  if (typeof req.body === 'string') return JSON.parse(req.body);
  const chunks = [];
  for await (const c of req) chunks.push(c);
  return JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}');
}

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  try {
    if (req.method === 'GET') {
      const blobs = await newestFirst();
      if (!blobs.length) return res.status(200).json({ data: null });
      const r = await fetch(blobs[0].url, { cache: 'no-store' });
      return res.status(200).json({ data: await r.json() });
    }

    if (req.method === 'POST') {
      // Password check for the admin login.
      if (!process.env.ADMIN_PASSWORD) return res.status(500).json({ error: 'ADMIN_PASSWORD is not set in Vercel.' });
      return authed(req) ? res.status(200).json({ ok: true }) : res.status(401).json({ error: 'Wrong password' });
    }

    if (req.method === 'PUT') {
      if (!authed(req)) return res.status(401).json({ error: 'Wrong password. Log out and log in again.' });
      const body = await readJson(req);
      if (!body || typeof body.settings !== 'object' || !Array.isArray(body.products)) {
        return res.status(400).json({ error: 'The data was not in the expected shape.' });
      }
      const saved = await put(PREFIX + Date.now() + '.json', JSON.stringify(body), {
        access: 'public', contentType: 'application/json', addRandomSuffix: true,
      });
      const old = (await newestFirst()).filter((b) => b.url !== saved.url).slice(4);
      if (old.length) await del(old.map((b) => b.url));
      return res.status(200).json({ ok: true });
    }

    res.setHeader('Allow', 'GET, POST, PUT');
    return res.status(405).json({ error: 'Method not allowed' });
  } catch (e) {
    return res.status(500).json({ error: (e && e.message) || 'Server error' });
  }
}
