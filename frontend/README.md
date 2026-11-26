# Frontend

React app with two screens: **Today** and **Timeline**. It reads from the backend API.

## Run it (development)

The backend must be running first (`docker compose up -d --build` from the project root).

```
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173 in your browser. The app calls the API at http://localhost:8000.
