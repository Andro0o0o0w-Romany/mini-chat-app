import React, { useState, useEffect } from 'react';
import { authAPI } from '../services/api';

const NewConversationModal = ({ onClose, onCreate }) => {
  const [users, setUsers] = useState([]);
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [conversationName, setConversationName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Safety check: ensure users is always an array
  const userList = Array.isArray(users) ? users : [];

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const response = await authAPI.getUsers();
      
      // Handle DRF pagination - data might be in 'results' key
      let usersData = response.data;
      if (usersData && typeof usersData === 'object' && 'results' in usersData) {
        usersData = usersData.results;
      }
      
      // Ensure users is always an array
      setUsers(Array.isArray(usersData) ? usersData : []);
      setError(''); // Clear any previous errors
    } catch (error) {
      console.error('Error loading users:', error);
      setError('Failed to load users. Please try again.');
      // Reset to empty array on error
      setUsers([]);
    } finally {
      setLoading(false);
    }
  };

  const handleUserToggle = (userId) => {
    setSelectedUsers((prev) =>
      prev.includes(userId)
        ? prev.filter((id) => id !== userId)
        : [...prev, userId]
    );
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (selectedUsers.length === 0) {
      setError('Please select at least one user');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      const conversationData = {
        participant_ids: selectedUsers,
        is_group: selectedUsers.length > 1,
      };

      if (selectedUsers.length > 1 && conversationName.trim()) {
        conversationData.name = conversationName.trim();
      }

      await onCreate(conversationData);
    } catch (error) {
      setError('Failed to create conversation');
      console.error('Error creating conversation:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6 fade-in">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">New Conversation</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-3 mb-4 rounded">
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Group Name (optional for group chats) */}
          {selectedUsers.length > 1 && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Group Name (Optional)
              </label>
              <input
                type="text"
                value={conversationName}
                onChange={(e) => setConversationName(e.target.value)}
                placeholder="Enter group name"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
              />
            </div>
          )}

          {/* User Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Users
            </label>
            <div className="max-h-64 overflow-y-auto border border-gray-200 rounded-lg">
              {loading ? (
                <div className="flex items-center justify-center py-8">
                  <div className="spinner"></div>
                </div>
              ) : userList.length === 0 ? (
                <p className="text-center text-gray-500 py-4">No users available</p>
              ) : (
                userList.map((user) => (
                  <label
                    key={user.id}
                    className="flex items-center space-x-3 p-3 hover:bg-gray-50 cursor-pointer border-b last:border-b-0"
                  >
                    <input
                      type="checkbox"
                      checked={selectedUsers.includes(user.id)}
                      onChange={() => handleUserToggle(user.id)}
                      className="w-5 h-5 text-primary-500 rounded focus:ring-primary-500"
                    />
                    <div className="w-10 h-10 rounded-full bg-gradient-to-r from-primary-500 to-secondary-500 flex items-center justify-center text-white font-semibold">
                      {user.username.charAt(0).toUpperCase()}
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-gray-800">
                        {user.full_name || user.username}
                      </p>
                      <p className="text-sm text-gray-500">{user.email}</p>
                    </div>
                  </label>
                ))
              )}
            </div>
          </div>

          {/* Selected Count */}
          {selectedUsers.length > 0 && (
            <p className="text-sm text-gray-600">
              {selectedUsers.length} user{selectedUsers.length > 1 ? 's' : ''} selected
            </p>
          )}

          {/* Actions */}
          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || selectedUsers.length === 0}
              className="flex-1 px-4 py-2 bg-gradient-to-r from-primary-500 to-secondary-500 text-white rounded-lg hover:shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Creating...' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default NewConversationModal;

