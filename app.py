
"""app.py
Streamlit front‑end for real‑time Dual‑LLM demo.
-----------------------------------------------
Run:
    streamlit run app.py
Needs:
    pip install stream# Clear conversation button in sidebar
with st.sidebar:
    st.header("🔧 Controls")
    
    # Scenario info
    st.markdown(f"**Current Scenario:**")
    st.info(scenario_options[st.session_state.selected_scenario])
    
    if st.session_state.conversation_complete:
        st.success("✅ Completed!")
    else:
        st.warning("🔄 In Progress")
    
    st.markdown("---")
    
    if st.button("🔄 Start New Conversation", use_container_width=True):
        st.session_state.conversation_history = []
        st.session_state.evaluation_history = []
        st.session_state.conversation_complete = False
        st.session_state.conversation_started = False
        st.session_state.coach_opening = ""
        st.session_state.final_evaluation = ""
        st.rerun()
    
    st.markdown("---")
    st.markdown(f"**Conversation turns:** {len(st.session_state.conversation_history)}")
    st.markdown(f"**Evaluations:** {len(st.session_state.evaluation_history)}")it-audiorecorder google-generativeai requests
"""

import streamlit as st
from audiorecorder import audiorecorder

from model_service import process, SCENARIOS, start_conversation, judge_final_evaluation

# Initialize session state for conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'evaluation_history' not in st.session_state:
    st.session_state.evaluation_history = []
if 'selected_scenario' not in st.session_state:
    st.session_state.selected_scenario = "free"
if 'conversation_complete' not in st.session_state:
    st.session_state.conversation_complete = False
if 'conversation_started' not in st.session_state:
    st.session_state.conversation_started = False
if 'coach_opening' not in st.session_state:
    st.session_state.coach_opening = ""
if 'final_evaluation' not in st.session_state:
    st.session_state.final_evaluation = ""

st.set_page_config(page_title="AI English Learning & IELTS Practice", layout="wide")
st.title("🎙️ AI English Learning & IELTS Practice")

st.markdown("""**Practice English conversation and get IELTS-style feedback!**

**How it works:**
1. � Choose a scenario (or free conversation)
2. �🎤 Record yourself speaking in English
3. 🤖 **Coach** guides the conversation and corrects errors
4. ⚖️ **Judge** evaluates your speech using IELTS criteria
5. 🏁 Complete the scenario goal to finish!

*The Coach will guide you through the scenario until the goal is achieved!*
""")

# Scenario selection
st.subheader("🎬 Choose Your Scenario")
scenario_options = {
    "free": "🗣️ Free Conversation",
    "restaurant": "🍽️ Restaurant - Ordering Food",
    "shopping": "👕 Shopping - Buying Clothes",
    "hotel": "🏨 Hotel - Check-in",
    "job_interview": "💼 Job Interview"
}

selected = st.selectbox(
    "Select a practice scenario:",
    options=list(scenario_options.keys()),
    format_func=lambda x: scenario_options[x],
    index=list(scenario_options.keys()).index(st.session_state.selected_scenario)
)

if selected != st.session_state.selected_scenario:
    st.session_state.selected_scenario = selected
    st.session_state.conversation_history = []
    st.session_state.evaluation_history = []
    st.session_state.conversation_complete = False
    st.session_state.conversation_started = False
    st.session_state.coach_opening = ""
    st.session_state.final_evaluation = ""
    st.rerun()

# Show scenario details
if st.session_state.selected_scenario != "free":
    scenario_info = SCENARIOS[st.session_state.selected_scenario]
    with st.expander("📋 Scenario Details"):
        st.write(f"**Your role:** Customer/Candidate")
        st.write(f"**AI role:** {scenario_info['role']}")
        st.write(f"**Goal:** {scenario_info['goal']}")
        st.write(f"**Steps:** {' → '.join(scenario_info['steps'])}")

# Show completion status
if st.session_state.conversation_complete:
    st.success("🎉 **Conversation Complete!** You've successfully finished this scenario. Start a new conversation to practice again!")

st.markdown("---")

# Create two columns: conversation on the left, evaluation on the right
col_chat, col_eval = st.columns([2, 1])

