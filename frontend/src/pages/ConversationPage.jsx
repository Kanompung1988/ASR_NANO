import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { Mic, Square, Send, Loader, CheckCircle, XCircle, RotateCcw, Volume2, Info } from 'lucide-react';

export default function ConversationPage() {
  const location = useLocation();
  const [scenarios, setScenarios] = useState([]);
  const [selectedScenario, setSelectedScenario] = useState(location.state?.selectedScenario || 'free');
  const [conversationStarted, setConversationStarted] = useState(false);
  const [coachOpening, setCoachOpening] = useState('');
  const [conversationHistory, setConversationHistory] = useState([]);
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [conversationComplete, setConversationComplete] = useState(false);
  const [finalEvaluation, setFinalEvaluation] = useState('');
  const [recordingTime, setRecordingTime] = useState(0);
  const [error, setError] = useState('');
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const messagesEndRef = useRef(null);
  const recordingIntervalRef = useRef(null);

  // Load scenarios
  useEffect(() => {
    axios.get('/api/scenarios')
      .then(res => setScenarios(res.data.scenarios))
      .catch(err => {
        console.error('Error loading scenarios:', err);
        setError('Failed to load scenarios. Please refresh the page.');
      });
  }, []);

  // Recording timer
  useEffect(() => {
    if (isRecording) {
      setRecordingTime(0);
      recordingIntervalRef.current = setInterval(() => {
        setRecordingTime(t => t + 1);
      }, 1000);
    } else {
      if (recordingIntervalRef.current) {
        clearInterval(recordingIntervalRef.current);
      }
      setRecordingTime(0);
    }
    return () => {
      if (recordingIntervalRef.current) {
        clearInterval(recordingIntervalRef.current);
      }
    };
  }, [isRecording]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [conversationHistory]);

  // Start conversation
  const handleStartConversation = async () => {
    setIsProcessing(true);
    setError('');
    try {
      const response = await axios.post('/api/conversation/start', {
        scenario_id: selectedScenario
      });
      setCoachOpening(response.data.opening_message);
      setConversationStarted(true);
      
      // Save to localStorage
      const session = {
        id: Date.now().toString(),
        scenario_id: selectedScenario,
        created_at: new Date().toISOString(),
        turns: 0,
        completed: false,
        opening: response.data.opening_message,
        conversation: []
      };
      saveSession(session);
    } catch (error) {
      console.error('Error starting conversation:', error);
      setError('Failed to start conversation. Please check if the backend server is running on port 8000.');
    }
    setIsProcessing(false);
  };

  // Start recording
  const startRecording = async () => {
    setError('');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100
        } 
      });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        setAudioBlob(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      setError('Cannot access microphone. Please allow microphone permission in your browser.');
    }
  };

  // Stop recording
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  // Send audio
  const sendAudio = async () => {
    if (!audioBlob) return;

    setIsProcessing(true);
    setError('');
    const formData = new FormData();
    formData.append('file', audioBlob, 'audio.wav');
    formData.append('scenario_id', selectedScenario);
    formData.append('history', JSON.stringify(conversationHistory));

    try {
      const response = await axios.post('/api/conversation/process', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      const newTurn = {
        user: response.data.transcript,
        coach: response.data.coach_response,
        timestamp: new Date().toISOString()
      };

      const updatedHistory = [...conversationHistory, newTurn];
      setConversationHistory(updatedHistory);
      setAudioBlob(null);

      // Check if complete
      if (response.data.is_complete) {
        setConversationComplete(true);
        // Get final evaluation
        const evalResponse = await axios.post('/api/evaluation/final', {
          conversation_history: updatedHistory
        });
        setFinalEvaluation(evalResponse.data.evaluation);
        
        // Update session
        updateSession({ 
          completed: true, 
          turns: updatedHistory.length,
          conversation: updatedHistory,
          finalEvaluation: evalResponse.data.evaluation
        });
      } else {
        updateSession({ 
          turns: updatedHistory.length,
          conversation: updatedHistory
        });
      }
    } catch (error) {
      console.error('Error processing audio:', error);
      setError('Failed to process audio. Please make sure the backend server is running and try again.');
    }
    setIsProcessing(false);
  };

  // Reset conversation
  const resetConversation = () => {
    setConversationStarted(false);
    setCoachOpening('');
    setConversationHistory([]);
    setConversationComplete(false);
    setFinalEvaluation('');
    setAudioBlob(null);
  };

  // Save/Update session in localStorage
  const saveSession = (session) => {
    const sessions = JSON.parse(localStorage.getItem('sessions') || '[]');
    sessions.push(session);
    localStorage.setItem('sessions', JSON.stringify(sessions));
    localStorage.setItem('currentSession', JSON.stringify(session));
  };

  const updateSession = (updates) => {
    const current = JSON.parse(localStorage.getItem('currentSession') || '{}');
    const updated = { ...current, ...updates, conversation: conversationHistory };
    localStorage.setItem('currentSession', JSON.stringify(updated));
    
    // Update in sessions list
    const sessions = JSON.parse(localStorage.getItem('sessions') || '[]');
    const index = sessions.findIndex(s => s.id === current.id);
    if (index !== -1) {
      sessions[index] = updated;
      localStorage.setItem('sessions', JSON.stringify(sessions));
    }
  };

  const currentScenario = scenarios.find(s => s.id === selectedScenario);
  
  const scenarioEmojis = {
    restaurant: '🍽️',
    shopping: '👕',
    hotel: '🏨',
    job_interview: '💼',
    free: '🗣️'
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl animate-fade-in">
      {/* Error Banner */}
      {error && (
        <div className="mb-6 bg-red-50 border-2 border-red-200 rounded-xl p-4 flex items-start gap-3">
          <XCircle className="w-6 h-6 text-red-500 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-red-800 mb-1">Error</h3>
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        </div>
      )}

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left Panel - Conversation */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                💬 Conversation
              </h2>
              {conversationStarted && (
                <button onClick={resetConversation} className="btn-secondary text-sm py-2 px-4 hover:bg-red-50 hover:border-red-300 hover:text-red-600">
                  <RotateCcw className="w-4 h-4 inline mr-2" />
                  New Conversation
                </button>
              )}
            </div>

            {/* Scenario Selection */}
            {!conversationStarted && (
              <div className="mb-6 animate-slide-up">
                <label className="block text-sm font-semibold mb-3 text-gray-700">
                  🎬 Choose Your Scenario:
                </label>
                <select 
                  value={selectedScenario}
                  onChange={(e) => setSelectedScenario(e.target.value)}
                  className="input-field text-lg"
                >
                  {scenarios.map(s => (
                    <option key={s.id} value={s.id}>
                      {scenarioEmojis[s.id] || '💬'} {s.title}
                    </option>
                  ))}
                </select>
                {currentScenario && (
                  <div className="mt-4 p-5 bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl border-2 border-blue-100">
                    <div className="flex items-start gap-2 mb-3">
                      <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                      <div>
                        <p className="text-sm font-semibold text-blue-900 mb-1">🎯 Scenario Goal:</p>
                        <p className="text-sm text-gray-700">{currentScenario.goal}</p>
                      </div>
                    </div>
                    {currentScenario.steps && currentScenario.steps.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-blue-200">
                        <p className="text-sm font-semibold text-blue-900 mb-2">📋 Steps:</p>
                        <ol className="text-sm text-gray-700 space-y-1 ml-4 list-decimal">
                          {currentScenario.steps.map((step, i) => (
                            <li key={i}>{step}</li>
                          ))}
                        </ol>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* Start Button */}
            {!conversationStarted && (
              <button 
                onClick={handleStartConversation}
                disabled={isProcessing}
                className="btn-primary w-full text-lg py-4"
              >
                {isProcessing ? (
                  <>
                    <Loader className="w-6 h-6 animate-spin inline mr-2" />
                    Starting...
                  </>
                ) : (
                  <>
                    🎬 Start Conversation
                  </>
                )}
              </button>
            )}

            {/* Messages */}
            {conversationStarted && (
              <div className="space-y-4 mb-6 max-h-[500px] overflow-y-auto p-2">
                {/* Coach Opening */}
                <div className="message-coach animate-slide-up shadow-md">
                  <div className="flex items-start gap-3">
                    <div className="text-3xl flex-shrink-0">🤖</div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="font-bold text-purple-700">Coach</span>
                        <Volume2 className="w-4 h-4 text-purple-500" />
                      </div>
                      <p className="text-gray-800 leading-relaxed">{coachOpening}</p>
                    </div>
                  </div>
                </div>

                {/* Conversation History */}
                {conversationHistory.map((turn, index) => (
                  <div key={index} className="space-y-3 animate-fade-in">
                    {/* User */}
                    <div className="message-user shadow-md">
                      <div className="flex items-start gap-3 justify-end">
                        <div className="text-right flex-1">
                          <div className="flex items-center gap-2 justify-end mb-2">
                            <span className="font-bold text-blue-700">You</span>
                            <Mic className="w-4 h-4 text-blue-500" />
                          </div>
                          <p className="text-gray-800 leading-relaxed">{turn.user}</p>
                          <p className="text-xs text-gray-500 mt-2">
                            {new Date(turn.timestamp).toLocaleTimeString()}
                          </p>
                        </div>
                        <div className="text-3xl flex-shrink-0">🧑</div>
                      </div>
                    </div>
                    {/* Coach */}
                    <div className="message-coach shadow-md">
                      <div className="flex items-start gap-3">
                        <div className="text-3xl flex-shrink-0">🤖</div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="font-bold text-purple-700">Coach</span>
                            <Volume2 className="w-4 h-4 text-purple-500" />
                          </div>
                          <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">{turn.coach}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>
            )}

            {/* Recording Controls */}
            {conversationStarted && !conversationComplete && (
              <div className="border-t-2 border-gray-100 pt-6">
                <div className="flex flex-col gap-3">
                  {!isRecording && !audioBlob && !isProcessing && (
                    <button 
                      onClick={startRecording} 
                      className="btn-primary text-lg py-4 hover:shadow-xl"
                    >
                      <Mic className="w-6 h-6 inline mr-2" />
                      🎙️ Record Your Response
                    </button>
                  )}
                  
                  {isRecording && (
                    <div className="space-y-3">
                      <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4 text-center">
                        <div className="flex items-center justify-center gap-3 mb-2">
                          <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                          <span className="text-red-700 font-bold">Recording...</span>
                          <span className="text-red-600 font-mono text-lg">{formatTime(recordingTime)}</span>
                        </div>
                        <p className="text-sm text-gray-600">Speak clearly into your microphone</p>
                      </div>
                      <button 
                        onClick={stopRecording} 
                        className="w-full bg-red-500 hover:bg-red-600 text-white px-6 py-4 rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all"
                      >
                        <Square className="w-5 h-5 inline mr-2" />
                        ⏹️ Stop Recording
                      </button>
                    </div>
                  )}
                  
                  {audioBlob && !isProcessing && (
                    <div className="space-y-3">
                      <div className="bg-green-50 border-2 border-green-200 rounded-xl p-4 text-center">
                        <CheckCircle className="w-8 h-8 text-green-500 mx-auto mb-2" />
                        <p className="text-green-700 font-semibold">Recording ready!</p>
                        <p className="text-sm text-gray-600">Send it to get Coach's feedback</p>
                      </div>
                      <div className="flex gap-3">
                        <button 
                          onClick={() => setAudioBlob(null)} 
                          className="btn-secondary flex-1 hover:bg-red-50 hover:border-red-300 hover:text-red-600"
                        >
                          <XCircle className="w-5 h-5 inline mr-2" />
                          Discard
                        </button>
                        <button 
                          onClick={sendAudio} 
                          className="btn-primary flex-1 text-lg py-3"
                        >
                          <Send className="w-5 h-5 inline mr-2" />
                          Send
                        </button>
                      </div>
                    </div>
                  )}
                  
                  {isProcessing && (
                    <div className="bg-blue-50 border-2 border-blue-200 rounded-xl p-6 text-center">
                      <Loader className="w-10 h-10 animate-spin text-blue-600 mx-auto mb-3" />
                      <p className="text-blue-700 font-semibold">Processing your speech...</p>
                      <p className="text-sm text-gray-600 mt-1">Transcribing and getting Coach's feedback</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Complete Message */}
            {conversationComplete && (
              <div className="bg-green-50 border-2 border-green-200 rounded-xl p-6 text-center">
                <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-green-700 mb-2">🎉 Conversation Complete!</h3>
                <p className="text-gray-700">Great job! Check your IELTS evaluation on the right →</p>
              </div>
            )}
          </div>
        </div>

        {/* Right Panel - Evaluation */}
        <div className="lg:col-span-1">
          <div className="card sticky top-24">
            <h2 className="text-2xl font-bold mb-6 bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
              ⚖️ IELTS Evaluation
            </h2>
            
            {!conversationStarted && (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">📊</div>
                <p className="text-gray-500 font-medium">Start a conversation to receive your IELTS evaluation</p>
              </div>
            )}

            {conversationStarted && !conversationComplete && (
              <div className="space-y-4 animate-slide-up">
                <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl p-6 text-white shadow-lg">
                  <div className="text-center">
                    <div className="text-6xl font-bold mb-2 animate-pulse-slow">
                      {conversationHistory.length}
                    </div>
                    <p className="text-sm font-semibold opacity-90">Turns Completed</p>
                  </div>
                </div>
                
                <div className="bg-yellow-50 border-2 border-yellow-200 rounded-xl p-4">
                  <div className="flex items-start gap-2">
                    <Info className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="text-sm text-yellow-800 font-semibold mb-1">In Progress</p>
                      <p className="text-xs text-yellow-700">
                        Continue the conversation. You'll receive comprehensive IELTS evaluation when the scenario is complete (typically 5-10 turns).
                      </p>
                    </div>
                  </div>
                </div>

                {currentScenario && (
                  <div className="bg-purple-50 rounded-xl p-4 border-2 border-purple-100">
                    <p className="text-xs text-purple-600 font-semibold mb-2">CURRENT SCENARIO</p>
                    <p className="text-sm font-bold text-purple-900">
                      {scenarioEmojis[selectedScenario]} {currentScenario.title}
                    </p>
                  </div>
                )}
              </div>
            )}

            {conversationComplete && finalEvaluation && (
              <div className="space-y-4 animate-slide-up">
                <div className="bg-gradient-to-br from-green-400 to-emerald-500 rounded-xl p-6 text-white shadow-lg text-center">
                  <CheckCircle className="w-12 h-12 mx-auto mb-3" />
                  <h3 className="font-bold text-lg">🎉 Completed!</h3>
                  <p className="text-sm opacity-90 mt-1">{conversationHistory.length} turns</p>
                </div>

                <div className="bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 rounded-xl p-6 border-2 border-blue-100 shadow-md">
                  <h3 className="font-bold mb-4 text-blue-900 flex items-center gap-2">
                    <CheckCircle className="w-5 h-5 text-green-600" />
                    Final IELTS Evaluation
                  </h3>
                  <div className="bg-white rounded-lg p-4 max-h-[500px] overflow-y-auto">
                    <div className="prose prose-sm max-w-none">
                      <pre className="whitespace-pre-wrap text-sm text-gray-800 font-sans leading-relaxed">
{finalEvaluation}
                      </pre>
                    </div>
                  </div>
                </div>

                <button 
                  onClick={resetConversation}
                  className="btn-primary w-full"
                >
                  <RotateCcw className="w-5 h-5 inline mr-2" />
                  Practice Again
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
