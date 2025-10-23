#!/bin/bash

# Mini Chat System Setup Script
# This script sets up both backend and frontend

set -e

echo "======================================"
echo "Mini Chat System - Setup Script"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python and Node.js are installed${NC}"
echo ""

# ====================================
# Backend Setup
# ====================================
echo "======================================"
echo "Setting up Backend..."
echo "======================================"
echo ""

cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOL
SECRET_KEY=django-insecure-dev-key-$(openssl rand -hex 32)
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
USE_MEMORY_CHANNELS=True
EOL
    echo -e "${GREEN}✓ Created .env file${NC}"
fi

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create demo data
echo "Creating demo data..."
python create_demo_data.py

echo -e "${GREEN}✓ Backend setup complete!${NC}"
echo ""

cd ..

# ====================================
# Frontend Setup
# ====================================
echo "======================================"
echo "Setting up Frontend..."
echo "======================================"
echo ""

cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOL
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_WS_URL=localhost:8000
EOL
    echo -e "${GREEN}✓ Created .env file${NC}"
fi

echo -e "${GREEN}✓ Frontend setup complete!${NC}"
echo ""

cd ..

# ====================================
# Final Instructions
# ====================================
echo "======================================"
echo "Setup Complete! 🎉"
echo "======================================"
echo ""
echo "To start the application:"
echo ""
echo -e "${YELLOW}Backend:${NC}"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo -e "${YELLOW}Frontend:${NC}"
echo "  cd frontend"
echo "  npm start"
echo ""
echo -e "${YELLOW}Demo Login:${NC}"
echo "  Username: demo"
echo "  Password: demo123"
echo ""
echo "Open http://localhost:3000 in your browser"
echo ""
echo -e "${GREEN}Happy Chatting! 💬${NC}"

