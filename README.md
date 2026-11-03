# Swift Sport

Website for Swift Sport / Tactical Gear, Embakasi, Nairobi. Built by MobKazi.

- `index.html`: the shop page and the admin panel (open `/#admin`).
- `data.json`: the starting products and shop details.
- `api/`: Vercel functions that save products and photos to Vercel Blob.

## Setup on Vercel
1. Import this repo (preset: Other).
2. Storage › Create › Blob, then connect it to the project.
3. Settings › Environment Variables: add `ADMIN_PASSWORD`.
4. Redeploy, open `/#admin` and log in.
