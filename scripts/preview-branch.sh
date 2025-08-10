#!/bin/bash

# Preview Branch Management Script
# This script helps manage the preview branch for draft blog posts

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Check if we're in the right directory
if [ ! -f "mkdocs.yml" ]; then
    print_error "This script must be run from the root of the bsmeding.github.io repository"
    exit 1
fi

# Function to show usage
show_usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  create    - Create and switch to preview branch"
    echo "  update    - Update preview branch with latest changes"
    echo "  publish   - Merge preview branch to main (publish drafts)"
    echo "  cleanup   - Delete preview branch and clean up"
    echo "  status    - Show current branch status"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 create    # Create preview branch"
    echo "  $0 update    # Update preview with new changes"
    echo "  $0 publish   # Publish drafts to main"
}

# Function to create preview branch
create_preview() {
    print_header "Creating Preview Branch"
    
    # Check if we're on main branch
    if [ "$(git branch --show-current)" != "main" ]; then
        print_warning "You're not on the main branch. Switching to main..."
        git checkout main
    fi
    
    # Pull latest changes
    print_status "Pulling latest changes from main..."
    git pull origin main
    
    # Create and switch to preview branch
    print_status "Creating preview branch..."
    git checkout -b preview
    
    # Push preview branch to remote
    print_status "Pushing preview branch to remote..."
    git push -u origin preview
    
    print_status "Preview branch created successfully!"
    print_status "You can now make changes and push to preview branch for testing."
    print_status "Preview URL will be available at: https://bsmeding.github.io/bsmeding.github.io/preview/"
}

# Function to update preview branch
update_preview() {
    print_header "Updating Preview Branch"
    
    # Check if we're on preview branch
    if [ "$(git branch --show-current)" != "preview" ]; then
        print_warning "You're not on the preview branch. Switching to preview..."
        git checkout preview
    fi
    
    # Pull latest changes from main
    print_status "Pulling latest changes from main..."
    git pull origin main
    
    # Add all changes
    print_status "Adding changes..."
    git add .
    
    # Check if there are changes to commit
    if git diff --cached --quiet; then
        print_warning "No changes to commit"
    else
        # Commit changes
        print_status "Committing changes..."
        git commit -m "Update preview with latest changes"
        
        # Push to remote
        print_status "Pushing to remote preview branch..."
        git push origin preview
    fi
    
    print_status "Preview branch updated successfully!"
}

# Function to publish drafts
publish_drafts() {
    print_header "Publishing Drafts"
    
    # Check if we're on preview branch
    if [ "$(git branch --show-current)" != "preview" ]; then
        print_error "You must be on the preview branch to publish drafts"
        exit 1
    fi
    
    # Find draft files
    DRAFT_FILES=$(find docs/blog/posts -name "*draft*" -type f)
    
    if [ -z "$DRAFT_FILES" ]; then
        print_warning "No draft files found"
        return
    fi
    
    print_status "Found draft files:"
    echo "$DRAFT_FILES"
    echo ""
    
    # Ask for confirmation
    read -p "Do you want to publish these drafts? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Publishing cancelled"
        return
    fi
    
    # Remove draft flag from files
    for file in $DRAFT_FILES; do
        print_status "Publishing $file..."
        # Remove draft: true from front matter
        sed -i '/draft: true/d' "$file"
        # Update title to remove (Draft)
        sed -i 's/ (Draft)//g' "$file"
    done
    
    # Add and commit changes
    git add .
    git commit -m "Publish draft posts"
    
    # Switch to main and merge
    print_status "Switching to main branch..."
    git checkout main
    
    print_status "Merging preview branch..."
    git merge preview
    
    print_status "Pushing to main..."
    git push origin main
    
    print_status "Drafts published successfully!"
    print_status "You can now clean up the preview branch with: $0 cleanup"
}

# Function to cleanup preview branch
cleanup_preview() {
    print_header "Cleaning Up Preview Branch"
    
    # Switch to main
    print_status "Switching to main branch..."
    git checkout main
    
    # Delete local preview branch
    print_status "Deleting local preview branch..."
    git branch -D preview
    
    # Delete remote preview branch
    print_status "Deleting remote preview branch..."
    git push origin --delete preview
    
    print_status "Preview branch cleaned up successfully!"
}

# Function to show status
show_status() {
    print_header "Branch Status"
    
    CURRENT_BRANCH=$(git branch --show-current)
    print_status "Current branch: $CURRENT_BRANCH"
    
    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        print_warning "You have uncommitted changes"
    else
        print_status "No uncommitted changes"
    fi
    
    # Check for draft files
    DRAFT_FILES=$(find docs/blog/posts -name "*draft*" -type f 2>/dev/null || true)
    if [ -n "$DRAFT_FILES" ]; then
        print_status "Draft files found:"
        echo "$DRAFT_FILES"
    else
        print_status "No draft files found"
    fi
    
    # Show recent commits
    print_status "Recent commits:"
    git log --oneline -5
}

# Main script logic
case "${1:-help}" in
    create)
        create_preview
        ;;
    update)
        update_preview
        ;;
    publish)
        publish_drafts
        ;;
    cleanup)
        cleanup_preview
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        print_error "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac
