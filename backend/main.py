"""
FastAPI Backend for English Learning App
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sys
import os
import json
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model_service import transcribe, coach_feedback, judge_final_evaluation, start_conversation, SCENARIOS

app = FastAPI(title="English Learning API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConversationStart(BaseModel):
    scenario_id: str

class FinalEvaluation(BaseModel):
    conversation_history: List[dict]

sessions = {}

@app.get("/")
def read_root():
    return {"message": "English Learning API", "status": "running"}

@app.get("/api/scenarios")
def get_scenarios():
    return {"scenarios": [{
        "id": k,
        "title": v["title"],
        "role": v["role"],
        "description": v["description"],
        "goal": v["goal"],
        "steps": v["steps"]
    } for k, v in SCENARIOS.items()]}

@app.post("/api/conversation/start")
def start_conversation_endpoint(data: ConversationStart):
    try:
        scenario = SCENARIOS.get(data.scenario_id)
        opening = start_conversation(scenario)
        return {"success": True, "opening_message": opening, "scenario_id": data.scenario_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/conversation/process")
async def process_conversation(file: UploadFile = File(...), scenario_id: str = "free", history: str = "[]"):
    try:
        audio_bytes = await file.read()
        conversation_history = json.loads(history)
        scenario = SCENARIOS.get(scenario_id) if scenario_id != "free" else None
        
        transcript = transcribe(audio_bytes)
        coach_response = coach_feedback(transcript, conversation_history, scenario)
        
        is_complete = "[CONVERSATION_COMPLETE]" in coach_response
        if is_complete:
            coach_response = coach_response.replace("[CONVERSATION_COMPLETE]", "").strip()
        
        return {"success": True, "transcript": transcript, "coach_response": coach_response, "is_complete": is_complete}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/evaluation/final")
def get_final_evaluation(data: FinalEvaluation):
    try:
        evaluation = judge_final_evaluation(data.conversation_history)
        return {"success": True, "evaluation": evaluation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
