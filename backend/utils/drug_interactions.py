"""
Drug Interaction and Medication Safety System

This module provides comprehensive drug interaction checking,
contraindication analysis, and medication safety protocols.
"""

from typing import Dict, List, Any, Optional, Tuple, Set
from enum import Enum
from dataclasses import dataclass
import logging
from models.schemas import PatientInfo

logger = logging.getLogger(__name__)

class InteractionSeverity(str, Enum):
    """Drug interaction severity levels"""
    CONTRAINDICATED = "contraindicated"  # Never use together
    MAJOR = "major"                      # Significant clinical impact
    MODERATE = "moderate"                # Monitor closely
    MINOR = "minor"                      # Minimal clinical significance

class DrugCategory(str, Enum):
    """Drug categories for interaction checking"""
    ANTICOAGULANT = "anticoagulant"
    ANTIBIOTIC = "antibiotic"
    ANTIHYPERTENSIVE = "antihypertensive"
    DIABETES_MEDICATION = "diabetes_medication"
    NSAID = "nsaid"
    ANTIDEPRESSANT = "antidepressant"
    CARDIAC_MEDICATION = "cardiac_medication"
    ANTICONVULSANT = "anticonvulsant"

@dataclass
class DrugInteraction:
    """Drug interaction data structure"""
    drug1: str
    drug2: str
    severity: InteractionSeverity
    mechanism: str
    clinical_effect: str
    management: str
    reference: str

@dataclass
class Contraindication:
    """Contraindication data structure"""
    medication: str
    condition: str
    reason: str
    severity: str
    alternative: Optional[str] = None

