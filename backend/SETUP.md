# Backend Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
USE_MEMORY_CHANNELS=True  # Optional: Use in-memory channels if Redis not available
```

### 3. Initialize Database

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Create Demo Data

```bash
python manage.py shell
```

In the Python shell:
```python
from accounts.models import User

# Create demo users
User.objects.create_user(username='demo', email='demo@example.com', password='demo123', first_name='Demo', last_name='User')
User.objects.create_user(username='alice', email='alice@example.com', password='alice123', first_name='Alice', last_name='Smith')
User.objects.create_user(username='bob', email='bob@example.com', password='bob123', first_name='Bob', last_name='Jones')
```

### 5. Start Redis (Optional)

If not using `USE_MEMORY_CHANNELS=True`:

```bash
# Ubuntu/Debian
sudo apt-get install redis-server
redis-server

# macOS
brew install redis
brew services start redis

# Docker
docker run -d -p 6379:6379 redis:alpine
```

### 6. Run Server

```bash
python manage.py runserver
```

Backend available at: `http://localhost:8000`

## API Testing

### Using curl

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo",
    "password": "demo123"
  }'

# Get conversations (replace TOKEN with your access token)
curl http://localhost:8000/api/chat/conversations/ \
  -H "Authorization: Bearer TOKEN"
```

## Admin Panel

Access Django admin at: `http://localhost:8000/admin`

Use the superuser credentials you created.

## Troubleshooting

### Redis Connection Error
If you see Redis connection errors:
1. Make sure Redis is running
2. Or set `USE_MEMORY_CHANNELS=True` in `.env`

### Migration Errors
```bash
# Delete database and migrations
rm db.sqlite3
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Recreate
python manage.py makemigrations
python manage.py migrate
```

### CORS Errors
Make sure `CORS_ALLOWED_ORIGINS` in settings includes your frontend URL.

