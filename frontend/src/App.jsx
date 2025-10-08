import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { Mic, History, Home, BookOpen } from 'lucide-react';
import ConversationPage from './pages/ConversationPage';
import HistoryPage from './pages/HistoryPage';
import HomePage from './pages/HomePage';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen">
        {/* Header */}
        <header className="bg-white shadow-md sticky top-0 z-50">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <Link to="/" className="flex items-center gap-3">
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-xl">
                  <BookOpen className="w-6 h-6 text-white" />
                </div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  AI English Coach
                </h1>
              </Link>
              
              <nav className="flex gap-4">
                <Link to="/" className="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-blue-50 transition-colors">
                  <Home className="w-5 h-5" />
                  <span className="hidden md:inline">Home</span>
                </Link>
                <Link to="/practice" className="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-blue-50 transition-colors">
                  <Mic className="w-5 h-5" />
                  <span className="hidden md:inline">Practice</span>
                </Link>
                <Link to="/history" className="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-blue-50 transition-colors">
                  <History className="w-5 h-5" />
                  <span className="hidden md:inline">History</span>
                </Link>
              </nav>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/practice" element={<ConversationPage />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-white border-t mt-20">
          <div className="container mx-auto px-4 py-6 text-center text-gray-600">
            <p>© 2025 AI English Coach. Practice makes perfect! 🎯</p>
          </div>
        </footer>
      </div>
    </BrowserRouter>
  );
}

export default App;
