# KAVACH AI — Frontend (Member 6)

Intelligent Disaster Risk, Vulnerability, Evacuation & Rescue Intelligence System.
This is the complete frontend: Authority Command Dashboard, Citizen Emergency
Interface, Rescue Team Interface, interactive GIS map, SOS system, live alerts,
and the closed-loop feedback simulation engine.

## Run it

```bash
npm install
npm run dev
```

Open the printed local URL. The app boots straight to `/login`, a role picker
(no real auth — as specified for the prototype).

The whole app runs on bundled mock data by default (`VITE_USE_MOCK_DATA=true`
in `.env`). To point it at the FastAPI backend once it exists, set
`VITE_USE_MOCK_DATA=false` and `VITE_API_BASE_URL` in `.env`. Every call in
`src/services/api.ts` automatically falls back to mock data if the backend is
unreachable, so the frontend never breaks mid-demo.

## Project structure

```
src/
├── components/   # StatCard, MapView, PriorityPanel, ShelterPanel, HospitalPanel,
│                 # RoutePanel, RescueMission, SOSModal, LiveAlerts, FeedbackTimeline,
│                 # SimulationControls, and shared UI (toasts, modals, states)
├── pages/        # LoginPage, DashboardPage, CitizenPage, RescuePage, SimulationPage
├── layouts/      # Layout, Navbar
├── context/      # DisasterContext — shared state + the closed-loop feedback engine
├── services/     # api.ts — centralized Axios client with mock-data fallback
├── mock/         # zones, households, hospitals, shelters, roads, routes, teams, alerts
├── types/        # shared TypeScript interfaces
└── utils/        # formatting/status helpers
```

## Routes

- `/login` — role picker
- `/dashboard` — Authority Command Dashboard (stats, map, priorities, shelters,
  hospitals, routes, feedback timeline, live alerts)
- `/citizen` — mobile-first SOS / evacuation / hazard-report interface
- `/rescue` — active mission, navigate / mark complete / report situation
- `/simulation` — Simulation Control Center for the demo script below

## Running the demo script live

1. On `/simulation`, click **Heavy Rain** — Zone Z17's risk jumps 48→87,
   turns CRITICAL, and the feedback panel streams the recalculation chain.
2. On `/dashboard`, click Z17 → **View Details** to see the Explainability
   panel ("Why is this area critical?").
3. Check the **Route panel** — primary route `R4 → R7 → S3` is shown.
4. Go to `/rescue`, open **Report Situation** on TEAM R-04, choose
   *Road blocked* → road **R7**, submit.
5. Back on `/dashboard`, watch **Closed-Loop Feedback**: 🚧 blocked → ⚠
   recalculating → 🔄 route changed → 🛣 new route `R4 → R9 → S3` → 🚑 team
   reassigned.
6. Go to `/citizen`, tap **Send SOS**.
7. Back on `/dashboard`, the new SOS appears in **Live Alerts** and gets
   auto-assigned to a team.

All of this is driven by `DisasterContext` — no manual code edits needed
between steps.

## Notes for the backend teammate

Expected endpoints are listed in `src/services/api.ts` — matching
`GET /zones`, `/households`, `/hospitals`, `/shelters`, `/roads`, `/routes`,
`/rescue-teams`, `/alerts`, and `POST /rescue-report`, `/sos`,
`/hazard-report`. Response shapes should match `src/types/index.ts`.
# 🚨 Kavach AI - Real-Time Disaster Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

## 🎯 Project Overview

**Kavach AI** transforms dynamic hazard information into habitation-level decisions by combining vulnerability, habitability, safe carrying capacity, relocation priority, shelter availability, route safety and what-if simulation.

### Core Features

1. **Dynamic Red-Zone Engine** - Real-time hazard detection and risk scoring
2. **Household Vulnerability Assessment** - AI-powered vulnerability scoring
3. **Priority Area Identification** - Intelligent resource allocation
4. **Shelter Capacity Intelligence** - Real-time capacity and reallocation
5. **Evacuation Route Optimization** - Safe route calculation
6. **Rescue Team Feedback Loop** - Closed-loop disaster intelligence
7. **Emergency Contact System** - SOS and emergency coordination

## 🏗️ Architecture
