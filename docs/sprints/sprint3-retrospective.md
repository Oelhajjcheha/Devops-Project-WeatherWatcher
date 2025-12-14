# Sprint 3 Retrospective

**Sprint Number:** Sprint 3  
**Sprint Duration:** December 5 - December 8, 2025  
**Retrospective Date:** December 8, 2025  
**Facilitator:** Kenny Tohme (Scrum Master)  
**Attendees:** Full Development Team

---

## Sprint 3 Overview

### Sprint Goal
Enhance Weather Watcher with advanced features, improve performance and reliability, and polish the user experience to deliver a production-ready application.

### Sprint Outcomes

**Completed User Stories:**
- [x] 5-Day Weather Forecast (5 SP) ✅ Closed
- [x] Full Country Names Display (3 SP) ✅ Closed
- [x] City Autocomplete & Search Improvements (5 SP) ✅ Closed
- [ ] Loading States & UI Polish (3 SP) 📋 New (Not Started)
- [ ] Sprint 3 Documentation (2 SP) 🔄 Active (In Progress)

**Total Story Points:**
- **Committed:** 18
- **Completed:** 13 (3 stories closed)
- **In Progress:** 2 (1 story active)
- **Not Started:** 3 (1 story new)
- **Velocity:** 13 story points completed (72% completion rate)

**Key Metrics:**
- Test Coverage: ~75% (maintained from Sprint 2)
- Pipeline Success Rate: 100%
- Deployment Frequency: As needed during sprint
- Application Uptime: 99%+
- Average API Response Time: ~2.0 seconds

---

## Retrospective Format: Start-Stop-Continue

### 🟢 What Went Well (Continue)

**Things the team did well that we should keep doing:**

1. **Excellent individual contributions**
   - Jack completed two major stories (Forecast and Autocomplete) effectively
   - Salmane delivered country names feature cleanly
   - Good focus on core functionality

2. **Comprehensive documentation as we developed**
   - Kenny maintained documentation throughout the sprint
   - Architecture diagram created with Mermaid
   - Product backlog created and organized

3. **Effective use of feature branches and pull requests**
   - All code changes went through proper review process
   - No merge conflicts or deployment issues
   - Clean git history

4. **Good prioritization decisions**
   - Team focused on core functionality over polish
   - Completed critical features that add user value
   - Made smart trade-offs when time was limited 

---

### 🔴 What Didn't Go Well (Stop)

**Things that didn't work and we should stop doing:**

1. **Not starting Loading States story**
   - Story was planned but not started
   - Could have been partially completed if started earlier
   - Should prioritize story start times better

2. **Documentation not completed by sprint end**
   - Retrospective still in progress
   - Should allocate more time for documentation tasks
   - Documentation is important for project completion 

---

### 🟡 What to Start Doing (Start)

**New practices or improvements we should implement:**

1. **Start all planned stories earlier in sprint**
   - Don't leave stories unstarted
   - Even partial progress is better than none
   - Better time management and story distribution

2. **Allocate dedicated time for documentation**
   - Don't treat documentation as "when I have time"
   - Schedule documentation tasks like code tasks
   - Complete documentation before sprint end

3. **Regular Azure DevOps Boards updates**
   - Update work items during daily standups
   - Keep burndown charts accurate
   - Better visibility for stakeholders

4. **Better story time estimation**
   - Some stories took longer than expected
   - Improve estimation accuracy
   - Build in buffer time for unknowns 

---

## Detailed Discussion Points

### Technical Achievements

**What technical wins did we have this sprint?**

- Successfully implemented 5-day weather forecast functionality
- Created comprehensive country code to name mapping
- Enhanced autocomplete with Google Places API integration
- Improved user experience with full country names
- Created Mermaid architecture diagram for documentation

**What technical challenges did we overcome?**

- Integrating forecast endpoint with existing weather service
- Creating comprehensive country code mapping dictionary
- Implementing autocomplete with proper error handling
- Designing forecast UI layout that works on all devices
- Coordinating frontend and backend for seamless integration 

---

### Process Improvements

**How well did our Scrum process work?**

- Daily Standups: [Effective]
  - Notes: Standups were concise and focused. Team members were well-prepared. Could improve by updating Azure DevOps Boards during standups.

- Sprint Planning: [Effective]
  - Notes: Planning session was thorough. All user stories well-defined with clear acceptance criteria. Story point estimation was accurate.

- Code Reviews: [Effective]
  - Notes: All PRs received timely reviews. Good feedback provided. Could start reviews earlier in sprint rather than end.

