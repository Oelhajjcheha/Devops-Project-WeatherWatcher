# CI/CD Pipeline Documentation

**Project:** Weather Watcher  
**Platform:** Azure Pipelines (Azure DevOps)  
**Created:** Sprint 1  
**Last Updated:** December 1, 2025

---

## 📋 Overview

The Weather Watcher project uses **Azure Pipelines** for continuous integration and continuous deployment (CI/CD). The pipeline automatically builds, tests, and deploys the application to Azure App Service whenever code is pushed to the `main` branch.

---

## 🏗️ Pipeline Architecture

### Pipeline File
**Location:** `azure-pipeline.yml` (root directory)  
**Type:** YAML-based pipeline  
**Trigger:** Commits to `main` branch

### Pipeline Stages

```
┌─────────────────────────────────────────────────────────────┐
│                    TRIGGER                                  │
│  Push to 'main' branch or Pull Request merge               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 1: CHECKOUT & SETUP                                  │
│  ├─ Checkout source code                                    │
│  ├─ Use Python 3.11                                         │
│  └─ Set up environment                                      │
│  Duration: ~30 seconds                                      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 2: BUILD                                             │
│  ├─ Upgrade pip                                             │
│  ├─ Install dependencies (requirements.txt)                 │
│  └─ Verify installation                                     │
│  Duration: ~1-2 minutes                                     │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 3: TEST                                              │
│  ├─ Run pytest                                              │
│  ├─ Generate test reports                                   │
│  └─ Validate test results                                   │
│  ❌ If tests fail → STOP PIPELINE                          │
│  ✅ If tests pass → Continue                               │
│  Duration: ~30 seconds                                      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 4: PACKAGE                                           │
│  ├─ Archive files to ZIP                                    │
│  ├─ Create deployment artifact                              │
│  └─ Publish artifact (drop.zip)                             │
│  Duration: ~30 seconds                                      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 5: DEPLOY                                            │
│  ├─ Connect to Azure (Service Connection)                   │
│  ├─ Deploy to App Service                                   │
│  ├─ Extract and run deployment package                      │
│  └─ Verify deployment success                               │
│  Duration: ~2-3 minutes                                     │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              DEPLOYMENT COMPLETE                            │
│  ✅ Application live at:                                    │
│  https://weather-watcher-4b2025.azurewebsites.net          │
└─────────────────────────────────────────────────────────────┘
```

**Total Pipeline Duration:** ~5-7 minutes

---

## 📄 Pipeline Configuration

### Complete `azure-pipeline.yml`

```yaml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - checkout: self

  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.11'
    displayName: 'Use Python 3.11'

  - script: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt
    displayName: 'Install dependencies'

  - script: |
      pytest --maxfail=1 --disable-warnings -q
    displayName: 'Run automated tests'

  - task: ArchiveFiles@2
    inputs:
      rootFolderOrFile: '$(System.DefaultWorkingDirectory)'
      includeRootFolder: false
      archiveType: 'zip'
      archiveFile: '$(Build.ArtifactStagingDirectory)/drop.zip'
      replaceExistingArchive: true
    displayName: 'Create ZIP for deployment'

  - task: PublishBuildArtifacts@1
    inputs:
      PathtoPublish: '$(Build.ArtifactStagingDirectory)/drop.zip'
      ArtifactName: 'drop'
    displayName: 'Publish artifact'

  - task: AzureWebApp@1
    inputs:
      azureSubscription: 'WeatherWatcherServiceConnection'
      appName: 'weather-watcher-4B2025'
      package: '$(Build.ArtifactStagingDirectory)/drop.zip'
    displayName: 'Deploy to Azure App Service'
```

---

## 🔧 Configuration Details

### Trigger Configuration

```yaml
trigger:
  branches:
    include:
      - main
```

**Behavior:**
- Pipeline runs automatically on push to `main` branch
- Does NOT run on feature branches
- Pull requests must be merged to `main` to trigger deployment

**Rationale:** Ensures only reviewed and approved code is deployed to production.

---

### Build Agent

```yaml
pool:
  vmImage: 'ubuntu-latest'
```

**Specifications:**
- **OS:** Ubuntu Linux (latest version)
- **Hosted by:** Microsoft Azure
- **Cost:** Free tier (1,800 minutes/month for private repos)
- **Python Support:** Pre-installed with multiple versions

---

### Python Setup

```yaml
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'
  displayName: 'Use Python 3.11'
```