class DrugInteractionSystem:
    """Comprehensive drug interaction and safety checking system"""
    
    def __init__(self):
        self.drug_interactions = self._load_drug_interactions()
        self.contraindications = self._load_contraindications()
        self.drug_categories = self._load_drug_categories()
        self.age_restrictions = self._load_age_restrictions()
        self.pregnancy_categories = self._load_pregnancy_categories()
        
    def _load_drug_interactions(self) -> List[DrugInteraction]:
        """Load comprehensive drug interaction database"""
        return [
            # Anticoagulant interactions
            DrugInteraction(
                drug1="warfarin", drug2="aspirin",
                severity=InteractionSeverity.MAJOR,
                mechanism="Additive anticoagulant effects",
                clinical_effect="Increased bleeding risk",
                management="Monitor INR closely, consider dose reduction",
                reference="FDA Drug Interactions Database"
            ),
            DrugInteraction(
                drug1="warfarin", drug2="ibuprofen",
                severity=InteractionSeverity.MAJOR,
                mechanism="Antiplatelet effect + anticoagulation",
                clinical_effect="Significantly increased bleeding risk",
                management="Avoid combination, use alternative pain relief",
                reference="Clinical Pharmacology Guidelines"
            ),
            
            # Cardiac medication interactions
            DrugInteraction(
                drug1="digoxin", drug2="amiodarone",
                severity=InteractionSeverity.MAJOR,
                mechanism="Reduced digoxin clearance",
                clinical_effect="Digoxin toxicity",
                management="Reduce digoxin dose by 50%, monitor levels",
                reference="Cardiology Drug Interaction Guide"
            ),
            
            # Diabetes medication interactions
            DrugInteraction(
                drug1="metformin", drug2="contrast_dye",
                severity=InteractionSeverity.CONTRAINDICATED,
                mechanism="Increased lactic acidosis risk",
                clinical_effect="Potentially fatal lactic acidosis",
                management="Stop metformin 48h before contrast procedures",
                reference="Diabetes Care Guidelines"
            ),
            
            # NSAID interactions
            DrugInteraction(
                drug1="ibuprofen", drug2="lisinopril",
                severity=InteractionSeverity.MODERATE,
                mechanism="Reduced ACE inhibitor effectiveness",
                clinical_effect="Decreased blood pressure control",
                management="Monitor blood pressure, consider alternative",
                reference="Hypertension Management Guidelines"
            ),
            
            # Antibiotic interactions
            DrugInteraction(
                drug1="ciprofloxacin", drug2="theophylline",
                severity=InteractionSeverity.MAJOR,
                mechanism="Inhibited theophylline metabolism",
                clinical_effect="Theophylline toxicity",
                management="Monitor theophylline levels, dose adjustment",
                reference="Antibiotic Interaction Database"
            ),
            
            # Antidepressant interactions
            DrugInteraction(
                drug1="sertraline", drug2="tramadol",
                severity=InteractionSeverity.MAJOR,
                mechanism="Serotonin syndrome risk",
                clinical_effect="Potentially life-threatening serotonin syndrome",
                management="Avoid combination, use alternative analgesic",
                reference="Psychiatry Drug Safety Guidelines"
            ),
            
            # Multiple drug class interactions
            DrugInteraction(
                drug1="atorvastatin", drug2="clarithromycin",
                severity=InteractionSeverity.MAJOR,
                mechanism="CYP3A4 inhibition",
                clinical_effect="Increased statin levels, rhabdomyolysis risk",
                management="Temporarily discontinue statin during antibiotic course",
                reference="Lipid Management Guidelines"
            )
        ]
    
    def _load_contraindications(self) -> List[Contraindication]:
        """Load medication contraindications based on medical conditions"""
        return [
            # Cardiovascular contraindications
            Contraindication(
                medication="metoprolol", condition="severe_asthma",
                reason="Beta-blockers can worsen bronchospasm",
                severity="absolute", alternative="amlodipine"
            ),
            Contraindication(
                medication="verapamil", condition="heart_failure",
                reason="Negative inotropic effects worsen heart failure",
                severity="absolute", alternative="amlodipine"
            ),
            
            # Renal contraindications
            Contraindication(
                medication="ibuprofen", condition="chronic_kidney_disease",
                reason="NSAIDs reduce kidney function",
                severity="relative", alternative="acetaminophen"
            ),
            Contraindication(
                medication="metformin", condition="severe_kidney_disease",
                reason="Risk of lactic acidosis",
                severity="absolute", alternative="insulin"
            ),
            
            # Liver contraindications
            Contraindication(
                medication="acetaminophen", condition="severe_liver_disease",
                reason="Hepatotoxicity risk",
                severity="relative", alternative="ibuprofen (if kidney function normal)"
            ),
            
            # Gastrointestinal contraindications
            Contraindication(
                medication="aspirin", condition="peptic_ulcer_disease",
                reason="Increased bleeding and ulcer risk",
                severity="relative", alternative="acetaminophen"
            ),
            
            # Respiratory contraindications
            Contraindication(
                medication="morphine", condition="severe_respiratory_depression",
                reason="Further respiratory depression",
                severity="absolute", alternative="non-opioid analgesics"
            ),
            
            # Allergy contraindications
            Contraindication(
                medication="penicillin", condition="penicillin_allergy",
                reason="Allergic reaction risk",
                severity="absolute", alternative="cephalexin (if no cross-reactivity)"
            )
        ]
    
    def _load_drug_categories(self) -> Dict[str, DrugCategory]:
        """Map medications to their therapeutic categories"""
        return {
            # Cardiovascular
            "warfarin": DrugCategory.ANTICOAGULANT,
            "heparin": DrugCategory.ANTICOAGULANT,
            "aspirin": DrugCategory.ANTICOAGULANT,
            "lisinopril": DrugCategory.ANTIHYPERTENSIVE,
            "metoprolol": DrugCategory.ANTIHYPERTENSIVE,
            "amlodipine": DrugCategory.ANTIHYPERTENSIVE,
            "digoxin": DrugCategory.CARDIAC_MEDICATION,
            
            # Diabetes
            "metformin": DrugCategory.DIABETES_MEDICATION,
            "insulin": DrugCategory.DIABETES_MEDICATION,
            "glipizide": DrugCategory.DIABETES_MEDICATION,
            
            # Anti-inflammatory
            "ibuprofen": DrugCategory.NSAID,
            "naproxen": DrugCategory.NSAID,
            "diclofenac": DrugCategory.NSAID,
            
            # Antibiotics
            "amoxicillin": DrugCategory.ANTIBIOTIC,
            "ciprofloxacin": DrugCategory.ANTIBIOTIC,
            "azithromycin": DrugCategory.ANTIBIOTIC,
            
            # Mental health
            "sertraline": DrugCategory.ANTIDEPRESSANT,
            "fluoxetine": DrugCategory.ANTIDEPRESSANT,
            "escitalopram": DrugCategory.ANTIDEPRESSANT
        }
    
    def _load_age_restrictions(self) -> Dict[str, Dict[str, Any]]:
        """Load age-based medication restrictions"""
        return {
            "aspirin": {
                "min_age": 18,
                "reason": "Reye's syndrome risk in children",
                "alternative": "acetaminophen"
            },
            "tetracycline": {
                "min_age": 8,
                "reason": "Tooth discoloration in developing teeth",
                "alternative": "amoxicillin"
            },
            "codeine": {
                "min_age": 18,
                "reason": "Respiratory depression risk in children",
                "alternative": "acetaminophen"
            },
            "benzodiazepines": {
                "elderly_caution": True,
                "reason": "Increased fall risk and cognitive impairment",
                "alternative": "non-benzodiazepine alternatives"
            }
        }
    
    def _load_pregnancy_categories(self) -> Dict[str, Dict[str, str]]:
        """Load pregnancy safety categories"""
        return {
            "metformin": {"category": "B", "safety": "Generally safe"},
            "insulin": {"category": "B", "safety": "Preferred for diabetes"},
            "warfarin": {"category": "X", "safety": "Contraindicated - teratogenic"},
            "lisinopril": {"category": "D", "safety": "Avoid - fetal toxicity"},
            "ibuprofen": {"category": "C/D", "safety": "Avoid in 3rd trimester"},
            "acetaminophen": {"category": "B", "safety": "Generally safe"}
        }
    
    async def check_drug_interactions(self, current_medications: List[str], 
                                    proposed_medication: str) -> Dict[str, Any]:
        """
        Comprehensive drug interaction checking
        
        Args:
            current_medications: List of patient's current medications
            proposed_medication: New medication being considered
            
        Returns:
            Dict containing interaction analysis and recommendations
        """
        try:
            all_medications = current_medications + [proposed_medication]
            interactions_found = []
            severity_summary = {
                "contraindicated": 0,
                "major": 0,
                "moderate": 0,
                "minor": 0
            }
            
            # Check each pair of medications
            for i, med1 in enumerate(all_medications):
                for med2 in all_medications[i+1:]:
                    interaction = self._find_interaction(med1.lower(), med2.lower())
                    if interaction:
                        interactions_found.append(interaction)
                        severity_summary[interaction.severity.value] += 1
            
            # Generate recommendations
            recommendations = self._generate_interaction_recommendations(interactions_found)
            
            # Check for drug class interactions
            class_warnings = self._check_drug_class_interactions(all_medications)
            
            return {
                "interactions_found": len(interactions_found),
                "interactions": [self._interaction_to_dict(i) for i in interactions_found],
                "severity_summary": severity_summary,
                "recommendations": recommendations,
                "class_warnings": class_warnings,
                "safe_to_prescribe": len([i for i in interactions_found if i.severity in [InteractionSeverity.CONTRAINDICATED, InteractionSeverity.MAJOR]]) == 0,
                "requires_monitoring": severity_summary["moderate"] > 0 or severity_summary["major"] > 0
            }
            
        except Exception as e:
            logger.error(f"Error checking drug interactions: {e}")
            return {
                "error": "Unable to check interactions",
                "safe_to_prescribe": False,
                "recommendations": ["Consult pharmacist or physician before prescribing"]
            }
    
    async def check_contraindications(self, medication: str, 
                                    patient_info: PatientInfo) -> Dict[str, Any]:
        """
        Check for contraindications based on patient conditions
        
        Args:
            medication: Medication being considered
            patient_info: Patient medical information
            
        Returns:
            Dict containing contraindication analysis
        """
        try:
            contraindications_found = []
            patient_conditions = [condition.lower() for condition in patient_info.medical_history or []]
            
            # Check medical history contraindications
            for contraindication in self.contraindications:
                if (contraindication.medication.lower() in medication.lower() and
                    any(condition in contraindication.condition for condition in patient_conditions)):
                    contraindications_found.append(contraindication)
            
            # Check age restrictions
            age_warnings = self._check_age_restrictions(medication, patient_info.age)
            
            # Check pregnancy considerations (if applicable)
            pregnancy_warnings = []
            if patient_info.gender.lower() == "female":
                pregnancy_warnings = self._check_pregnancy_safety(medication)
            
            # Check allergy contraindications
            allergy_warnings = self._check_drug_allergies(medication, patient_info.allergies or [])
            
            return {
                "contraindications_found": len(contraindications_found),
                "contraindications": [self._contraindication_to_dict(c) for c in contraindications_found],
                "age_warnings": age_warnings,
                "pregnancy_warnings": pregnancy_warnings,
                "allergy_warnings": allergy_warnings,
                "safe_to_prescribe": len(contraindications_found) == 0 and len(allergy_warnings) == 0,
                "requires_caution": len(age_warnings) > 0 or len(pregnancy_warnings) > 0
            }
            
        except Exception as e:
            logger.error(f"Error checking contraindications: {e}")
            return {
                "error": "Unable to check contraindications",
                "safe_to_prescribe": False
            }
    
    async def suggest_alternatives(self, medication: str, 
                                 contraindications: List[str]) -> List[Dict[str, Any]]:
        """Suggest alternative medications when contraindications exist"""
        alternatives = []
        
        # Get medication category
        med_category = self.drug_categories.get(medication.lower())
        if not med_category:
            return alternatives
        
        # Find alternatives in same category
        for drug, category in self.drug_categories.items():
            if category == med_category and drug != medication.lower():
                # Check if alternative has fewer contraindications
                alt_contraindications = [
                    c for c in self.contraindications 
                    if c.medication.lower() == drug and c.condition in contraindications
                ]
                
                if len(alt_contraindications) < len(contraindications):
                    alternatives.append({
                        "medication": drug.title(),
                        "category": category.value,
                        "fewer_contraindications": len(alt_contraindications),
                        "reason": f"Alternative in same therapeutic class with fewer contraindications"
                    })
        
        return alternatives[:5]  # Return top 5 alternatives
    
    def _find_interaction(self, med1: str, med2: str) -> Optional[DrugInteraction]:
        """Find interaction between two medications"""
        for interaction in self.drug_interactions:
            if ((interaction.drug1.lower() == med1 and interaction.drug2.lower() == med2) or
                (interaction.drug1.lower() == med2 and interaction.drug2.lower() == med1)):
                return interaction
        return None
    
    def _generate_interaction_recommendations(self, interactions: List[DrugInteraction]) -> List[str]:
        """Generate recommendations based on found interactions"""
        recommendations = []
        
        contraindicated = [i for i in interactions if i.severity == InteractionSeverity.CONTRAINDICATED]
        major = [i for i in interactions if i.severity == InteractionSeverity.MAJOR]
        moderate = [i for i in interactions if i.severity == InteractionSeverity.MODERATE]
        
        if contraindicated:
            recommendations.append("DO NOT USE TOGETHER - Contraindicated drug combination found")
            recommendations.extend([i.management for i in contraindicated])
        
        if major:
            recommendations.append("MAJOR INTERACTION - Requires immediate physician consultation")
            recommendations.extend([i.management for i in major])
        
        if moderate:
            recommendations.append("Monitor closely for adverse effects")
            recommendations.extend([i.management for i in moderate])
        
        if not interactions:
            recommendations.append("No significant drug interactions found")
        
        return recommendations
    
    def _check_drug_class_interactions(self, medications: List[str]) -> List[str]:
        """Check for interactions between drug classes"""
        warnings = []
        drug_classes = []
        
        for med in medications:
            category = self.drug_categories.get(med.lower())
            if category:
                drug_classes.append(category)
        
        # Check for problematic combinations
        if DrugCategory.ANTICOAGULANT in drug_classes and DrugCategory.NSAID in drug_classes:
            warnings.append("Anticoagulant + NSAID: Increased bleeding risk")
        
        if drug_classes.count(DrugCategory.ANTIHYPERTENSIVE) > 2:
            warnings.append("Multiple blood pressure medications: Monitor for hypotension")
        
        return warnings
    
    def _check_age_restrictions(self, medication: str, age: int) -> List[str]:
        """Check age-based medication restrictions"""
        warnings = []
        
        for drug, restrictions in self.age_restrictions.items():
            if drug.lower() in medication.lower():
                if "min_age" in restrictions and age < restrictions["min_age"]:
                    warnings.append(f"{drug.title()}: {restrictions['reason']} (Min age: {restrictions['min_age']})")
                
                if "elderly_caution" in restrictions and age >= 65:
                    warnings.append(f"{drug.title()}: {restrictions['reason']} (Elderly patient)")
        
        return warnings
    
    def _check_pregnancy_safety(self, medication: str) -> List[str]:
        """Check pregnancy safety considerations"""
        warnings = []
        
        for drug, info in self.pregnancy_categories.items():
            if drug.lower() in medication.lower():
                if info["category"] in ["D", "X"]:
                    warnings.append(f"{drug.title()}: Category {info['category']} - {info['safety']}")
                elif info["category"] == "C":
                    warnings.append(f"{drug.title()}: Category C - Use only if benefits outweigh risks")
        
        return warnings
    
    def _check_drug_allergies(self, medication: str, allergies: List[str]) -> List[str]:
        """Check for drug allergy contraindications"""
        warnings = []
        
        for allergy in allergies:
            allergy_lower = allergy.lower()
            if allergy_lower in medication.lower():
                warnings.append(f"ALLERGY ALERT: Patient allergic to {allergy}")
            
            # Check for cross-reactivity
            if "penicillin" in allergy_lower and any(x in medication.lower() for x in ["amoxicillin", "ampicillin"]):
                warnings.append("CROSS-REACTIVITY: Penicillin allergy may cross-react with this medication")
        
        return warnings
    
    def _interaction_to_dict(self, interaction: DrugInteraction) -> Dict[str, Any]:
        """Convert DrugInteraction to dictionary"""
        return {
            "drug1": interaction.drug1,
            "drug2": interaction.drug2,
            "severity": interaction.severity.value,
            "mechanism": interaction.mechanism,
            "clinical_effect": interaction.clinical_effect,
            "management": interaction.management,
            "reference": interaction.reference
        }
    
    def _contraindication_to_dict(self, contraindication: Contraindication) -> Dict[str, Any]:
        """Convert Contraindication to dictionary"""
        return {
            "medication": contraindication.medication,
            "condition": contraindication.condition,
            "reason": contraindication.reason,
            "severity": contraindication.severity,
            "alternative": contraindication.alternative
        }
