# Visual Studio Setup for RaiderBot-Production

## Prerequisites
- Visual Studio 2022 with Python Development workload
- Python 3.12+ installed
- Git for Windows

## Setup Instructions

### 1. Open the Project
1. Open Visual Studio 2022
2. File → Open → Project/Solution
3. Select `RaiderBot-Production.sln`

### 2. Configure Python Environment
1. Right-click the project in Solution Explorer
2. Select "Python Environments"
3. Add virtual environment or use global Python 3.12+
4. Install dependencies: `pip install -r requirements-dev.txt`

### 3. Set Environment Variables
Create a `.env` file in the project root with:
```
FOUNDRY_TOKEN=your_token_here
FOUNDRY_BASE_URL=https://raiderexpress.palantirfoundry.com
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
```

### 4. Debugging
- Use F5 to start debugging with the default configuration (MCP Server)
- Switch between configurations using the dropdown in the toolbar:
  - **MCP Server** (server.py) - Main MCP server for Claude Desktop integration
  - **HTTP Server** (http_server.py) - Cloud deployment HTTP wrapper
  - **Foundry Tests** (test_real_foundry.py) - Test Foundry API integration
  - **Comprehensive Tests** (run_comprehensive_tests.py) - Full test suite
  - **Debug Foundry Endpoints** (debug_foundry_endpoints.py) - API endpoint debugging

### 5. Available Tasks
Access tasks via View → Task Runner Explorer:
- **Install Dependencies**: Installs production requirements
- **Install Dev Dependencies**: Installs development tools
- **Run Tests**: Executes comprehensive test suite
- **Run Foundry Tests**: Tests Foundry API integration
- **Test Server Integration**: Tests server functionality
- **Lint Code**: Runs pylint on source code
- **Format Code**: Formats code with black
- **Type Check**: Runs mypy type checking
- **Start MCP Server**: Launches MCP server for development
- **Start HTTP Server**: Launches HTTP server for testing
- **Deploy to Foundry**: Deploys to Palantir Foundry

## IntelliSense Features
- Auto-completion for Foundry SDK methods
- Type hints for async/await patterns
- Import suggestions for src/ modules
- Error detection and syntax highlighting
- Debugging support for async functions

## Key Components

### Foundry SDK Integration
The project includes a custom Foundry SDK (`src/foundry_sdk.py`) with:
- `FoundryClient` class for API interactions
- Workshop application creation and management
- User dashboard provisioning
- Workbook visualization updates

### MCP Server Architecture
- **server.py**: Main MCP server with Foundry integration
- **http_server.py**: HTTP wrapper for cloud deployment
- Multiple specialized services in `src/` directory

### Testing Framework
- Comprehensive integration tests
- Real Foundry API testing
- Server integration validation
- Production deployment verification

## Compatibility
This Visual Studio setup is fully compatible with:
- Existing VS Code configuration
- Continue.dev custom commands (`.continue/config.json`)
- Docker deployment workflows (`Dockerfile`, `docker-compose.yml`)
- GitHub Actions CI/CD
- Railway/cloud deployment configurations

## Debugging Tips

### Async/Await Debugging
- Set breakpoints in async functions normally
- Use "Step Into" (F11) to debug async calls
- Watch variables in async context using the Locals window

### Foundry API Debugging
- Use the "Debug Foundry Endpoints" configuration to test API calls
- Check environment variables are loaded in Debug → Windows → Environment
- Monitor HTTP requests in the Output window

### MCP Server Debugging
- Start with "MCP Server" configuration
- Connect Claude Desktop to test MCP functionality
- Use logging statements for MCP message flow debugging

## Troubleshooting

### IntelliSense Issues
- Verify Python environment is correctly set in Solution Explorer
- Check that `src/` is in the search path (configured in .pyproj)
- Reload the project if IntelliSense stops working

### Import Errors
- Ensure PYTHONPATH includes `src/` directory (configured in launch.vs.json)
- Verify all dependencies are installed with `pip install -r requirements-dev.txt`
- Check that `__init__.py` files exist in all package directories

### Debugging Issues
- Confirm environment variables are loaded (check Debug → Windows → Environment)
- Verify Python interpreter is set correctly
- Check that debugpy is installed for remote debugging support

### Foundry Connection Issues
- Verify FOUNDRY_TOKEN is set and valid
- Check FOUNDRY_BASE_URL points to correct Foundry instance
- Test connection with "Debug Foundry Endpoints" configuration

## Development Workflow

### 1. Daily Development
1. Open Visual Studio and load the solution
2. Pull latest changes from git
3. Run "Install Dev Dependencies" task if requirements changed
4. Use "MCP Server" or "HTTP Server" configuration for development
5. Set breakpoints and debug as needed

### 2. Testing
1. Run "Run Tests" task for comprehensive testing
2. Use "Run Foundry Tests" for Foundry-specific testing
3. Debug individual test files using the debugger

### 3. Code Quality
1. Run "Lint Code" task before committing
2. Use "Format Code" task to maintain consistent formatting
3. Run "Type Check" task to catch type errors

### 4. Deployment
1. Test locally with debugging configurations
2. Run "Deploy to Foundry" task for Foundry deployment
3. Use Docker configurations for containerized deployment

## Advanced Features

### Custom Build Configurations
The project supports both Debug and Release configurations:
- **Debug**: Full debugging symbols, verbose logging
- **Release**: Optimized for production deployment

### Multiple Startup Projects
Configure multiple startup projects for complex debugging scenarios:
1. Right-click solution in Solution Explorer
2. Select "Set Startup Projects"
3. Choose "Multiple startup projects"
4. Set actions for different components

### Remote Debugging
For debugging deployed applications:
1. Install debugpy on target environment
2. Configure remote debugging in launch.vs.json
3. Attach to remote Python process

## Integration with Continue.dev

The Visual Studio setup maintains full compatibility with Continue.dev:
- Custom commands remain available in VS Code
- Foundry scaffolding commands work in both IDEs
- Shared configuration in `.continue/config.json`

To use both IDEs:
1. Use Visual Studio for debugging and comprehensive development
2. Use VS Code with Continue.dev for rapid prototyping and AI assistance
3. Both environments share the same Python configuration and dependencies