**Details:**
- Ensures Python 3.11 is used (matches production runtime)
- Sets Python 3.11 as the active version in PATH
- Compatible with FastAPI and all dependencies

---

### Dependency Installation

```yaml
- script: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
  displayName: 'Install dependencies'
```

**Dependencies Installed:**
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- pytest==7.4.3
- httpx==0.25.2
- python-dotenv==1.0.0
- gunicorn==21.2.0

**Note:** Sprint 2 will add weather API client libraries and Application Insights SDK.

---

### Testing Stage

```yaml
- script: |
    pytest --maxfail=1 --disable-warnings -q
  displayName: 'Run automated tests'
```

**Pytest Options:**
- `--maxfail=1`: Stop after first test failure (fail fast)
- `--disable-warnings`: Suppress warning messages
- `-q`: Quiet mode (concise output)

**Failure Behavior:**
- If ANY test fails → Pipeline stops
- Deployment is blocked
- Developer notified via Azure DevOps

**Success Behavior:**
- All tests pass → Continue to packaging
- Green checkmark in Azure DevOps

---

### Packaging Stage

```yaml
- task: ArchiveFiles@2
  inputs:
    rootFolderOrFile: '$(System.DefaultWorkingDirectory)'
    includeRootFolder: false
    archiveType: 'zip'
    archiveFile: '$(Build.ArtifactStagingDirectory)/drop.zip'
    replaceExistingArchive: true
  displayName: 'Create ZIP for deployment'
```

**What Gets Packaged:**
- Application code (`app/` folder)
- Tests (`tests/` folder)
- Documentation (`docs/` folder)
- Configuration files (`requirements.txt`, etc.)
- Pipeline file (`azure-pipeline.yml`)

**Excluded:**
- `.git` folder
- `__pycache__` folders
- `.pyc` files
- Virtual environments

---

### Artifact Publishing

```yaml
- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)/drop.zip'
    ArtifactName: 'drop'
  displayName: 'Publish artifact'
```

**Purpose:**
- Makes build artifact available for deployment
- Stores artifact in Azure DevOps for 30 days
- Enables manual re-deployment if needed
- Provides audit trail

---

### Deployment Stage

```yaml
- task: AzureWebApp@1
  inputs:
    azureSubscription: 'WeatherWatcherServiceConnection'
    appName: 'weather-watcher-4B2025'
    package: '$(Build.ArtifactStagingDirectory)/drop.zip'
  displayName: 'Deploy to Azure App Service'
```

**Service Connection:** `WeatherWatcherServiceConnection`
- Type: Azure Resource Manager
- Scope: Subscription-level access
- Authentication: Service Principal
- Configured in: Azure DevOps Project Settings

**Deployment Target:**
- **App Service:** weather-watcher-4B2025
- **Resource Group:** BCSAI2025-DEVOPS-STUDENT-4B
- **Region:** North Europe
- **Runtime:** Python 3.11

**Deployment Process:**
1. Connect to Azure using service principal
2. Upload ZIP package to App Service
3. Extract package on App Service
4. Run build process (SCM_DO_BUILD_DURING_DEPLOYMENT=true)
5. Install dependencies in production
6. Restart application
7. Verify deployment health

---

## 🔐 Security & Credentials

### Service Connection Setup

**Created in:** Azure DevOps → Project Settings → Service Connections

**Name:** WeatherWatcherServiceConnection

**Type:** Azure Resource Manager

**Authentication Method:** Service Principal (automatic)

**Permissions:**
- Contributor access to Resource Group `BCSAI2025-DEVOPS-STUDENT-4B`
- Deploy to App Service
- Read/Write App Service configuration

**Security:**
- Service principal credentials stored securely in Azure DevOps
- NOT visible in pipeline YAML
- Rotated automatically by Azure

---

## 📊 Pipeline Monitoring

### Viewing Pipeline Runs

**Location:** Azure DevOps → Pipelines → Runs

**Information Available:**
- Run status (Success/Failed/In Progress)
- Duration of each stage
- Test results
- Deployment logs
- Artifact downloads

### Pipeline Status Badge

Add to README.md:
```markdown
[![Build Status](https://dev.azure.com/.../badge)](https://dev.azure.com/...)
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### Issue: Tests Fail in Pipeline but Pass Locally

**Cause:** Different Python version or missing dependencies

**Solution:**
```bash
# Ensure local Python matches pipeline
python --version  # Should be 3.11.x

