import React from 'react';
import { useMutation } from 'react-query';
import { Box, Typography, Card, CardContent, Button, Alert } from '@mui/material';
import healthcareAPI, { SymptomInput, Symptom, PatientInfo } from '../services/api';

const EmergencyCheck: React.FC = () => {
  const [result, setResult] = React.useState<any>(null);
  const [error, setError] = React.useState<string>('');

  const [patientInfo] = React.useState<PatientInfo>({ age: 30, gender: 'other', medical_history: [], medications: [], allergies: [] });
  const [symptoms] = React.useState<Symptom[]>([{ name: 'chest pain', severity: 'severe' } as Symptom]);

  const mutation = useMutation((input: SymptomInput) => healthcareAPI.emergencyCheck(input), {
    onSuccess: (data) => { setResult(data); setError(''); },
    onError: () => setError('Failed to run emergency check'),
  });

  const runCheck = () => {
    // Send SymptomInput directly, matching backend expectations
    mutation.mutate({
      symptoms,
      patient_info: patientInfo,
      chief_complaint: 'Demo emergency check',
    });
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Emergency Check</Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        This quick check uses red flags to detect potential emergencies.
      </Typography>
      <Button variant="contained" onClick={runCheck} disabled={mutation.isLoading}>Run Demo Check</Button>
      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      {result && (
        <Card sx={{ mt: 3 }}>
          <CardContent>
            <Typography variant="h6">Result</Typography>
            <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(result, null, 2)}</pre>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default EmergencyCheck;
