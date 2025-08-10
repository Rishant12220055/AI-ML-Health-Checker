import axios, { AxiosResponse } from 'axios';

// Types for API communication
export interface Symptom {
  name: string;
  severity: 'mild' | 'moderate' | 'severe' | 'critical';
  duration?: string;
  description?: string;
  location?: string;
}

export interface PatientInfo {
  age: number;
  gender: string;
  medical_history: string[];
  medications: string[];
  allergies: string[];
}

export interface SymptomInput {
  symptoms: Symptom[];
  patient_info: PatientInfo;
  chief_complaint: string;
  additional_notes?: string;
}

export interface Condition {
  name: string;
  icd_code?: string;
  probability: number;
  confidence: number;
  description: string;
  symptoms_match: string[];
  risk_factors: string[];
}

export interface Treatment {
  name: string;
  type: string;
  description: string;
  dosage?: string;
  duration?: string;
  side_effects: string[];
  contraindications: string[];
  who_guideline?: string;
  cdc_guideline?: string;
}

export interface DiagnosisExplanation {
  reasoning_steps: string[];
  evidence_supporting: string[];
  evidence_against: string[];
  alternative_diagnoses: string[];
  confidence_factors: Record<string, number>;
  guidelines_used: string[];
}

export interface DiagnosisResponse {
  session_id: string;
  timestamp: string;
  urgency_level: 'emergency' | 'urgent' | 'moderate' | 'low';
  symptom_classification: Record<string, any>;
  possible_conditions: Condition[];
  recommended_treatments: Treatment[];
  next_steps: string[];
  warning_signs: string[];
  when_to_seek_care: string;
  explanation: DiagnosisExplanation;
  disclaimer: string;
}

export interface UrgencyAssessment {
  urgency_level: string;
  symptoms: string[];
}

export interface HealthStatus {
  status: string;
  database: boolean;
  guidelines: boolean;
  agents: Record<string, boolean>;
}

// Configure axios instance
// In Vite, environment variables use import.meta.env and must be prefixed with VITE_
const API_BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL;

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth tokens or other headers
apiClient.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 500) {
      console.error('Server error:', error.response.data);
    } else if (error.response?.status === 404) {
      console.error('Endpoint not found:', error.config.url);
    } else if (error.code === 'ECONNABORTED') {
      console.error('Request timeout');
    }
    return Promise.reject(error);
  }
);

// API service class
class HealthcareAPI {
  // Health check endpoint
  async healthCheck(): Promise<HealthStatus> {
    const response: AxiosResponse<HealthStatus> = await apiClient.get('/health');
    return response.data;
  }

  // Main symptom analysis endpoint
  async analyzeSymptoms(symptomInput: SymptomInput): Promise<DiagnosisResponse> {
    const response: AxiosResponse<DiagnosisResponse> = await apiClient.post(
      '/analyze-symptoms',
      symptomInput
    );
    return response.data;
  }

  // Quick urgency assessment
  async assessUrgency(symptoms: string[]): Promise<UrgencyAssessment> {
    const response: AxiosResponse<UrgencyAssessment> = await apiClient.post(
      '/assess-urgency',
      { symptoms }
    );
    return response.data;
  }

  // Get information about a specific condition
  async getConditionInfo(conditionName: string): Promise<any> {
    const response: AxiosResponse<any> = await apiClient.get(
      `/conditions/${encodeURIComponent(conditionName)}`
    );
    return response.data;
  }

  // Get treatment guidelines for a condition
  async getTreatments(conditionName: string): Promise<any> {
    const response: AxiosResponse<any> = await apiClient.get(
      `/treatments/${encodeURIComponent(conditionName)}`
    );
    return response.data;
  }

  // Get explainable AI output for a diagnosis
  async explainDiagnosis(diagnosisId: string): Promise<any> {
    const response: AxiosResponse<any> = await apiClient.post(
      '/explain-diagnosis',
      { diagnosis_id: diagnosisId }
    );
    return response.data;
  }

  // Get WHO guidelines
  async getWHOGuidelines(): Promise<any> {
    const response: AxiosResponse<any> = await apiClient.get('/medical-guidelines/who');
    return response.data;
  }

  // Get CDC guidelines
  async getCDCGuidelines(): Promise<any> {
    const response: AxiosResponse<any> = await apiClient.get('/medical-guidelines/cdc');
    return response.data;
  }

  // ---------------- Enhanced v2 Endpoints ----------------
  async diagnoseV2(symptomInput: SymptomInput): Promise<DiagnosisResponse> {
    const response: AxiosResponse<DiagnosisResponse> = await apiClient.post('/api/v2/diagnose', symptomInput);
    return response.data;
  }

