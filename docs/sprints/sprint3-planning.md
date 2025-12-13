# Sprint 3 Planning Document

**Sprint Duration:** December 5 - December 8, 2025 (4 days)  
**Sprint Goal:** Enhance user experience, improve reliability, and add advanced features

---

## Sprint Information

- **Sprint Number:** Sprint 3
- **Start Date:** December 5, 2025
- **End Date:** December 8, 2025
- **Sprint Duration:** 4 days
- **Team Size:** 5 members
- **Team Capacity:** 80 hours (5 members × 4 days × 4 hours/day)

---

## Team Roles

| Role                  | Name    | Responsibilities                                                          |
| --------------------- | ------- | ------------------------------------------------------------------------- |
| Product Owner         | Omar    | Prioritize backlog, define acceptance criteria, stakeholder communication |
| Scrum Master          | Kenny   | Facilitate ceremonies, remove blockers, ensure Scrum process              |
| Developer 1           | Jack    | Backend development and API integration                                   |
| Developer 2           | Adrian  | Frontend development and UI/UX                                            |
| Developer 3           | Salmane | Testing and monitoring enhancements                                       |

---

## Sprint Goal

**Primary Goal:**  
Enhance Weather Watcher with advanced features, improve performance and reliability, and polish the user experience to deliver a production-ready application.

**Success Criteria:**

- [ ] 5-day weather forecast fully functional with real API integration
- [ ] City autocomplete working with Google Places API
- [ ] Application Insights monitoring dashboard operational
- [ ] Error handling and retry logic improved
- [ ] Performance optimizations implemented
- [ ] All tests passing with >85% coverage
- [ ] Documentation complete and up-to-date

---

## Sprint 2 Review Summary

### What We Completed in Sprint 2 ✅

- ✅ Weather API integration complete (Google Maps Weather API)
- ✅ Weather display frontend with modern dark theme UI
- ✅ City search functionality with autocomplete
- ✅ 5-day forecast display (UI implemented, API integration in progress)
- ✅ Application Insights integration with custom telemetry
- ✅ Comprehensive test suite with pytest
- ✅ Country code to name conversion
- ✅ Multiple API endpoints (/api/weather, /weather/{city}, /api/cities/autocomplete, /api/forecast)
- ✅ Responsive design for mobile and desktop
- ✅ Error handling and user-friendly error messages

### What Carried Over to Sprint 3 📋

- Complete 5-day forecast API integration (OpenWeatherMap)
- Enhanced monitoring dashboard in Azure
- Performance optimizations (caching, rate limiting)
- Additional test coverage for edge cases
- Documentation refinements

---

## Product Backlog Items Selected for Sprint 3

### Epic: Weather Watcher Enhancement

**Total Story Points:** 18

---

### User Story #1: 5-Day Weather Forecast

**Priority:** 1 (Critical)  
**Story Points:** 5  
**Assigned To:** Developer 1 (Jack Raja Shawki Samawi)  
**Status:** ✅ Closed

**Description:**  
As a user, I want to see a 5-day weather forecast, so that I can plan my activities ahead of time.

**Acceptance Criteria:**

- [x] Forecast endpoint added to weather service
- [x] /api/forecast API endpoint created
- [x] Forecast UI layout designed
- [x] Forecast display logic implemented
- [x] Forecast cards styled
- [x] Forecast functionality tested

**Tasks:**

1. [x] Add forecast endpoint to weather service
2. [x] Create /api/forecast API endpoint
3. [x] Design forecast UI layout
4. [x] Implement forecast display logic
5. [x] Style forecast cards
6. [x] Test forecast functionality

**Total Estimated Time:** TBD

---

### User Story #2: Full Country Names Display

**Priority:** 1 (Critical)  
**Story Points:** 3  
**Assigned To:** Developer 3 (Salmane Mouhib)  
**Status:** ✅ Closed

**Description:**  
As a user, I want to see full country names instead of country codes, so that the information is more readable and user-friendly.

**Acceptance Criteria:**

- [x] Country code mapping dictionary created
- [x] Country name conversion function implemented
- [x] Weather API responses updated to include full country names
- [x] Country name display tested

**Tasks:**

