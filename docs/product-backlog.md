# Product Backlog

**Project:** Weather Watcher  
**Last Updated:** December 5, 2025  
**Product Owner:** Omar  
**Scrum Master:** Kenny

---

## Backlog Overview

This document contains all user stories, features, and requirements for the Weather Watcher application. Stories are organized by epic and prioritized by the Product Owner.

**Total Story Points:** 50 points  
**Completed:** 33 points  
**In Progress:** 2 points  
**Remaining:** 15 points

---

## Epic 1: Infrastructure & Deployment (Sprint 1)

**Status:** ✅ Complete  
**Story Points:** 14

### User Story #1: Deploy Application Infrastructure to Azure

**Priority:** 1 (Critical)  
**Story Points:** 5  
**Sprint:** Sprint 1  
**Status:** ✅ Complete  
**Assigned To:** Developer 1 (Jack)

**Description:**  
As a developer, I want Azure infrastructure set up, so that I can deploy the application online.

**Acceptance Criteria:**
- ✅ Azure Resource Group created
- ✅ Azure App Service running with Python 3.11
- ✅ Application Insights configured and collecting data
- ✅ Application accessible via public URL
- ✅ All resources documented in README

---

### User Story #2: Automated CI/CD Pipeline

**Priority:** 1 (Critical)  
**Story Points:** 5  
**Sprint:** Sprint 1  
**Status:** ✅ Complete  
**Assigned To:** Developer 2 (Omar)

**Description:**  
As a developer, I want an automated deployment pipeline, so that code deploys automatically when I push to main branch.

**Acceptance Criteria:**
- ✅ Pipeline triggers on push to main branch
- ✅ Pipeline builds Python application
- ✅ Pipeline runs all automated tests
- ✅ Pipeline deploys to Azure on success
- ✅ Failed tests block deployment
- ✅ Pipeline completes in under 5 minutes

---

### User Story #3: Application Monitoring and Logging

**Priority:** 2 (High)  
**Story Points:** 2  
**Sprint:** Sprint 1  
**Status:** ✅ Complete  
**Assigned To:** Developer 3 (Salmane)

**Description:**  
As a developer, I want monitoring and logging enabled, so that I can track application health and debug issues.

**Acceptance Criteria:**
- ✅ Application Insights connected to App Service
- ✅ Dashboard shows key metrics (uptime, response time, errors)
- ✅ Health endpoint is monitored
- ✅ Errors are logged and visible
- ✅ Alerts configured for failures

---

### User Story #4: Project Documentation

**Priority:** 2 (High)  
**Story Points:** 2  
**Sprint:** Sprint 1  
**Status:** ✅ Complete  
**Assigned To:** Scrum Master (Adrian)

**Description:**  
As a team member, I want complete project documentation, so that I can understand, contribute to, and maintain the project.

**Acceptance Criteria:**
- ✅ README with setup instructions
- ✅ Architecture diagram
- ✅ CI/CD pipeline documentation
- ✅ Definition of Done
- ✅ Sprint planning documents

---

## Epic 2: Core Weather Functionality (Sprint 2)

**Status:** ✅ Complete  
**Story Points:** 18

### User Story #139: Sprint 2 Documentation & Project Updates

**Priority:** 1 (Critical)  
**Story Points:** 2  
**Sprint:** Sprint 2  
**Status:** ✅ Complete  
**Assigned To:** Scrum Master (Salmane)

**Description:**  
As a team member, I want comprehensive Sprint 2 documentation and project updates, so that all stakeholders understand our progress and the project is properly documented.

**Acceptance Criteria:**
- ✅ Sprint 2 Planning document created
- ✅ Daily Scrum Notes updated for Sprint 2
- ✅ README updated with Sprint 2 features
- ✅ Architecture diagram created/updated
- ✅ CI/CD documentation updated
- ✅ Sprint 2 Retrospective template created

---

### User Story #140: Weather API Integration

**Priority:** 1 (Critical)  
**Story Points:** 5  
**Sprint:** Sprint 2  
**Status:** ✅ Complete  
**Assigned To:** Developer 1 (Omar)

**Description:**  
As a user, I want the application to fetch real-time weather data, so that I can view current weather conditions.

**Acceptance Criteria:**
- ✅ Weather API selected (Google Maps Weather API)
- ✅ API key configured in Azure App Service settings
- ✅ Backend endpoint created to fetch weather data
- ✅ Error handling for API failures
- ✅ Response data properly formatted
- ✅ API rate limits considered and handled

