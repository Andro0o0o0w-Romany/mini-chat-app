# Mini Chat System with Dashboard 💬

A modern, full-stack real-time chat application built with Django REST Framework (backend) and React (frontend). This application demonstrates WebSocket integration, JWT authentication, and elegant UI design.

## ✨ Features

### Backend (Django + DRF)
- ✅ Real-time messaging using Django Channels and WebSocket
- ✅ RESTful API with Django REST Framework
- ✅ JWT token authentication
- ✅ User management and authentication
- ✅ Conversation and message models
- ✅ Online status tracking
- ✅ Typing indicators
- ✅ Unread message counts
- ✅ **Duplicate conversation prevention** (prevents multiple 1-on-1 chats with same user)

### Frontend (React)
- ✅ Modern, elegant UI with Tailwind CSS
- ✅ Dashboard with statistics (total conversations, messages sent, unread count)
- ✅ Real-time chat with WebSocket connection
- ✅ Conversation list with last message preview
- ✅ Typing indicators
- ✅ User online/offline status
- ✅ Responsive design for mobile and desktop
- ✅ Beautiful animations and transitions
- ✅ **Toast notifications** for user feedback
- ✅ **Smart conversation management** (auto-redirect to existing conversations)

## 🏗️ Architecture

### Backend Structure
```
backend/
├── chat_project/          # Django project settings
│   ├── settings.py        # Configuration
│   ├── urls.py           # URL routing
│   ├── asgi.py           # ASGI configuration for WebSocket
│   └── wsgi.py           # WSGI configuration
├── accounts/             # User authentication app
│   ├── models.py         # Custom User model
│   ├── views.py          # Auth views (login, register, logout)
│   ├── serializers.py    # User serializers
│   └── urls.py          # Auth endpoints
├── chat/                # Chat functionality app
│   ├── models.py        # Conversation, Message, Participant models
│   ├── views.py         # Chat API views
│   ├── serializers.py   # Chat serializers
│   ├── consumers.py     # WebSocket consumer
│   ├── routing.py       # WebSocket routing
│   ├── middleware.py    # JWT WebSocket authentication
│   └── urls.py         # Chat endpoints
└── requirements.txt    # Python dependencies
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/       # Reusable components
│   │   ├── Navbar.js
│   │   ├── StatsCard.js
│   │   ├── ConversationList.js
│   │   ├── ChatWindow.js
│   │   └── NewConversationModal.js
│   ├── pages/           # Page components
│   │   ├── Login.js
│   │   ├── Register.js
│   │   └── Dashboard.js
│   ├── context/         # React Context
│   │   └── AuthContext.js
│   ├── services/        # API services
│   │   └── api.js
│   ├── utils/          # Utility functions
│   │   └── dateUtils.js
│   ├── App.js          # Main app component
│   └── index.css       # Global styles
└── package.json        # Node dependencies
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- Redis (for WebSocket channel layers)

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
Create a `.env` file in the backend directory:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

5. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser (optional):**
```bash
python manage.py createsuperuser
```

7. **Create demo users (for testing):**
```bash
python manage.py shell
```
Then in the Python shell:
```python
from accounts.models import User
User.objects.create_user(username='demo', email='demo@example.com', password='demo123', first_name='Demo', last_name='User')
User.objects.create_user(username='alice', email='alice@example.com', password='alice123', first_name='Alice', last_name='Smith')
User.objects.create_user(username='bob', email='bob@example.com', password='bob123', first_name='Bob', last_name='Jones')
exit()
```

8. **Install and start Redis (required for WebSocket):**
```bash
# On Ubuntu/Debian
sudo apt-get install redis-server
redis-server

# On macOS
brew install redis
brew services start redis

# On Windows
# Download and install from https://redis.io/download
```

9. **Run the development server:**
```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

**Note:** For development without Redis, you can use in-memory channel layers by adding this to your `.env`:
```env
USE_MEMORY_CHANNELS=True
```

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Set up environment variables:**
Create a `.env` file in the frontend directory:
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_WS_URL=localhost:8000
```

4. **Start the development server:**
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## 🎯 Usage

### 1. Register/Login
- Open `http://localhost:3000`
- Register a new account or login with demo credentials:
  - Username: `demo`
  - Password: `demo123`

### 2. Dashboard
After logging in, you'll see:
- **Statistics Cards**: Total conversations, messages sent, and unread messages
- **Conversation List**: All your conversations with last message preview
- **Chat Window**: Select a conversation to view and send messages

