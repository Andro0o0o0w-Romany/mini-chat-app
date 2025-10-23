# Mini Chat System - Architecture Documentation

## System Overview

This is a modern, real-time chat application built with a decoupled architecture:
- **Backend**: Django REST Framework with Django Channels for WebSocket support
- **Frontend**: React with modern hooks and context API
- **Real-time**: WebSocket connections for instant messaging
- **Authentication**: JWT tokens for secure API access

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Dashboard  │  │ Chat Window  │  │ Conversation │          │
│  │  Statistics  │  │  WebSocket   │  │     List     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│           │                 │                  │                 │
│           └─────────────────┼──────────────────┘                │
│                             │                                    │
│                    ┌────────▼────────┐                          │
│                    │   API Service   │                          │
│                    │  (Axios + WS)   │                          │
│                    └────────┬────────┘                          │
└─────────────────────────────┼───────────────────────────────────┘
                              │
                    HTTP/HTTPS│WebSocket
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      Backend (Django)                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │     REST     │  │   WebSocket  │  │     Auth     │          │
│  │   Endpoints  │  │   Consumer   │  │   Middleware │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                  │                   │
│         └─────────────────┼──────────────────┘                  │
│                           │                                      │
│                  ┌────────▼────────┐                            │
│                  │   Django ORM    │                            │
│                  └────────┬────────┘                            │
│                           │                                      │
│         ┌─────────────────┼─────────────────┐                  │
│         │                 │                 │                   │
│    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐              │
│    │  User   │      │  Conv   │      │ Message │              │
│    │  Model  │      │  Model  │      │  Model  │              │
│    └─────────┘      └─────────┘      └─────────┘              │
└──────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
              ┌─────▼─────┐       ┌─────▼─────┐
              │  SQLite   │       │   Redis   │
              │  Database │       │  Channels │
              └───────────┘       └───────────┘
```

## Component Architecture

### Frontend Components

#### 1. **Pages**
- **Login/Register**: Authentication forms with validation
- **Dashboard**: Main application interface with stats, conversations, and chat

#### 2. **Components**
- **Navbar**: User menu and navigation
- **StatsCard**: Display key metrics (conversations, messages, unread)
- **ConversationList**: Scrollable list of conversations with previews
- **ChatWindow**: Real-time messaging interface with WebSocket
- **NewConversationModal**: Create new 1-on-1 or group conversations

#### 3. **Context**
- **AuthContext**: Global authentication state management
  - User information
  - Login/logout functions
  - Token management

#### 4. **Services**
- **API Service**: Centralized API calls
  - Axios instance with interceptors
  - Automatic token refresh
  - WebSocket URL generation

### Backend Architecture

#### 1. **Apps**

##### Accounts App
- Custom User model with additional fields
- JWT authentication endpoints
- User profile management

##### Chat App
- Conversation model (1-on-1 and group)
- Message model with timestamps
- Participant model for conversation membership
- WebSocket consumer for real-time chat

#### 2. **API Endpoints**

**Authentication** (`/api/auth/`)
- `POST /token/` - Login (get JWT)
- `POST /token/refresh/` - Refresh token
- `POST /register/` - Register new user
- `POST /logout/` - Logout
- `GET /me/` - Get current user
- `PATCH /me/` - Update profile
- `GET /users/` - List all users

**Chat** (`/api/chat/`)
- `GET /conversations/` - List conversations
- `POST /conversations/` - Create conversation
- `GET /conversations/{id}/` - Get conversation
- `GET /conversations/stats/` - Dashboard stats
- `POST /conversations/{id}/mark_read/` - Mark as read
- `GET /messages/?conversation={id}` - Get messages
- `POST /messages/` - Send message

**WebSocket**
- `ws://host/ws/chat/{id}/?token={jwt}` - Real-time chat

#### 3. **WebSocket Flow**

```
Client                          Server
  │                               │
  ├─ Connect (with JWT token) ──>│
  │                               ├─ Authenticate
  │                               ├─ Join room group
  │<────── Connection accepted ───┤
  │                               │
  ├─ Send message ───────────────>│
  │                               ├─ Save to DB
  │                               ├─ Broadcast to group
  │<────── Message received ──────┤
  │                               │
  ├─ Send typing indicator ──────>│
  │                               ├─ Broadcast typing
  │<────── Typing indicator ──────┤
  │                               │
  ├─ Disconnect ─────────────────>│
  │                               ├─ Update online status
  │                               └─ Leave room group
```

## Data Models

### User Model
```python
- id (PK)
- username (unique)
- email (unique)
- password (hashed)
- first_name
- last_name
- avatar (ImageField)
- bio
- is_online
- last_seen
- created_at
- updated_at
```

### Conversation Model
```python
- id (PK)
- name (optional, for groups)
- is_group (boolean)
- created_by (FK -> User)
- created_at
- updated_at
```

### Participant Model
```python
- id (PK)
- conversation (FK -> Conversation)
- user (FK -> User)
- joined_at
- last_read_at
```

