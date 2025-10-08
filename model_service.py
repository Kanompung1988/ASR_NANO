
"""model_service.py
Core backend for Dual-LLM demo
--------------------------------
Functions:
- transcribe()  : Typhoon ASR -> text
- coach_feedback(): Gemini coach feedback
- judge_feedback(): Gemini judge/scoring
- process()     : end‑to‑end helper
Set env vars:
  export TYPHOON_API_KEY=...
  export GOOGLE_API_KEY=...
Install deps:
  pip install openai google-generativeai requests
"""

import os, requests
from google.generativeai import configure, GenerativeModel
import openai
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

# ---------- Keys ----------
TYPHOON_KEY = os.getenv("TYPHOON_API_KEY")
GEMINI_KEY  = os.getenv("GEMINI_API_KEY")
if not TYPHOON_KEY or not GEMINI_KEY:
    raise RuntimeError("❌ Please set TYPHOON_API_KEY and GEMINI_API_KEY environment variables.")

# ---------- Typhoon ASR ----------
TYPHOON_BASE   = "https://api.opentyphoon.ai/v1"
TYPHOON_ASR_MD = "typhoon-asr-large-v1"
HEADERS        = { "Authorization": f"Bearer {TYPHOON_KEY}" }

def transcribe(audio_bytes: bytes, language_code: str = "auto") -> str:
    """Send raw WAV/MP3 bytes to Typhoon ASR → return transcript."""
    try:
        # Try Typhoon ASR first
        files = { "file": ("audio.wav", audio_bytes, "audio/wav") }
        data  = { "model": TYPHOON_ASR_MD, "language_code": language_code }
        resp  = requests.post(f"{TYPHOON_BASE}/audio/transcriptions",
                              headers=HEADERS, data=data, files=files, timeout=90)
        resp.raise_for_status()
        return resp.json()["text"].strip()
    except Exception as e:
        # Fallback to Gemini for transcription
        print(f"Typhoon ASR failed: {e}")
        print("Falling back to Gemini for transcription...")
        try:
            import google.generativeai as genai
            from pathlib import Path
            import tempfile
            
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name
            
            # Upload to Gemini
            audio_file = genai.upload_file(path=tmp_path)
            
            # Transcribe using Gemini
            model = genai.GenerativeModel("gemini-2.5-flash")
            prompt = "Please transcribe this audio accurately. Only provide the transcription text, nothing else."
            response = model.generate_content([prompt, audio_file])
            
            # Cleanup
            Path(tmp_path).unlink()
            
            return response.text.strip()
        except Exception as gemini_error:
            error_msg = f"Both Typhoon ASR and Gemini transcription failed.\nTyphoon: {e}\nGemini: {gemini_error}"
            print(error_msg)
            raise RuntimeError(error_msg)

# ---------- Gemini ----------
configure(api_key=GEMINI_KEY)

def _gemini_chat(system_prompt: str, user_prompt: str,
                 model_name: str = "gemini-2.5-flash") -> str:
    model = GenerativeModel(model_name,
                            system_instruction=system_prompt)
    resp  = model.generate_content(user_prompt)
    return resp.text.strip()

def coach_feedback(text: str, conversation_history: list = None, scenario: dict = None) -> str:
    """Coach corrects errors and continues the conversation naturally."""
    
    # Default free conversation
    if not scenario:
        sys = """You are a friendly English conversation partner helping someone practice English.
When the user speaks:
1. Acknowledge what they said
2. Gently correct any grammar or vocabulary errors in a natural way (briefly, don't over-correct)
3. Continue the conversation by asking a follow-up question or adding to the topic
Keep your response conversational, natural and encouraging. Remember the conversation context."""
    else:
        # Scenario-based conversation
        sys = f"""You are role-playing as: {scenario['role']}
Scenario: {scenario['description']}
Goal: {scenario['goal']}

Your responsibilities:
1. Stay in character as {scenario['role']}
2. Guide the conversation through these steps: {', '.join(scenario['steps'])}
3. Gently correct the learner's English errors in a natural way
4. When the goal is achieved, naturally conclude the conversation

IMPORTANT: When you think the conversation goal has been completed, end your response with the marker: [CONVERSATION_COMPLETE]"""
    
    # Build conversation context
    if conversation_history:
        context = "Previous conversation:\n"
        for entry in conversation_history:
            context += f"User: {entry['user']}\nYou: {entry['coach']}\n\n"
        usr = f"{context}User now says:\n'''\n{text}\n'''\n\nPlease respond as their conversation partner."
    else:
        if scenario:
            usr = f"The learner said:\n'''\n{text}\n'''\n\nThis is the first message. Start the {scenario['title']} scenario naturally."
        else:
            usr = f"The learner said:\n'''\n{text}\n'''\n\nPlease respond as their conversation partner and start a natural conversation."
    
    return _gemini_chat(sys, usr)

