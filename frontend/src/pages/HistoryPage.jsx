import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import { Calendar, MessageCircle, Award, Trash2, Eye } from 'lucide-react';

export default function HistoryPage() {
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = () => {
    const stored = localStorage.getItem('sessions');
    if (stored) {
      setSessions(JSON.parse(stored).reverse()); // Most recent first
    }
  };

  const deleteSession = (sessionId) => {
    if (!confirm('Delete this conversation?')) return;
    
    const updated = sessions.filter(s => s.id !== sessionId);
    localStorage.setItem('sessions', JSON.stringify(updated));
    setSessions(updated);
    if (selectedSession?.id === sessionId) {
      setSelectedSession(null);
    }
  };

  const clearAllHistory = () => {
    if (!confirm('Delete ALL conversation history? This cannot be undone.')) return;
    
    localStorage.removeItem('sessions');
    localStorage.removeItem('currentSession');
    setSessions([]);
    setSelectedSession(null);
  };

  const scenarioEmojis = {
    restaurant: '🍽️',
    shopping: '👕',
    hotel: '🏨',
    job_interview: '💼',
    free: '🗣️'
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-4xl font-bold">📜 Conversation History</h1>
        {sessions.length > 0 && (
          <button 
            onClick={clearAllHistory}
            className="btn-secondary text-sm py-2 px-4 text-red-600 hover:border-red-500"
          >
            <Trash2 className="w-4 h-4 inline mr-2" />
            Clear All
          </button>
        )}
      </div>

      {sessions.length === 0 ? (
        <div className="card text-center py-20">
          <div className="text-6xl mb-4">📭</div>
          <h2 className="text-2xl font-bold mb-2 text-gray-700">No Conversations Yet</h2>
          <p className="text-gray-600 mb-6">Start practicing to build your conversation history!</p>
          <a href="/practice" className="btn-primary inline-block">
            Start Your First Conversation
          </a>
        </div>
      ) : (
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Sessions List */}
          <div className="lg:col-span-1 space-y-4">
            {sessions.map((session) => (
              <div
                key={session.id}
                onClick={() => setSelectedSession(session)}
                className={`card cursor-pointer transition-all ${
                  selectedSession?.id === session.id 
                    ? 'ring-2 ring-blue-500 bg-blue-50' 
                    : 'hover:shadow-xl'
                }`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span className="text-3xl">{scenarioEmojis[session.scenario_id] || '🗣️'}</span>
                    <div>
                      <h3 className="font-bold text-lg">
                        {session.scenario_id.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </h3>
                      <p className="text-xs text-gray-500 flex items-center gap-1">
                        <Calendar className="w-3 h-3" />
                        {format(new Date(session.created_at), 'MMM dd, yyyy HH:mm')}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      deleteSession(session.id);
                    }}
                    className="text-gray-400 hover:text-red-500"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
                
                <div className="flex items-center justify-between text-sm">
                  <span className="flex items-center gap-1 text-gray-600">
                    <MessageCircle className="w-4 h-4" />
                    {session.turns || 0} turns
                  </span>
                  {session.completed && (
                    <span className="flex items-center gap-1 text-green-600 font-semibold">
                      <Award className="w-4 h-4" />
                      Completed
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Session Details */}
          <div className="lg:col-span-2">
            {selectedSession ? (
              <div className="card">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold flex items-center gap-2">
                    <span className="text-3xl">{scenarioEmojis[selectedSession.scenario_id]}</span>
                    Session Details
                  </h2>
                  {selectedSession.completed && (
                    <span className="bg-green-100 text-green-700 px-4 py-2 rounded-full text-sm font-semibold">
                      ✅ Completed
                    </span>
                  )}
                </div>

                {/* Session Info */}
                <div className="grid grid-cols-2 gap-4 mb-6 p-4 bg-gray-50 rounded-xl">
                  <div>
                    <p className="text-sm text-gray-600">Scenario</p>
                    <p className="font-semibold">{selectedSession.scenario_id.replace('_', ' ').toUpperCase()}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Date</p>
                    <p className="font-semibold">{format(new Date(selectedSession.created_at), 'MMM dd, yyyy')}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Turns</p>
                    <p className="font-semibold">{selectedSession.turns || 0}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Status</p>
                    <p className="font-semibold">{selectedSession.completed ? 'Completed' : 'In Progress'}</p>
                  </div>
                </div>

                {/* Conversation */}
                {selectedSession.opening && (
                  <div className="space-y-4">
                    <h3 className="font-bold text-lg">💬 Conversation</h3>
                    
                    {/* Coach Opening */}
                    <div className="message-coach">
                      <div className="flex items-start gap-3">
                        <div className="text-2xl">🤖</div>
                        <div>
                          <div className="font-semibold text-sm text-purple-700 mb-1">Coach</div>
                          <p className="text-gray-800">{selectedSession.opening}</p>
                        </div>
                      </div>
                    </div>

                    {/* Turns */}
                    {selectedSession.conversation && selectedSession.conversation.map((turn, index) => (
                      <div key={index} className="space-y-3">
                        <div className="message-user">
                          <div className="flex items-start gap-3 justify-end">
                            <div className="text-right">
                              <div className="font-semibold text-sm text-blue-700 mb-1">You</div>
                              <p className="text-gray-800">{turn.user}</p>
                            </div>
                            <div className="text-2xl">🧑</div>
                          </div>
                        </div>
                        <div className="message-coach">
                          <div className="flex items-start gap-3">
                            <div className="text-2xl">🤖</div>
                            <div>
                              <div className="font-semibold text-sm text-purple-700 mb-1">Coach</div>
                              <p className="text-gray-800">{turn.coach}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <div className="card text-center py-20">
                <Eye className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-bold text-gray-700 mb-2">Select a Session</h3>
                <p className="text-gray-600">Click on a conversation from the list to view details</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
