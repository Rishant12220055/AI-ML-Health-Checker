"""
AI Healthcare Assistant - Accuracy Analysis
This script analyzes the diagnostic accuracy and performance metrics
"""
import sys
import os
import asyncio
from datetime import datetime

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

try:
    from models.schemas import PatientInfo, Symptom, SymptomInput, Severity
    from agents.coordinator import AgentCoordinator
    from utils.database_manager import DatabaseManager
    from utils.medical_guidelines import MedicalGuidelinesManager
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

async def analyze_accuracy():
    """Comprehensive accuracy analysis of the AI Healthcare Assistant"""
    
    print("📊 AI Healthcare Assistant - Accuracy Analysis")
    print("=" * 70)
    print(f"🕒 Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Initialize components
    print("🔧 Initializing system components...")
    db_manager = DatabaseManager()
    guidelines_manager = MedicalGuidelinesManager()
    coordinator = AgentCoordinator(db_manager, guidelines_manager)
    await coordinator.initialize_agents()
    
    # Test cases with known expected outcomes
    test_cases = [
        {
            "name": "Common Cold",
            "expected_top_condition": "Common Cold",
            "expected_urgency": "MODERATE",
            "patient": PatientInfo(age=28, gender="female", medical_history=[], medications=[], allergies=[]),
            "symptoms": [
                Symptom(name="runny nose", severity=Severity.MILD, duration="3 days", description="Clear nasal discharge"),
                Symptom(name="sore throat", severity=Severity.MILD, duration="2 days", description="Scratchy feeling"),
                Symptom(name="cough", severity=Severity.MILD, duration="2 days", description="Dry cough")
            ],
            "complaint": "I think I have a cold"
        },
        {
            "name": "Severe Chest Pain (Emergency)",
            "expected_top_condition": "Myocardial Infarction",
            "expected_urgency": "EMERGENCY",
            "patient": PatientInfo(age=55, gender="male", medical_history=["hypertension", "diabetes"], medications=["metformin"], allergies=[]),
            "symptoms": [
                Symptom(name="chest pain", severity=Severity.SEVERE, duration="30 minutes", description="Crushing chest pain"),
                Symptom(name="shortness of breath", severity=Severity.SEVERE, duration="30 minutes", description="Cannot breathe"),
                Symptom(name="nausea", severity=Severity.MODERATE, duration="30 minutes", description="Feeling sick")
            ],
            "complaint": "Severe chest pain and can't breathe"
        },
        {
            "name": "Tension Headache",
            "expected_top_condition": "Tension Headache",
            "expected_urgency": "LOW",
            "patient": PatientInfo(age=32, gender="female", medical_history=[], medications=[], allergies=[]),
            "symptoms": [
                Symptom(name="headache", severity=Severity.MODERATE, duration="4 hours", description="Band-like pressure around head"),
                Symptom(name="neck tension", severity=Severity.MILD, duration="4 hours", description="Tight neck muscles")
            ],
            "complaint": "Tension headache from work stress"
        },
        {
            "name": "Flu Symptoms",
            "expected_top_condition": "Influenza",
            "expected_urgency": "MODERATE",
            "patient": PatientInfo(age=25, gender="male", medical_history=[], medications=[], allergies=[]),
            "symptoms": [
                Symptom(name="fever", severity=Severity.MODERATE, duration="2 days", description="102°F temperature"),
                Symptom(name="body aches", severity=Severity.MODERATE, duration="2 days", description="Muscle aches all over"),
                Symptom(name="fatigue", severity=Severity.SEVERE, duration="2 days", description="Extreme tiredness"),
                Symptom(name="cough", severity=Severity.MILD, duration="1 day", description="Dry cough")
            ],
            "complaint": "Feel like I have the flu"
        },
        {
            "name": "Migraine",
            "expected_top_condition": "Migraine",
            "expected_urgency": "MODERATE",
            "patient": PatientInfo(age=29, gender="female", medical_history=["migraine"], medications=[], allergies=[]),
            "symptoms": [
                Symptom(name="severe headache", severity=Severity.SEVERE, duration="6 hours", description="Throbbing pain on one side"),
                Symptom(name="nausea", severity=Severity.MODERATE, duration="6 hours", description="Feeling nauseous"),
                Symptom(name="light sensitivity", severity=Severity.MODERATE, duration="6 hours", description="Light hurts eyes")
            ],
            "complaint": "Severe migraine attack"
        }
    ]
    
    # Track accuracy metrics
    total_tests = len(test_cases)
    correct_top_diagnosis = 0
    correct_urgency = 0
    confidence_scores = []
    processing_times = []
    
    print(f"\n🧪 Running {total_tests} accuracy test cases...")
    print("=" * 70)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 TEST {i}: {test_case['name']}")
        print("-" * 40)
        
        # Create symptom input
        symptom_input = SymptomInput(
            patient_info=test_case["patient"],
            symptoms=test_case["symptoms"],
            chief_complaint=test_case["complaint"],
            additional_notes="Accuracy test case"
        )
        
        try:
            # Time the processing
            start_time = datetime.now()
            result = await coordinator.process_symptoms(symptom_input)
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            processing_times.append(processing_time)
            
            # Get top diagnosis
            top_condition = result.possible_conditions[0] if result.possible_conditions else None
            
            # Check accuracy
            top_diagnosis_correct = False
            urgency_correct = False
            
            if top_condition:
                # Check if expected condition is in top 3 results
                top_3_names = [cond.name for cond in result.possible_conditions[:3]]
                if test_case["expected_top_condition"] in top_3_names:
                    top_diagnosis_correct = True
                    if top_condition.name == test_case["expected_top_condition"]:
                        correct_top_diagnosis += 1
                
                confidence_scores.append(top_condition.probability)
                
                print(f"✅ Top Diagnosis: {top_condition.name} ({top_condition.probability:.1%} confidence)")
                print(f"🎯 Expected: {test_case['expected_top_condition']}")
                print(f"✅ Match: {'✅ Yes' if top_diagnosis_correct else '❌ No'}")
            
            # Check urgency accuracy
            actual_urgency = str(result.urgency_level).split('.')[-1]
            expected_urgency = test_case["expected_urgency"]
            if actual_urgency == expected_urgency:
                urgency_correct = True
                correct_urgency += 1
            
            print(f"🚨 Urgency: {actual_urgency}")
            print(f"🎯 Expected: {expected_urgency}")
            print(f"✅ Match: {'✅ Yes' if urgency_correct else '❌ No'}")
            print(f"⏱️  Processing Time: {processing_time:.2f}s")
            
            # Additional metrics
            print(f"🏥 Treatment Options: {len(result.recommended_treatments)}")
            print(f"⚠️  Warning Signs: {len(result.warning_signs)}")
            print(f"💡 Next Steps: {len(result.next_steps)}")
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            processing_times.append(0)
            confidence_scores.append(0)
    
    # Calculate overall accuracy metrics
    print("\n" + "=" * 70)
    print("📈 OVERALL ACCURACY ANALYSIS")
    print("=" * 70)
    
    diagnosis_accuracy = (correct_top_diagnosis / total_tests) * 100
    urgency_accuracy = (correct_urgency / total_tests) * 100
    avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
    avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
    
    print(f"🎯 Diagnostic Accuracy: {diagnosis_accuracy:.1f}% ({correct_top_diagnosis}/{total_tests})")
    print(f"🚨 Urgency Assessment Accuracy: {urgency_accuracy:.1f}% ({correct_urgency}/{total_tests})")
    print(f"🔥 Average Confidence Score: {avg_confidence:.1f}%")
    print(f"⏱️  Average Processing Time: {avg_processing_time:.2f} seconds")
    
    # Performance ratings
    print("\n📊 PERFORMANCE RATINGS:")
    print("-" * 30)
    
    if diagnosis_accuracy >= 80:
        print("🌟 Diagnostic Accuracy: EXCELLENT")
    elif diagnosis_accuracy >= 70:
        print("⭐ Diagnostic Accuracy: GOOD")
    elif diagnosis_accuracy >= 60:
        print("🔶 Diagnostic Accuracy: FAIR")
    else:
        print("🔴 Diagnostic Accuracy: NEEDS IMPROVEMENT")
    
    if urgency_accuracy >= 90:
        print("🌟 Urgency Assessment: EXCELLENT")
    elif urgency_accuracy >= 80:
        print("⭐ Urgency Assessment: GOOD")
    elif urgency_accuracy >= 70:
        print("🔶 Urgency Assessment: FAIR")
    else:
        print("🔴 Urgency Assessment: NEEDS IMPROVEMENT")
    
    if avg_confidence >= 70:
        print("🌟 AI Confidence: HIGH")
    elif avg_confidence >= 60:
        print("⭐ AI Confidence: MODERATE")
    else:
        print("🔶 AI Confidence: LOW")
    
    if avg_processing_time <= 2.0:
        print("🌟 Response Speed: EXCELLENT")
    elif avg_processing_time <= 5.0:
        print("⭐ Response Speed: GOOD")
    else:
        print("🔶 Response Speed: ACCEPTABLE")
    
    # Overall system grade
    overall_score = (diagnosis_accuracy + urgency_accuracy) / 2
    print(f"\n🏆 OVERALL SYSTEM SCORE: {overall_score:.1f}%")
    
    if overall_score >= 85:
        print("🎉 GRADE: A+ (PRODUCTION READY)")
    elif overall_score >= 75:
        print("✅ GRADE: A (HIGHLY RELIABLE)")
    elif overall_score >= 65:
        print("⚡ GRADE: B (GOOD PERFORMANCE)")
    else:
        print("⚠️  GRADE: C (NEEDS IMPROVEMENT)")
    
    print("\n" + "=" * 70)
    print("🏥 AI Healthcare Assistant accuracy analysis complete!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(analyze_accuracy())
