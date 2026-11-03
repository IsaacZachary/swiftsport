import { put } from '@vercel/blob';

// Receives one product photo (already resized on the phone) and stores it in Vercel Blob.
const MAX_BYTES = 4 * 1024 * 1024;
const TYPES = ['image/jpeg', 'image/png', 'image/webp'];

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }
  const key = process.env.ADMIN_PASSWORD;
  if (!key || req.headers['x-admin-key'] !== key) return res.status(401).json({ error: 'Wrong password. Log out and log in again.' });

  const type = String(req.headers['content-type'] || '').split(';')[0].trim();
  if (!TYPES.includes(type)) return res.status(415).json({ error: 'Send a JPEG, PNG or WebP photo.' });

  try {
    const chunks = [];
    let size = 0;
    for await (const c of req) {
      size += c.length;
      if (size > MAX_BYTES) return res.status(413).json({ error: 'That photo is too large. Try a smaller one.' });
      chunks.push(c);
    }
    const ext = type === 'image/png' ? 'png' : type === 'image/webp' ? 'webp' : 'jpg';
    const blob = await put('products/photo.' + ext, Buffer.concat(chunks), {
      access: 'public', contentType: type, addRandomSuffix: true,
    });
    return res.status(200).json({ url: blob.url });
  } catch (e) {
    return res.status(500).json({ error: (e && e.message) || 'Upload failed' });
  }
}
