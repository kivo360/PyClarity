# Test Container Setup

## Overview

This setup provides an isolated testing environment using Docker containers with three distinct container types:

1. **Development Container** (`devcontainer`) - For live development with mounted code
2. **Test Container** (`testcontainer`) - Ephemeral containers that run tests and exit
3. **Snapshot Container** (`snapshotcontainer`) - For creating reproducible test environments

## Container Architecture

### Container Types

```
┌─────────────────────────────────────┐
│        Docker Compose Network       │
│                                     │
│  ┌─────────────────┐  ┌──────────┐  │
│  │  devcontainer   │  │ postgres │  │
│  │                 │  │          │  │
│  │ • Live dev      │◄─┤ • DB     │  │
│  │ • Mounted code  │  │ • Port   │  │
│  │ • Persistent    │  │   5432   │  │
│  └─────────────────┘  └──────────┘  │
│                                     │
│  ┌─────────────────┐                │
│  │ testcontainer   │                │
│  │                 │                │
│  │ • Ephemeral     │                │
│  │ • Runs & exits  │                │
│  │ • Clean state   │                │
│  └─────────────────┘                │
│                                     │
│  ┌─────────────────┐                │
│  │snapshotcontainer│                │
│  │                 │                │
│  │ • Snapshots     │                │
│  │ • Reproducible  │                │
│  │ • State capture │                │
│  └─────────────────┘                │
└─────────────────────────────────────┘
```

### Key Benefits

1. **No Port Conflicts**: PostgreSQL runs internally, not exposed to host
2. **Ephemeral Testing**: Test containers run and exit, ensuring clean state
3. **Live Development**: Development container mounts code for real-time changes
4. **Snapshot Capability**: Capture and restore reproducible environments
5. **Service Discovery**: Containers can reach each other using service names

## Usage

### Ephemeral Test Containers

```bash
# Run integration tests (container starts, runs tests, exits)
./scripts/run_tests_in_container.sh test_integration

# Run schema generation demo (ephemeral)
./scripts/run_tests_in_container.sh demo_schema

# Run custom LLM providers demo (ephemeral)
./scripts/run_tests_in_container.sh demo_llm

# Run all tests and demos (ephemeral)
./scripts/run_tests_in_container.sh all
```

### Development Container

```bash
# Open shell in development container (persistent)
./scripts/run_tests_in_container.sh dev_shell

# From inside the container, you can run:
python test_integration.py
python demo_schema_generation.py
python demo_custom_llm_providers.py
```

### Snapshot Management

```bash
# Create a snapshot of current state
./scripts/run_tests_in_container.sh create_snapshot my_working_state

# List available snapshots
./scripts/run_tests_in_container.sh list_snapshots

# Restore from snapshot
./scripts/run_tests_in_container.sh restore_snapshot my_working_state

# Open shell in snapshot container
./scripts/run_tests_in_container.sh snapshot_shell
```

### Container Management

```bash
# Stop all containers
./scripts/run_tests_in_container.sh stop

# View container logs
./scripts/run_tests_in_container.sh logs

# Clean up containers and volumes
./scripts/run_tests_in_container.sh clean
```

## Container Behavior

### Ephemeral Test Containers

- **Start**: Container starts fresh for each test run
- **Execute**: Runs the specified test/demo command
- **Exit**: Container terminates after completion
- **Benefits**: 
  - Clean state every time
  - No resource accumulation
  - Reproducible test environment

### Development Container

- **Start**: Container starts and stays running
- **Mount**: Code is mounted for live development
- **Persistent**: Container remains active for development
- **Benefits**:
  - Real-time code changes
  - Interactive debugging
  - Long-running development sessions

### Snapshot Container

- **Start**: Container starts for snapshot operations
- **Capture**: Records current state and dependencies
- **Restore**: Can restore to previous states
- **Benefits**:
  - Reproducible environments
  - Dependency version tracking
  - State preservation

## Environment Variables

All containers are configured with these environment variables:

- `DATABASE_URL=postgresql://pyclarity:pyclarity@postgres:5432/pyclarity`
- `PYTHONPATH=/workspaces/src`

## Manual Docker Commands

If you prefer to use Docker commands directly:

```bash
# Start development environment
docker compose up -d

# Run ephemeral test
docker compose --profile test run --rm testcontainer python test_integration.py

# Open development shell
docker compose exec devcontainer bash

# Create snapshot
docker compose --profile snapshot run --rm snapshotcontainer bash -c "uv sync && echo 'Snapshot created'"

# Stop everything
docker compose down
docker compose --profile test down
docker compose --profile snapshot down
```

## Troubleshooting

### Container Won't Start

```bash
# Check if containers are running
docker compose ps

# View logs
docker compose logs

# Restart containers
docker compose down
docker compose up -d
```

### Ephemeral Container Issues

```bash
# Check if test profile is working
docker compose --profile test ps

# Run test with verbose output
docker compose --profile test run --rm testcontainer bash -c "set -x && python test_integration.py"
```

### Snapshot Issues

```bash
# Check snapshot directory
ls -la snapshots/

# Create snapshot with custom name
./scripts/run_tests_in_container.sh create_snapshot debug_state
```

### Port Conflicts

If you see port conflict errors:

1. Stop any local PostgreSQL instances: `brew services stop postgresql`
2. Check for other Docker containers: `docker ps`
3. Use the container setup which doesn't expose ports to the host

## Development Workflow

### For Testing

1. **Run Tests**: `./scripts/run_tests_in_container.sh test_integration`
2. **Check Results**: Tests run in clean ephemeral container
3. **Iterate**: Make changes and run tests again

### For Development

1. **Start Dev Environment**: `./scripts/run_tests_in_container.sh dev_shell`
2. **Make Changes**: Edit code in mounted volume
3. **Test Changes**: Run tests from within container
4. **Create Snapshot**: `./scripts/run_tests_in_container.sh create_snapshot working_state`

### For Debugging

1. **Create Snapshot**: Capture current working state
2. **Make Changes**: Experiment with modifications
3. **Test Changes**: Run tests in ephemeral containers
4. **Restore if Needed**: `./scripts/run_tests_in_container.sh restore_snapshot working_state`

This setup ensures your tests run in a consistent, isolated environment while providing flexibility for development and debugging. 