- Documentation: [Effective]
  - Notes: Documentation maintained throughout sprint. Architecture diagram updated. Product backlog created. Excellent work by Kenny. 

---

### Team Collaboration

**How well did we collaborate as a team?**

- Communication: [Excellent]
  - Notes: Team communicated effectively via Teams/Discord. Quick responses to questions. Good coordination between developers.

- Knowledge Sharing: [Good]
  - Notes: Team shared knowledge during code reviews and standups. Could improve by documenting API integration learnings earlier.

- Support and Helping: [Excellent]
  - Notes: Team members helped each other when blockers arose. Jack and Salmane collaborated well on error handling. Great team spirit. 

---

### Blockers and Impediments

**What blockers did we face?**

| Blocker | Impact | How Resolved | Prevention Strategy |
| ------- | ------ | ------------ | ------------------- |
| OpenWeatherMap API key not configured initially | Medium | Configured during sprint, delayed testing | Set up all API keys during sprint planning |
| Async test configuration issues | Low | Fixed pytest-asyncio setup | Document async testing setup in project docs |
| Performance baseline not established early | Low | Measured mid-sprint, still achieved targets | Establish performance baselines at sprint start |

---

### Sprint Goal Achievement

**Did we achieve our Sprint Goal?**
- [x] Partially

**Explanation:**
We successfully completed 3 out of 5 user stories (5-Day Forecast, Country Names Display, and Autocomplete improvements). The core weather functionality is enhanced and working well. However, Loading States & UI Polish was not started, and Sprint 3 Documentation is still in progress. The application is functional and improved, but some polish features remain for future sprints.

**What helped us succeed?**
- Strong team collaboration and communication
- Clear sprint planning with well-defined user stories
- Effective use of feature branches and code reviews
- Focus on core functionality over polish
- Good prioritization of critical features

**What prevented us from succeeding?**
- Time constraints prevented starting Loading States story
- Documentation still in progress (retrospective being completed)
- Some stories took longer than estimated 

---

## User Story Completion Review

### Story #1: 5-Day Weather Forecast

**Status:** ✅ Closed

**Notes:**
- Successfully added forecast endpoint to weather service
- Created /api/forecast API endpoint
- Designed and implemented forecast UI layout
- Forecast display logic working correctly
- Forecast cards styled and responsive
- Forecast functionality tested and verified

**Challenges:**
- Integrating forecast data with existing weather service
- Designing UI layout for 5-day forecast display
- Ensuring forecast updates when searching for new city

**Lessons Learned:**
- Forecast endpoint integration requires careful service design
- UI layout planning saves time during implementation
- Testing forecast with various cities ensures reliability 

---

### Story #2: Full Country Names Display

**Status:** ✅ Closed

**Notes:**
- Created comprehensive country code mapping dictionary
- Implemented country name conversion function
- Updated weather API responses to include full country names
- Country name display tested and working correctly

**Challenges:**
- Creating comprehensive country code mapping
- Ensuring conversion function handles all edge cases
- Updating API responses without breaking existing functionality

**Lessons Learned:**
- Country code mapping improves user experience
- Conversion functions need to handle edge cases
- Testing with various countries ensures reliability 

---

### Story #3: City Autocomplete & Search Improvements

**Status:** ✅ Closed

**Notes:**
- Researched and chose appropriate autocomplete approach
- Implemented autocomplete API endpoint
- Added autocomplete JavaScript logic with keyboard navigation
- Styled autocomplete dropdown with smooth animations
- Added loading and error states
- Autocomplete functionality tested thoroughly

**Challenges:**
- Choosing the right autocomplete approach (Google Places API)
- Implementing smooth keyboard navigation
- Handling API errors gracefully
- Optimizing autocomplete performance

**Lessons Learned:**
- Research phase is important for choosing the right solution
- Keyboard navigation significantly improves UX
- Loading and error states make features feel polished
- Autocomplete debouncing prevents excessive API calls 

---

### Story #4: Loading States & UI Polish

**Status:** 📋 New (Not Started)

**Notes:**
- Story was planned but not started in Sprint 3
- Will be carried over to future sprint
- Includes loading spinner, skeleton screens, animations, and improved error messages

**Challenges:**
- Story not started due to time constraints
- Other higher priority stories took precedence

**Lessons Learned:**
- Prioritization is important when time is limited
- UI polish can be deferred if core functionality is working
- Loading states improve perceived performance 

---

### Story #5: Sprint 3 Documentation

**Status:** 🔄 Active (In Progress)

**Notes:**
- Sprint 3 Planning Document created ✅
- README updated with new features ✅
- Architecture diagram created/updated ✅
- Sprint 3 retrospective in progress 🔄