def judge_feedback(text: str) -> str:
    """Judge evaluates the ORIGINAL user speech based on IELTS criteria."""
    sys = """You are an IELTS Speaking examiner. Evaluate the speaker's performance based on these criteria:
1. Pronunciation (0-9): clarity, accent, intonation (analyze based on transcript patterns, word choices, and complexity)
2. Vocabulary (0-9): range, accuracy, appropriateness
3. Grammar (0-9): accuracy, range, complexity
4. Fluency & Coherence (0-9): smoothness, hesitation, logical flow

Provide scores and brief justification for each criterion. Be objective and based only on what was actually said."""
    usr = f"Original speech transcript:\n'''\n{text}\n'''\n\nPlease provide IELTS-style evaluation with scores (0-9) for each criterion."
    return _gemini_chat(sys, usr)

def judge_final_evaluation(conversation_history: list) -> str:
    """Judge provides FINAL comprehensive IELTS evaluation after full conversation."""
    sys = """You are an IELTS Speaking examiner. Provide a COMPREHENSIVE evaluation based on the ENTIRE conversation.

Evaluate these criteria (0-9 scale):
1. Pronunciation (0-9): Based on transcript patterns, complexity of words used, and natural language flow
2. Vocabulary (0-9): Range, accuracy, appropriateness across the entire conversation
3. Grammar (0-9): Accuracy, range, complexity throughout all responses
4. Fluency & Coherence (0-9): Overall smoothness, logical progression, ability to sustain conversation

Provide:
- Individual scores for each criterion
- Detailed justification for each score
- Overall band score (average of 4 criteria)
- Specific strengths and areas for improvement
- Example sentences that demonstrate strong/weak points"""

    # Build full conversation transcript
    full_transcript = "Full Conversation Transcript:\n\n"
    for i, entry in enumerate(conversation_history, 1):
        full_transcript += f"Turn {i} - User: {entry['user']}\n"
    
    usr = f"{full_transcript}\n\nPlease provide a COMPREHENSIVE IELTS evaluation based on this complete conversation."
    return _gemini_chat(sys, usr)

# ---------- Convenience wrapper ----------
def process(audio_bytes: bytes, conversation_history: list = None, scenario: dict = None) -> tuple[str, str, str]:
    """Return (transcript, coach_feedback, judge_feedback).
    Note: judge_feedback is now just per-turn notes, not full evaluation."""
    transcript = transcribe(audio_bytes)
    coach = coach_feedback(transcript, conversation_history, scenario)
    
    # Don't evaluate every turn - just return empty or brief note
    judge_note = f"Turn {len(conversation_history) + 1 if conversation_history else 1} recorded. Evaluation will be provided at the end of conversation."
    
    return transcript, coach, judge_note

def start_conversation(scenario: dict = None) -> str:
    """Start a conversation - Coach speaks first."""
    if not scenario:
        # Free conversation
        sys = """You are a friendly English conversation partner helping someone practice English.
Start a natural, friendly conversation. Introduce yourself and ask an engaging question to get the conversation going."""
        usr = "Please start a conversation with the learner."
    else:
        # Scenario-based conversation
        sys = f"""You are role-playing as: {scenario['role']}
Scenario: {scenario['description']}
Goal: {scenario['goal']}

Start the {scenario['title']} scenario naturally. Greet the customer/guest/candidate and begin the interaction according to your role."""
        usr = f"Start the {scenario['title']} scenario. You speak first."
    
    return _gemini_chat(sys, usr)

# ---------- Predefined Scenarios ----------
SCENARIOS = {
    "restaurant": {
        "title": "Ordering Food at a Restaurant",
        "role": "a waiter/waitress at a restaurant",
        "description": "The learner is a customer who wants to order food",
        "goal": "Help the customer order food, drinks, and complete the order",
        "steps": ["Greet customer", "Present menu/specials", "Take order", "Confirm order", "Thank customer"],
    },
    "shopping": {
        "title": "Shopping at a Clothing Store",
        "role": "a sales assistant at a clothing store",
        "description": "The learner wants to buy clothes",
        "goal": "Help the customer find and purchase clothing items",
        "steps": ["Greet customer", "Ask what they're looking for", "Show options", "Discuss size/color", "Complete purchase"],
    },
    "hotel": {
        "title": "Hotel Check-in",
        "role": "a hotel receptionist",
        "description": "The learner is checking into a hotel",
        "goal": "Complete the check-in process",
        "steps": ["Greet guest", "Verify reservation", "Collect information", "Explain facilities", "Give room key"],
    },
    "job_interview": {
        "title": "Job Interview",
        "role": "an interviewer for a company",
        "description": "The learner is applying for a job position",
        "goal": "Conduct a complete job interview",
        "steps": ["Introduce yourself", "Ask about background", "Discuss experience", "Ask about strengths/weaknesses", "Close interview"],
    },
    "free": {
        "title": "Free Conversation",
        "role": None,
        "description": "Open conversation on any topic",
        "goal": "Natural conversation practice",
        "steps": [],
    }
}
