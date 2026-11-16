# Chirag Portfolio API

A minimal Vercel Functions backend for the Chirag Tank portfolio.

## Endpoint

`GET /api/health` returns:

```json
{
  "ok": true,
  "service": "chirag-portfolio-api"
}
```

The endpoint allows browser requests from `http://localhost:3000` and the
production portfolio origin configured with the `FRONTEND_ORIGIN` environment
variable.

## Deploy to Vercel

Import this repository as a new Vercel project. Set `FRONTEND_ORIGIN` to the
production portfolio URL, for example `https://chirag-portfolio-zeta-nine.vercel.app`,
then deploy. The function is available at `/api/health` on the new project URL.
