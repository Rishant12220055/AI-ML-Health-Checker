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
  Stack,
  Avatar,
  Divider,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { 
  Add, 
  Delete, 
  Send, 
  ArrowBack, 
  ArrowForward,
  Person,
  MedicalServices,
  Psychology,
  CheckCircle
} from '@mui/icons-material';
import { useMutation } from 'react-query';
import { motion, AnimatePresence } from 'framer-motion';
import healthcareAPI, { Symptom, PatientInfo, SymptomInput } from '../services/api';

const SymptomChecker: React.FC = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
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

  const diagnosisMutation = useMutation(healthcareAPI.diagnoseV2, {
    onSuccess: (data) => {
      navigate('/diagnosis-results', { state: { results: data } });
    },
  });

  const handleNext = () => setStep(prev => prev + 1);
  const handleBack = () => setStep(prev => prev - 1);

  const addSymptom = () => {
    if (currentSymptom.name.trim()) {
      setSymptoms(prev => [...prev, { ...currentSymptom }]);
      setCurrentSymptom({ 
        name: '', 
        severity: 'mild', 
        duration: '', 
        description: '', 
        location: '' 
      });
    }
  };

  const removeSymptom = (index: number) => {
    setSymptoms(prev => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = () => {
    const symptomInput: SymptomInput = {
      patient_info: patientInfo,
      symptoms,
      chief_complaint: chiefComplaint,
      additional_notes: additionalNotes,
    };
    diagnosisMutation.mutate(symptomInput);
  };

  const stepVariants = {
    hidden: { opacity: 0, x: 50 },
    visible: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: -50 }
  };

  return (
    <Box sx={{ 
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
      py: 4
    }}>
      <Container maxWidth="lg">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <Typography 
              variant="h3" 
              sx={{ 
                color: 'white', 
                fontWeight: 700,
                mb: 2,
                fontSize: { xs: '2rem', md: '3rem' }
              }}
            >
              AI Symptom Checker
            </Typography>
            <Typography 
              variant="h6" 
              sx={{ 
                color: 'rgba(255,255,255,0.9)',
                fontWeight: 300,
                maxWidth: '600px',
                mx: 'auto'
              }}
            >
              Get personalized health insights with our advanced AI diagnosis system
            </Typography>
          </Box>
        </motion.div>

        {/* Progress Indicator */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <Card sx={{ 
            mb: 4, 
            background: 'rgba(255,255,255,0.95)',
            backdropFilter: 'blur(20px)',
            borderRadius: 3
          }}>
            <CardContent sx={{ p: 3 }}>
              <Stack direction="row" spacing={4} justifyContent="center">
                {[
                  { num: 1, label: 'Patient Info', icon: <Person /> },
                  { num: 2, label: 'Symptoms', icon: <MedicalServices /> },
                  { num: 3, label: 'Analysis', icon: <Psychology /> }
                ].map((item) => (
                  <Box key={item.num} sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Avatar sx={{ 
                      bgcolor: step >= item.num ? '#667eea' : '#e0e0e0',
                      color: step >= item.num ? 'white' : '#666',
                      transition: 'all 0.3s ease'
                    }}>
                      {step > item.num ? <CheckCircle /> : item.icon}
                    </Avatar>
                    <Typography 
                      sx={{ 
                        fontWeight: step === item.num ? 600 : 400,
                        color: step >= item.num ? '#667eea' : '#666'
                      }}
                    >
                      {item.label}
                    </Typography>
                  </Box>
                ))}
              </Stack>
            </CardContent>
          </Card>
        </motion.div>

        {/* Step Content */}
        <AnimatePresence mode="wait">
          <motion.div
            key={step}
            variants={stepVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
            transition={{ duration: 0.4 }}
          >
            <Card sx={{ 
              background: 'rgba(255,255,255,0.95)',
              backdropFilter: 'blur(20px)',
              borderRadius: 3,
              boxShadow: '0 30px 100px rgba(0,0,0,0.3)'
            }}>
              <CardContent sx={{ p: 5 }}>
                {step === 1 && (
                  <Box>
                    <Typography variant="h4" sx={{ mb: 4, fontWeight: 600, color: '#1a1a1a' }}>
                      Patient Information
                    </Typography>
                    <Grid container spacing={4}>
                      <Grid item xs={12} md={6}>
                        <TextField
                          fullWidth
                          label="Age"
                          type="number"
                          value={patientInfo.age || ''}
                          onChange={(e) => setPatientInfo(prev => ({ 
                            ...prev, 
                            age: parseInt(e.target.value) || 0 
                          }))}
                          sx={{ 
                            '& .MuiOutlinedInput-root': {
                              borderRadius: 2,
                              '&:hover fieldset': {
                                borderColor: '#667eea',
                              },
                              '&.Mui-focused fieldset': {
                                borderColor: '#667eea',
                              },
                            }
                          }}
                        />
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <FormControl fullWidth>
                          <InputLabel>Gender</InputLabel>
                          <Select
                            value={patientInfo.gender}
                            label="Gender"
                            onChange={(e) => setPatientInfo(prev => ({ 
                              ...prev, 
                              gender: e.target.value 
                            }))}
                            sx={{ borderRadius: 2 }}
                          >
                            <MenuItem value="male">Male</MenuItem>
                            <MenuItem value="female">Female</MenuItem>
                            <MenuItem value="other">Other</MenuItem>
                          </Select>
                        </FormControl>
                      </Grid>
                      <Grid item xs={12}>
                        <TextField
                          fullWidth
                          label="Medical History (comma-separated)"
                          multiline
                          rows={3}
                          value={patientInfo.medical_history.join(', ')}
                          onChange={(e) => setPatientInfo(prev => ({
                            ...prev,
                            medical_history: e.target.value.split(',').map(item => item.trim()).filter(Boolean)
                          }))}
                          sx={{ 
                            '& .MuiOutlinedInput-root': {
                              borderRadius: 2,
                            }
                          }}
                        />
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <TextField
                          fullWidth
                          label="Current Medications (comma-separated)"
                          multiline
                          rows={2}
                          value={patientInfo.medications.join(', ')}
                          onChange={(e) => setPatientInfo(prev => ({
                            ...prev,
                            medications: e.target.value.split(',').map(item => item.trim()).filter(Boolean)
                          }))}
                          sx={{ 
                            '& .MuiOutlinedInput-root': {
                              borderRadius: 2,
                            }
                          }}
                        />
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <TextField
                          fullWidth
                          label="Known Allergies (comma-separated)"
                          multiline
                          rows={2}
                          value={patientInfo.allergies.join(', ')}
                          onChange={(e) => setPatientInfo(prev => ({
                            ...prev,
                            allergies: e.target.value.split(',').map(item => item.trim()).filter(Boolean)
                          }))}
                          sx={{ 
                            '& .MuiOutlinedInput-root': {
                              borderRadius: 2,
                            }
                          }}
                        />
                      </Grid>
                    </Grid>
                  </Box>
                )}

                {step === 2 && (
                  <Box>
                    <Typography variant="h4" sx={{ mb: 4, fontWeight: 600, color: '#1a1a1a' }}>
                      Describe Your Symptoms
                    </Typography>
                    
                    <Grid container spacing={4}>
                      <Grid item xs={12} md={6}>
                        <TextField
                          fullWidth
                          label="Symptom Name"
                          value={currentSymptom.name}
                          onChange={(e) => setCurrentSymptom(prev => ({ 
                            ...prev, 
                            name: e.target.value 
                          }))}
                          sx={{ mb: 2, '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
                        />
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <FormControl fullWidth sx={{ mb: 2 }}>
                          <InputLabel>Severity</InputLabel>
                          <Select
                            value={currentSymptom.severity}
                            label="Severity"
                            onChange={(e) => setCurrentSymptom(prev => ({ 
                              ...prev, 
                              severity: e.target.value as 'mild' | 'moderate' | 'severe' | 'critical'
                            }))}
                            sx={{ borderRadius: 2 }}
                          >
                            <MenuItem value="mild">Mild</MenuItem>
                            <MenuItem value="moderate">Moderate</MenuItem>
                            <MenuItem value="severe">Severe</MenuItem>
                            <MenuItem value="critical">Critical</MenuItem>
                          </Select>
                        </FormControl>
                      </Grid>
                      <Grid item xs={12}>
                        <TextField
                          fullWidth
                          label="Location (optional)"
                          value={currentSymptom.location || ''}
                          onChange={(e) => setCurrentSymptom(prev => ({ 
                            ...prev, 
                            location: e.target.value 
                          }))}
                          placeholder="e.g., left side, abdomen, head"
                          sx={{ mb: 2, '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <TextField
                          fullWidth
                          label="Duration"
                          value={currentSymptom.duration}
                          onChange={(e) => setCurrentSymptom(prev => ({ 
                            ...prev, 
                            duration: e.target.value 
                          }))}
                          placeholder="e.g., 3 days, 2 weeks"
                          sx={{ mb: 2, '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <TextField
                          fullWidth
                          label="Description"
                          multiline
                          rows={3}
                          value={currentSymptom.description}
                          onChange={(e) => setCurrentSymptom(prev => ({ 
                            ...prev, 
                            description: e.target.value 
                          }))}
                          placeholder="Describe the symptom in detail..."
                          sx={{ mb: 3, '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
                        />
                      </Grid>
                    </Grid>

                    <Button
                      variant="contained"
                      startIcon={<Add />}
                      onClick={addSymptom}
                      sx={{ 
                        mb: 4,
                        background: 'linear-gradient(45deg, #667eea, #764ba2)',
                        borderRadius: 3,
                        px: 4,
                        py: 1.5
                      }}
                    >
                      Add Symptom
                    </Button>

                    {symptoms.length > 0 && (
                      <Box>
                        <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                          Added Symptoms:
                        </Typography>
                        <Stack spacing={2}>
                          {symptoms.map((symptom, index) => (
                            <motion.div
                              key={index}
                              initial={{ opacity: 0, scale: 0.9 }}
                              animate={{ opacity: 1, scale: 1 }}
                              transition={{ duration: 0.3 }}
                            >
                              <Card sx={{ 
                                p: 2, 
                                background: '#f8f9ff',
                                border: '1px solid #e0e7ff'
                              }}>
                                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                  <Box>
                                    <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                                      {symptom.name}
                                    </Typography>
                                    <Stack direction="row" spacing={1} sx={{ mb: 1 }}>
                                      <Chip 
                                        label={symptom.severity} 
                                        size="small"
                                        color={
                                          symptom.severity === 'critical' ? 'error' :
                                          symptom.severity === 'severe' ? 'error' :
                                          symptom.severity === 'moderate' ? 'warning' : 'success'
                                        }
                                        sx={{
                                          fontWeight: 600,
                                          ...(symptom.severity === 'critical' && {
                                            backgroundColor: '#d32f2f',
                                            color: 'white',
                                            animation: 'pulse 2s infinite'
                                          })
                                        }}
                                      />
                                      {symptom.duration && <Chip label={symptom.duration} size="small" variant="outlined" />}
                                      {symptom.location && <Chip label={symptom.location} size="small" variant="outlined" color="primary" />}
                                    </Stack>
                                    <Typography color="text.secondary">
                                      {symptom.description}
                                    </Typography>
                                  </Box>
                                  <Button
                                    color="error"
                                    onClick={() => removeSymptom(index)}
                                    sx={{ minWidth: 'auto' }}
                                  >
                                    <Delete />
                                  </Button>
                                </Box>
                              </Card>
                            </motion.div>
                          ))}
                        </Stack>
                      </Box>
                    )}
                  </Box>
                )}

                {step === 3 && (
                  <Box>
                    <Typography variant="h4" sx={{ mb: 4, fontWeight: 600, color: '#1a1a1a' }}>
                      Review & Submit
                    </Typography>
                    
                    <Grid container spacing={4}>
                      <Grid item xs={12} md={6}>
                        <Paper sx={{ p: 3, background: '#f8f9ff', borderRadius: 3 }}>
                          <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                            Patient Information
                          </Typography>
                          <Typography><strong>Age:</strong> {patientInfo.age}</Typography>
                          <Typography><strong>Gender:</strong> {patientInfo.gender}</Typography>
                          {patientInfo.medical_history.length > 0 && (
                            <Typography><strong>Medical History:</strong> {patientInfo.medical_history.join(', ')}</Typography>
                          )}
                          {patientInfo.medications.length > 0 && (
                            <Typography><strong>Medications:</strong> {patientInfo.medications.join(', ')}</Typography>
                          )}
                          {patientInfo.allergies.length > 0 && (
                            <Typography><strong>Allergies:</strong> {patientInfo.allergies.join(', ')}</Typography>
                          )}
                        </Paper>
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <Paper sx={{ p: 3, background: '#f8f9ff', borderRadius: 3 }}>
                          <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                            Symptoms ({symptoms.length})
                          </Typography>
                          {symptoms.map((symptom, index) => (
                            <Typography key={index} sx={{ mb: 1 }}>
                              • {symptom.name} ({symptom.severity})
                            </Typography>
                          ))}
                        </Paper>
                      </Grid>
                    </Grid>

                    <TextField
                      fullWidth
                      label="Chief Complaint"
                      multiline
                      rows={3}
                      value={chiefComplaint}
                      onChange={(e) => setChiefComplaint(e.target.value)}
                      placeholder="What is the main reason for your visit?"
                      sx={{ my: 3, '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
                    />

                    <TextField
                      fullWidth
                      label="Additional Notes (optional)"
                      multiline
                      rows={2}
                      value={additionalNotes}
                      onChange={(e) => setAdditionalNotes(e.target.value)}
                      placeholder="Any additional information you'd like to share..."
                      sx={{ mb: 3, '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
                    />

                    {diagnosisMutation.isError && (
                      <Alert severity="error" sx={{ mb: 3 }}>
                        Failed to get diagnosis. Please try again.
                      </Alert>
                    )}
                  </Box>
                )}

                {/* Navigation Buttons */}
                <Divider sx={{ my: 4 }} />
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Button
                    variant="outlined"
                    startIcon={<ArrowBack />}
                    onClick={step === 1 ? () => navigate('/') : handleBack}
                    sx={{ 
                      borderRadius: 3,
                      px: 4,
                      py: 1.5,
                      borderColor: '#667eea',
                      color: '#667eea'
                    }}
                  >
                    {step === 1 ? 'Back to Home' : 'Previous'}
                  </Button>

                  {step < 3 ? (
                    <Button
                      variant="contained"
                      endIcon={<ArrowForward />}
                      onClick={handleNext}
                      disabled={
                        (step === 1 && (!patientInfo.age || !patientInfo.gender)) ||
                        (step === 2 && symptoms.length === 0)
                      }
                      sx={{ 
                        background: 'linear-gradient(45deg, #667eea, #764ba2)',
                        borderRadius: 3,
                        px: 4,
                        py: 1.5
                      }}
                    >
                      Next
                    </Button>
                  ) : (
                    <Button
                      variant="contained"
                      endIcon={diagnosisMutation.isLoading ? <CircularProgress size={20} color="inherit" /> : <Send />}
                      onClick={handleSubmit}
                      disabled={diagnosisMutation.isLoading || symptoms.length === 0}
                      sx={{ 
                        background: 'linear-gradient(45deg, #10b981, #06b6d4)',
                        borderRadius: 3,
                        px: 4,
                        py: 1.5
                      }}
                    >
                      {diagnosisMutation.isLoading ? 'Analyzing...' : 'Get Diagnosis'}
                    </Button>
                  )}
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </AnimatePresence>
      </Container>
    </Box>
  );
};

export default SymptomChecker;
