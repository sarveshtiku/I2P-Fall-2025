#!/bin/bash

# ContextLink Setup Script
echo "🧩 Setting up ContextLink - Universal AI Memory Fabric"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Create virtual environment for backend
echo "📦 Setting up Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Copy environment file
echo "⚙️ Setting up environment configuration..."
if [ ! -f .env ]; then
    cp env.example .env
    echo "📝 Created .env file from template. Please update with your API keys."
fi

# Create database directory
echo "🗄️ Setting up database..."
mkdir -p data/postgres

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your API keys"
echo "2. Start the database: docker-compose up postgres -d"
echo "3. Run migrations: cd backend && source venv/bin/activate && python -c 'from app.core.database import init_db; import asyncio; asyncio.run(init_db())'"
echo "4. Start the backend: cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload"
echo "5. Start the frontend: cd frontend && npm run dev"
echo ""
echo "Or use Docker: docker-compose up"
