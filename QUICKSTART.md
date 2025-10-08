# 🎯 Quick Start Guide

## Step 1: Install Frontend Dependencies

```bash
cd /Users/t333838/Desktop/KPPP/frontend
npm install
```

## Step 2: Install Backend Dependencies (if not done)

```bash
cd /Users/t333838/Desktop/KPPP
pip install fastapi uvicorn python-multipart
```

## Step 3: Start Backend

Open Terminal 1:
```bash
cd /Users/t333838/Desktop/KPPP/backend
python main.py
```

Backend will run on: **http://localhost:8000**

## Step 4: Start Frontend

Open Terminal 2:
```bash
cd /Users/t333838/Desktop/KPPP/frontend
npm run dev
```

Frontend will run on: **http://localhost:3000**

## Step 5: Open in Browser

Go to: **http://localhost:3000**

---

## 🎮 Features

### Home Page
- Beautiful landing page
- Feature overview
- Scenario selection
- Quick start button

### Practice Page
- Choose scenario
- Coach starts conversation
- Record audio responses
- Real-time transcript
- Coach feedback
- IELTS evaluation at end

### History Page
- View all past conversations
- Filter by scenario
- Delete conversations
- Replay conversations

---

## 📱 UI Screenshots (Conceptual)

### 🏠 Home Page
```
┌──────────────────────────────────────┐
│  🎙️ AI English Coach                │
│                                      │
│  Master English Speaking             │
│  Practice real conversations         │
│  Get instant IELTS feedback          │
│                                      │
│  [Start Practicing Now →]           │
│                                      │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │
│  │ 🎤  │ │ 🏆  │ │ 📈  │ │ ⏰  │  │
│  │Real │ │IELTS│ │Track│ │Multi│  │
│  └─────┘ └─────┘ └─────┘ └─────┘  │
│                                      │
│  Choose Scenario:                    │
│  [🍽️] [👕] [🏨] [💼] [🗣️]          │
└──────────────────────────────────────┘
```

### 💬 Practice Page
```
┌─────────────────────┬───────────────┐
│ 💬 Conversation     │ ⚖️ Evaluation │
│                     │               │
│ 🤖 Coach:           │ 🔄 In Progress│
│ "Good evening!      │               │
│  Welcome..."        │ Turns: 3      │
│                     │               │
│ 🧑 You:             │ Continue      │
│ "I'd like to        │ conversation  │
│  order food"        │ ...           │
│                     │               │
│ 🤖 Coach:           │ Evaluation    │
│ "Great! Here's      │ will appear   │
│  our menu..."       │ at the end    │
│                     │               │
│ [🎙️ Record]        │               │
└─────────────────────┴───────────────┘
```

### 📜 History Page
```
┌─────────────┬─────────────────────────┐
│ Sessions    │ Session Details         │
│             │                         │
│ ┌─────────┐ │ 🍽️ Restaurant          │
│ │🍽️ Rest  │ │                         │
│ │Oct 8    │ │ Date: Oct 8, 2025      │
│ │3 turns  │ │ Turns: 3               │
│ │✅ Done  │ │ Status: Completed      │
│ └─────────┘ │                         │
│             │ 💬 Conversation         │
│ ┌─────────┐ │                         │
│ │🏨 Hotel │ │ 🤖: "Good evening..."  │
│ │Oct 7    │ │ 🧑: "I'd like..."      │
│ │5 turns  │ │ 🤖: "Great! Here's..." │
│ └─────────┘ │                         │
└─────────────┴─────────────────────────┘
```

---

## 🎨 Design Features

✨ **Beautiful Gradients**
- Blue to purple gradients
- Smooth animations
- Hover effects

📱 **Responsive Design**
- Works on desktop, tablet, mobile
- Adaptive layouts
- Touch-friendly controls

🎯 **Intuitive UX**
- Clear navigation
- Visual feedback
- Error handling

💾 **Auto-Save**
- Conversations saved automatically
- Resume from where you left off
- Export history

---

## 🔧 Customization

Edit colors in `tailwind.config.js`:
```js
colors: {
  primary: {...}  // Change main colors
}
```

Edit API URL in `vite.config.js`:
```js
proxy: {
  '/api': {
    target: 'http://your-backend-url'
  }
}
```

---

Enjoy practicing! 🎉