  async emergencyCheck(symptomInput: SymptomInput): Promise<any> {
    // Send SymptomInput directly, not nested
    const response: AxiosResponse<any> = await apiClient.post('/api/v2/emergency-check', symptomInput);
    return response.data;
  }

  async riskAssessment(patientInfo: PatientInfo, symptomInput: SymptomInput): Promise<any> {
    const response: AxiosResponse<any> = await apiClient.post('/api/v2/risk-assessment', {
      patient_info: patientInfo,
      symptom_input: symptomInput,
    } as any);
    return response.data;
  }

  async checkDrugInteractions(medications: string[], patientAge: number, allergies: string[] = []): Promise<any> {
    const response: AxiosResponse<any> = await apiClient.post('/api/v2/drug-interactions', {
      medications,
      patient_age: patientAge,
      allergies,
    });
    return response.data;
  }

  async uncertaintyAnalysis(symptomInput: SymptomInput, predictedConditions: any[] = [], treatments: any[] = []): Promise<any> {
    const response: AxiosResponse<any> = await apiClient.post('/api/v2/uncertainty-analysis', {
      symptom_input: symptomInput,
      predicted_conditions: predictedConditions,
      treatments,
    } as any);
    return response.data;
  }

  async getAnalyticsDashboard(hours = 24): Promise<any> {
    const response: AxiosResponse<any> = await apiClient.get(`/api/v2/analytics/dashboard`, { params: { hours } });
    return response.data;
  }

  async getMetrics(metricType: string, hours = 24): Promise<any> {
    const response: AxiosResponse<any> = await apiClient.get(`/api/v2/analytics/metrics/${encodeURIComponent(metricType)}`, { params: { hours } });
    return response.data;
  }

  async getAdvancedHealth(): Promise<any> {
    const response: AxiosResponse<any> = await apiClient.get('/api/v2/system/health-advanced');
    return response.data;
  }

  async getSystemPerformance(): Promise<any> {
    const response: AxiosResponse<any> = await apiClient.get('/api/v2/system/performance');
    return response.data;
  }

  async submitFeedback(sessionId: string, rating: number, feedbackText?: string, improvementSuggestions: string[] = []): Promise<any> {
    const response: AxiosResponse<any> = await apiClient.post('/api/v2/feedback', null, {
      params: {
        session_id: sessionId,
        rating,
        feedback_text: feedbackText,
        improvement_suggestions: improvementSuggestions,
      },
    });
    return response.data;
  }
}

// Create and export singleton instance
const healthcareAPI = new HealthcareAPI();
export default healthcareAPI;

// Utility functions for common operations
export const validateSymptomInput = (input: SymptomInput): string[] => {
  const errors: string[] = [];

  if (!input.symptoms || input.symptoms.length === 0) {
    errors.push('At least one symptom must be provided');
  }

  if (!input.patient_info) {
    errors.push('Patient information is required');
  } else {
    if (!input.patient_info.age || input.patient_info.age < 0 || input.patient_info.age > 150) {
      errors.push('Valid age is required');
    }
    if (!input.patient_info.gender) {
      errors.push('Gender is required');
    }
  }

  if (!input.chief_complaint || input.chief_complaint.trim().length === 0) {
    errors.push('Chief complaint is required');
  }

  return errors;
};

export const formatUrgencyLevel = (level: string): { text: string; color: string } => {
  const urgencyMap = {
    emergency: { text: 'Emergency - Seek immediate care', color: '#d32f2f' },
    urgent: { text: 'Urgent - Seek care within 24 hours', color: '#f57c00' },
    moderate: { text: 'Moderate - Schedule appointment soon', color: '#fbc02d' },
    low: { text: 'Low - Monitor symptoms', color: '#388e3c' },
  };

  return urgencyMap[level as keyof typeof urgencyMap] || { text: 'Unknown', color: '#757575' };
};

export const formatConfidence = (confidence: number): string => {
  if (confidence >= 0.8) return 'High confidence';
  if (confidence >= 0.6) return 'Moderate confidence';
  if (confidence >= 0.4) return 'Low confidence';
  return 'Very low confidence';
};

// Error handling utility
export const handleAPIError = (error: any): string => {
  if (error.response) {
    // Server responded with error status
    if (error.response.status === 500) {
      return 'Server error occurred. Please try again later.';
    } else if (error.response.status === 404) {
      return 'Service not found. Please check your connection.';
    } else if (error.response.status === 400) {
      return error.response.data?.detail || 'Invalid request. Please check your input.';
    }
  } else if (error.request) {
    // Network error
    return 'Network error. Please check your internet connection.';
  } else if (error.code === 'ECONNABORTED') {
    // Timeout error
    return 'Request timed out. Please try again.';
  }
  
  return 'An unexpected error occurred. Please try again.';
};
