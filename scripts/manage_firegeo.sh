#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}🐳 PyClarity Firegeo Manager${NC}"
    echo "=================================="
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to check if Docker Compose is available
check_compose() {
    if ! docker compose version > /dev/null 2>&1; then
        print_error "Docker Compose is not available. Please install Docker Compose and try again."
        exit 1
    fi
}

# Function to check if required files exist
check_files() {
    if [ ! -f "docker-compose.yml" ]; then
        print_error "docker-compose.yml not found. Please run setup_firegeo.sh first."
        exit 1
    fi
    
    if [ ! -f "Dockerfile.firegeo" ]; then
        print_error "Dockerfile.firegeo not found. Please run setup_firegeo.sh first."
        exit 1
    fi
}

# Function to show help
show_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup          - Set up Firegeo Next.js app (clone and configure)"
    echo "  dev            - Start development environment with watch mode"
    echo "  build          - Build production image"
    echo "  start          - Start production environment"
    echo "  stop           - Stop all containers"
    echo "  restart        - Restart all containers"
    echo "  logs           - Show logs from all containers"
    echo "  logs:firegeo   - Show Firegeo app logs"
    echo "  logs:db        - Show database logs"
    echo "  shell          - Open shell in Firegeo container"
    echo "  db:push        - Push database schema"
    echo "  db:studio      - Open Drizzle Studio"
    echo "  db:reset       - Reset database (drop and recreate)"
    echo "  clean          - Clean up containers and volumes"
    echo "  status         - Show container status"
    echo "  help           - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup       # Initial setup"
    echo "  $0 dev         # Start development with watch mode"
    echo "  $0 logs        # View all logs"
    echo ""
    echo "🔍 Modern Docker Compose Watch Features:"
    echo "  - Hot reloading for code changes"
    echo "  - Automatic rebuilds for dependency changes"
    echo "  - Smart restarts for configuration changes"
    echo "  - Ignored paths for optimal performance"
}

# Function to setup Firegeo
setup_firegeo() {
    print_status
    print_success "Setting up Firegeo Next.js app..."
    
    if [ ! -f "scripts/setup_firegeo.sh" ]; then
        print_error "setup_firegeo.sh not found!"
        exit 1
    fi
    
    chmod +x scripts/setup_firegeo.sh
    ./scripts/setup_firegeo.sh
    
    print_success "Firegeo setup complete!"
    echo ""
    echo "🚀 Next steps:"
    echo "1. Update .env.local with your API keys"
    echo "2. Run: $0 dev"
    echo "3. Visit: http://localhost:3000"
}

# Function to start development environment with watch
start_dev() {
    print_status
    print_success "Starting development environment with modern watch mode..."
    
    # Use the modern docker compose watch command
    docker compose up --watch
    
    print_success "Development environment started with watch mode!"
    echo ""
    echo "🌐 Services:"
    echo "  - PostgreSQL: localhost:5432"
    echo "  - Firegeo App: http://localhost:3000"
    echo ""
    echo "🔄 Modern Watch Features:"
    echo "  - Hot reloading for code changes (sync)"
    echo "  - Automatic rebuilds for package.json changes (rebuild)"
    echo "  - Smart restarts for config changes (sync+restart)"
    echo "  - Ignored paths: node_modules/, .next/, __pycache__/"
    echo ""
    echo "📋 Useful commands:"
    echo "  $0 logs        # View logs"
    echo "  $0 shell       # Open shell"
    echo "  $0 stop        # Stop services"
}

# Function to build production image
build_production() {
    print_status
    print_success "Building production image..."
    
    docker compose build firegeo-app --target production
    
    print_success "Production image built!"
}

# Function to start production environment
start_production() {
    print_status
    print_success "Starting production environment..."
    
    docker compose up -d
    
    print_success "Production environment started!"
    echo ""
    echo "🌐 Services:"
    echo "  - PostgreSQL: localhost:5432"
    echo "  - Firegeo App: http://localhost:3000"
}

# Function to stop all containers
stop_containers() {
    print_status
    print_success "Stopping all containers..."
    
    docker compose down
    
    print_success "All containers stopped!"
}

# Function to restart containers
restart_containers() {
    print_status
    print_success "Restarting containers..."
    
    docker compose restart
    
    print_success "Containers restarted!"
}

# Function to show logs
show_logs() {
    print_status
    print_success "Showing logs from all containers..."
    
    docker compose logs -f
}

# Function to show specific logs
show_specific_logs() {
    local service=$1
    print_status
    print_success "Showing logs for $service..."
    
    docker compose logs -f $service
}

# Function to open shell
open_shell() {
    print_status
    print_success "Opening shell in Firegeo container..."
    
    docker compose exec firegeo-app /bin/sh
}

# Function to push database schema
push_db_schema() {
    print_status
    print_success "Pushing database schema..."
    
    docker compose exec firegeo-app npm run db:push
    
    print_success "Database schema pushed!"
}

# Function to open Drizzle Studio
open_db_studio() {
    print_status
    print_success "Opening Drizzle Studio..."
    
    docker compose exec firegeo-app npm run db:studio
}

# Function to reset database
reset_database() {
    print_status
    print_warning "This will drop and recreate the database. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_success "Resetting database..."
        
        # Stop containers
        docker compose down
        
        # Remove database volume
        docker volume rm pyclarity_postgres_data 2>/dev/null || true
        
        # Start containers
        docker compose up -d
        
        print_success "Database reset complete!"
    else
        print_warning "Database reset cancelled."
    fi
}

# Function to clean up
clean_up() {
    print_status
    print_warning "This will remove all containers, volumes, and images. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_success "Cleaning up..."
        
        # Stop and remove containers
        docker compose down -v
        
        # Remove images
        docker rmi pyclarity-firegeo-app 2>/dev/null || true
        
        print_success "Cleanup complete!"
    else
        print_warning "Cleanup cancelled."
    fi
}

# Function to show status
show_status() {
    print_status
    print_success "Container status:"
    
    docker compose ps
}

# Main script logic
main() {
    # Check prerequisites
    check_docker
    check_compose
    check_files
    
    # Parse command
    case "${1:-help}" in
        setup)
            setup_firegeo
            ;;
        dev)
            start_dev
            ;;
        build)
            build_production
            ;;
        start)
            start_production
            ;;
        stop)
            stop_containers
            ;;
        restart)
            restart_containers
            ;;
        logs)
            show_logs
            ;;
        logs:firegeo)
            show_specific_logs firegeo-app
            ;;
        logs:db)
            show_specific_logs postgres
            ;;
        shell)
            open_shell
            ;;
        db:push)
            push_db_schema
            ;;
        db:studio)
            open_db_studio
            ;;
        db:reset)
            reset_database
            ;;
        clean)
            clean_up
            ;;
        status)
            show_status
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@" 