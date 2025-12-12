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
| Product Owner         | Jack    | Prioritize backlog, define acceptance criteria, stakeholder communication |
| Scrum Master          | Salmane | Facilitate ceremonies, remove blockers, ensure Scrum process              |
| Developer 1           | Omar    | Backend development and API integration                                   |
| Developer 2           | Adrian  | Frontend development and UI/UX                                            |
| Developer 3           | Kenny   | Testing and monitoring enhancements                                       |

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

**Total Story Points:** 20

---

### User Story #201: Complete 5-Day Forecast Integration

**Priority:** 1  
**Story Points:** 5  
**Assigned To:** Developer 1 (Omar)

**Description:**  
As a user, I want to see a 5-day weather forecast, so that I can plan my activities ahead of time.

**Acceptance Criteria:**

- [ ] OpenWeatherMap API key configured in Azure App Service
- [ ] Forecast endpoint returns real data from OpenWeatherMap API
- [ ] Forecast data properly formatted and displayed in frontend
- [ ] Forecast shows daily high/low temperatures
- [ ] Forecast shows weather conditions and icons for each day
- [ ] Error handling for forecast API failures
- [ ] Forecast updates when searching for a new city

**Tasks:**

1. Configure OPENWEATHER_API_KEY in Azure App Service (0.5h)
2. Update forecast endpoint to use real OpenWeatherMap API (2h)
3. Parse and format forecast data correctly (1.5h)
4. Test forecast endpoint with various cities (1h)
5. Update frontend to handle forecast errors gracefully (1h)
6. Add unit tests for forecast service (1.5h)
7. Document forecast API usage (0.5h)

**Total Estimated Time:** 8 hours

---

### User Story #202: Enhance City Autocomplete

**Priority:** 1  
**Story Points:** 3  
**Assigned To:** Developer 1 (Omar) - Shared with Developer 2 (Adrian)

**Description:**  
As a user, I want improved city autocomplete suggestions, so that I can quickly find and select cities.

**Acceptance Criteria:**

- [ ] Autocomplete shows city and country in suggestions
- [ ] Keyboard navigation (arrow keys, enter, escape) works smoothly
- [ ] Autocomplete handles API errors gracefully
- [ ] Suggestions are limited to 10 results
- [ ] Autocomplete debouncing prevents excessive API calls
- [ ] Loading state shown during autocomplete fetch

**Tasks:**

1. Enhance autocomplete endpoint response format (1h)
2. Improve frontend autocomplete UI/UX (1.5h)
3. Add keyboard navigation improvements (1h)
4. Implement debouncing for autocomplete requests (0.5h)
5. Add error handling for autocomplete failures (0.5h)
6. Test autocomplete with various inputs (0.5h)

**Total Estimated Time:** 5 hours

---

### User Story #203: Application Insights Dashboard Enhancement

**Priority:** 2  
**Story Points:** 3  
**Assigned To:** Developer 3 (Kenny)

**Description:**  
As a developer, I want a comprehensive monitoring dashboard, so that I can track application health and performance.

**Acceptance Criteria:**

- [ ] Custom dashboard created in Azure Application Insights
- [ ] Dashboard shows weather API call metrics
- [ ] Dashboard displays error rates and response times
- [ ] Dashboard includes autocomplete usage metrics
- [ ] Alerts configured for critical errors
- [ ] Dashboard accessible to all team members

**Tasks:**

1. Create Application Insights dashboard (1.5h)
2. Add custom metrics widgets (weather searches, API calls) (1.5h)
3. Configure alerts for high error rates (1h)
4. Add performance metrics (response times) (1h)
5. Document dashboard setup and usage (0.5h)
6. Share dashboard access with team (0.5h)

**Total Estimated Time:** 6 hours

---

### User Story #204: Performance Optimization

**Priority:** 2  
**Story Points:** 3  
**Assigned To:** Developer 1 (Omar)

**Description:**  
As a user, I want fast response times, so that I can get weather information quickly.

**Acceptance Criteria:**

- [ ] API response times < 2 seconds for weather queries
- [ ] Autocomplete response times < 500ms
- [ ] Frontend loading states optimized
- [ ] API calls are cached where appropriate
- [ ] Rate limiting implemented to prevent abuse
- [ ] Performance metrics tracked in Application Insights

**Tasks:**

1. Analyze current performance bottlenecks (1h)
2. Implement response caching for weather data (2h)
3. Optimize API calls (parallel requests where possible) (1h)
4. Add rate limiting to prevent abuse (1h)
5. Monitor performance improvements (0.5h)
6. Document performance optimizations (0.5h)

