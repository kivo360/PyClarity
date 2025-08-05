#!/bin/bash

# Script to run tests and demos in isolated containers
# Supports ephemeral test containers and snapshot containers

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐳 PyClarity Container Test Runner${NC}"
echo "======================================"

# Function to check if containers are running
check_containers() {
    echo -e "${YELLOW}📋 Checking container status...${NC}"
    
    # Check if postgres is running
    if ! docker compose ps postgres | grep -q "Up"; then
        echo -e "${RED}❌ PostgreSQL container is not running${NC}"
        echo "Starting containers..."
        docker compose up -d postgres
        echo -e "${YELLOW}⏳ Waiting for PostgreSQL to be ready...${NC}"
        sleep 10
    fi
}

# Function to run a command in an ephemeral test container
run_in_ephemeral_container() {
    local command="$1"
    local description="$2"
    
    echo -e "${BLUE}🔧 Running: $description${NC}"
    echo -e "${YELLOW}Command: $command${NC}"
    echo "----------------------------------"
    
    # Create and run ephemeral test container
    echo -e "${PURPLE}🚀 Starting ephemeral test container...${NC}"
    
    # Run the command in a new container that will exit after completion
    docker compose --profile test run --rm testcontainer bash -c "
        echo '📦 Installing dependencies...'
        uv sync
        
        echo '🧪 Running test command...'
        $command
        
        echo '✅ Test completed, container will exit'
    "
    
    echo -e "${GREEN}✅ Completed: $description${NC}"
    echo ""
}

# Function to run a command in a persistent container
run_in_persistent_container() {
    local command="$1"
    local description="$2"
    local container_name="$3"
    
    echo -e "${BLUE}🔧 Running: $description${NC}"
    echo -e "${YELLOW}Command: $command${NC}"
    echo "----------------------------------"
    
    # Check if container is running, start if not
    if ! docker compose ps $container_name | grep -q "Up"; then
        echo -e "${YELLOW}🚀 Starting $container_name...${NC}"
        docker compose up -d $container_name
        sleep 5
    fi
    
    # Install dependencies and run command
    docker compose exec $container_name bash -c "
        echo '📦 Installing dependencies...'
        uv sync
        
        echo '🧪 Running command...'
        $command
    "
    
    echo -e "${GREEN}✅ Completed: $description${NC}"
    echo ""
}

# Function to create a snapshot
create_snapshot() {
    local snapshot_name="$1"
    
    echo -e "${PURPLE}📸 Creating snapshot: $snapshot_name${NC}"
    
    # Start snapshot container if not running
    if ! docker compose --profile snapshot ps snapshotcontainer | grep -q "Up"; then
        echo -e "${YELLOW}🚀 Starting snapshot container...${NC}"
        docker compose --profile snapshot up -d snapshotcontainer
        sleep 5
    fi
    
    # Install dependencies and create snapshot
    docker compose --profile snapshot exec snapshotcontainer bash -c "
        echo '📦 Installing dependencies...'
        uv sync
        
        echo '📸 Creating snapshot...'
        # Create a snapshot of the current state
        echo 'Current state:' > /workspaces/snapshots/$snapshot_name.txt
        date >> /workspaces/snapshots/$snapshot_name.txt
        echo 'Dependencies:' >> /workspaces/snapshots/$snapshot_name.txt
        uv tree >> /workspaces/snapshots/$snapshot_name.txt
        
        echo 'Cache info:' >> /workspaces/snapshots/$snapshot_name.txt
        echo 'UV cache location: /home/user/.cache/uv' >> /workspaces/snapshots/$snapshot_name.txt
        ls -la /home/user/.cache/uv/ >> /workspaces/snapshots/$snapshot_name.txt 2>/dev/null || echo 'No UV cache found' >> /workspaces/snapshots/$snapshot_name.txt
        
        echo 'Virtual environment:' >> /workspaces/snapshots/$snapshot_name.txt
        ls -la /opt/venv/ >> /workspaces/snapshots/$snapshot_name.txt 2>/dev/null || echo 'No venv found' >> /workspaces/snapshots/$snapshot_name.txt
        
        echo '✅ Snapshot created: /workspaces/snapshots/$snapshot_name.txt'
    "
    
    echo -e "${GREEN}✅ Snapshot created: $snapshot_name${NC}"
}

