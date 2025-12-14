# Weather Watcher

Weather Watcher is a cloud-native web application developed as part of the **BCSAI-SDDO DevOps course** at IE University.  
The project demonstrates the design, deployment, monitoring, and documentation of a modern DevOps-enabled application using cloud services and automated CI/CD practices.

The application provides weather information for cities worldwide, enhanced with autocomplete search, monitoring, and observability.

---

## Project Goals

- Build a cloud-deployed web application using modern DevOps practices
- Implement automated CI/CD pipelines
- Ensure monitoring, logging, and observability
- Apply Scrum methodology across multiple sprints
- Deliver a clean, professional, and production-ready project

---

## Features

- 🌤️ Current weather information by city  
- 📅 5-day weather forecast  
- 🔍 City autocomplete using Google Places API (with mock fallback)  
- 🔄 Temperature unit toggle (Celsius / Fahrenheit)  
- 📊 Weather comparison between cities  
- ❤️ Health check endpoint for monitoring  
- 📈 Application Insights telemetry and logging  
- 🚀 Automated CI/CD pipeline with GitHub Actions  

---

## Architecture Overview

The system follows a cloud-native architecture:

- Frontend: HTML, CSS, JavaScript  
- Backend: FastAPI (Python 3.11)  
- External APIs: OpenWeatherMap, Google Places API  
- Cloud Platform: Microsoft Azure  
- Hosting: Azure App Service (Linux, Free Tier)  
- CI/CD: GitHub Actions  
- Monitoring: Azure Application Insights  

The application is deployed automatically through a CI/CD pipeline and monitored using dashboards, logs, and alerts.

---

## Technology Stack

Backend:
- Python 3.11
- FastAPI
- Uvicorn

Frontend:
- HTML
- CSS
- JavaScript

Cloud & DevOps:
- Microsoft Azure App Service
- Azure Application Insights
- GitHub Actions (CI/CD)
- GitHub Secrets for environment variables

Testing:
- pytest
- httpx

---

## Setup Instructions (Local)

1. Clone the repository  
   git clone https://github.com/Oelhajjcheha/Devops-Project-WeatherWatcher.git
   cd weather-watcher  

2. Create a virtual environment and install dependencies  
   python -m venv venv  
   source venv/bin/activate  
   pip install -r requirements.txt  

3. Set environment variables  
   OPENWEATHER_API_KEY=your_key  
   GOOGLE_PLACES_API_KEY=your_key  

4. Run the application  
   uvicorn app.main:app --reload  

5. Run tests  
   pytest  

---

## Deployment & CI/CD

The project uses **GitHub Actions** for Continuous Integration and Continuous Deployment.

Pipeline behavior:
- Triggers on push or merge to main
- Installs dependencies
- Runs all automated tests
- Deploys to Azure App Service on success
- Blocks deployment if tests fail

This ensures consistent, reliable, and repeatable deployments.

---

## Monitoring & Observability

The application is monitored using **Azure Application Insights**, which provides:

- Request and dependency tracking
- Error and exception logging
- Response time monitoring
- Custom telemetry for weather searches and city autocomplete usage
- Alerts for failures and unhealthy states

Dashboards and log queries were used to validate telemetry and system health.

---

## API Endpoints

Root  
GET /  
Returns the main application interface.

Health Check  
GET /health  
Returns application health status for monitoring.

Weather  
GET /api/weather?city=<city>  
Returns current weather data for a city.

Forecast  
GET /api/forecast?city=<city>  
Returns a 5-day weather forecast.

Autocomplete  
GET /api/cities/autocomplete?query=<text>  
Returns city suggestions using Google Places API.

---

## Scrum & Sprint Summary

The project was developed over **4 sprints** using Scrum methodology.

- Sprint 1: Infrastructure setup and CI/CD foundation  
- Sprint 2: Core weather functionality  
- Sprint 3: Advanced features and UX improvements  
- Sprint 4: Documentation, monitoring, cleanup, and final submission  

Detailed sprint planning and retrospectives are available in the docs/sprints folder.

---

## Team Contributions (Sprint 4 Roles)

| Name | Role | Contributions |
|------|------|---------------|
| Omar El Hajj Chehade | Scrum Master | Documentation leadership, retrospectives, architecture, final submission |
| Adrian | Product Owner | Backlog prioritization, requirements validation, UX direction |
| Kenny | Developer | Backend support, CI/CD validation, telemetry assistance |
| Jack | Developer | Backend features, API integration, testing |
| Salmane | Developer | Monitoring, Application Insights, dashboards |

---

## Lessons Learned

- CI/CD automation significantly improves reliability
- Monitoring and telemetry should be integrated early
- Documentation must be treated as a first-class deliverable
- Clear Git workflows prevent last-minute issues
- Cloud free tiers introduce limitations such as cold starts

---

## Project Status

Completed  
The Weather Watcher project is fully implemented, deployed, monitored, and documented, and is ready for academic evaluation.

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

- **Homepage:** https://weather-watcher-4b2025.azurewebsites.net/
- **Health Check:** https://weather-watcher-4b2025.azurewebsites.net/health
- **API Info:** https://weather-watcher-4b2025.azurewebsites.net/api/info
- **Weather API:** https://weather-watcher-4b2025.azurewebsites.net/api/weather?city=London
- **Forecast API:** https://weather-watcher-4b2025.azurewebsites.net/api/forecast?city=Madrid
- **Autocomplete:** https://weather-watcher-4b2025.azurewebsites.net/api/cities/autocomplete?query=New

### Deployment Status

- ✅ Application deployed successfully
- ✅ All endpoints verified working
- ✅ Build process configured with SCM_DO_BUILD_DURING_DEPLOYMENT=true
- ✅ CI/CD pipeline operational
- ✅ Application Insights monitoring active

## Architecture

![Architecture Diagram](image.png)

### System Architecture Overview

The Weather Watcher application follows a cloud-native architecture:

1. **Frontend:** Single-page application served directly from FastAPI
2. **Backend API:** FastAPI application handling all API requests
3. **External APIs:** 
   - Google Maps Weather API (current conditions)
   - Google Places API (autocomplete)
   - OpenWeatherMap API (5-day forecast)
4. **Monitoring:** Azure Application Insights for telemetry and logging
5. **Deployment:** Azure App Service with CI/CD via Azure DevOps

## Azure Resources

**Resource Group:**  
`BCSAI2025-DEVOPS-STUDENT-4B`

**App Service:**  
`weather-watcher-4B2025`  
**URL:** weather-watcher-4b2025.azurewebsites.net

**Application Insights:**  
`ai-weather-watcher`

**Pipeline URL:**  
https://github.com/Oelhajjcheha/Devops-Project-WeatherWatcher/actions

---

### Additional Azure resources created automatically:

- **App Service Plan:** `asp-weather-watcher`
- **Log Analytics Workspace:** `e0b9cada-61bc-4b5a-bd7a-52c606726ef7`
- **Smart Detector Alert:** `Failure Anomalies - ai-weather-watcher`
- **Metric Alert:** `Failed requests`
- **Action Group:** `devops-alerts`
- **Shared Dashboard:** `83dea926-dda3-41c1-a7ac-03667ee213f3`
- **Azure Workbook:** `06a88c54-5b0a-4b9d-b670-e5522d9b51cb`

IE University - BCSAI - SDDO - 2025
