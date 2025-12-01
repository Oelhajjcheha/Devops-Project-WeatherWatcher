# Weather Watcher ☁️🌤️

A cloud-native weather application built with FastAPI and deployed on Microsoft Azure. Get real-time weather information for any city around the world.

**Course:** BCSAI-SDDO (Software Development & DevOps) - IE University  
**Academic Year:** 2025  
**Final Demo:** December 4, 2025

---

## 🎯 Project Overview

Weather Watcher is a full-stack web application that provides real-time weather data using modern DevOps practices. The project demonstrates cloud infrastructure setup, CI/CD automation, monitoring, and Scrum methodology.

### Sprint Goals

**Sprint 1 (Nov 26-28):** ✅ COMPLETED
- Deploy working FastAPI application to Azure App Service
- Set up automated CI/CD pipeline
- Establish basic monitoring

**Sprint 2 (Dec 2-4):** 🚧 IN PROGRESS
- Implement weather API integration
- Build user-friendly weather display interface
- Enhance monitoring with Application Insights
- Comprehensive testing and documentation

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.11)
- **Server:** Uvicorn with Gunicorn
- **Testing:** pytest, httpx

### Frontend
- **UI:** HTML5, CSS3, JavaScript
- **Design:** Responsive, mobile-first

### Cloud & DevOps
- **Cloud Platform:** Microsoft Azure
- **Hosting:** Azure App Service (Linux, F1 Free tier)
- **CI/CD:** Azure Pipelines
- **Monitoring:** Azure Application Insights
- **Version Control:** Azure DevOps Repos (Git)

### External APIs
- **Weather Data:** OpenWeatherMap / WeatherAPI (TBD in Sprint 2)

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
```bash
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=app --cov-report=html
```

### Test Structure
```
tests/
├── __init__.py
├── test_main.py           # Basic endpoint tests
├── test_weather.py        # Weather API tests (Sprint 2)
└── test_integration.py    # Integration tests (Sprint 2)
```

---

## 🚀 Deployment

### Automated Deployment (CI/CD)
Every push to the `main` branch triggers:
1. **Build:** Install dependencies
2. **Test:** Run all pytest tests
3. **Deploy:** Automatic deployment to Azure App Service

**Pipeline Status:** ✅ Operational  
**Average Deploy Time:** ~3-5 minutes

### Manual Deployment (Azure CLI)
```bash
# Login to Azure
az login --use-device-code

# Deploy application
az webapp up \
  --name weather-watcher-4B2025 \
  --resource-group BCSAI2025-DEVOPS-STUDENT-4B \
  --runtime "PYTHON|3.11"

# View logs
az webapp log tail \
  --name weather-watcher-4B2025 \
  --resource-group BCSAI2025-DEVOPS-STUDENT-4B

# Restart app
az webapp restart \
  --name weather-watcher-4B2025 \
  --resource-group BCSAI2025-DEVOPS-STUDENT-4B
```

---

## 📊 Monitoring & Logging

### Application Insights (Sprint 2)
- **Custom Metrics:** Weather API call count, response times
- **Error Tracking:** Automatic exception logging
- **Performance:** Request duration, dependency tracking
- **Alerts:** Configured for critical failures

### Health Monitoring
Monitor application health: https://weather-watcher-4b2025.azurewebsites.net/health

Expected Response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "sprint": 2
}
```

---

## 🔐 Environment Variables

Required environment variables (configured in Azure App Service):

```bash
# Sprint 2 - Weather API
WEATHER_API_KEY=<your-api-key>
WEATHER_API_URL=<api-endpoint>

# Application Insights (Sprint 2)
APPLICATIONINSIGHTS_CONNECTION_STRING=<connection-string>
```

---

## 📈 Project Metrics

### Sprint 1 Velocity
- **Story Points Committed:** 14
- **Story Points Completed:** 14
- **Velocity:** 14
- **Sprint Duration:** 2 days

### Sprint 2 Target
- **Story Points Committed:** 18
- **Sprint Duration:** 3 days
- **Target Velocity:** 18

---

## 🤝 Contributing

### Git Workflow
1. Create feature branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make changes and commit
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

3. Push to Azure DevOps
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create Pull Request in Azure DevOps

5. Get code review approval (minimum 1 reviewer)

6. Merge to `main` (triggers automatic deployment)

### Branch Naming Convention
- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Critical production fixes
- `docs/` - Documentation updates

---

## 📝 Definition of Done

A feature is considered **DONE** when:
- ✅ Code written and follows coding standards
- ✅ Code reviewed by at least one team member
- ✅ Unit tests written and passing
- ✅ Integration tests passing (if applicable)
- ✅ CI pipeline tests pass
- ✅ Deployed to Azure App Service
- ✅ Feature works in production
- ✅ No errors in logs
- ✅ Documentation updated
- ✅ Acceptance criteria met

---

## 📞 Support & Contact

**Course:** BCSAI-SDDO  
**Institution:** IE University  
**Academic Year:** 2025  

**Team Contact:** Via Azure DevOps or project Teams channel

---

## 📄 License

This project is an academic assignment for IE University's BCSAI-SDDO course.

---

## 🙏 Acknowledgments

- **IE University** - BCSAI Program
- **Microsoft Azure** - Cloud infrastructure
- **FastAPI** - Web framework
- **OpenWeatherMap/WeatherAPI** - Weather data providers

---

**Last Updated:** December 1, 2025  
**Project Status:** Sprint 2 In Progress  
**Final Demo:** December 4, 2025

---

## 🎯 Quick Links

- 🌐 [Live Application](https://weather-watcher-4b2025.azurewebsites.net)
- 📊 [Azure DevOps Board](https://adasilvaieu2023@dev.azure.com/adasilvaieu2023/devops%20group%20project%20Adrian/)
- 📚 [Sprint 2 Planning](docs/sprints/sprint2-planning.md)
- ✅ [Definition of Done](docs/definition-of-done.md)

---

**Built with ❤️ by the Weather Watcher Team**  
*IE University - BCSAI - 2025*


## 📡 API Endpoints

### Current Endpoints (Sprint 1)
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/` | Homepage with project info | ✅ Live |
| GET | `/health` | Health check endpoint | ✅ Live |
| GET | `/api/info` | API information | ✅ Live |

