import asyncio
import json
from models.schemas import SymptomInput, Symptom, Severity, PatientInfo
from agents.condition_matcher import ConditionMatcherAgent


async def main():
    agent = ConditionMatcherAgent()
    await agent.initialize()
    inp = SymptomInput(
        symptoms=[
            Symptom(name="fever", severity=Severity.MODERATE),
            Symptom(name="cough", severity=Severity.MILD),
            Symptom(name="fatigue", severity=Severity.MILD),
        ],
        patient_info=PatientInfo(age=30, gender="male"),
        chief_complaint="Fever and cough",
    )
    res = await agent.process_symptoms(inp, {})
    # Pydantic v1/v2 compatibility
    to_dict = getattr(res, "model_dump", None) or getattr(res, "dict")
    data = to_dict()
    dd = data.get("results", {}).get("differential_diagnosis", [])
    out = {
        "agent": data.get("agent_name"),
        "confidence": data.get("confidence"),
        "dd_count": len(dd),
        "top": dd[0] if dd else None,
    }
    print(json.dumps(out))


if __name__ == "__main__":
    asyncio.run(main())