### Message Model
```python
- id (PK)
- conversation (FK -> Conversation)
- sender (FK -> User)
- content (text)
- is_read (boolean)
- created_at
- updated_at
```

## Real-time Communication

### WebSocket Message Types

#### 1. **Chat Message**
```json
{
  "type": "message",
  "content": "Hello world"
}
```

#### 2. **Typing Indicator**
```json
{
  "type": "typing",
  "is_typing": true
}
```

#### 3. **User Status**
```json
{
  "type": "user_status",
  "user_id": 1,
  "username": "alice",
  "is_online": true
}
```

## Security

### Authentication Flow

1. **Registration/Login**
   - User submits credentials
   - Server validates and returns JWT tokens (access + refresh)
   - Tokens stored in localStorage

2. **API Requests**
   - Access token sent in Authorization header
   - Token validated by custom JWTAuthentication class
   - User identified from token

3. **Token Refresh**
   - Access token expires (24 hours)
   - Frontend intercepts 401 error
   - Automatically refreshes using refresh token
   - Refresh token expires (7 days)

4. **WebSocket Authentication**
   - JWT token passed in query parameter
   - Custom middleware validates token
   - Connection accepted if valid

### Security Features

- ✅ Password hashing (Django's PBKDF2)
- ✅ JWT token authentication
- ✅ Token refresh mechanism
- ✅ CORS protection
- ✅ CSRF protection (for forms)
- ✅ SQL injection protection (ORM)
- ✅ XSS protection (React escaping)
- ✅ Secure WebSocket with token validation

## Performance Optimizations

### Backend
- Database query optimization with `select_related()` and `prefetch_related()`
- Message pagination (50 per page)
- Redis for WebSocket channel layers (scalable)
- Efficient WebSocket room grouping

### Frontend
- Component-level state management (avoid unnecessary re-renders)
- Lazy loading of conversations
- Optimistic UI updates
- WebSocket connection reuse
- Debounced typing indicators

## Scalability Considerations

### Horizontal Scaling
- **Backend**: Multiple Django servers behind load balancer
- **Redis**: Redis cluster for channel layers
- **Database**: Read replicas for query distribution
- **Static Files**: CDN for media/static files

### Vertical Scaling
- **Database**: PostgreSQL with connection pooling
- **Redis**: Increased memory for channel layers
- **WebSocket**: Daphne with multiple workers

## Deployment Architecture

```
                    ┌─────────────┐
                    │   Browser   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Nginx     │
                    │   (Reverse  │
                    │   Proxy)    │
                    └──┬───────┬──┘
                       │       │
        Static Files   │       │  API/WS
            ┌──────────┘       └──────────┐
            │                             │
    ┌───────▼───────┐            ┌────────▼────────┐
    │  React Build  │            │  Daphne (ASGI)  │
    │  (Static)     │            │  Django Channels│
    └───────────────┘            └────────┬────────┘
                                          │
                            ┌─────────────┼─────────────┐
                            │             │             │
                      ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
                      │PostgreSQL │ │   Redis   │ │   Media   │
                      └───────────┘ └───────────┘ └───────────┘
```

## Technology Choices

### Why Django Channels?
- Native WebSocket support for Django
- Integrates with Django ORM and auth
- Scalable with Redis backend
- Battle-tested in production

### Why React?
- Component-based architecture
- Virtual DOM for performance
- Large ecosystem
- Easy WebSocket integration

### Why JWT?
- Stateless authentication
- Works across domains
- Mobile-friendly
- Easily refreshable

### Why Redis?
- Fast in-memory data store
- Pub/sub for WebSocket messages
- Scalable channel layer
- Simple setup

## Future Enhancements

1. **File Sharing**: Upload images/documents in chat
2. **Voice/Video**: WebRTC integration
3. **Push Notifications**: Browser/mobile notifications
4. **Search**: Full-text search for messages
5. **Reactions**: Emoji reactions to messages
6. **Read Receipts**: Show when messages are read
7. **Message Editing**: Edit/delete sent messages
8. **User Presence**: More detailed online status
9. **Threads**: Reply to specific messages
10. **Encryption**: End-to-end encryption for messages

## Development Best Practices

### Backend
- Use serializers for all API responses
- Keep views thin, logic in models/services
- Write tests for critical paths
- Use proper error handling
- Log important events
- Document API endpoints

### Frontend
- Component reusability
- Proper error boundaries
- Loading and error states
- Responsive design
- Accessibility (ARIA labels)
- Clean code structure

## Testing Strategy

### Backend Tests
- Model tests (data validation)
- API endpoint tests (DRF TestCase)
- WebSocket consumer tests (ChannelsLiveServerTestCase)
- Authentication tests

### Frontend Tests
- Component unit tests (Jest)
- Integration tests (React Testing Library)
- E2E tests (Cypress)

## Monitoring & Logging

### Backend
- Django logging framework
- Error tracking (Sentry)
- Performance monitoring (New Relic)
- Database query monitoring

### Frontend
- Browser console errors
- React error boundaries
- Performance monitoring (Web Vitals)
- User analytics

---

This architecture provides a solid foundation for a production-ready chat application while maintaining simplicity and readability.