**Challenges:**
- Keeping documentation current with rapid development
- Creating comprehensive architecture diagram
- Organizing all documentation effectively

**Lessons Learned:**
- Documentation should be maintained throughout sprint
- Architecture diagrams help visualize system components
- Product backlog helps track all work across sprints 

---


---


---

## Action Items for Future Sprints

**Specific, measurable actions the team commits to:**

| Action Item | Assigned To | Priority | Due Date | Success Criteria |
| ----------- | ----------- | -------- | -------- | ---------------- |
| 1. Complete Loading States & UI Polish story | Adrian | High | Next Sprint | Loading states implemented and tested |
| 2. Finish Sprint 3 Documentation | Kenny | High | End of Sprint 3 | Retrospective completed and shared |
| 3. Start all planned stories early in sprint | All Developers | High | Next Sprint | All stories started by day 2 |
| 4. Allocate dedicated time for documentation | Scrum Master | Medium | Next Sprint | Documentation tasks scheduled like code tasks |
| 5. Update Azure DevOps Boards daily | All Developers | Medium | Next Sprint | Boards updated during standups |

---

## Lessons Learned

### Technical Lessons

1. **Lesson: Forecast Data Integration Requires Careful Planning**
   - **Context:** Integrating forecast endpoint with existing weather service required careful design
   - **Impact:** Successful integration but took time to get right
   - **Application for Future:** Plan service integration points early, design APIs carefully

2. **Lesson: Country Code Mapping Improves UX**
   - **Context:** Converting country codes to full names makes information more readable
   - **Impact:** Users see "United Kingdom" instead of "GB" - much better UX
   - **Application for Future:** Always consider user-facing data formatting 

---

### Process Lessons

1. **Lesson: Start Stories Early in Sprint**
   - **Context:** Loading States story was not started, leaving work incomplete
   - **Impact:** Story carries over to next sprint, incomplete sprint
   - **Application for Future:** Start all planned stories, even if partially, early in sprint

2. **Lesson: Documentation Needs Dedicated Time**
   - **Context:** Documentation tasks were treated as secondary
   - **Impact:** Retrospective still in progress at sprint end
   - **Application for Future:** Schedule documentation like code tasks, allocate dedicated time 

---

## Team Morale and Satisfaction

**Anonymous Team Happiness Metric (1-5 scale):**

| Team Member | Happiness Score | Comments |
| ----------- | --------------- | -------- |
| Omar (PO)   | ⭐⭐⭐⭐⭐ (5/5) |          |
| Kenny (SM)  | ⭐⭐⭐⭐⭐ (5/5) |          |
| Jack        | ⭐⭐⭐⭐⭐ (5/5) |          |
| Adrian      | ⭐⭐⭐⭐⭐ (5/5) |          |
| Salmane     | ⭐⭐⭐⭐⭐ (5/5) |          |

**Average Team Happiness:** 4.4/5

---

## Recognition and Appreciation

**Shout-outs to team members for exceptional contributions:**

- **Jack:** For completing two major stories (5-Day Forecast and Autocomplete improvements) - excellent backend and frontend work
- **Salmane:** For implementing full country names display feature - improved user experience
- **Kenny (SM):** For maintaining documentation and creating comprehensive project documentation
- **Omar (PO):** For clear prioritization and stakeholder communication
- **Adrian:** For being ready to work on Loading States (story planned for next sprint)

---

## Sprint Comparison

### Sprint 1 vs Sprint 2 vs Sprint 3 Comparison

| Metric                  | Sprint 1 | Sprint 2 | Sprint 3 | Trend     |
| ----------------------- | -------- | -------- | -------- | --------- |
| Story Points Completed  | ~14      | ~18      | 13       | ➡️ Stable |
| Velocity                | 14       | 18       | 13       | ➡️ Stable |
| Test Coverage           | ~60%     | ~75%     | ~75%     | ➡️ Stable |
| Bugs Found              | 0        | 2        | 0        | 📈 Improving |
| Deployment Success Rate | 100%     | 100%     | 100%     | ➡️ Stable |
| Team Satisfaction       | 4.5/5    | 4.2/5    | 4.4/5    | ➡️ Stable |
| API Response Time       | N/A      | ~2.5s    | ~2.0s    | 📈 Improving |

**Trend Legend:** 📈 Improving | ➡️ Stable | 📉 Declining

---

## Performance Metrics

### API Performance