**Total Estimated Time:** 6 hours

---

### User Story #205: Enhanced Error Handling and Resilience

**Priority:** 2  
**Story Points:** 3  
**Assigned To:** Developer 1 (Omar) - Shared with Developer 3 (Kenny)

**Description:**  
As a user, I want reliable error handling, so that I understand what went wrong and can retry when appropriate.

**Acceptance Criteria:**

- [ ] Retry logic for transient API failures
- [ ] Clear error messages for different error types
- [ ] Graceful degradation when APIs are unavailable
- [ ] Error logging to Application Insights
- [ ] User-friendly error messages in frontend
- [ ] Retry button functionality works correctly

**Tasks:**

1. Implement retry logic with exponential backoff (2h)
2. Improve error messages for different scenarios (1h)
3. Add graceful degradation for API failures (1.5h)
4. Enhance error logging with context (1h)
5. Update frontend error handling (1h)
6. Test error scenarios thoroughly (1h)

**Total Estimated Time:** 7.5 hours

---

### User Story #206: Test Coverage and Quality Assurance

**Priority:** 2  
**Story Points:** 3  
**Assigned To:** Developer 3 (Kenny)

**Description:**  
As a developer, I want comprehensive test coverage, so that I can ensure code quality and catch bugs early.

**Acceptance Criteria:**

- [ ] Test coverage > 85% for all modules
- [ ] Integration tests for all API endpoints
- [ ] Edge cases and error scenarios tested
- [ ] Async tests properly configured and passing
- [ ] Test coverage report generated in CI pipeline
- [ ] All tests passing in CI/CD pipeline

**Tasks:**

1. Fix async test configuration issues (1.5h)
2. Add integration tests for forecast endpoint (1.5h)
3. Add tests for autocomplete edge cases (1h)
4. Add tests for error handling scenarios (1.5h)
5. Generate and review coverage report (0.5h)
6. Update CI pipeline with coverage reporting (1h)

**Total Estimated Time:** 7 hours

---

### User Story #207: Documentation and Architecture Updates

**Priority:** 3  
**Story Points:** 2  
**Assigned To:** Scrum Master (Salmane)

**Description:**  
As a team member, I want up-to-date documentation, so that I can understand the system architecture and contribute effectively.

**Acceptance Criteria:**

- [ ] Architecture diagram updated with all components
- [ ] API documentation complete
- [ ] README updated with all features
- [ ] Deployment guide updated
- [ ] Sprint 3 documentation complete

**Tasks:**

1. Update architecture diagram (1.5h)
2. Update README with Sprint 3 features (1h)
3. Document API endpoints and usage (1h)
4. Update deployment documentation (0.5h)
5. Create Sprint 3 retrospective (1h)

**Total Estimated Time:** 5 hours

---

## Sprint Backlog Summary

| User Story                              | Story Points | Status      | Assignee |
| --------------------------------------- | ------------ | ----------- | -------- |
| Complete 5-Day Forecast Integration      | 5            | Not Started | Omar     |
| Enhance City Autocomplete                | 3            | Not Started | Omar/Adrian |
| Application Insights Dashboard           | 3            | Not Started | Kenny    |
| Performance Optimization                 | 3            | Not Started | Omar     |
| Enhanced Error Handling                 | 3            | Not Started | Omar/Kenny |
| Test Coverage and QA                    | 3            | Not Started | Kenny    |
| Documentation Updates                   | 2            | Not Started | Salmane  |
| **TOTAL**                               | **22**       | **0/22 Done** |        |

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
  - User stories selected and estimated (22 story points total)
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

## Branch Strategy

### Git Workflow (Continued from Sprint 2)

- **Main Branch:** Always deployable, protected
- **Feature Branches:** Created for each developer's work
  - `feature/forecast-integration` (Omar)
  - `feature/autocomplete-enhancement` (Omar/Adrian)
  - `feature/monitoring-dashboard` (Kenny)
  - `feature/performance-optimization` (Omar)
  - `feature/error-handling` (Omar/Kenny)
  - `feature/test-coverage` (Kenny)
  - `feature/sprint3-docs` (Salmane)
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

**Target Velocity:** 22 story points

| Day                | Story Points Completed | Story Points Remaining |
| ------------------ | ---------------------- | ---------------------- |
| Dec 5 (Start)      | 0                      | 22                     |
| Dec 6              | TBD                    | TBD                    |
| Dec 7              | TBD                    | TBD                    |
| Dec 8 (End/Demo)   | TBD                    | 0 (Goal)               |

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
**Created By:** Salmane Mouhib (Scrum Master)  
**Last Updated:** December 5, 2025

