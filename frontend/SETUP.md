# Frontend Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env` file:
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_WS_URL=localhost:8000
```

### 3. Install Tailwind CSS

The project uses Tailwind CSS. Make sure to install it:

```bash
npm install -D tailwindcss postcss autoprefixer
```

If you need to regenerate the Tailwind config:
```bash
npx tailwindcss init
```

### 4. Start Development Server

```bash
npm start
```

Frontend available at: `http://localhost:3000`

## Development

### Project Structure

```
src/
├── components/        # Reusable UI components
├── pages/            # Page components (routes)
├── context/          # React Context (state management)
├── services/         # API service layer
├── utils/            # Helper functions
├── App.js            # Main app component
└── index.css         # Global styles
```

### Key Components

- **Navbar**: Top navigation with user menu
- **StatsCard**: Dashboard statistics display
- **ConversationList**: List of conversations with preview
- **ChatWindow**: Main chat interface with real-time messaging
- **NewConversationModal**: Create new conversations

### State Management

Uses React Context API for:
- **AuthContext**: User authentication state
- Component-level state with useState hooks

### API Integration

All API calls are centralized in `src/services/api.js`:
- Axios instance with interceptors
- Automatic token refresh
- WebSocket connection helper

## Building for Production

```bash
npm run build
```

Build files will be in the `build/` directory.

## Common Issues

### Tailwind Styles Not Working

Make sure `tailwind.config.js` has the correct content paths:
```javascript
content: ["./src/**/*.{js,jsx,ts,tsx}"]
```

### API Connection Errors

1. Check if backend is running on port 8000
2. Verify `.env` file has correct API URL
3. Check CORS settings in Django

### WebSocket Not Connecting

1. Make sure Django Channels is running
2. Check Redis is running (if not using in-memory)
3. Verify JWT token is being passed correctly
4. Check browser console for WebSocket errors

### npm install Errors

Try clearing npm cache:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance Tips

- Messages are paginated to prevent loading issues
- WebSocket connections are closed when component unmounts
- Images/avatars can be optimized with lazy loading
- Consider implementing virtual scrolling for large conversation lists