| Endpoint | Target | Sprint 2 | Sprint 3 | Status |
| -------- | ------ | -------- | -------- | ------ |
| /api/weather | <2s | ~2.5s | ~2.0s | ✅ Met Target |
| /api/forecast | <2s | N/A | ~2.0s | ✅ Met Target |
| /api/cities/autocomplete | <500ms | ~400ms | ~400ms | ✅ Met Target |

### Test Coverage

| Module | Sprint 2 | Sprint 3 | Target | Status |
| ------ | -------- | -------- | ------ | ------ |
| app/main.py | ~70% | ~75% | >70% | ✅ Maintained |
| app/services/weather_service.py | ~80% | ~80% | >75% | ✅ Maintained |
| Overall | ~75% | ~75% | >70% | ➡️ Stable |

---

## Looking Ahead

### Carry-Over Items

**What didn't we complete that needs to move to future sprints?**

- [ ] Loading States & UI Polish (3 SP) - Not started, will be prioritized in next sprint
- [ ] Complete Sprint 3 Documentation (retrospective in progress)

### Future Sprint Priorities

**Based on this retrospective, what should we prioritize next?**

1. Complete Loading States & UI Polish (carry-over from Sprint 3)
2. Finalize Sprint 3 Documentation (complete retrospective)
3. Continue improving test coverage and code quality 

### Future Sprint Capacity

**Expected team capacity for future sprints:**
- Team Size: 5 members
- Sprint Duration: 3-4 days (based on project timeline)
- Planned Velocity: 13-15 story points (based on Sprint 3 velocity of 13)

---

## Final Thoughts

### Scrum Master Observations

Sprint 3 was successful with 3 out of 5 user stories completed (72% completion rate). The team demonstrated excellent collaboration, with Jack completing two major stories (Forecast and Autocomplete) and Salmane completing the Country Names feature. The core functionality is working well. Loading States & UI Polish was not started due to time constraints, and documentation is still in progress. The team prioritized core features over polish, which was the right decision. Overall, good progress on critical features.

### Product Owner Feedback

The three completed user stories (5-Day Forecast, Country Names Display, and Autocomplete) add significant value to users. The application is more functional and user-friendly. While Loading States & UI Polish would improve the user experience, the core features are working well. The application meets MVP requirements. Documentation completion is important and should be finished soon.

### Team Summary

The team is satisfied with Sprint 3 outcomes. We completed the most critical features (forecast, country names, autocomplete) which directly improve user experience. Communication was good, and collaboration was effective. The team made good prioritization decisions, focusing on core functionality. Loading States can be addressed in a future sprint. Documentation is nearly complete.



---

## Appendix: Retrospective Activities Used

**Activity Format:** Start-Stop-Continue

**Other Activities Considered:**
- Mad-Sad-Glad
- Sailboat Retrospective
- 4 Ls (Liked, Learned, Lacked, Longed For)
- Timeline Retrospective

**Why We Chose Start-Stop-Continue:**
Simple, action-oriented format that's easy for all team members to contribute to and results in clear action items.

---

## Sprint 3 Achievements Summary

### Features Delivered

- [x] 5-day forecast fully functional ✅
- [x] Full country names display implemented ✅
- [x] City autocomplete & search improvements completed ✅
- [ ] Loading states & UI polish (not started) 📋
- [ ] Sprint 3 documentation (in progress) 🔄

### Technical Debt Addressed

- [x] Country name conversion implemented ✅
- [x] Autocomplete functionality enhanced ✅
- [x] Forecast integration completed ✅

### Technical Debt Created

- [ ] Loading States & UI Polish story not started (carry-over to next sprint)
- [ ] Sprint 3 Documentation still in progress (retrospective being completed) 

---

**Document Created:** December 5, 2025  
**Retrospective Date:** December 8, 2025  
**Facilitator:** Kenny Tohme (Scrum Master)  
**Status:** ✅ Completed

---

## How to Use This Template

**Before the Retrospective:**
1. Review Sprint 3 metrics and outcomes
2. Gather data on completed stories, velocity, and quality metrics
3. Identify any known issues or wins to seed discussion
4. Review Sprint 3 planning document for committed items

**During the Retrospective:**
1. Set the stage (5 min) - Remind team of sprint goal
2. Gather data (10 min) - Fill in metrics and outcomes
3. Generate insights (15 min) - Discuss Start-Stop-Continue
4. Decide what to do (10 min) - Create action items
5. Close (5 min) - Thank team and confirm next steps

**After the Retrospective:**
1. Share completed retrospective with team
2. Add action items to future sprint backlog
3. Track action items in Daily Scrums
4. Review action items in next retrospective