---

### User Story #141: Weather Display Frontend

**Priority:** 1 (Critical)  
**Story Points:** 5  
**Sprint:** Sprint 2  
**Status:** ✅ Complete  
**Assigned To:** Developer 2 (Adrian)

**Description:**  
As a user, I want to see weather information in a clean, user-friendly interface, so that I can easily understand the weather conditions.

**Acceptance Criteria:**
- ✅ Weather search page created
- ✅ User can enter city name
- ✅ Current weather displayed (temperature, conditions, humidity, wind)
- ✅ Weather icons displayed based on conditions
- ✅ Responsive design works on mobile and desktop
- ✅ Loading states and error messages shown

---

### User Story #142: Enhanced Application Monitoring

**Priority:** 2 (High)  
**Story Points:** 3  
**Sprint:** Sprint 2  
**Status:** ✅ Complete  
**Assigned To:** Developer 3 (Kenny)

**Description:**  
As a developer, I want comprehensive monitoring and logging, so that I can track application performance and debug issues quickly.

**Acceptance Criteria:**
- ✅ Application Insights fully integrated
- ✅ Custom metrics tracking (weather API calls, response times)
- ✅ Monitoring dashboard shows weather-specific metrics
- ✅ Alerts configured for API failures
- ✅ Log queries created for common debugging scenarios
- ✅ Performance metrics tracked

---

### User Story #143: Testing and Quality Assurance

**Priority:** 2 (High)  
**Story Points:** 3  
**Sprint:** Sprint 2  
**Status:** ✅ Complete  
**Assigned To:** Developer 3 (Kenny)

**Description:**  
As a developer, I want comprehensive test coverage, so that I can ensure code quality and catch bugs early.

**Acceptance Criteria:**
- ✅ Unit tests for all new endpoints
- ✅ Integration tests for weather API
- ✅ Test coverage > 70%
- ✅ All tests passing in CI pipeline
- ✅ Edge cases and error scenarios tested

---

## Epic 3: Enhanced Features & Optimization (Sprint 3)

**Status:** 🔄 In Progress  
**Story Points:** 18

### User Story #1: 5-Day Weather Forecast

**Priority:** 1 (Critical)  
**Story Points:** 5  
**Sprint:** Sprint 3  
**Status:** ✅ Closed  
**Assigned To:** Developer 1 (Jack Raja Shawki Samawi)

**Description:**  
As a user, I want to see a 5-day weather forecast, so that I can plan my activities ahead of time.

**Acceptance Criteria:**
- [x] Forecast endpoint added to weather service
- [x] /api/forecast API endpoint created
- [x] Forecast UI layout designed
- [x] Forecast display logic implemented
- [x] Forecast cards styled
- [x] Forecast functionality tested

---

### User Story #2: Full Country Names Display

**Priority:** 1 (Critical)  
**Story Points:** 3  
**Sprint:** Sprint 3  
**Status:** ✅ Closed  
**Assigned To:** Developer 3 (Salmane Mouhib)

**Description:**  
As a user, I want to see full country names instead of country codes, so that the information is more readable and user-friendly.

**Acceptance Criteria:**
- [x] Country code mapping dictionary created
- [x] Country name conversion function implemented
- [x] Weather API responses updated to include full country names
- [x] Country name display tested

---

### User Story #3: City Autocomplete & Search Improvements

**Priority:** 1 (Critical)  
**Story Points:** 5  
**Sprint:** Sprint 3  
**Status:** ✅ Closed  
**Assigned To:** Developer 1 (Jack Raja Shawki Samawi)

**Description:**  
As a user, I want improved city autocomplete and search functionality, so that I can quickly find and select cities.

**Acceptance Criteria:**
- [x] Autocomplete approach researched and chosen
- [x] Autocomplete API endpoint implemented
- [x] Autocomplete JavaScript logic added
- [x] Autocomplete dropdown styled
- [x] Loading and error states added
- [x] Autocomplete functionality tested

---

### User Story #4: Loading States & UI Polish

**Priority:** 2 (High)  
**Story Points:** 3  
**Sprint:** Sprint 3  
**Status:** 📋 New (Not Started)  
**Assigned To:** Developer 2 (Adrian Kia Rekaa Hasini Da Silva)

**Description:**  
As a user, I want smooth loading states and polished UI, so that the application feels professional and responsive.