1. [x] Create country code mapping dictionary
2. [x] Implement country name conversion function
3. [x] Update weather API responses
4. [x] Test country name display

**Total Estimated Time:** TBD

---

### User Story #3: City Autocomplete & Search Improvements

**Priority:** 1 (Critical)  
**Story Points:** 5  
**Assigned To:** Developer 1 (Jack Raja Shawki Samawi)  
**Status:** ✅ Closed

**Description:**  
As a user, I want improved city autocomplete and search functionality, so that I can quickly find and select cities.

**Acceptance Criteria:**

- [x] Autocomplete approach researched and chosen
- [x] Autocomplete API endpoint implemented
- [x] Autocomplete JavaScript logic added
- [x] Autocomplete dropdown styled
- [x] Loading and error states added
- [x] Autocomplete functionality tested

**Tasks:**

1. [x] Research and choose autocomplete approach
2. [x] Implement autocomplete API endpoint
3. [x] Add autocomplete JavaScript logic
4. [x] Style autocomplete dropdown
5. [x] Add loading and error states
6. [x] Test autocomplete functionality

**Total Estimated Time:** TBD

---

### User Story #4: Loading States & UI Polish

**Priority:** 2 (High)  
**Story Points:** 3  
**Assigned To:** Developer 2 (Adrian Kia Rekaa Hasini Da Silva)  
**Status:** 📋 New (Not Started)

**Description:**  
As a user, I want smooth loading states and polished UI, so that the application feels professional and responsive.

**Acceptance Criteria:**

- [ ] Loading spinner component created
- [ ] Skeleton loading screens added
- [ ] Fade-in animations implemented
- [ ] Button loading states added
- [ ] Error message display improved

**Tasks:**

1. [ ] Create loading spinner component
2. [ ] Add skeleton loading screens
3. [ ] Implement fade-in animations
4. [ ] Add button loading states
5. [ ] Improve error message display

**Total Estimated Time:** TBD

---

### User Story #5: Sprint 3 Documentation

**Priority:** 2 (High)  
**Story Points:** 2  
**Assigned To:** Scrum Master (Kenny Tohme)  
**Status:** 🔄 Active (In Progress)

**Description:**  
As a team member, I want comprehensive Sprint 3 documentation, so that all stakeholders understand our progress and the project is properly documented.

**Acceptance Criteria:**

- [x] Sprint 3 Planning Document created
- [x] README updated with new features
- [x] Architecture diagram created/updated
- [ ] Sprint 3 retrospective completed

**Tasks:**

1. [x] Create Sprint 3 Planning Document
2. [x] Update README with new features
3. [x] Create or update architecture diagram
4. [ ] Write Sprint 3 retrospective

**Total Estimated Time:** TBD

---

## Sprint Backlog Summary

| User Story                              | Story Points | Status      | Assignee |
| --------------------------------------- | ------------ | ----------- | -------- |
| 5-Day Weather Forecast                  | 5            | ✅ Closed   | Jack     |
| Full Country Names Display              | 3            | ✅ Closed   | Salmane  |
| City Autocomplete & Search Improvements | 5            | ✅ Closed   | Jack     |
| Loading States & UI Polish              | 3            | 📋 New     | Adrian   |
| Sprint 3 Documentation                  | 2            | 🔄 Active  | Kenny    |
| **TOTAL**                               | **18**       | **3/5 Complete (13 SP)** |        |

**Completion Rate:** 72% (13 out of 18 story points completed)

---

## Technical Implementation Details

### Technology Stack (Sprint 3 Additions)

**Existing:**
- Backend: FastAPI (Python 3.11)
- Frontend: HTML/CSS/JavaScript (Vanilla JS)
- Cloud: Microsoft Azure
- Hosting: Azure App Service (Linux, F1 Free tier)
- CI/CD: Azure Pipelines
- Version Control: Azure DevOps Repos (Git)
- Testing: pytest
- Weather API: Google Maps Weather API
- Monitoring: Azure Application Insights

**New for Sprint 3:**
- Forecast API: OpenWeatherMap API (5-day forecast)
- Caching: In-memory caching for API responses
- Rate Limiting: API rate limiting middleware

