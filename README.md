# Weather Watcher

Cloud-native web application built with FastAPI and deployed on Microsoft Azure.

## Sprint 1 Goal
Deploy a working application to Azure with automated CI/CD pipeline.

## Tech Stack
- FastAPI (Python 3.11)
- Azure App Service
- Azure DevOps
- Azure Application Insights

## Local Setup

### 1. Clone the repository
bash
git clone <your-repo-url>
cd weather-watcher


### 2. Install dependencies
bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt


### 3. Run the app
bash
uvicorn app.main:app --reload


Open http://localhost:8000 in your browser.

### 4. Run tests
bash
pytest tests/ -v


## API Endpoints
- GET / - Homepage
- GET /health - Health check
- GET /api/info - Project info

## Team - Sprint 1
- *Product Owner:* [Kenny]
- *Scrum Master:* [Adrian]
- *Developers:* [Jack Omar, Salmane]

## Documentation
- [Definition of Done](docs/definition-of-done.md)
- [Sprint Planning](docs/sprints/sprint1-planning.md)
- [Daily Scrum Notes](docs/sprints/daily-scrum-notes.md)

## Links
- *Azure DevOps:* [https://adasilvaieu2023@dev.azure.com/adasilvaieu2023/devops%20group%20project%20Adrian/_git/weather%20watcher]
- *Live App:* Coming soon

## Current Status
- [x] Local development setup
- [x] FastAPI app with 3 endpoints
- [x] Tests passing (3/3)
- [ ] Azure deployment
- [ ] CI/CD pipeline

---

IE University - BCSAI - SDDO - 2025