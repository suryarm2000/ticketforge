# TicketForge

An event ticketing and booking platform, built step by step to learn full-stack development:
React frontend, FastAPI backend, PostgreSQL database, and the production concerns around them
(auth, transactions, caching, background jobs, testing, CI, deployment).

Users browse events and book seats. Organizers create and manage events. Admins see analytics.
The hard part, and the point of the project: two people must never book the same seat.

## Stack

- Frontend: React (Vite)
- Backend: Python, FastAPI, SQLAlchemy, Alembic
- Database: PostgreSQL (via Docker)
- Later: Redis, Celery/ARQ, Docker Compose, GitHub Actions, WebSockets

## Roadmap

| Phase | Focus |
|---|---|
| 0 | Repo, tooling, project skeleton |
| 1 | REST basics: events CRUD in FastAPI |
| 2 | PostgreSQL, SQLAlchemy models, migrations |
| 3 | Auth: signup/login, JWT, roles |
| 4 | React frontend: browsing, login, booking flow, organizer dashboard |
| 5 | Booking engine: seat holds, transactions, no double-booking |
| 6 | Performance: indexes, pagination, search, Redis cache, rate limiting |
| 7 | Background jobs: emails, hold expiry, payment webhooks |
| 8 | Tests, Docker Compose, CI, deployment |
| 9 | Stretch: live seat map (WebSockets), analytics, Stripe test mode |

Daily progress and notes are in [LEARNING.md](LEARNING.md).

## Status

Phase 0: setting up.
