# Sprint 2 Planning Document

**Sprint Duration:** December 2 - December 4, 2025 (3 days)  
**Sprint Goal:** Implement core weather functionality and enhance monitoring capabilities

---

## Sprint Information

- **Sprint Number:** Sprint 2
- **Start Date:** December 2, 2025
- **End Date:** December 4, 2025
- **Sprint Duration:** 3 days
- **Team Size:** 5 members
- **Team Capacity:** 60 hours (5 members × 3 days × 4 hours/day)

---

## Team Roles

| Role                  | Name    | Responsibilities                                                          |
| --------------------- | ------- | ------------------------------------------------------------------------- |
| Product Owner         | Jack    | Prioritize backlog, define acceptance criteria, stakeholder communication |
| Scrum Master          | Salmane | Facilitate ceremonies, remove blockers, ensure Scrum process              |
| Developer 1           | Omar    | Backend development and API integration                                   |
| Developer 2           | Adrian  | Frontend development and UI/UX                                            |
| Developer 3           | Kenny   | Testing and monitoring enhancements                                       |

---

## Sprint Goal

**Primary Goal:**  
Build the core Weather Watcher functionality by integrating weather API, implementing weather display features, and enhancing monitoring capabilities.

**Success Criteria:**

- [ ] Weather API integration complete and functional
- [ ] Users can view current weather for a location
- [ ] Application Insights fully configured with custom metrics
- [ ] Enhanced monitoring dashboard with weather-specific metrics
- [ ] All documentation updated and complete
- [ ] All tests passing with >80% coverage

---

## Sprint 1 Review Summary

### What We Completed in Sprint 1 ✅

- Azure App Service deployed and running (weather-watcher-4B2025)
- CI/CD pipeline operational with Azure Pipelines
- All basic endpoints working (/, /health, /api/info)
- Application accessible at: https://weather-watcher-4b2025.azurewebsites.net
- Basic project documentation established

### What Carried Over to Sprint 2 📋

- Application Insights integration (partially completed)
- Monitoring dashboard creation
- Architecture diagram
- Enhanced documentation

---

## Product Backlog Items Selected for Sprint 2

### Epic: Weather Watcher MVP

**Total Story Points:** TBD (to be estimated during planning)

---

### User Story #139: Sprint 2 Documentation & Project Updates

**Priority:** 1  
**Story Points:** 2  
**Assigned To:** Scrum Master (Salmane)  
**Status:** ✅ COMPLETED

**Description:**  
As a team member, I want comprehensive Sprint 2 documentation and project updates, so that all stakeholders understand our progress and the project is properly documented.

**Acceptance Criteria:**

- [x] Sprint 2 Planning document created
- [x] Daily Scrum Notes updated for Sprint 2
- [x] README updated with Sprint 2 features
- [x] Architecture diagram created/updated
- [x] CI/CD documentation updated
- [x] Sprint 2 Retrospective template created

**Tasks:**

1. [x] Create Sprint 2 Planning document (1h) - COMPLETED
2. [x] Update Daily Scrum Notes template for Sprint 2 (0.5h) - COMPLETED
3. [x] Update README with new features and changes (1h) - COMPLETED
4. [x] Create/update architecture diagram (1.5h) - COMPLETED
5. [x] Document pipeline and deployment process (0.5h) - COMPLETED
6. [x] Create Sprint 2 Retrospective template (0.5h) - COMPLETED

**Total Estimated Time:** 5 hours  
**Status:** ✅ ALL TASKS COMPLETED

---

### User Story #TBD: Weather API Integration

**Priority:** 1  
**Story Points:** 5  
**Assigned To:** Developer 1 (Omar)

**Description:**  
As a user, I want the application to fetch real-time weather data, so that I can view current weather conditions.

**Acceptance Criteria:**

- [ ] Weather API selected (e.g., OpenWeatherMap, WeatherAPI)
- [ ] API key configured in Azure App Service settings
- [ ] Backend endpoint created to fetch weather data
- [ ] Error handling for API failures
- [ ] Response data properly formatted
- [ ] API rate limits considered and handled

**Tasks:**

1. Research and select weather API provider (0.5h)
2. Create API account and get API key (0.5h)
3. Configure API key in Azure App Service environment variables (0.5h)
4. Create backend service to fetch weather data (2h)
5. Implement error handling and retry logic (1h)
6. Add unit tests for weather service (1.5h)
7. Document API integration in README (0.5h)

**Total Estimated Time:** 6.5 hours

---

### User Story #TBD: Weather Display Frontend

**Priority:** 1  
**Story Points:** 5  
**Assigned To:** Developer 2 (Adrian)

**Description:**  
As a user, I want to see weather information in a clean, user-friendly interface, so that I can easily understand the weather conditions.

**Acceptance Criteria:**

- [ ] Weather search page created
- [ ] User can enter city name
- [ ] Current weather displayed (temperature, conditions, humidity, wind)
- [ ] Weather icons displayed based on conditions
- [ ] Responsive design works on mobile and desktop
- [ ] Loading states and error messages shown

**Tasks:**