### API Endpoints (Current + New)

| Method | Endpoint                      | Description                        | Status      |
| ------ | ----------------------------- | ---------------------------------- | ----------- |
| GET    | /                             | Homepage with weather UI           | ✅ Complete |
| GET    | /health                       | Health check                       | ✅ Complete |
| GET    | /api/info                     | Project info                       | ✅ Complete |
| GET    | /api/weather                  | Get weather by city (query param)  | ✅ Complete |
| GET    | /weather/{city}               | Get weather by city (path param)   | ✅ Complete |
| GET    | /api/cities/autocomplete      | City autocomplete suggestions      | ✅ Complete |
| GET    | /api/forecast                 | 5-day weather forecast             | 🔄 In Progress |
| GET    | /api/debug                    | Debug configuration                | ✅ Complete |

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

- **Date:** December 5, 2025
- **Duration:** 1.5 hours
- **Outcomes:**
  - Sprint goal defined
  - User stories selected and estimated (18 story points total)
  - Tasks broken down and time-boxed for 4-day sprint
  - Team members assigned

### Sprint Review

- **Date:** December 8, 2025 (End of Sprint)
- **Time:** TBD
- **Duration:** 1 hour
- **Attendees:** Team + Stakeholders (Professor/TA)
- **Agenda:**
  - Demo enhanced weather features
  - Show 5-day forecast functionality
  - Present monitoring dashboard
  - Review completed User Stories
  - Gather feedback
  - Update Product Backlog for future sprints

### Sprint Retrospective

- **Date:** December 8, 2025 (After Sprint Review)
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
  - Action items for future sprints

---

## Risks and Mitigation

### Identified Risks

| Risk                              | Impact | Probability | Mitigation                                              |
| --------------------------------- | ------ | ----------- | ------------------------------------------------------- |
| OpenWeatherMap API rate limits    | Medium | Medium      | Monitor usage, implement caching, use free tier wisely |
| Performance optimization complexity | Medium | Low         | Start with simple caching, iterate based on results    |
| Test coverage target (85%)        | Medium | Medium      | Prioritize critical paths, use coverage tools          |
| Integration testing challenges    | Medium | Low         | Use mocking, test incrementally                         |
| Time constraints for all features  | High   | Medium      | Prioritize must-have features, defer nice-to-haves     |

---

## Dependencies

### External Dependencies

- OpenWeatherMap API key and account setup
- Azure Application Insights dashboard access
- Continued Azure subscription access
- Google Maps API key (already configured)

### Internal Dependencies

- Forecast frontend depends on forecast API being ready
- Dashboard depends on Application Insights metrics
- Performance optimizations depend on baseline measurements
- Documentation depends on features being finalized

---

## Kanban Board and Work Item Tracking

### Azure DevOps Boards

All Sprint 3 work items are tracked using **Azure DevOps Boards** with the following workflow:

**Board States:**
- **Backlog** → **To Do** → **In Progress** → **Review** → **Done**

