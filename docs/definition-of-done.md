markdown# Definition of Done

A Product Backlog item is considered *DONE* when:

## Code Quality
- [ ] Code is written and follows team coding standards
- [ ] Code is reviewed by at least one team member
- [ ] No critical code smells or security issues

## Testing
- [ ] Unit tests are written and passing
- [ ] Tests pass locally
- [ ] CI pipeline tests pass
- [ ] Test coverage > 60%

## Deployment
- [ ] Feature is deployed to Azure App Service
- [ ] Deployment pipeline succeeds
- [ ] Application is accessible via public URL

## Monitoring
- [ ] Endpoint returns expected responses
- [ ] No errors in Application Insights logs
- [ ] Monitoring dashboard shows healthy status

## Documentation
- [ ] README is updated if needed
- [ ] API endpoints are documented
- [ ] Code has necessary comments

*If an item does NOT meet all criteria, it returns to the Product Backlog.*