1. Design weather display UI mockup (0.5h)
2. Create weather search form (1.5h)
3. Implement weather display component (2h)
4. Add weather icons and styling (1.5h)
5. Implement responsive CSS (1h)
6. Add loading and error states (0.5h)
7. Test across different devices (0.5h)

**Total Estimated Time:** 7.5 hours

---

### User Story #TBD: Enhanced Application Monitoring

**Priority:** 2  
**Story Points:** 3  
**Assigned To:** Developer 3 (Kenny)

**Description:**  
As a developer, I want comprehensive monitoring and logging, so that I can track application performance and debug issues quickly.

**Acceptance Criteria:**

- [ ] Application Insights fully integrated
- [ ] Custom metrics tracking (weather API calls, response times)
- [ ] Monitoring dashboard shows weather-specific metrics
- [ ] Alerts configured for API failures
- [ ] Log queries created for common debugging scenarios
- [ ] Performance metrics tracked

**Tasks:**

1. Complete Application Insights resource setup (0.5h)
2. Add Application Insights SDK to Python app (1h)
3. Implement custom metrics for weather API (1.5h)
4. Create monitoring dashboard in Azure (1.5h)
5. Configure alerts for critical failures (0.5h)
6. Document monitoring setup and queries (0.5h)

**Total Estimated Time:** 5.5 hours

---

### User Story #TBD: Testing and Quality Assurance

**Priority:** 2  
**Story Points:** 3  
**Assigned To:** Developer 3 (Kenny) - Shared with Monitoring

**Description:**  
As a developer, I want comprehensive test coverage, so that I can ensure code quality and catch bugs early.

**Acceptance Criteria:**

- [ ] Unit tests for all new endpoints
- [ ] Integration tests for weather API
- [ ] Test coverage > 70%
- [ ] All tests passing in CI pipeline
- [ ] Edge cases and error scenarios tested

**Tasks:**

1. Write unit tests for weather service (2h)
2. Write integration tests for weather endpoints (1.5h)
3. Add tests for error scenarios (1h)
4. Generate test coverage report (0.5h)
5. Update CI pipeline with coverage reporting (0.5h)

**Total Estimated Time:** 5.5 hours

**Note:** Kenny will handle both monitoring and testing tasks in parallel.

---

## Sprint Backlog Summary

| User Story                              | Story Points | Status      | Assignee |
| --------------------------------------- | ------------ | ----------- | -------- |
| Sprint 2 Documentation & Project Updates| 2            | ✅ Done     | Salmane  |
| Weather API Integration                 | 5            | Not Started | Omar     |
| Weather Display Frontend                | 5            | Not Started | Adrian   |
| Enhanced Application Monitoring         | 3            | Not Started | Kenny    |
| Testing and Quality Assurance           | 3            | Not Started | Kenny    |
| **TOTAL**                               | **18**       | **2/18 Done** |        |

---

## Technical Implementation Details

### Technology Stack (Sprint 2 Additions)

**Existing:**
- Backend: FastAPI (Python 3.11)
- Frontend: HTML/CSS
- Cloud: Microsoft Azure
- Hosting: Azure App Service (Linux, F1 Free tier)
- CI/CD: Azure Pipelines
- Version Control: Azure DevOps Repos (Git)
- Testing: pytest

**New for Sprint 2:**
- Weather API: TBD (OpenWeatherMap, WeatherAPI, or similar)
- Application Insights: Azure Application Insights (full integration)
- Frontend Framework: Consider lightweight JS framework or vanilla JS
- Additional Dependencies: requests, opencensus-azure, etc.

### API Endpoints to be Created

| Method | Endpoint              | Description                        |
| ------ | --------------------- | ---------------------------------- |
| GET    | /weather/{city}       | Get current weather for a city     |
| GET    | /weather/search       | Search weather by city name        |
| POST   | /weather/favorite     | Add city to favorites (future)     |

---

## Sprint Ceremonies Schedule

### Daily Standup

- **Time:** 10:00 AM daily
- **Duration:** 15 minutes max
- **Platform:** Teams/Discord
- **Format:** Each team member answers:
  1. What I completed yesterday
  2. What I'll work on today
  3. Any blockers

### Sprint Planning

- **Date:** December 2, 2025
- **Duration:** 1.5 hours
- **Outcomes:**
  - Sprint goal defined
  - User stories selected and estimated (18 story points total)
  - Tasks broken down and time-boxed for 3-day sprint
  - Team members assigned

### Sprint Review

- **Date:** December 4, 2025 (End of Sprint)
- **Time:** TBD
- **Duration:** 1 hour
- **Attendees:** Team + Stakeholders (Professor/TA)
- **Agenda:**
  - Demo working weather features
  - Review completed User Stories
  - Gather feedback
  - Update Product Backlog for Sprint 3

### Sprint Retrospective

- **Date:** December 4, 2025 (After Sprint Review)
- **Time:** TBD
- **Duration:** 45 minutes
- **Attendees:** Team only
- **Format:** Start-Stop-Continue
- **Agenda:**
  - What went well
  - What didn't go well
  - What to start doing
  - What to stop doing
  - What to continue doing
  - Action items for Sprint 3

---

## Risks and Mitigation

