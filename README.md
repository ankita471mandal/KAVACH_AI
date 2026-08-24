# KAVACH\_AI

\## Routing Module



The routing module provides risk-aware route selection for evacuation and rescue operations.



\### Current Features



\- Loads open roads from `gis/data/roads.geojson`

\- Loads active routes from `gis/data/routes.geojson`

\- Connects to the Risk API using `GET /risk`

\- Converts zone risk scores into routing safety scores

\- Ranks available routes based on safety

\- Selects the safest active route



\### Routing Files



\- `routing/risk\_client.py` - Risk API client

\- `routing/road\_loader.py` - Loads open roads

\- `routing/route\_loader.py` - Loads active routes

\- `routing/risk\_router.py` - Calculates routing safety based on risk

\- `routing/route\_ranker.py` - Ranks routes

\- `routing/route\_selector.py` - Selects the best route

\- `routing/config.py` - Routing configuration



\### Current Status



The routing logic has been implemented and tested with the available mock GIS route data.



Live Risk API integration is pending because the Risk API backend is not currently running locally.



\### Example



The current mock route `ROUTE01` has a base safety score of `92`.



Risk-aware routing adjusts the safety score according to the hazard risk.



For example:



\- Risk score `20` → routing safety score `86.0`

\- Risk score `62.3` → routing safety score `64.85`

\- Risk score `85` → routing safety score `53.5`