with col_chat:
    st.header("💬 Conversation")
    
    # Start conversation button (Coach speaks first)
    if not st.session_state.conversation_started and not st.session_state.conversation_complete:
        st.info("👇 Click the button below to start the conversation. The Coach will greet you first!")
        
        if st.button("🎬 Start Conversation", type="primary", use_container_width=True):
            with st.spinner('🤖 Coach is preparing to greet you...'):
                scenario_config = SCENARIOS[st.session_state.selected_scenario] if st.session_state.selected_scenario != "free" else None
                coach_opening = start_conversation(scenario_config)
                
                st.session_state.coach_opening = coach_opening
                st.session_state.conversation_started = True
                st.rerun()
    
    # Display coach's opening message
    if st.session_state.conversation_started and st.session_state.coach_opening:
        st.markdown("**🤖 Coach:**")
        st.success(st.session_state.coach_opening)
        st.markdown("---")
    
    # Display conversation history
    if st.session_state.conversation_history:
        for i, entry in enumerate(st.session_state.conversation_history):
            with st.container():
                st.markdown(f"**🧑 You said:**")
                st.info(entry['user'])
                
                # Show transcript if available
                if 'transcript' in entry and entry['transcript']:
                    with st.expander("� Transcript (what was heard)"):
                        st.text(entry['transcript'])
                
                st.markdown(f"**🤖 Coach:**")
                st.success(entry['coach'])
                st.markdown("---")
    
    # Audio recorder
    st.subheader("🎤 Record Your Response")
    
    # Only show recorder if conversation has started
    if not st.session_state.conversation_started:
        st.warning("⚠️ Please start the conversation first using the button above.")
    # Disable recording if conversation is complete
    elif st.session_state.conversation_complete:
        st.warning("⚠️ This conversation is complete. Start a new conversation to continue practicing.")
    else:
        audio_segment = audiorecorder("🎙️ Click to Record", "⏹️ Click to Stop")
        
        if audio_segment and len(audio_segment) > 0:
            # Convert AudioSegment to bytes for display and processing
            from io import BytesIO
            audio_buffer = BytesIO()
            audio_segment.export(audio_buffer, format="wav")
            audio_bytes = audio_buffer.getvalue()
            
            st.audio(audio_bytes, format='audio/wav')
            
            if st.button("📤 Send & Get Feedback", type="primary", use_container_width=True):
                with st.spinner('🎯 Transcribing and analyzing your speech...'):
                    # Get scenario config
                    scenario_config = SCENARIOS[st.session_state.selected_scenario] if st.session_state.selected_scenario != "free" else None
                    
                    try:
                        transcript, coach, judge = process(
                            audio_bytes, 
                            st.session_state.conversation_history,
                            scenario_config
                        )
                        
                        # Check if conversation is complete
                        if "[CONVERSATION_COMPLETE]" in coach:
                            st.session_state.conversation_complete = True
                            coach = coach.replace("[CONVERSATION_COMPLETE]", "").strip()
                            
                            # Generate final IELTS evaluation
                            with st.spinner('📊 Generating final IELTS evaluation...'):
                                st.session_state.final_evaluation = judge_final_evaluation(
                                    st.session_state.conversation_history + [{'user': transcript, 'coach': coach}]
                                )
                        
                        # Add to conversation history
                        st.session_state.conversation_history.append({
                            'user': transcript,
                            'transcript': transcript,  # Store transcript separately
                            'coach': coach
                        })
                        
                        # Don't store per-turn evaluations anymore - just note the turn
                        st.session_state.evaluation_history.append({
                            'turn': len(st.session_state.conversation_history),
                            'transcript': transcript,
                            'evaluation': judge  # This is just a note now
                        })
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.info("💡 Tip: Make sure your audio is clear and in WAV format. Try recording again.")

with col_eval:
    st.header("⚖️ IELTS Evaluation")
    
    # Show final evaluation if conversation is complete
    if st.session_state.conversation_complete and st.session_state.final_evaluation:
        st.success("🎉 **Conversation Complete!**")
        st.subheader("📊 Final IELTS Evaluation")
        st.markdown("*Based on your entire conversation:*")
        st.write(st.session_state.final_evaluation)
        
        # Show conversation summary
        with st.expander(f"📜 Conversation Summary ({len(st.session_state.conversation_history)} turns)"):
            for i, entry in enumerate(st.session_state.conversation_history, 1):
                st.markdown(f"**Turn {i}:**")
                st.caption(entry['user'])
    
    # Show turn counter while in progress
    elif st.session_state.conversation_started:
        st.info(f"🔄 **Conversation in Progress**\n\nTurns completed: {len(st.session_state.conversation_history)}\n\n*Continue the conversation. IELTS evaluation will be provided when you complete the scenario (usually 5-10 turns).*")
        
        # Show recent turns
        if st.session_state.conversation_history:
            with st.expander(f"📝 Your responses ({len(st.session_state.conversation_history)} turns)"):
                for i, entry in enumerate(st.session_state.conversation_history, 1):
                    st.markdown(f"**Turn {i}:** {entry['user']}")
    
    else:
        st.info("Start a conversation to receive IELTS evaluation at the end.")

# Clear conversation button in sidebar
with st.sidebar:
    st.header("🔧 Controls")
    if st.button("� Start New Conversation", use_container_width=True):
        st.session_state.conversation_history = []
        st.session_state.evaluation_history = []
        st.rerun()
    
    st.markdown("---")
    st.markdown(f"**Conversation turns:** {len(st.session_state.conversation_history)}")
    st.markdown(f"**Evaluations:** {len(st.session_state.evaluation_history)}")
