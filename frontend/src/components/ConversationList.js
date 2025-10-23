import React from 'react';
import { formatDistanceToNow } from '../utils/dateUtils';

const ConversationList = ({ conversations, selectedConversation, onSelect, onNewConversation }) => {
  // Safety check: ensure conversations is an array
  const conversationList = Array.isArray(conversations) ? conversations : [];
  
  const getConversationName = (conversation) => {
    if (conversation.name) {
      return conversation.name;
    }
    
    if (conversation.other_participants && conversation.other_participants.length > 0) {
      return conversation.other_participants
        .map(p => p.full_name || p.username)
        .join(', ');
    }
    
    return 'New Conversation';
  };

  const getConversationAvatar = (conversation) => {
    if (conversation.other_participants && conversation.other_participants.length > 0) {
      return conversation.other_participants[0].username.charAt(0).toUpperCase();
    }
    return '?';
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex justify-between items-center mb-3">
          <h2 className="text-xl font-bold text-gray-800">Conversations</h2>
          <button
            onClick={onNewConversation}
            className="bg-gradient-to-r from-primary-500 to-secondary-500 text-white p-2 rounded-lg hover:shadow-lg transition"
            title="New Conversation"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
          </button>
        </div>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto">
        {conversationList.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-400 p-4">
            <div className="text-4xl mb-2">💬</div>
            <p className="text-center">No conversations yet</p>
            <button
              onClick={onNewConversation}
              className="mt-4 text-primary-500 hover:text-primary-600 font-semibold"
            >
              Start a new conversation
            </button>
          </div>
        ) : (
          conversationList.map((conversation) => (
            <div
              key={conversation.id}
              onClick={() => onSelect(conversation)}
              className={`p-4 border-b border-gray-100 cursor-pointer transition-all duration-200 ${
                selectedConversation?.id === conversation.id 
                  ? 'bg-primary-50 border-l-4 border-l-primary-500 shadow-sm' 
                  : 'hover:bg-gray-50 border-l-4 border-l-transparent'
              }`}
            >
              <div className="flex items-start space-x-3">
                {/* Avatar */}
                <div className="w-12 h-12 rounded-full bg-gradient-to-r from-primary-500 to-secondary-500 flex items-center justify-center text-white font-semibold flex-shrink-0">
                  {getConversationAvatar(conversation)}
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex justify-between items-start mb-1">
                    <h3 className="font-semibold text-gray-800 truncate">
                      {getConversationName(conversation)}
                    </h3>
                    {conversation.last_message_preview && (
                      <span className="text-xs text-gray-500 ml-2 flex-shrink-0">
                        {formatDistanceToNow(conversation.last_message_preview.created_at)}
                      </span>
                    )}
                  </div>

                  {conversation.last_message_preview ? (
                    <p className="text-sm text-gray-600 truncate">
                      <span className="font-medium">
                        {conversation.last_message_preview.sender}:
                      </span>{' '}
                      {conversation.last_message_preview.content}
                    </p>
                  ) : (
                    <p className="text-sm text-gray-400 italic">No messages yet</p>
                  )}

                  {conversation.unread_count > 0 && (
                    <div className="mt-1">
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-primary-500 text-white">
                        {conversation.unread_count} new
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ConversationList;