# Function to restore from snapshot
restore_snapshot() {
    local snapshot_name="$1"
    
    echo -e "${PURPLE}🔄 Restoring from snapshot: $snapshot_name${NC}"
    
    # This would typically involve restoring the exact dependency versions
    # For now, we'll just show the snapshot contents
    if [ -f "snapshots/$snapshot_name.txt" ]; then
        echo -e "${YELLOW}📋 Snapshot contents:${NC}"
        cat "snapshots/$snapshot_name.txt"
    else
        echo -e "${RED}❌ Snapshot not found: $snapshot_name${NC}"
    fi
}

# Main execution
main() {
    local script_name="$1"
    local snapshot_name="$2"
    
    case "$script_name" in
        "test_integration")
            check_containers
            run_in_ephemeral_container "python test_integration.py" "Integration Tests"
            ;;
        "demo_schema")
            check_containers
            run_in_ephemeral_container "python demo_schema_generation.py" "Schema Generation Demo"
            ;;
        "demo_llm")
            check_containers
            run_in_ephemeral_container "python demo_custom_llm_providers.py" "Custom LLM Providers Demo"
            ;;
        "all")
            check_containers
            echo -e "${BLUE}🎯 Running all tests and demos in ephemeral containers...${NC}"
            run_in_ephemeral_container "python demo_schema_generation.py && python demo_custom_llm_providers.py && python test_integration.py" "All Tests and Demos"
            ;;
        "dev_shell")
            check_containers
            echo -e "${BLUE}🐚 Opening shell in development container...${NC}"
            docker compose exec devcontainer bash
            ;;
        "test_shell")
            check_containers
            echo -e "${BLUE}🐚 Opening shell in test container...${NC}"
            docker compose --profile test exec testcontainer bash
            ;;
        "snapshot_shell")
            check_containers
            echo -e "${BLUE}🐚 Opening shell in snapshot container...${NC}"
            docker compose --profile snapshot exec snapshotcontainer bash
            ;;
        "create_snapshot")
            if [ -z "$snapshot_name" ]; then
                snapshot_name="snapshot_$(date +%Y%m%d_%H%M%S)"
            fi
            create_snapshot "$snapshot_name"
            ;;
        "restore_snapshot")
            if [ -z "$snapshot_name" ]; then
                echo -e "${RED}❌ Please provide snapshot name${NC}"
                exit 1
            fi
            restore_snapshot "$snapshot_name"
            ;;
        "list_snapshots")
            echo -e "${BLUE}📋 Available snapshots:${NC}"
            if [ -d "snapshots" ]; then
                ls -la snapshots/
            else
                echo "No snapshots directory found"
            fi
            ;;
        "stop")
            echo -e "${YELLOW}🛑 Stopping all containers...${NC}"
            docker compose down
            docker compose --profile test down
            docker compose --profile snapshot down
            ;;
        "logs")
            echo -e "${BLUE}📋 Showing container logs...${NC}"
            docker compose logs -f
            ;;
        "clean")
            echo -e "${YELLOW}🧹 Cleaning up containers and volumes...${NC}"
            docker compose down -v
            docker compose --profile test down -v
            docker compose --profile snapshot down -v
            docker system prune -f
            ;;
        "cache_info")
            echo -e "${BLUE}📋 UV Cache Information${NC}"
            echo "=================================="
            
            # Check if any container is running to inspect cache
            if docker compose ps | grep -q "Up"; then
                echo -e "${YELLOW}📦 UV Cache Status:${NC}"
                docker compose exec devcontainer bash -c "
                    echo 'UV cache location: /home/user/.cache/uv'
                    ls -la /home/user/.cache/uv/ 2>/dev/null || echo 'No UV cache found'
                    echo ''
                    echo 'Virtual environment:'
                    ls -la /opt/venv/ 2>/dev/null || echo 'No venv found'
                    echo ''
                    echo 'Cache size:'
                    du -sh /home/user/.cache/uv/ 2>/dev/null || echo 'Cache not found'
                    du -sh /opt/venv/ 2>/dev/null || echo 'Venv not found'
                "
            else
                echo -e "${RED}❌ No containers running. Start a container first to inspect cache.${NC}"
            fi
            ;;
        "cache_clear")
            echo -e "${YELLOW}🗑️  Clearing UV cache...${NC}"
            
            # Stop all containers
            docker compose down
            docker compose --profile test down
            docker compose --profile snapshot down
            
            # Remove cache volume
            docker volume rm pyclarity_uv-cache-volume 2>/dev/null || echo "Cache volume not found"
            
            echo -e "${GREEN}✅ UV cache cleared${NC}"
            ;;
        "cache_backup")
            local backup_name="$2"
            if [ -z "$backup_name" ]; then
                backup_name="cache_backup_$(date +%Y%m%d_%H%M%S)"
            fi
            
            echo -e "${PURPLE}💾 Creating cache backup: $backup_name${NC}"
            
            # Create backup directory
            mkdir -p cache_backups
            
            # Backup cache volume
            docker run --rm -v pyclarity_uv-cache-volume:/cache -v $(pwd)/cache_backups:/backup alpine tar czf /backup/$backup_name.tar.gz -C /cache .
            
            echo -e "${GREEN}✅ Cache backup created: cache_backups/$backup_name.tar.gz${NC}"
            ;;
        "cache_restore")
            local backup_name="$2"
            if [ -z "$backup_name" ]; then
                echo -e "${RED}❌ Please provide backup name${NC}"
                exit 1
            fi
            
            echo -e "${PURPLE}🔄 Restoring cache from backup: $backup_name${NC}"
            
            # Stop all containers
            docker compose down
            docker compose --profile test down
            docker compose --profile snapshot down
            
            # Remove existing cache volume
            docker volume rm pyclarity_uv-cache-volume 2>/dev/null || echo "Cache volume not found"
            
            # Create new cache volume and restore
            docker run --rm -v pyclarity_uv-cache-volume:/cache -v $(pwd)/cache_backups:/backup alpine sh -c "
                mkdir -p /cache
                tar xzf /backup/$backup_name.tar.gz -C /cache
            "
            
            echo -e "${GREEN}✅ Cache restored from: cache_backups/$backup_name.tar.gz${NC}"
            ;;
        *)
            echo -e "${RED}❌ Unknown command: $script_name${NC}"
            echo ""
            echo -e "${BLUE}Usage:${NC}"
            echo "  $0 test_integration    - Run integration tests (ephemeral)"
            echo "  $0 demo_schema         - Run schema generation demo (ephemeral)"
            echo "  $0 demo_llm            - Run custom LLM providers demo (ephemeral)"
            echo "  $0 all                 - Run all tests and demos (ephemeral)"
            echo "  $0 dev_shell           - Open shell in development container"
            echo "  $0 test_shell          - Open shell in test container"
            echo "  $0 snapshot_shell      - Open shell in snapshot container"
            echo "  $0 create_snapshot [name] - Create a snapshot of current state"
            echo "  $0 restore_snapshot <name> - Restore from snapshot"
            echo "  $0 list_snapshots      - List available snapshots"
            echo "  $0 stop                - Stop all containers"
            echo "  $0 logs                - Show container logs"
            echo "  $0 clean               - Clean up containers and volumes"
            echo ""
            echo -e "${BLUE}Cache Management:${NC}"
            echo "  $0 cache_info          - Show UV cache information"
            echo "  $0 cache_clear         - Clear UV cache"
            echo "  $0 cache_backup [name] - Backup UV cache"
            echo "  $0 cache_restore <name> - Restore UV cache from backup"
            echo ""
            echo -e "${YELLOW}Examples:${NC}"
            echo "  $0 test_integration"
            echo "  $0 all"
            echo "  $0 create_snapshot my_working_state"
            echo "  $0 restore_snapshot my_working_state"
            echo "  $0 dev_shell"
            echo "  $0 cache_backup my_working_cache"
            echo "  $0 cache_restore my_working_cache"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@" 