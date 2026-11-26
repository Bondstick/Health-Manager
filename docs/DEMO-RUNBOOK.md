# Demo runbook (hackathon day)

One public link serves the app and the API. Run these in order.

## 1. Build the app (once, or after any frontend change)
```
cd ~/Health-Manager/frontend
npm install
npm run build
```

## 2. Start the backend and database
```
cd ~/Health-Manager
docker compose up -d --build
docker compose exec api python -m app.seed
```
Check http://localhost:8000/health shows `"status":"ok"`.

## 3. Create the public link
In a second Ubuntu window:
```
cloudflared tunnel --url http://127.0.0.1:8000
```
It prints a line like `https://something-random.trycloudflare.com`. That is the link for judges.

## 4. Check the public link
Open the link on your phone (on mobile data, not your Wi-Fi). You should see the Today screen.

## Notes
- The free quick link changes each time you restart `cloudflared`, and it has no uptime guarantee. Use it for the demo only.
- Keep the laptop plugged in, with sleep turned off. Keep the backup video ready.
- Only demo data is in the system. Do not add real patient information.
- To stop the public link, press Ctrl+C in the cloudflared window.
