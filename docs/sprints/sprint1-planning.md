**Sprint Duration:** November 26-28, 2025 (2 days)  
**Sprint Goal:** Deploy a working FastAPI application to Azure App Service with automated CI/CD pipeline and basic monitoring

---

## Sprint Information

- **Sprint Number:** Sprint 1
- **Start Date:** November 26, 2025
- **End Date:** November 28, 2025
- **Sprint Duration:** 2 days
- **Team Size:** 6 members
- **Team Capacity:** 48 hours (6 members × 2 days × 4 hours/day)

---

## Team Roles

| Role                         | Name    | Responsibilities                                                          |
| ---------------------------- | ------- | ------------------------------------------------------------------------- |
| Product Owner                | Kenny   | Prioritize backlog, define acceptance criteria, stakeholder communication |
| Scrum Master                 | Adrian  | Facilitate ceremonies, remove blockers, ensure Scrum process              |
| Developer 1 (Infrastructure) | Jack    | Azure infrastructure setup and deployment                                 |
| Developer 2 (CI/CD)          | Omar    | Automated pipeline configuration                                          |
| Developer 3 (Monitoring)     | Salmane | Application Insights and documentation                                    |

---

## Sprint Goal

**Primary Goal:**  
Deploy a working "Hello World" FastAPI application to Azure App Service with automated CI/CD pipeline and basic monitoring.

**Success Criteria:**

- ✅ Application accessible via public URL
- ✅ All endpoints (/, /health, /api/info) working
- ✅ Automated CI/CD pipeline operational
- ✅ Basic monitoring configured
- ✅ Complete documentation

---

## Product Backlog Items Selected for Sprint 1

### Epic: Weather Watcher MVP

**Total Story Points:** 14 points

---

### User Story #1: Deploy Application Infrastructure to Azure

**Priority:** 1  
**Story Points:** 5  
**Assigned To:** Developer 1 (Jack)

**Description:**  
As a developer, I want Azure infrastructure set up, so that I can deploy the application online.

**Acceptance Criteria:**

- ✅ Azure Resource Group created
- ✅ Azure App Service running with Python 3.11
- ✅ Application Insights configured and collecting data
- ✅ Application accessible via public URL
- ✅ All resources documented in README

**Tasks:**

1. Create FastAPI application structure (2h) - COMPLETED
2. Implement basic API endpoints (/, /health, /api/info) (2h) - COMPLETED
3. Create requirements.txt with dependencies (0.5h) - COMPLETED
4. Create .gitignore for Python project (0.5h) - COMPLETED
5. Set up project folder structure (app, docs, tests) (0.5h) - COMPLETED
6. Create Azure Resource Group (0.5h) - COMPLETED
7. Create Azure App Service Plan (F1 tier) (0.5h) - COMPLETED
8. Create Azure App Service with Python 3.11 (1h) - COMPLETED
9. Get Azure deployment credentials (0.5h) - COMPLETED
10. Deploy application to Azure App Service (1h) - COMPLETED
11. Verify application is accessible via public URL (0.5h) - COMPLETED

---

### User Story #2: Automated CI/CD Pipeline

**Priority:** 1  
**Story Points:** 5  
**Assigned To:** Developer 2 (Omar)

**Description:**  
As a developer, I want an automated deployment pipeline, so that code deploys automatically when I push to main branch.

**Acceptance Criteria:**

- Pipeline triggers on push to main branch
- Pipeline builds Python application
- Pipeline runs all automated tests
- Pipeline deploys to Azure on success
- Failed tests block deployment
- Pipeline completes in under 5 minutes

**Tasks:**

1. Create azure-pipelines.yml file (1h)
2. Configure pipeline build stage (1.5h)
3. Configure pipeline test stage (1h)
4. Set up Azure service connection in DevOps (1h)
5. Configure pipeline deployment stage (2h)
6. Test pipeline runs successfully end-to-end (1h)

---

### User Story #3: Application Monitoring and Logging

**Priority:** 2  
**Story Points:** 2  
**Assigned To:** Developer 3 (Salmane)

**Description:**  
As a developer, I want monitoring and logging enabled, so that I can track application health and debug issues.

**Acceptance Criteria:**

- Application Insights connected to App Service
- Dashboard shows key metrics (uptime, response time, errors)
- Health endpoint is monitored
- Errors are logged and visible
- Alerts configured for failures

**Tasks:**

1. Create Application Insights resource in Azure (0.5h)
2. Connect Application Insights to App Service (1h)
3. Add Application Insights SDK to Python app (1h)
4. Create monitoring dashboard in Azure (1h)
5. Verify metrics are being collected (0.5h)

---

### User Story #4: Project Documentation

**Priority:** 2  
**Story Points:** 2  
**Assigned To:** Scrum Master (Adrian)

**Description:**  
As a team member, I want complete project documentation, so that I can understand, contribute to, and maintain the project.

**Acceptance Criteria:**

- README with setup instructions and architecture diagram
- Definition of Done documented
- Sprint 1 Planning document complete
- Daily Scrum Notes template created
- All Sprint 1 artifacts documented
- Azure resource URLs documented

**Tasks:**

1. Create basic README.md (1h) - COMPLETED
2. Create Definition of Done document (1h) - COMPLETED
3. Add architecture diagram to README (1h)
4. Document all Azure resource names and URLs (0.5h) - COMPLETED
5. Create Sprint 1 Planning document (1h) - IN PROGRESS
6. Update Daily Scrum Notes template (0.5h)

**Status:** IN PROGRESS

---

## Sprint Backlog Summary