**Acceptance Criteria:**
- [ ] Loading spinner component created
- [ ] Skeleton loading screens added
- [ ] Fade-in animations implemented
- [ ] Button loading states added
- [ ] Error message display improved

---

### User Story #5: Sprint 3 Documentation

**Priority:** 2 (High)  
**Story Points:** 2  
**Sprint:** Sprint 3  
**Status:** 🔄 Active (In Progress)  
**Assigned To:** Scrum Master (Kenny Tohme)

**Description:**  
As a team member, I want comprehensive Sprint 3 documentation, so that all stakeholders understand our progress and the project is properly documented.

**Acceptance Criteria:**
- [x] Sprint 3 Planning Document created
- [x] README updated with new features
- [x] Architecture diagram created/updated
- [ ] Sprint 3 retrospective completed

---

## Epic 4: Future Enhancements (Backlog)

**Status:** 📋 Not Started  
**Story Points:** TBD

### User Story #301: User Favorites

**Priority:** 3 (Medium)  
**Story Points:** 5  
**Sprint:** Future  
**Status:** 📋 Not Started

**Description:**  
As a user, I want to save favorite cities, so that I can quickly access weather for locations I check frequently.

**Acceptance Criteria:**
- [ ] User can add cities to favorites
- [ ] Favorites stored in database
- [ ] Quick access to favorite cities
- [ ] Remove favorites functionality

---

### User Story #302: Weather History

**Priority:** 3 (Medium)  
**Story Points:** 3  
**Sprint:** Future  
**Status:** 📋 Not Started

**Description:**  
As a user, I want to see historical weather data, so that I can compare current conditions with past data.

**Acceptance Criteria:**
- [ ] Historical weather data available
- [ ] Comparison charts
- [ ] Date range selection

---

### User Story #303: Weather Alerts

**Priority:** 4 (Low)  
**Story Points:** 5  
**Sprint:** Future  
**Status:** 📋 Not Started

**Description:**  
As a user, I want to receive weather alerts, so that I can be notified of severe weather conditions.

**Acceptance Criteria:**
- [ ] Alert configuration
- [ ] Email/SMS notifications
- [ ] Alert thresholds configurable

---

## Backlog Statistics

### By Status

| Status | Story Points | Count |
|--------|--------------|-------|
| ✅ Complete | 33 | 9 |
| 🔄 In Progress | 2 | 1 |
| 📋 Not Started | 15 | 4 |
| **Total** | **50** | **14** |

### By Priority

| Priority | Story Points | Count |
|----------|--------------|-------|
| 1 (Critical) | 28 | 7 |
| 2 (High) | 8 | 3 |
| 3 (Medium) | 8 | 3 |
| 4 (Low) | 5 | 1 |

### By Epic

| Epic | Story Points | Status |
|------|--------------|--------|
| Infrastructure & Deployment | 14 | ✅ Complete |
| Core Weather Functionality | 18 | ✅ Complete |
| Enhanced Features & Optimization | 18 | 🔄 In Progress (13/18 complete) |
| Future Enhancements | TBD | 📋 Not Started |

---

## Backlog Management

### Kanban Board

All user stories are tracked in **Azure DevOps Boards** with the following workflow:

- **Backlog** → **To Do** → **In Progress** → **Review** → **Done**

**Board URL:** [Azure DevOps Boards](https://dev.azure.com/adasilvaieu2023/devops%20group%20project%20Adrian/_boards/board/t/)

### Refinement Process

- Product Owner reviews and prioritizes backlog items weekly
- Team estimates story points during sprint planning
- Backlog items are refined before being selected for sprints
- Acceptance criteria are defined before work begins

### Definition of Ready

A user story is ready for sprint planning when:
- [ ] Description is clear and complete
- [ ] Acceptance criteria are defined
- [ ] Story points are estimated
- [ ] Dependencies are identified
- [ ] Technical approach is understood

---

## Notes

- Story IDs follow the pattern: Sprint 1 (#1-4), Sprint 2 (#139-143), Sprint 3 (#201-207), Future (#301+)
- Story points use Fibonacci sequence (1, 2, 3, 5, 8, 13)
- Priority: 1 = Critical, 2 = High, 3 = Medium, 4 = Low
- Status: ✅ Complete, 🔄 In Progress, 📋 Not Started, ❌ Blocked

---

**Document Created:** December 5, 2025  
**Last Updated:** December 5, 2025  
**Maintained By:** Product Owner (Omar) and Scrum Master (Kenny)

