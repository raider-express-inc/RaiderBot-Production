# Devin Handoff: Deployment Fix Plan

This repository contains several security and configuration issues that must be resolved before RaiderBot can be safely deployed. The following checklist summarises the critical fixes applied and outstanding tasks.

## Credentials Cleanup
- Removed hard coded Snowflake credentials from `server.py`, `http_server.py` and `test_before_deploy.py`.
- Updated `DEPLOYMENT_GUIDE.md` to use placeholder values instead of real credentials.
- Tests and server startup now validate that required Snowflake environment variables are set.

## Remaining Steps for Deployment
1. **Verify Palantir SDK and CLI Availability**
   - Install `palantir-foundry-sdk` and `foundry-cli` if available for your environment.
   - Configure `~/.foundry/config.json` and authenticate with `foundry-cli login`.

2. **Set Environment Variables Securely**
   - Export the following variables for both local runs and deployment:
     - `SNOWFLAKE_ACCOUNT`
     - `SNOWFLAKE_USER`
     - `SNOWFLAKE_PASSWORD`
     - `SNOWFLAKE_WAREHOUSE`
     - `SNOWFLAKE_DATABASE`
     - `SNOWFLAKE_SCHEMA`
     - `FOUNDRY_URL`, `FOUNDRY_CLIENT_ID`, `FOUNDRY_CLIENT_SECRET` or `FOUNDRY_AUTH_TOKEN`

3. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Run Tests**
   ```bash
   python run_comprehensive_tests.py
   ```
   Ensure all tests pass before attempting deployment.

5. **Review GitHub Security Settings**
   - Verify the repository is private and that branch protection rules are in place.
   - Configure secret scanning and Dependabot alerts.
   - Remove any leftover secrets from commit history if necessary.

6. **Deployment**
   - Use the provided deployment scripts under `deployment/` or `foundry_setup.sh` once authentication is configured.

This document can be provided to Devin as a concise summary of the current state and the steps required to finalise deployment.
