import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { chatAPI } from '../services/api';
import Navbar from '../components/Navbar';
import StatsCard from '../components/StatsCard';
import ConversationList from '../components/ConversationList';
import ChatWindow from '../components/ChatWindow';
import NewConversationModal from '../components/NewConversationModal';
import Toast from '../components/Toast';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    total_conversations: 0,
    total_messages_sent: 0,
    total_unread: 0,
    recent_conversations: [],
  });
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showNewConversation, setShowNewConversation] = useState(false);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [statsRes, conversationsRes] = await Promise.all([
        chatAPI.getStats(),
        chatAPI.getConversations(),
      ]);
      
      setStats(statsRes.data);
      
      // Handle DRF pagination - data might be in 'results' key
      let conversationsData = conversationsRes.data;
      if (conversationsData && typeof conversationsData === 'object' && 'results' in conversationsData) {
        conversationsData = conversationsData.results;
      }
      
      // Ensure conversations is always an array
      setConversations(Array.isArray(conversationsData) ? conversationsData : []);
    } catch (error) {
      console.error('Error loading data:', error);
      // Reset to empty arrays on error
      setConversations([]);
      setStats({
        total_conversations: 0,
        total_messages_sent: 0,
        total_unread: 0,
        recent_conversations: [],
      });
    } finally {
      setLoading(false);
    }
  };

  const handleConversationSelect = (conversation) => {
    setSelectedConversation(conversation);
  };

  const handleNewConversation = async (conversationData) => {
    try {
      const response = await chatAPI.createConversation(conversationData);
      const conversation = response.data;
      
      // Check if this is an existing conversation
      if (conversation.is_existing) {
        // Find the conversation in the current list
        const existingInList = conversations.find(c => c.id === conversation.id);
        
        if (existingInList) {
          // Just select it if it's already in the list
          setSelectedConversation(existingInList);
        } else {
          // Add it to the list if it's not there (shouldn't happen, but handle it)
          setConversations([conversation, ...conversations]);
          setSelectedConversation(conversation);
        }
        
        // Show a notification to the user
        setToast({
          message: 'A conversation with this user already exists. Opening existing conversation...',
          type: 'info'
        });
      } else {
        // This is a new conversation, add it to the list
        setConversations([conversation, ...conversations]);
        setSelectedConversation(conversation);
        
        // Show success notification
        setToast({
          message: 'New conversation created successfully!',
          type: 'success'
        });
      }
      
      setShowNewConversation(false);
      loadData(); // Refresh stats
    } catch (error) {
      console.error('Error creating conversation:', error);
      throw error;
    }
  };

  const handleMessageSent = () => {
    loadData(); // Refresh conversations and stats
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="container mx-auto px-4 py-6">
        {/* Stats Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <StatsCard
            title="Total Conversations"
            value={stats.total_conversations}
            icon="💬"
            color="primary"
          />
          <StatsCard
            title="Messages Sent"
            value={stats.total_messages_sent}
            icon="📨"
            color="secondary"
          />
          <StatsCard
            title="Unread Messages"
            value={stats.total_unread}
            icon="🔔"
            color="accent"
          />
        </div>

        {/* Main Chat Interface */}
        <div className="bg-white rounded-2xl shadow-lg overflow-hidden" style={{ height: 'calc(100vh - 280px)', minHeight: '500px' }}>
          <div className="grid grid-cols-12 h-full">
            {/* Conversations List */}
            <div className="col-span-12 md:col-span-4 border-r border-gray-200 h-full overflow-hidden">
              <ConversationList
                conversations={conversations}
                selectedConversation={selectedConversation}
                onSelect={handleConversationSelect}
                onNewConversation={() => setShowNewConversation(true)}
              />
            </div>

            {/* Chat Window */}
            <div className="col-span-12 md:col-span-8 h-full overflow-hidden">
              {selectedConversation ? (
                <ChatWindow
                  conversation={selectedConversation}
                  user={user}
                  onMessageSent={handleMessageSent}
                />
              ) : (
                <div className="h-full flex items-center justify-center text-gray-400">
                  <div className="text-center">
                    <div className="text-6xl mb-4">💭</div>
                    <p className="text-xl">Select a conversation to start chatting</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* New Conversation Modal */}
      {showNewConversation && (
        <NewConversationModal
          onClose={() => setShowNewConversation(false)}
          onCreate={handleNewConversation}
        />
      )}

      {/* Toast Notification */}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
};

export default Dashboard;