### 3. Start a New Conversation
- Click the "+" button in the conversation list
- Select one or more users
- For group chats, optionally add a group name
- Click "Create" to start chatting

### 4. Real-time Features
- Messages appear instantly using WebSocket
- See typing indicators when others are typing
- View online/offline status of users
- Unread message counts update in real-time

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/token/` - Login (get JWT tokens)
- `POST /api/auth/token/refresh/` - Refresh access token
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/me/` - Get current user
- `PATCH /api/auth/me/` - Update user profile
- `GET /api/auth/users/` - List all users

### Chat
- `GET /api/chat/conversations/` - List conversations
- `POST /api/chat/conversations/` - Create conversation
- `GET /api/chat/conversations/{id}/` - Get conversation details
- `GET /api/chat/conversations/stats/` - Get dashboard statistics
- `POST /api/chat/conversations/{id}/mark_read/` - Mark conversation as read
- `GET /api/chat/messages/?conversation={id}` - Get messages for conversation
- `POST /api/chat/messages/` - Send message (alternative to WebSocket)

### WebSocket
- `ws://localhost:8000/ws/chat/{conversation_id}/?token={jwt_token}` - Chat WebSocket

## 🎨 Design Features

### UI/UX Highlights
- **Gradient Backgrounds**: Beautiful purple/blue gradient theme
- **Smooth Animations**: Fade-in, slide animations for messages
- **Responsive Design**: Works seamlessly on mobile and desktop
- **Modern Components**: Rounded corners, shadows, hover effects
- **Loading States**: Spinners and loading indicators
- **Error Handling**: User-friendly error messages
- **Typing Indicators**: Animated dots show when users are typing
- **Message Bubbles**: Different styles for sent/received messages
- **Avatar Placeholders**: Colorful gradient avatars with initials

### Color Scheme
- Primary: Purple (#667eea)
- Secondary: Deep Purple (#764ba2)
- Accent: Pink to Purple gradient
- Background: Gradient from primary to secondary

## 🧪 Testing

### Test Real-time Chat
1. Open two different browsers or incognito windows
2. Login with different users in each window
3. Start a conversation
4. Send messages and observe real-time updates
5. Try typing to see typing indicators
6. Check online/offline status updates

### Test Features
- Create one-on-one conversations
- Create group conversations
- Send multiple messages
- Check unread counts
- Test mark as read functionality
- Verify statistics update in real-time

## 🔧 Technology Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework 3.14** - REST API
- **Django Channels 4.0** - WebSocket support
- **PyJWT 2.8** - Custom JWT authentication
- **channels-redis** - Redis channel layer
- **django-cors-headers** - CORS handling

### Frontend
- **React 18.2** - UI library
- **React Router 6.20** - Routing
- **Axios 1.6** - HTTP client
- **Tailwind CSS** - Styling (via custom CSS)
- **WebSocket API** - Real-time communication

### Database
- **SQLite** - Development database (can be replaced with PostgreSQL)

### Cache/Message Broker
- **Redis** - WebSocket channel layer

## 📝 Development Notes

### WebSocket Authentication
JWT tokens are passed via query parameters for WebSocket connections:
```javascript
ws://localhost:8000/ws/chat/{conversation_id}/?token={access_token}
```

### CORS Configuration
The backend is configured to accept requests from `http://localhost:3000` by default. Update `CORS_ALLOWED_ORIGINS` in settings for production.

### Channel Layers
The application uses Redis for channel layers in production. For development without Redis, set `USE_MEMORY_CHANNELS=True` in the environment variables.

### Token Refresh
The frontend automatically refreshes JWT tokens when they expire, providing a seamless user experience.

## 🚀 Production Deployment

### Backend
1. Set `DEBUG=False` in production
2. Use a production database (PostgreSQL recommended)
3. Set up proper `SECRET_KEY`
4. Configure allowed hosts
5. Set up Redis for channel layers
6. Use a production ASGI server (Daphne, Uvicorn)
7. Set up static file serving
8. Configure HTTPS for secure WebSocket (wss://)

### Frontend
1. Update API URLs in `.env`
2. Build for production: `npm run build`
3. Serve build files with Nginx or similar
4. Configure HTTPS

## 🤝 Contributing

This is a demo project showcasing full-stack development skills. Feel free to use it as a template for your own projects!

## 📄 License

MIT License - Feel free to use this project for learning and development.

## 👨‍💻 Author

Built with ❤️ to demonstrate modern web development practices.

---

**Happy Chatting! 💬**