### Upcoming Endpoints (Sprint 2)
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/weather/{city}` | Get current weather for a city | 🚧 In Progress |
| GET | `/weather/search` | Search weather by city name | 🚧 Planned |

---

## 👥 Team Structure

### Sprint 1 (Nov 26-28, 2025)
- **Product Owner:** Kenny
- **Scrum Master:** Adrian
- **Developers:** Jack, Omar, Salmane

### Sprint 2 (Dec 2-4, 2025)
- **Product Owner:** Jack
- **Scrum Master:** Salmane
- **Developer 1 (Backend/API):** Omar
- **Developer 2 (Frontend/UI):** Adrian
- **Developer 3 (Monitoring/Testing):** Kenny

## 📚 Documentation

### Project Documentation
- [Definition of Done](docs/definition-of-done.md)
- [CI/CD Pipeline Documentation](docs/CI-CD-Pipeline-Documentation.md)
- [Architecture Diagram](#-architecture) (see below)

### Sprint 1 Documentation
- [Sprint 1 Planning](docs/sprints/sprint1-planning.md)
- [Sprint 1 Daily Scrum Notes](docs/sprints/daily-scrum-notes.md)

### Sprint 2 Documentation
- [Sprint 2 Planning](docs/sprints/sprint2-planning.md)
- [Sprint 2 Daily Scrum Notes](docs/sprints/sprint2-daily-scrum-notes.md)
- [Sprint 2 Retrospective](docs/sprints/sprint2-retrospective.md)

## 🔗 Important Links

- **Live Application:** https://weather-watcher-4b2025.azurewebsites.net
- **Azure DevOps:** https://adasilvaieu2023@dev.azure.com/adasilvaieu2023/devops%20group%20project%20Adrian/_git/weather%20watcher
- **Azure Portal:** Resource Group `BCSAI2025-DEVOPS-STUDENT-4B`

---

## 🚀 Current Status

### Sprint 1 Achievements ✅
- [x] Local development environment set up
- [x] FastAPI application with 3 endpoints
- [x] Unit tests passing (3/3, 100% pass rate)
- [x] Azure App Service deployed and running
- [x] CI/CD pipeline with Azure Pipelines
- [x] Application accessible via public URL
- [x] Basic project documentation

### Sprint 2 In Progress 🚧
- [x] Sprint 2 planning and documentation
- [ ] Weather API integration
- [ ] Weather display frontend
- [ ] Application Insights monitoring
- [ ] Comprehensive testing (target >70% coverage)
- [ ] Final demo preparation

---

## Azure Deployment Information

### Resource Details
- **Resource Group:** BCSAI2025-DEVOPS-STUDENT-4B
- **App Service Plan:** asp-weather-watcher (F1 Free tier)
- **App Service Name:** weather-watcher-4B2025
- **Location:** North Europe
- **Runtime:** Python 3.11

### Live Application
- **URL:** https://weather-watcher-4b2025.azurewebsites.net

### Endpoints
- Homepage: https://weather-watcher-4b2025.azurewebsites.net/
- Health Check: https://weather-watcher-4b2025.azurewebsites.net/health
- API Info: https://weather-watcher-4b2025.azurewebsites.net/api/info

### Deployment Status
- ✅ Application deployed successfully
- ✅ All endpoints verified working
- ✅ Build process configured with SCM_DO_BUILD_DURING_DEPLOYMENT=true
" >> README.md
```
```
🎉 INFRASTRUCTURE DEPLOYMENT COMPLETE! 🎉

✅ Azure App Service is live and running!

📋 Deployment Details:
- Resource Group: BCSAI2025-DEVOPS-STUDENT-4B
- App Service: weather-watcher-4B2025
- Location: North Europe
- Runtime: Python 3.11

🌐 Live URL: https://weather-watcher-4b2025.azurewebsites.net

✅ All endpoints verified working:
- / (homepage)
- /health (health check)
- /api/info (API information)

IE University - BCSAI - SDDO - 2025