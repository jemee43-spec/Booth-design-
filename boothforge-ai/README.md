# BOOTHFORGE AI

**Phase 1 development scaffold** — responsive Arabic project dashboard + FastAPI project API.

## Run locally

Requires Python 3.11+ and Node.js 20+.

### API
```bash
cd services/api
python -m venv .venv
source .venv/bin/activate # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Web (new terminal)
```bash
cd apps/web
npm install
npm run dev
```

Open http://localhost:3000 and API documentation at http://localhost:8000/docs.

## Implemented
- Arabic responsive project creation UI and project list
- Validated booth dimensions and area calculation
- FastAPI project create/list/get endpoints
- Brand file upload endpoint (PNG/JPEG/SVG/PDF, max 5 MB)
- Persistent local JSON data (development only)
- Explicit 501 for unavailable AI generation, no simulated output
- Basic API test

## Not implemented yet
Authentication, tenant isolation, PostgreSQL, secure object storage, brand analysis, image generation adapters, design gallery, revisions, PDF export, FreeCAD and AutoCAD integration. **Do not deploy publicly** before implementing authentication, secure upload processing, storage isolation, and production infrastructure.

## Architecture
`apps/web` Next.js frontend; `services/api` FastAPI service. Future geometry and CAD service should be independent and derive all outputs from validated parametric geometry.
