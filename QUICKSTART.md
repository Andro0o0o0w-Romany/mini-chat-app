# 🚀 Quick Start Guide

Get the Mini Chat System running in 5 minutes!

## Prerequisites

Make sure you have installed:
- Python 3.8+ ([Download](https://www.python.org/downloads/))
- Node.js 14+ ([Download](https://nodejs.org/))
- Redis (optional, for production WebSocket)

## Option 1: Automated Setup (Recommended)

### Linux/macOS:
```bash
chmod +x setup.sh
./setup.sh
```

### Windows:
```cmd
setup.bat
```

Then follow the instructions to start the servers.

## Option 2: Manual Setup

### Backend Setup (5 steps)

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database
python manage.py migrate

# 5. Create demo data
python create_demo_data.py
```

### Frontend Setup (3 steps)

```bash
# 1. Navigate to frontend (in a new terminal)
cd frontend

# 2. Install dependencies
npm install

# 3. Create .env file
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env
echo "REACT_APP_WS_URL=localhost:8000" >> .env
```

## Running the Application

### Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python manage.py runserver
```
✅ Backend running at http://localhost:8000

### Terminal 2 - Frontend:
```bash
cd frontend
npm start
```
✅ Frontend running at http://localhost:3000

## Login & Test

1. Open your browser to http://localhost:3000
2. Login with demo account:
   - Username: `demo`
   - Password: `demo123`

3. Try these features:
   - ✨ View dashboard statistics
   - 💬 Click on existing conversations
   - 📝 Send real-time messages
   - ➕ Create new conversations
   - 👥 Add multiple users for group chat

## Demo Accounts

| Username | Password | Name |
|----------|----------|------|
| demo | demo123 | Demo User |
| alice | alice123 | Alice Smith |
| bob | bob123 | Bob Jones |
| charlie | charlie123 | Charlie Brown |

## Testing Real-time Chat

1. **Open two browser windows** (or use incognito mode)
2. Login as `demo` in window 1
3. Login as `alice` in window 2
4. Start a conversation between them
5. Send messages and watch them appear instantly!
6. Try typing to see the typing indicator

## Troubleshooting

### Backend won't start?
- Make sure virtual environment is activated
- Check if port 8000 is available
- Verify all dependencies are installed: `pip list`

### Frontend won't start?
- Check if port 3000 is available
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

### WebSocket not working?
- By default, the app uses in-memory channels (no Redis needed)
- Check browser console for WebSocket connection errors
- Verify backend is running on port 8000

### Can't login?
- Make sure you ran `python create_demo_data.py`
- Check Django logs in the terminal
- Try creating a new user via `/register` page

## Project Structure

```
Mini chat app with django & react/
├── backend/              # Django backend
│   ├── chat/            # Chat app (models, views, WebSocket)
│   ├── accounts/        # User authentication
│   └── chat_project/    # Django settings
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── pages/       # Page components
│   │   ├── context/     # State management
│   │   └── services/    # API services
│   └── public/
└── docs/                # Documentation
```

## What's Next?

- 📖 Read [README.md](README.md) for full documentation
- 🏗️ Check [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- 🔧 See [backend/SETUP.md](backend/SETUP.md) for detailed backend setup
- ⚛️ See [frontend/SETUP.md](frontend/SETUP.md) for detailed frontend setup

## Support

Having issues? Check:
1. All prerequisites are installed
2. Both backend and frontend servers are running
3. No port conflicts (8000, 3000)
4. Virtual environment is activated for backend
5. .env files are created with correct values

## Pro Tips

- 💡 Use `python manage.py createsuperuser` to create admin account
- 💡 Access Django admin at http://localhost:8000/admin
- 💡 Check browser DevTools console for errors
- 💡 Use React DevTools extension for debugging
- 💡 Enable Django DEBUG=True for detailed error messages

---

**Happy Chatting! 💬**

If everything is working, you should see a beautiful gradient interface with real-time messaging! 🎉

