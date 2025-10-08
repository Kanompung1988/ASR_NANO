import React from 'react';
import { Link } from 'react-router-dom';
import { Mic, Award, TrendingUp, Clock, ArrowRight } from 'lucide-react';

export default function HomePage() {
  const features = [
    {
      icon: <Mic className="w-8 h-8" />,
      title: "Real-time Conversation",
      description: "Practice speaking English with AI coach that responds naturally"
    },
    {
      icon: <Award className="w-8 h-8" />,
      title: "IELTS Evaluation",
      description: "Get comprehensive feedback based on official IELTS criteria"
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: "Track Progress",
      description: "View your conversation history and improvement over time"
    },
    {
      icon: <Clock className="w-8 h-8" />,
      title: "Multiple Scenarios",
      description: "Practice different situations: restaurant, hotel, interview, and more"
    }
  ];

  const scenarios = [
    { id: 'restaurant', emoji: '🍽️', title: 'Restaurant', description: 'Order food and drinks' },
    { id: 'shopping', emoji: '👕', title: 'Shopping', description: 'Buy clothes and accessories' },
    { id: 'hotel', emoji: '🏨', title: 'Hotel', description: 'Check-in and hotel services' },
    { id: 'job_interview', emoji: '💼', title: 'Job Interview', description: 'Professional interview practice' },
    { id: 'free', emoji: '🗣️', title: 'Free Talk', description: 'Open conversation practice' },
  ];

  return (
    <div className="container mx-auto px-4 py-12">
      {/* Hero Section */}
      <div className="text-center mb-20 animate-fade-in">
        <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
          Master English Speaking
        </h1>
        <p className="text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Practice real conversations with AI coach and get instant IELTS-style feedback
        </p>
        <Link to="/practice" className="btn-primary inline-flex items-center gap-2 text-lg">
          Start Practicing Now
          <ArrowRight className="w-5 h-5" />
        </Link>
      </div>

      {/* Features Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-20">
        {features.map((feature, index) => (
          <div 
            key={index}
            className="card text-center animate-slide-up hover:scale-105 transition-transform"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <div className="inline-flex p-4 bg-gradient-to-br from-blue-100 to-purple-100 rounded-2xl mb-4 text-blue-600">
              {feature.icon}
            </div>
            <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
            <p className="text-gray-600">{feature.description}</p>
          </div>
        ))}
      </div>

      {/* Scenarios Section */}
      <div className="mb-20">
        <h2 className="text-4xl font-bold text-center mb-12">Choose Your Scenario</h2>
        <div className="grid md:grid-cols-3 lg:grid-cols-5 gap-6">
          {scenarios.map((scenario, index) => (
            <Link
              key={scenario.id}
              to="/practice"
              state={{ selectedScenario: scenario.id }}
              className="card text-center hover:scale-105 transition-transform cursor-pointer group"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <div className="text-5xl mb-3 group-hover:scale-110 transition-transform">
                {scenario.emoji}
              </div>
              <h3 className="text-lg font-bold mb-2 text-gray-800">{scenario.title}</h3>
              <p className="text-sm text-gray-600">{scenario.description}</p>
            </Link>
          ))}
        </div>
      </div>

      {/* How It Works */}
      <div className="card bg-gradient-to-br from-blue-50 to-purple-50">
        <h2 className="text-3xl font-bold text-center mb-8">How It Works</h2>
        <div className="grid md:grid-cols-4 gap-6">
          {[
            { step: 1, title: 'Choose Scenario', desc: 'Select a conversation topic' },
            { step: 2, title: 'Coach Starts', desc: 'AI coach greets you first' },
            { step: 3, title: 'Record & Respond', desc: 'Speak naturally in English' },
            { step: 4, title: 'Get Feedback', desc: 'Receive IELTS evaluation' },
          ].map((item) => (
            <div key={item.step} className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                {item.step}
              </div>
              <h3 className="font-bold mb-2">{item.title}</h3>
              <p className="text-sm text-gray-600">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
