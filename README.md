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

## Python verification endpoint

`GET /api/python-check` returns a small JSON response confirming that the
Python runtime is working:

```json
{
  "ok": true,
  "runtime": "python",
  "service": "chirag-portfolio-api",
  "message": "Python endpoint is running."
}
```

## Portfolio contact form (Gmail SMTP)

`POST /api/contact` accepts JSON with `name`, `email`, `message`, and an optional
`website` honeypot field. It validates input and sends the message using Gmail
SMTP; the sender's email is set as `Reply-To`. The API returns a generic success
for filled honeypot submissions. Configure these Vercel environment variables:

- `FRONTEND_ORIGIN`: exact deployed portfolio origin (for example, `https://chirag-portfolio-zeta-nine.vercel.app`)
- `SMTP_HOST`: `smtp.gmail.com`
- `SMTP_PORT`: `587`
- `SMTP_USERNAME`: Gmail address used to send mail
- `SMTP_APP_PASSWORD`: Google App Password for that account (keep this secret)
- `CONTACT_TO_EMAIL`: inbox that receives messages, normally `tankchirag22@gmail.com`

Use an App Password, not the Gmail account password. Keep credentials out of
Git and redeploy the API after adding or changing environment variables. The
endpoint limits request size and field lengths and checks browser origins; add a
shared rate limiter before exposing it to significant public traffic.
