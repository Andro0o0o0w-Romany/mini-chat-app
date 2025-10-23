import React, { useState, useEffect, useRef, useCallback } from 'react';
import { chatAPI, getWebSocketURL } from '../services/api';
import { formatMessageTime, formatDateSeparator, isSameDay, formatFullDate } from '../utils/dateUtils';

const ChatWindow = ({ conversation, user, onMessageSent }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [typingUsers, setTypingUsers] = useState(new Set());
  const messagesEndRef = useRef(null);
  const typingTimeoutRef = useRef(null);
  const wsRef = useRef(null);

  const loadMessages = useCallback(async () => {
    try {
      setLoading(true);
      const response = await chatAPI.getMessages(conversation.id);
      
      // Handle DRF pagination - data might be in 'results' key
      let messagesData = response.data;
      if (messagesData && typeof messagesData === 'object' && 'results' in messagesData) {
        messagesData = messagesData.results;
      }
      
      // Ensure messagesData is an array and reverse to show oldest first
      const messages = Array.isArray(messagesData) ? messagesData : [];
      setMessages(messages.reverse());
      
      // Mark conversation as read
      await chatAPI.markConversationRead(conversation.id);
    } catch (error) {
      console.error('Error loading messages:', error);
      setMessages([]); // Reset to empty array on error
    } finally {
      setLoading(false);
    }
  }, [conversation.id]);

  const connectWebSocket = useCallback(() => {
    const token = localStorage.getItem('access_token');
    const wsURL = getWebSocketURL(conversation.id, token);
    
    const websocket = new WebSocket(wsURL);

    websocket.onopen = () => {
      console.log('WebSocket connected');
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'message') {
        setMessages((prev) => [...prev, data.message]);
        onMessageSent();
      } else if (data.type === 'typing') {
        if (data.is_typing) {
          setTypingUsers((prev) => new Set(prev).add(data.username));
        } else {
          setTypingUsers((prev) => {
            const newSet = new Set(prev);
            newSet.delete(data.username);
            return newSet;
          });
        }
      } else if (data.type === 'user_status') {
        console.log(`User ${data.username} is ${data.is_online ? 'online' : 'offline'}`);
      }
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    websocket.onclose = () => {
      console.log('WebSocket disconnected');
    };

    wsRef.current = websocket;
  }, [conversation.id, onMessageSent]);

  useEffect(() => {
    loadMessages();
    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (typingTimeoutRef.current) {
        clearTimeout(typingTimeoutRef.current);
      }
    };
  }, [conversation.id, loadMessages, connectWebSocket]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    
    if (!newMessage.trim() || !wsRef.current) return;

    wsRef.current.send(JSON.stringify({
      type: 'message',
      content: newMessage.trim(),
    }));

    setNewMessage('');
    
    // Stop typing indicator
    wsRef.current.send(JSON.stringify({
      type: 'typing',
      is_typing: false,
    }));
  };

  const handleTyping = (e) => {
    setNewMessage(e.target.value);

    if (!wsRef.current) return;

    // Send typing indicator
    wsRef.current.send(JSON.stringify({
      type: 'typing',
      is_typing: true,
    }));

    // Clear previous timeout
    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current);
    }

    // Stop typing after 2 seconds of inactivity
    typingTimeoutRef.current = setTimeout(() => {
      if (wsRef.current) {
        wsRef.current.send(JSON.stringify({
          type: 'typing',
          is_typing: false,
        }));
      }
    }, 2000);
  };

  const getConversationName = () => {
    if (conversation.name) {
      return conversation.name;
    }
    
    if (conversation.other_participants && conversation.other_participants.length > 0) {
      return conversation.other_participants
        .map(p => p.full_name || p.username)
        .join(', ');
    }
    
    return 'Conversation';
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex-shrink-0 px-4 py-3 border-b border-gray-200 bg-white">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-full bg-gradient-to-r from-primary-500 to-secondary-500 flex items-center justify-center text-white font-semibold text-sm">
              {getConversationName().charAt(0).toUpperCase()}
            </div>
            <div>
              <h3 className="font-semibold text-gray-800 text-sm">{getConversationName()}</h3>
              <p className="text-xs text-gray-500">
                {conversation.participants_count} participants
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 pb-6 bg-gray-50">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-400">
            <div className="text-4xl mb-2">💬</div>
            <p>No messages yet. Start the conversation!</p>
          </div>
        ) : (
          messages.map((message, index) => {
            const isOwnMessage = message.sender === user.id;
            const showDateSeparator = index === 0 || !isSameDay(message.created_at, messages[index - 1].created_at);
            
            return (
              <React.Fragment key={message.id}>
                {/* Date Separator */}
                {showDateSeparator && (
                  <div className="flex justify-center my-4">
                    <div className="bg-gray-200 text-gray-600 text-xs font-medium px-4 py-1 rounded-full shadow-sm">
                      {formatDateSeparator(message.created_at)}
                    </div>
                  </div>
                )}
                
                {/* Message */}
                <div
                  className={`flex mb-3 ${isOwnMessage ? 'justify-end' : 'justify-start'} ${
                    isOwnMessage ? 'message-right' : 'message-left'
                  }`}
                >
                  <div className={`max-w-xs lg:max-w-md ${isOwnMessage ? 'order-2' : 'order-1'}`}>
                    {!isOwnMessage && (
                      <p className="text-xs font-medium text-gray-600 mb-1 ml-2">
                        {message.sender_name || message.sender_username}
                      </p>
                    )}
                    <div
                      className={`rounded-2xl px-4 py-2 shadow-sm ${
                        isOwnMessage
                          ? 'bg-gradient-to-r from-primary-500 to-secondary-500 text-white'
                          : 'bg-white text-gray-800'
                      }`}
                    >
                      <p className="break-words mb-1">{message.content}</p>
                      <div className="flex items-center justify-between gap-2">
                        <p
                          className={`text-xs ${
                            isOwnMessage ? 'text-primary-100' : 'text-gray-500'
                          }`}
                          title={formatFullDate(message.created_at)}
                        >
                          {formatMessageTime(message.created_at)}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </React.Fragment>
            );
          })
        )}
        
        {/* Typing Indicator */}
        {typingUsers.size > 0 && (
          <div className="flex justify-start">
            <div className="bg-white rounded-2xl px-4 py-2 shadow">
              <div className="typing-indicator">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="flex-shrink-0 p-3 bg-white border-t border-gray-200">
        <form onSubmit={handleSendMessage} className="flex items-center space-x-2">
          <input
            type="text"
            value={newMessage}
            onChange={handleTyping}
            placeholder="Type a message..."
            className="flex-1 px-4 py-2.5 border border-gray-300 rounded-full focus:ring-2 focus:ring-primary-500 focus:border-transparent transition text-sm"
          />
          <button
            type="submit"
            disabled={!newMessage.trim()}
            className="bg-gradient-to-r from-primary-500 to-secondary-500 text-white p-2.5 rounded-full hover:shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
              />
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatWindow;

