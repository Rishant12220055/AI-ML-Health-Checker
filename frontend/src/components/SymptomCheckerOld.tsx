import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Chip,
  Grid,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Stepper,
  Step,
  StepLabel,
  useTheme,
  alpha,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Add, Delete, Send, ArrowBack, ArrowForward } from '@mui/icons-material';
import { useMutation } from 'react-query';
import healthcareAPI, { Symptom, PatientInfo, SymptomInput } from '../services/api';

const steps = ['Patient Information', 'Symptoms', 'Review & Submit'];

const SymptomChecker: React.FC = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const [activeStep, setActiveStep] = useState(0);
  const [patientInfo, setPatientInfo] = useState<PatientInfo>({
    age: 0,
    gender: '',
    medical_history: [],
    medications: [],
    allergies: [],
  });
  const [symptoms, setSymptoms] = useState<Symptom[]>([]);
  const [chiefComplaint, setChiefComplaint] = useState('');
  const [additionalNotes, setAdditionalNotes] = useState('');
  const [currentSymptom, setCurrentSymptom] = useState<Symptom>({
    name: '',
    severity: 'mild',
    duration: '',
    description: '',
    location: '',
  });

  // Mutation for analyzing symptoms
  const analyzeSymptomsMutation = useMutation(
    (data: SymptomInput) => healthcareAPI.analyzeSymptoms(data),
    {
      onSuccess: (data) => {
        try {
          sessionStorage.setItem(`diagnosis_${data.session_id}`, JSON.stringify(data));
        } catch (e) {
          console.warn('Could not persist diagnosis in sessionStorage:', e);
        }
        navigate(`/results/${data.session_id}`);
      },
      onError: (error) => {
        console.error('Error analyzing symptoms:', error);
      },
    }
  );

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleAddSymptom = () => {
    if (currentSymptom.name.trim()) {
      setSymptoms([...symptoms, { ...currentSymptom }]);
      setCurrentSymptom({
        name: '',
        severity: 'mild',
        duration: '',
        description: '',
        location: '',
      });
    }
  };

  const handleRemoveSymptom = (index: number) => {
    setSymptoms(symptoms.filter((_, i) => i !== index));
  };

  const handleSubmit = () => {
    const symptomInput: SymptomInput = {
      symptoms,
      patient_info: patientInfo,
      chief_complaint: chiefComplaint,
      additional_notes: additionalNotes,
    };

    analyzeSymptomsMutation.mutate(symptomInput);
  };

  const isStepValid = (step: number): boolean => {
    switch (step) {
      case 0:
        return patientInfo.age > 0 && patientInfo.gender !== '';
      case 1:
        return symptoms.length > 0 && chiefComplaint.trim() !== '';
      case 2:
        return true;
      default:
        return false;
    }
  };

  const renderPatientInfoStep = () => (
    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <TextField
          fullWidth
          label="Age"
          type="number"
          value={patientInfo.age || ''}
          onChange={(e) =>
            setPatientInfo({ ...patientInfo, age: parseInt(e.target.value) || 0 })
          }
          inputProps={{ min: 0, max: 120 }}
          required
        />
      </Grid>
      <Grid item xs={12} md={6}>
        <FormControl fullWidth required>
          <InputLabel>Gender</InputLabel>
          <Select
            value={patientInfo.gender}
            onChange={(e) =>
              setPatientInfo({ ...patientInfo, gender: e.target.value })
            }
            label="Gender"
          >
            <MenuItem value="male">Male</MenuItem>
            <MenuItem value="female">Female</MenuItem>
            <MenuItem value="other">Other</MenuItem>
            <MenuItem value="prefer_not_to_say">Prefer not to say</MenuItem>
          </Select>
        </FormControl>
      </Grid>
      <Grid item xs={12}>
        <TextField
          fullWidth
          label="Medical History (comma-separated)"
          multiline
          rows={2}
          value={patientInfo.medical_history.join(', ')}
          onChange={(e) =>
            setPatientInfo({
              ...patientInfo,
              medical_history: e.target.value.split(',').map((item) => item.trim()).filter(Boolean),
            })
          }
          placeholder="e.g., diabetes, hypertension, asthma"
        />
      </Grid>
      <Grid item xs={12}>
        <TextField
          fullWidth
          label="Current Medications (comma-separated)"
          multiline
          rows={2}
          value={patientInfo.medications.join(', ')}
          onChange={(e) =>
            setPatientInfo({
              ...patientInfo,
              medications: e.target.value.split(',').map((item) => item.trim()).filter(Boolean),
            })
          }
          placeholder="e.g., aspirin, metformin, lisinopril"
        />
      </Grid>
      <Grid item xs={12}>
        <TextField
          fullWidth
          label="Known Allergies (comma-separated)"
          multiline
          rows={2}
          value={patientInfo.allergies.join(', ')}
          onChange={(e) =>
            setPatientInfo({
              ...patientInfo,
              allergies: e.target.value.split(',').map((item) => item.trim()).filter(Boolean),
            })
          }
          placeholder="e.g., penicillin, peanuts, latex"
        />
      </Grid>
    </Grid>
  );

  const renderSymptomsStep = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Chief Complaint
      </Typography>
      <TextField
        fullWidth
        label="What is your main concern or reason for seeking medical advice?"
        multiline
        rows={3}
        value={chiefComplaint}
        onChange={(e) => setChiefComplaint(e.target.value)}
        required
        sx={{ mb: 3 }}
      />

      <Typography variant="h6" gutterBottom>
        Add Symptoms
      </Typography>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Symptom Name"
            value={currentSymptom.name}
            onChange={(e) =>
              setCurrentSymptom({ ...currentSymptom, name: e.target.value })
            }
            placeholder="e.g., headache, fever, cough"
          />
        </Grid>
        <Grid item xs={12} md={2}>
          <FormControl fullWidth>
            <InputLabel>Severity</InputLabel>
            <Select
              value={currentSymptom.severity}
              onChange={(e) =>
                setCurrentSymptom({
                  ...currentSymptom,
                  severity: e.target.value as Symptom['severity'],
                })
              }
              label="Severity"
            >
              <MenuItem value="mild">Mild</MenuItem>
              <MenuItem value="moderate">Moderate</MenuItem>
              <MenuItem value="severe">Severe</MenuItem>
              <MenuItem value="critical">Critical</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={2}>
          <TextField
            fullWidth
            label="Duration"
            value={currentSymptom.duration}
            onChange={(e) =>
              setCurrentSymptom({ ...currentSymptom, duration: e.target.value })
            }
            placeholder="e.g., 2 days, 1 week"
          />
        </Grid>
        <Grid item xs={12} md={2}>
          <TextField
            fullWidth
            label="Location"
            value={currentSymptom.location}
            onChange={(e) =>
              setCurrentSymptom({ ...currentSymptom, location: e.target.value })
            }
            placeholder="e.g., forehead, chest"
          />
        </Grid>
        <Grid item xs={12} md={2}>
          <Button
            fullWidth
            variant="contained"
            onClick={handleAddSymptom}
            startIcon={<Add />}
            disabled={!currentSymptom.name.trim()}
            sx={{ height: '56px' }}
          >
            Add
          </Button>
        </Grid>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Additional Description"
            value={currentSymptom.description}
            onChange={(e) =>
              setCurrentSymptom({ ...currentSymptom, description: e.target.value })
            }
            placeholder="Any additional details about this symptom"
          />
        </Grid>
      </Grid>

      {symptoms.length > 0 && (
        <Box>
          <Typography variant="h6" gutterBottom>
            Current Symptoms
          </Typography>
          <Grid container spacing={2}>
            {symptoms.map((symptom, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card>
                  <CardContent>
                    <Box display="flex" justifyContent="space-between" alignItems="start">
                      <Box>
                        <Typography variant="subtitle1" fontWeight="bold">
                          {symptom.name}
                        </Typography>
                        <Chip
                          label={symptom.severity}
                          size="small"
                          color={
                            symptom.severity === 'critical'
                              ? 'error'
                              : symptom.severity === 'severe'
                              ? 'warning'
                              : symptom.severity === 'moderate'
                              ? 'primary'
                              : 'default'
                          }
                          sx={{ mt: 1, mb: 1 }}
                        />
                        {symptom.duration && (
                          <Typography variant="body2" color="text.secondary">
                            Duration: {symptom.duration}
                          </Typography>
                        )}
                        {symptom.location && (
                          <Typography variant="body2" color="text.secondary">
                            Location: {symptom.location}
                          </Typography>
                        )}
                        {symptom.description && (
                          <Typography variant="body2" color="text.secondary">
                            {symptom.description}
                          </Typography>
                        )}
                      </Box>
                      <Button
                        size="small"
                        color="error"
                        onClick={() => handleRemoveSymptom(index)}
                        startIcon={<Delete />}
                      >
                        Remove
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      <TextField
        fullWidth
        label="Additional Notes"
        multiline
        rows={3}
        value={additionalNotes}
        onChange={(e) => setAdditionalNotes(e.target.value)}
        placeholder="Any other information you think might be relevant"
        sx={{ mt: 3 }}
      />
    </Box>
  );

  const renderReviewStep = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Review Your Information
      </Typography>
      
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
            Patient Information
          </Typography>
          <Typography>Age: {patientInfo.age}</Typography>
          <Typography>Gender: {patientInfo.gender}</Typography>
          {patientInfo.medical_history.length > 0 && (
            <Typography>Medical History: {patientInfo.medical_history.join(', ')}</Typography>
          )}
          {patientInfo.medications.length > 0 && (
            <Typography>Medications: {patientInfo.medications.join(', ')}</Typography>
          )}
          {patientInfo.allergies.length > 0 && (
            <Typography>Allergies: {patientInfo.allergies.join(', ')}</Typography>
          )}
        </CardContent>
      </Card>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
            Chief Complaint
          </Typography>
          <Typography>{chiefComplaint}</Typography>
        </CardContent>
      </Card>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
            Symptoms ({symptoms.length})
          </Typography>
          {symptoms.map((symptom, index) => (
            <Box key={index} sx={{ mb: 2 }}>
              <Typography variant="body1" fontWeight="bold">
                {symptom.name} ({symptom.severity})
              </Typography>
              {symptom.duration && <Typography variant="body2">Duration: {symptom.duration}</Typography>}
              {symptom.location && <Typography variant="body2">Location: {symptom.location}</Typography>}
              {symptom.description && <Typography variant="body2">{symptom.description}</Typography>}
            </Box>
          ))}
        </CardContent>
      </Card>

      {additionalNotes && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Additional Notes
            </Typography>
            <Typography>{additionalNotes}</Typography>
          </CardContent>
        </Card>
      )}

      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="body2">
          <strong>Medical Disclaimer:</strong> This AI assessment is for informational purposes only 
          and should not replace professional medical advice, diagnosis, or treatment. Always seek 
          the advice of qualified healthcare providers with questions about your health.
        </Typography>
      </Alert>
    </Box>
  );

  const getStepContent = (step: number) => {
    switch (step) {
      case 0:
        return renderPatientInfoStep();
      case 1:
        return renderSymptomsStep();
      case 2:
        return renderReviewStep();
      default:
        return 'Unknown step';
    }
  };

  return (
    <Box
      sx={{
        minHeight: 'calc(100vh - 64px)',
        background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.05)} 0%, ${alpha(theme.palette.secondary.main, 0.05)} 100%)`,
        pt: 4,
        pb: 6,
      }}
    >
      <Container maxWidth="md">
        <Paper 
          elevation={0} 
          sx={{ 
            p: 4, 
            borderRadius: 3,
            background: 'white',
            border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
          }}
        >
          <Typography 
            variant="h4" 
            component="h1" 
            gutterBottom 
            align="center"
            sx={{
              fontWeight: 700,
              background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              color: 'transparent',
              mb: 3,
            }}
          >
            AI Symptom Checker
          </Typography>
          
          <Stepper 
            activeStep={activeStep} 
            sx={{ 
              pt: 3, 
              pb: 5,
              '& .MuiStepIcon-root.Mui-active': {
                color: theme.palette.primary.main,
              },
              '& .MuiStepIcon-root.Mui-completed': {
                color: theme.palette.success.main,
              },
            }}
          >
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>

          {getStepContent(activeStep)}

          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
            <Button
              onClick={handleBack}
              disabled={activeStep === 0}
              variant="outlined"
              startIcon={<ArrowBack />}
              sx={{ borderRadius: 2 }}
            >
              Back
            </Button>
            
            {activeStep === steps.length - 1 ? (
              <Button
                variant="contained"
                onClick={handleSubmit}
                disabled={analyzeSymptomsMutation.isLoading || !isStepValid(activeStep)}
                startIcon={analyzeSymptomsMutation.isLoading ? <CircularProgress size={20} /> : <Send />}
                sx={{
                  borderRadius: 2,
                  background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                  '&:hover': {
                    background: `linear-gradient(45deg, ${theme.palette.primary.dark}, ${theme.palette.secondary.dark})`,
                  },
                }}
              >
                {analyzeSymptomsMutation.isLoading ? 'Analyzing...' : 'Get AI Analysis'}
              </Button>
            ) : (
              <Button
                variant="contained"
                onClick={handleNext}
                disabled={!isStepValid(activeStep)}
                endIcon={<ArrowForward />}
                sx={{
                  borderRadius: 2,
                  background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                  '&:hover': {
                    background: `linear-gradient(45deg, ${theme.palette.primary.dark}, ${theme.palette.secondary.dark})`,
                  },
                }}
              >
                Next
              </Button>
            )}
          </Box>

          {analyzeSymptomsMutation.isError && (
            <Alert severity="error" sx={{ mt: 2, borderRadius: 2 }}>
              An error occurred while analyzing your symptoms. Please try again.
            </Alert>
          )}
        </Paper>
      </Container>
    </Box>
  );
};

export default SymptomChecker;