**Board URL:** [Azure DevOps Boards](https://dev.azure.com/adasilvaieu2023/devops%20group%20project%20Adrian/_boards/board/t/)

**Work Item Types:**
- User Stories (Epic level)
- Tasks (Story level)
- Bugs (if any)

**Board Columns:**
1. **Backlog:** All Sprint 3 user stories
2. **To Do:** Stories ready to start
3. **In Progress:** Stories currently being worked on
4. **Review:** Stories ready for code review
5. **Done:** Completed stories

**Daily Updates:**
- Team members update work items during daily standups
- Move items between columns as work progresses
- Link commits and pull requests to work items

**Burndown Tracking:**
- Sprint burndown chart automatically generated from board
- Shows remaining story points over time
- Helps identify if sprint is on track

---

## Branch Strategy

### Git Workflow (Continued from Sprint 2)

- **Main Branch:** Always deployable, protected
- **Feature Branches:** Created for each developer's work
  - `feature/forecast-integration` (Jack)
  - `feature/autocomplete-enhancement` (Jack/Adrian)
  - `feature/monitoring-dashboard` (Salmane)
  - `feature/performance-optimization` (Jack)
  - `feature/error-handling` (Jack/Salmane)
  - `feature/test-coverage` (Salmane)
  - `feature/sprint3-docs` (Kenny)
- **Pull Requests:** Required for merging to main
- **Code Reviews:** Minimum 1 approval required
- **CI Pipeline:** Must pass before merge

---

## Definition of Done (Sprint 3)

A User Story is considered **DONE** when:

### Code Quality
- [ ] Code is written and follows team coding standards
- [ ] Code is reviewed by at least one team member
- [ ] No critical code smells or security issues
- [ ] Code is properly commented
- [ ] Performance requirements met

### Testing
- [ ] Unit tests are written and passing
- [ ] Integration tests are written and passing
- [ ] Tests pass locally
- [ ] CI pipeline tests pass
- [ ] Test coverage > 85% for new code
- [ ] Edge cases and error scenarios tested

### Deployment
- [ ] Feature is deployed to Azure App Service
- [ ] Deployment pipeline succeeds
- [ ] Application is accessible via public URL
- [ ] Feature works in production environment
- [ ] Performance metrics acceptable

### Monitoring
- [ ] Endpoint returns expected responses
- [ ] No errors in Application Insights logs
- [ ] Custom metrics configured (if applicable)
- [ ] Performance is acceptable (<2s response time)
- [ ] Dashboard shows relevant metrics

### Documentation
- [ ] README is updated with new features
- [ ] API endpoints are documented
- [ ] Environment variables documented
- [ ] Architecture diagram updated
- [ ] Sprint documentation complete

---

## Notes and Decisions

### Key Decisions Made

1. **Forecast API Selection:** OpenWeatherMap chosen for 5-day forecast (complements Google Weather API for current conditions)
2. **Caching Strategy:** In-memory caching for weather data (5-minute TTL) to reduce API calls
3. **Performance Target:** <2s response time for weather queries, <500ms for autocomplete
4. **Test Coverage Goal:** 85% minimum coverage for all modules

### Lessons Learned from Sprint 2

✅ **Keep Doing:**
- Regular communication and standups
- Feature branches and PR reviews
- Comprehensive testing
- Documentation as we go
- Modern UI/UX design

⚠️ **Improve:**
- Earlier API integration testing
- More frequent commits
- Better time estimation
- Performance monitoring from start

### Sprint 3 Focus Areas

1. **User Value:** Complete forecast functionality and enhanced autocomplete
2. **Quality:** High test coverage and robust error handling
3. **Performance:** Fast response times and optimized API usage
4. **Monitoring:** Comprehensive dashboard for observability
5. **Documentation:** Complete and up-to-date documentation

---

## Sprint Burndown Chart

**Target Velocity:** 18 story points

| Day                | Story Points Completed | Story Points Remaining |
| ------------------ | ---------------------- | ---------------------- |
| Dec 5 (Start)      | 0                      | 18                     |
| Dec 6              | TBD                    | TBD                    |
| Dec 7              | TBD                    | TBD                    |
| Dec 8 (End/Demo)   | 13                     | 5 (3 SP carry-over)    |

---

## Success Metrics

### Sprint 3 Will Be Successful If:

1. ✅ 5-day forecast is fully functional with real API data
2. ✅ Autocomplete works smoothly with keyboard navigation
3. ✅ Application Insights dashboard shows comprehensive metrics
4. ✅ All tests passing with >85% coverage
5. ✅ API response times < 2 seconds
6. ✅ Error handling is robust and user-friendly
7. ✅ All documentation is complete and accurate
8. ✅ Application is production-ready

---

## Appendix

### Useful Resources

**APIs:**
- [OpenWeatherMap Forecast API](https://openweathermap.org/api/forecast5) - 5-day forecast
- [Google Places Autocomplete](https://developers.google.com/maps/documentation/places/web-service/autocomplete)

**Azure Documentation:**
- [Application Insights Dashboards](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-dashboards)
- [Performance Optimization](https://docs.microsoft.com/en-us/azure/app-service/overview-performance)

**Testing Resources:**
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

---

**Document Created:** December 5, 2025  
**Created By:** Kenny Tohme (Scrum Master)  
**Last Updated:** December 5, 2025