| User Story                         | Story Points | Status      | Assignee |
| ---------------------------------- | ------------ | ----------- | -------- |
| Deploy Application Infrastructure  | 5            | Developer 1 |
| Automated CI/CD Pipeline           | 5            | Developer 2 |
| Application Monitoring and Logging | 2            | Developer 3 |
| Project Documentation              | 2            | Developer 3 |
| **TOTAL**                          | **14**       |             |          |

---

## Technical Implementation Details

### Technology Stack

- **Backend:** FastAPI (Python 3.11)
- **Frontend:** HTML/CSS (minimal, embedded)
- **Cloud Platform:** Microsoft Azure
- **Hosting:** Azure App Service (Linux, F1 Free tier)
- **CI/CD:** Azure Pipelines
- **Monitoring:** Azure Application Insights
- **Version Control:** Azure DevOps Repos (Git)
- **Testing:** pytest
- **Dependencies:** fastapi, uvicorn, pytest, httpx, python-dotenv, gunicorn

### Azure Resources Created

| Resource Type        | Name                        | Details                                      |
| -------------------- | --------------------------- | -------------------------------------------- |
| Resource Group       | BCSAI2025-DEVOPS-STUDENT-4B | Location: West Europe                        |
| App Service Plan     | asp-weather-watcher         | Tier: F1 (Free), OS: Linux                   |
| App Service          | weather-watcher-4B2025      | Runtime: Python 3.11, Location: North Europe |
| Application Insights | (To be created)             | For monitoring and logging                   |

### Live Application

- **URL:** https://weather-watcher-4b2025.azurewebsites.net
- **Endpoints:**
  - `/` - Homepage with project information
  - `/health` - Health check endpoint
  - `/api/info` - API information endpoint

---

---

## Sprint Ceremonies Schedule

### Daily Standup

- **Time:** 10:00 AM daily
- **Duration:** 15 minutes max
- **Format:** Each team member answers:
  1. What I completed yesterday
  2. What I'll work on today
  3. Any blockers

### Sprint Review

- **Date:** November 28, 2025 (End of Sprint)
- **Time:** TBD
- **Duration:** 1 hour
- **Attendees:** Team + Stakeholders (Professor/TA)
- **Agenda:**
  - Demo working application
  - Review completed User Stories
  - Gather feedback
  - Update Product Backlog

### Sprint Retrospective

- **Date:** November 28, 2025 (After Sprint Review)
- **Time:** TBD
- **Duration:** 45 minutes
- **Attendees:** Team only
- **Agenda:**
  - What went well
  - What didn't go well
  - Action items for Sprint 2

---

## Risks and Mitigation

### Identified Risks

| Risk                        | Impact | Probability | Mitigation                                          |
| --------------------------- | ------ | ----------- | --------------------------------------------------- |
| Azure quota limits reached  | High   | Medium      | Use different regions, coordinate resource creation |
| Deployment failures         | High   | Low         | Enable proper build settings, test locally first    |
| Time constraints (2 days)   | Medium | High        | Focus on MVP, defer nice-to-haves                   |
| Team coordination issues    | Medium | Low         | Daily standups, clear communication                 |
| Azure Free tier limitations | Low    | High        | Documented expectations, plan for cold starts       |

---

## Dependencies

### External Dependencies

- Azure subscription access for all team members
- Azure DevOps permissions properly configured
- Internet connectivity for deployment

### Internal Dependencies

- Developer 2 (CI/CD) depends on Developer 1 (Infrastructure) completing Azure setup
- Developer 3 (Monitoring) depends on Developer 1 (Infrastructure) completing App Service creation
- All developers depend on Scrum Master for blocker resolution

---

## Branch Strategy

### Git Workflow

- **Main Branch:** Always deployable, protected
- **Feature Branches:** Created for each developer's work
  - `feature/azure-infrastructure` (Developer 1)
  - `feature/ci-cd-pipeline` (Developer 2)
  - `feature/monitoring-docs` (Developer 3)
- **Pull Requests:** Required for merging to main
- **Code Reviews:** Minimum 1 approval required

---

## Notes and Decisions

### Key Decisions Made

1. **Sprint Duration:** Reduced from 5 days to 2 days due to project timeline
2. **Subscription:** Using "Azure Simple IE Instituto de Empresa" (shared class subscription)
3. **Resource Group:** Using pre-created `BCSAI2025-DEVOPS-STUDENT-4B` instead of creating new
4. **Region:** North Europe selected (West Europe had quota limits)
5. **Deployment Method:** Using `az webapp up` with forced build settings

### Lessons Learned (In Progress)

- Always create feature branch before starting work
- Azure Free tier has quota limits (10 per region)
- `SCM_DO_BUILD_DURING_DEPLOYMENT=true` is essential for Python apps
- F1 tier has slow cold start times (30-60 seconds)

---

## Sprint Burndown

**Target Velocity:** 14 story points

| Day            | Story Points Completed | Story Points Remaining |
| -------------- | ---------------------- | ---------------------- |
| Nov 26 (Start) | 0                      | 14                     |
| Nov 27         | 5                      | 9                      |
| Nov 28 (End)   | TBD                    | TBD                    |

---

---

## Appendix

### Useful Commands

**Azure CLI Login:**

```bash
az login --use-device-code
```

**Deploy Application:**

```bash
az webapp up --name weather-watcher-4B2025 --resource-group BCSAI2025-DEVOPS-STUDENT-4B --runtime "PYTHON|3.11"
```

**View Logs:**

```bash
az webapp log tail --name weather-watcher-4B2025 --resource-group BCSAI2025-DEVOPS-STUDENT-4B
```

**Restart App Service:**

```bash
az webapp restart --name weather-watcher-4B2025 --resource-group BCSAI2025-DEVOPS-STUDENT-4B
```

### References

- [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Azure DevOps Documentation](https://docs.microsoft.com/en-us/azure/devops/)
- [Scrum Guide](https://scrumguides.org/)

---