### Identified Risks

| Risk                              | Impact | Probability | Mitigation                                              |
| --------------------------------- | ------ | ----------- | ------------------------------------------------------- |
| Weather API rate limits           | High   | Medium      | Implement caching, choose API with generous free tier   |
| Weather API costs                 | Medium | Low         | Use free tier, monitor usage closely                    |
| Complex frontend implementation   | Medium | Medium      | Start with simple UI, iterate based on time available   |
| Application Insights setup issues | Medium | Low         | Follow Azure documentation, test incrementally          |
| Integration testing challenges    | Medium | Medium      | Mock API responses, use test API keys                   |
| Final demo on December 4          | High   | High        | Ensure MVP ready by Dec 3, buffer time for issues       |

---

## Dependencies

### External Dependencies

- Weather API provider selection and API key
- Azure Application Insights resource availability
- Continued Azure subscription access
- Internet connectivity for API calls

### Internal Dependencies

- Frontend depends on backend API endpoints being ready
- Testing depends on features being implemented
- Monitoring depends on Application Insights setup
- Documentation depends on features being finalized

---

## Branch Strategy

### Git Workflow (Continued from Sprint 1)

- **Main Branch:** Always deployable, protected
- **Feature Branches:** Created for each developer's work
  - `feature/weather-api-integration` (Omar)
  - `feature/weather-frontend` (Adrian)
  - `feature/app-insights` (Kenny)
  - `feature/sprint2-docs` (Salmane)
- **Pull Requests:** Required for merging to main
- **Code Reviews:** Minimum 1 approval required
- **CI Pipeline:** Must pass before merge

---

## Definition of Done (Sprint 2)

A User Story is considered **DONE** when:

### Code Quality
- [ ] Code is written and follows team coding standards
- [ ] Code is reviewed by at least one team member
- [ ] No critical code smells or security issues
- [ ] Code is properly commented

### Testing
- [ ] Unit tests are written and passing
- [ ] Integration tests are written and passing
- [ ] Tests pass locally
- [ ] CI pipeline tests pass
- [ ] Test coverage > 80% for new code

### Deployment
- [ ] Feature is deployed to Azure App Service
- [ ] Deployment pipeline succeeds
- [ ] Application is accessible via public URL
- [ ] Feature works in production environment

### Monitoring
- [ ] Endpoint returns expected responses
- [ ] No errors in Application Insights logs
- [ ] Custom metrics configured (if applicable)
- [ ] Performance is acceptable (<2s response time)

### Documentation
- [ ] README is updated with new features
- [ ] API endpoints are documented
- [ ] Environment variables documented
- [ ] Architecture diagram updated if needed

---

## Notes and Decisions

### Key Decisions to Make in Sprint Planning

1. **Weather API Selection:** Which provider? (OpenWeatherMap, WeatherAPI, AccuWeather)
2. **Frontend Approach:** Vanilla JS or lightweight framework?
3. **Story Point Estimation:** Need to estimate all user stories
4. **Team Assignments:** Confirm who takes which user story
5. **Stretch Goals:** What if we finish early?

### Lessons Learned from Sprint 1

✅ **Keep Doing:**
- Early infrastructure setup
- Clear documentation
- Regular communication
- Feature branches and PRs

⚠️ **Improve:**
- Earlier Application Insights setup
- More frequent commits
- Better time estimation
- More granular tasks

### Sprint 2 Focus Areas

1. **User Value:** Actual weather features that users can interact with
2. **Quality:** Comprehensive testing and monitoring
3. **Documentation:** Keep docs updated as we build
4. **Team Collaboration:** Better coordination between frontend/backend

---

## Sprint Burndown Chart

**Target Velocity:** 18 story points

| Day                | Story Points Completed | Story Points Remaining |
| ------------------ | ---------------------- | ---------------------- |
| Dec 2 (Start)      | 0                      | 18                     |
| Dec 3              | TBD                    | TBD                    |
| Dec 4 (End/Demo)   | TBD                    | 0 (Goal)               |

---

## Success Metrics

### Sprint 2 Will Be Successful If:

1. ✅ Weather functionality is working in production
2. ✅ Users can search for a city and see weather data
3. ✅ Application Insights is fully configured
4. ✅ All tests passing with >80% coverage
5. ✅ CI/CD pipeline deploys successfully
6. ✅ Application is demo-ready for December 4
7. ✅ All documentation is complete and accurate

---

## Appendix

### Useful Resources

**Weather APIs:**
- [OpenWeatherMap](https://openweathermap.org/api) - 1000 calls/day free
- [WeatherAPI](https://www.weatherapi.com/) - 1M calls/month free
- [Visual Crossing](https://www.visualcrossing.com/) - 1000 calls/day free

**Azure Documentation:**
- [Application Insights for Python](https://docs.microsoft.com/en-us/azure/azure-monitor/app/opencensus-python)
- [Azure App Service Configuration](https://docs.microsoft.com/en-us/azure/app-service/configure-common)

**Testing Resources:**
- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

---

**Document Created:** December 1, 2025  
**Created By:** Salmane Mouhib (Scrum Master)  
**Last Updated:** December 1, 2025
