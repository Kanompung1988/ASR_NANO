"""
Simple Test Script - No Web UI Required
----------------------------------------
Test the dual-LLM system with a mock audio file or text input
No ffmpeg/ffprobe needed!

Usage:
    python test_simple.py
"""

from model_service import coach_feedback, judge_feedback, SCENARIOS

def test_with_text():
    """Test the system using text input (no audio needed)"""
    print("=" * 60)
    print("🧪 TESTING DUAL-LLM SYSTEM (Text Mode - No Audio)")
    print("=" * 60)
    
    # Simulate transcribed text (as if audio was already transcribed)
    test_inputs = [
        "Hello, I would like to order some food please",
        "I want a steak with french fries",
        "Medium rare please, and a coke",
        "No, that's all. Thank you"
    ]
    
    # Test Restaurant Scenario
    scenario = SCENARIOS["restaurant"]
    conversation_history = []
    
    print(f"\n📍 Scenario: {scenario['title']}")
    print(f"🎭 AI Role: {scenario['role']}")
    print(f"🎯 Goal: {scenario['goal']}\n")
    print("=" * 60)
    
    for i, user_text in enumerate(test_inputs, 1):
        print(f"\n{'='*60}")
        print(f"TURN {i}")
        print(f"{'='*60}")
        
        print(f"\n🧑 USER SAID:")
        print(f"   {user_text}")
        
        # Get Coach response
        print(f"\n🤖 COACH RESPONSE:")
        coach_response = coach_feedback(user_text, conversation_history, scenario)
        print(f"   {coach_response}")
        
        # Check if complete
        if "[CONVERSATION_COMPLETE]" in coach_response:
            print("\n🎉 CONVERSATION COMPLETE!")
            coach_response = coach_response.replace("[CONVERSATION_COMPLETE]", "").strip()
        
        # Get Judge evaluation
        print(f"\n⚖️ JUDGE EVALUATION:")
        judge_response = judge_feedback(user_text)
        print(f"   {judge_response}")
        
        # Update history
        conversation_history.append({
            'user': user_text,
            'coach': coach_response
        })
        
        print(f"\n{'-'*60}")
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETED!")
    print(f"Total turns: {len(conversation_history)}")
    print("=" * 60)

def test_all_scenarios():
    """Test all scenarios with sample inputs"""
    print("\n" + "=" * 60)
    print("🧪 TESTING ALL SCENARIOS")
    print("=" * 60)
    
    for scenario_key, scenario in SCENARIOS.items():
        if scenario_key == "free":
            continue
            
        print(f"\n{'='*60}")
        print(f"Testing: {scenario['title']}")
        print(f"{'='*60}")
        
        # Sample first message
        sample_inputs = {
            "restaurant": "Hi, I'd like to see the menu",
            "shopping": "Hello, I'm looking for a shirt",
            "hotel": "Hi, I have a reservation",
            "job_interview": "Good morning, I'm here for the interview"
        }
        
        user_text = sample_inputs.get(scenario_key, "Hello")
        print(f"\n🧑 User: {user_text}")
        
        coach_response = coach_feedback(user_text, None, scenario)
        print(f"\n🤖 Coach: {coach_response[:200]}...")
        
        print(f"\n✅ {scenario['title']} - Working!")
    
    print("\n" + "=" * 60)
    print("✅ ALL SCENARIOS TESTED!")
    print("=" * 60)

def interactive_test():
    """Interactive testing - type your responses"""
    print("\n" + "=" * 60)
    print("🎮 INTERACTIVE TEST MODE")
    print("=" * 60)
    print("\nChoose a scenario:")
    print("1. Restaurant")
    print("2. Shopping")
    print("3. Hotel")
    print("4. Job Interview")
    print("5. Free Conversation")
    
    choice = input("\nEnter number (1-5): ").strip()
    
    scenario_map = {
        "1": "restaurant",
        "2": "shopping",
        "3": "hotel",
        "4": "job_interview",
        "5": "free"
    }
    
    scenario_key = scenario_map.get(choice, "free")
    scenario = SCENARIOS[scenario_key] if scenario_key != "free" else None
    
    if scenario:
        print(f"\n📍 Scenario: {scenario['title']}")
        print(f"🎭 Your role: Customer/Candidate")
        print(f"🤖 AI role: {scenario['role']}")
        print(f"🎯 Goal: {scenario['goal']}")
    else:
        print("\n📍 Mode: Free Conversation")
    
    print("\n" + "=" * 60)
    print("Type your responses (or 'quit' to exit)")
    print("=" * 60 + "\n")
    
    conversation_history = []
    turn = 0
    
    while True:
        turn += 1
        print(f"\n{'='*60}")
        print(f"TURN {turn}")
        print(f"{'='*60}")
        
        user_text = input("\n🧑 You: ").strip()
        
        if user_text.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not user_text:
            print("⚠️ Please say something!")
            turn -= 1
            continue
        
        # Get Coach response
        print(f"\n🤖 Coach:")
        coach_response = coach_feedback(user_text, conversation_history, scenario)
        
        if "[CONVERSATION_COMPLETE]" in coach_response:
            print("🎉 " + coach_response.replace("[CONVERSATION_COMPLETE]", "").strip())
            print("\n✅ Conversation Complete!")
            break
        else:
            print(coach_response)
        
        # Get Judge evaluation
        print(f"\n⚖️ Judge Evaluation:")
        judge_response = judge_feedback(user_text)
        print(judge_response)
        
        # Update history
        conversation_history.append({
            'user': user_text,
            'coach': coach_response
        })

if __name__ == "__main__":
    print("\n" + "🎙️ AI ENGLISH LEARNING - SIMPLE TEST TOOL ".center(60, "="))
    print("\nChoose test mode:")
    print("1. 🤖 Automated Test (Restaurant scenario)")
    print("2. 🌟 Test All Scenarios (quick check)")
    print("3. 🎮 Interactive Test (type your responses)")
    print("4. 🔧 Custom (modify this file to test)")
    
    mode = input("\nEnter number (1-4): ").strip()
    
    if mode == "1":
        test_with_text()
    elif mode == "2":
        test_all_scenarios()
    elif mode == "3":
        interactive_test()
    else:
        print("\n💡 Tip: Edit this file to add your own test cases!")
        print("You can test with any text input - no audio needed.\n")
        test_with_text()
