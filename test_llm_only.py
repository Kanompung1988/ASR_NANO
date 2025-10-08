"""
Test LLM Components Only (No Audio/Transcription)
-------------------------------------------------
This tests Coach and Judge LLMs without using Typhoon ASR
Perfect for testing when you don't have audio files

Usage:
    python test_llm_only.py
"""

from model_service import coach_feedback, judge_feedback, judge_final_evaluation, SCENARIOS
import json

def quick_test():
    """Quick test of Coach and Judge"""
    print("\n" + "="*70)
    print(" QUICK LLM TEST ".center(70, "="))
    print("="*70)
    
    # Test input
    user_speech = "I want to buying a new shirt for my sister birthday party next week"
    
    print(f"\n📝 User's Speech (with errors):")
    print(f"   '{user_speech}'")
    
    # Test Coach
    print(f"\n🤖 COACH (Free Conversation):")
    print("-" * 70)
    coach_resp = coach_feedback(user_speech, None, None)
    print(coach_resp)
    
    # Test Judge
    print(f"\n⚖️ JUDGE (IELTS Evaluation):")
    print("-" * 70)
    judge_resp = judge_feedback(user_speech)
    print(judge_resp)
    
    print("\n" + "="*70)

def test_scenario_progression():
    """Test how Coach guides through a scenario"""
    print("\n" + "="*70)
    print(" SCENARIO PROGRESSION TEST ".center(70, "="))
    print("="*70)
    
    scenario = SCENARIOS["restaurant"]
    
    # Simulate a conversation
    messages = [
        "Hello, I'd like to order",
        "Can I see the menu?",
        "I'll have the salmon please",
        "With water, please",
        "No, that's all"
    ]
    
    conversation_history = []
    
    print(f"\n📍 Scenario: {scenario['title']}")
    print(f"🎯 Goal: {scenario['goal']}")
    print(f"📋 Steps: {' → '.join(scenario['steps'])}")
    print("\n" + "-"*70 + "\n")
    
    for i, msg in enumerate(messages, 1):
        print(f"Turn {i}:")
        print(f"  🧑 Customer: {msg}")
        
        coach_resp = coach_feedback(msg, conversation_history, scenario)
        
        if "[CONVERSATION_COMPLETE]" in coach_resp:
            print(f"  🤖 Waiter: {coach_resp.replace('[CONVERSATION_COMPLETE]', '').strip()}")
            conversation_history.append({'user': msg, 'coach': coach_resp})
            print("\n  🎉 Conversation marked as COMPLETE!")
            break
        else:
            print(f"  🤖 Waiter: {coach_resp}")
        
        conversation_history.append({
            'user': msg,
            'coach': coach_resp
        })
        
        print()
    
    print("-"*70)
    print(f"✅ Total turns: {len(conversation_history)}")
    
    # Generate final evaluation
    print("\n" + "="*70)
    print(" FINAL IELTS EVALUATION ".center(70, "="))
    print("="*70)
    print("\n📊 Generating comprehensive evaluation...\n")
    
    final_eval = judge_final_evaluation(conversation_history)
    print(final_eval)
    print("\n" + "="*70)

def test_error_correction():
    """Test Coach's error correction ability"""
    print("\n" + "="*70)
    print(" ERROR CORRECTION TEST ".center(70, "="))
    print("="*70)
    
    test_cases = [
        {
            "input": "I go to school yesterday and meet my friend",
            "errors": ["go → went", "meet → met"]
        },
        {
            "input": "She don't likes coffee very much",
            "errors": ["don't → doesn't", "likes → like"]
        },
        {
            "input": "We was planning to went there tomorrow",
            "errors": ["was → were", "went → go"]
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print("-" * 70)
        print(f"📝 User said: '{case['input']}'")
        print(f"❌ Expected errors: {', '.join(case['errors'])}")
        
        coach_resp = coach_feedback(case['input'], None, None)
        print(f"\n🤖 Coach response:")
        print(f"   {coach_resp}")
        print()

def test_judge_consistency():
    """Test if Judge gives consistent evaluations"""
    print("\n" + "="*70)
    print(" JUDGE CONSISTENCY TEST ".center(70, "="))
    print("="*70)
    
    # Different quality speeches
    speeches = {
        "Poor": "I... uh... want go shop... buy thing... uh... yes",
        "Average": "I want to go shopping tomorrow to buy some clothes for work",
        "Good": "I'm planning to visit the shopping center tomorrow afternoon to purchase some professional attire for my new job"
    }
    
    for level, speech in speeches.items():
        print(f"\n{level} Level Speech:")
        print("-" * 70)
        print(f"📝 '{speech}'")
        
        evaluation = judge_feedback(speech)
        print(f"\n⚖️ Evaluation:")
        print(evaluation)
        print()

def compare_scenarios():
    """Compare Coach behavior across scenarios"""
    print("\n" + "="*70)
    print(" SCENARIO COMPARISON TEST ".center(70, "="))
    print("="*70)
    
    user_msg = "Hello"
    
    for key, scenario in SCENARIOS.items():
        if key == "free":
            continue
        
        print(f"\n{'='*70}")
        print(f"Scenario: {scenario['title']}")
        print(f"AI Role: {scenario['role']}")
        print("-" * 70)
        
        response = coach_feedback(user_msg, None, scenario)
        print(f"🤖 Response: {response[:150]}...")
        print()

def main():
    """Main menu"""
    print("\n" + "🧪 LLM TESTING TOOL ".center(70, "="))
    print("\nSelect test to run:")
    print("1. 🚀 Quick Test (Coach + Judge)")
    print("2. 📊 Scenario Progression (Restaurant)")
    print("3. ✏️  Error Correction Test")
    print("4. 🎯 Judge Consistency Test")
    print("5. 🔄 Compare All Scenarios")
    print("6. 🌟 Run All Tests")
    
    choice = input("\nEnter number (1-6): ").strip()
    
    if choice == "1":
        quick_test()
    elif choice == "2":
        test_scenario_progression()
    elif choice == "3":
        test_error_correction()
    elif choice == "4":
        test_judge_consistency()
    elif choice == "5":
        compare_scenarios()
    elif choice == "6":
        print("\n🌟 Running all tests...\n")
        quick_test()
        test_scenario_progression()
        test_error_correction()
        test_judge_consistency()
        compare_scenarios()
        print("\n" + "="*70)
        print("✅ ALL TESTS COMPLETED!")
        print("="*70)
    else:
        print("Invalid choice, running quick test...")
        quick_test()

if __name__ == "__main__":
    main()