# Test with same flags as pipeline
pytest --maxfail=1 --disable-warnings -q
```

---

#### Issue: Deployment Fails with "Package Not Found"

**Cause:** Artifact not published correctly

**Solution:**
- Check ArchiveFiles task completed successfully
- Verify artifact appears in pipeline run artifacts
- Check file paths in YAML (case-sensitive)

---

#### Issue: Application Not Starting After Deployment

**Cause:** Missing environment variables or build configuration

**Solution:**
```bash
# Check App Service configuration
az webapp config appsettings list \
  --name weather-watcher-4B2025 \
  --resource-group BCSAI2025-DEVOPS-STUDENT-4B

# Ensure SCM_DO_BUILD_DURING_DEPLOYMENT is set
az webapp config appsettings set \
  --name weather-watcher-4B2025 \
  --resource-group BCSAI2025-DEVOPS-STUDENT-4B \
  --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true

# View deployment logs
az webapp log tail \
  --name weather-watcher-4B2025 \
  --resource-group BCSAI2025-DEVOPS-STUDENT-4B
```

---

#### Issue: Pipeline Takes Too Long

**Current Duration:** 5-7 minutes (acceptable)

**If Exceeding 10 Minutes:**
- Check for large dependency installations
- Review test execution time
- Consider caching dependencies (future optimization)

---

## 🚀 Best Practices

### ✅ Do's

1. **Always run tests locally before pushing**
   ```bash
   pytest tests/ -v
   ```

2. **Use feature branches for development**
   ```bash
   git checkout -b feature/my-feature
   ```

3. **Keep pipeline YAML in version control**
   - Treat `azure-pipeline.yml` as code
   - Review changes in PRs

4. **Monitor pipeline failures immediately**
   - Set up Azure DevOps notifications
   - Fix broken builds ASAP

5. **Add tests for new features**
   - Maintain high test coverage
   - Tests are deployment gatekeepers

### ❌ Don'ts

1. **Don't push directly to main**
   - Use PRs for all changes
   - Requires at least 1 reviewer

2. **Don't skip tests**
   - Never disable pytest in pipeline
   - Tests protect production

3. **Don't commit secrets**
   - Use Azure App Service settings
   - Never hardcode API keys

4. **Don't ignore pipeline failures**
   - Failed pipeline = broken deployment
   - Fix or rollback immediately

---

## 📈 Pipeline Metrics

### Sprint 1 Performance

| Metric | Value |
|--------|-------|
| Average Duration | 5-7 minutes |
| Success Rate | 100% |
| Deployments | ~10 |
| Failed Tests Caught | 0 |
| Deployment Frequency | On-demand (PR merge) |

### Sprint 2 Goals

- Maintain <10 minute pipeline duration
- Add test coverage reporting
- Implement automatic rollback on failure
- Add staging slot deployment (if time permits)

---

## 🔄 Future Enhancements

### Planned Improvements (Sprint 3+)

1. **Multi-Stage Pipeline**
   ```yaml
   stages:
     - stage: Build
     - stage: Test
     - stage: DeployDev
     - stage: DeployProd
   ```

2. **Test Coverage Reporting**
   ```yaml
   - script: pytest --cov=app --cov-report=xml
   - task: PublishCodeCoverageResults@1
   ```

3. **Deployment Slots**
   - Deploy to staging slot first
   - Swap to production after validation
   - Zero-downtime deployments

4. **Dependency Caching**
   - Cache pip packages
   - Reduce build time

5. **Performance Testing**
   - Add load tests to pipeline
   - Monitor response times

---

## 📚 References

### Official Documentation

- [Azure Pipelines Documentation](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
- [Azure App Service Deployment](https://docs.microsoft.com/en-us/azure/app-service/deploy-continuous-deployment)
- [YAML Schema Reference](https://docs.microsoft.com/en-us/azure/devops/pipelines/yaml-schema)

### Team Resources

- [Sprint 1 Planning](sprint1-planning.md)
- [Sprint 2 Planning](sprint2-planning.md)
- [Definition of Done](definition-of-done.md)

---

## 📞 Support

**Pipeline Issues:** Contact Omar (Developer 1 - CI/CD Lead)  
**Azure Issues:** Contact Jack (Product Owner / Infrastructure)  
**General Questions:** Contact Salmane (Scrum Master)

---

**Document Created:** December 1, 2025  
**Author:** Salmane Mouhib (Scrum Master)  
**Last Updated:** December 1, 2025  
**Version:** 1.0

---

**Status:** ✅ Pipeline Operational and Documented
