# 🎙️ AI English Coach - React Web Application

A beautiful, modern web application for practicing English conversation with AI coach and receiving IELTS-style feedback.

## ✨ Features

- 🎤 **Real-time Voice Recording** - Practice speaking naturally
- 🤖 **AI Coach** - Get corrections and continue conversations
- ⚖️ **IELTS Evaluation** - Comprehensive feedback on 4 criteria
- 📊 **Progress Tracking** - View conversation history
- 🎯 **Multiple Scenarios** - Restaurant, Hotel, Shopping, Job Interview, Free Talk
- 💾 **Auto-Save** - Conversations saved to localStorage
- 📱 **Responsive Design** - Works on all devices
- 🎨 **Beautiful UI** - Modern design with Tailwind CSS

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- API Keys: Typhoon ASR, Google Gemini

### Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Copy .env file from parent directory
cp ../.env .

# Run FastAPI server
python main.py
```

Backend will run on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:3000`

## 📁 Project Structure

```
KPPP/
├── backend/
│   ├── main.py              # FastAPI backend
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── HomePage.jsx          # Landing page
│   │   │   ├── ConversationPage.jsx  # Main practice page
│   │   │   └── HistoryPage.jsx       # History viewer
│   │   ├── App.jsx          # Main app component
│   │   ├── main.jsx         # Entry point
│   │   └── index.css        # Tailwind styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── model_service.py         # Shared LLM logic
├── .env                     # API keys
└── README.md
```

## 🎮 How to Use

1. **Choose Scenario** - Select from Restaurant, Shopping, Hotel, Interview, or Free Talk
2. **Start Conversation** - Coach will greet you first
3. **Record Response** - Click mic to record, stop when done
4. **Get Feedback** - Receive coach response and continue
5. **Complete Scenario** - Conversation ends when goal is achieved
6. **View Evaluation** - Get comprehensive IELTS-style scores
7. **Check History** - View all past conversations

## 🔧 API Endpoints

- `GET /api/scenarios` - List all scenarios
- `POST /api/conversation/start` - Start new conversation
- `POST /api/audio/transcribe` - Transcribe audio
- `POST /api/conversation/process` - Process audio and get response
- `POST /api/evaluation/final` - Get final IELTS evaluation
- `GET /api/sessions` - Get all sessions
- `POST /api/sessions` - Create new session

## 💾 Data Storage

- **LocalStorage** - Conversation history stored in browser
- **Session Storage** - Current conversation state
- Keys:
  - `sessions` - Array of all conversation sessions
  - `currentSession` - Active conversation data

## 🎨 Tech Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - API calls
- **React Router** - Navigation
- **Lucide React** - Icons
- **date-fns** - Date formatting

### Backend
- **FastAPI** - Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Google Gemini** - LLM for coach/judge
- **Typhoon ASR** - Speech-to-text (with Gemini fallback)

## 🔒 Environment Variables

Create `.env` file in root:

```env
GEMINI_API_KEY=your_gemini_key_here
TYPHOON_API_KEY=your_typhoon_key_here
```

## 📦 Production Build

```bash
cd frontend
npm run build
# Output in frontend/dist/
```

Serve with any static host or use:
```bash
npm run preview
```

## 🐛 Troubleshooting

### Audio Recording Not Working
- Check browser microphone permissions
- Use HTTPS (required for getUserMedia API)
- Try different browser (Chrome/Edge recommended)

### Typhoon ASR Errors
- System automatically falls back to Gemini
- Check API key validity
- Ensure audio is in correct format

### CORS Issues
- Backend CORS configured for localhost:3000 and localhost:5173
- Update `allow_origins` in backend/main.py for production

## 📝 License

MIT License - feel free to use for learning and practice!

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

---

**Made with ❤️ for English learners worldwide**
