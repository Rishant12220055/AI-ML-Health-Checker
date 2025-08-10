import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Paper, Typography, Alert, Chip, Box, Grid, Card, CardContent, Divider, Button } from '@mui/material';
import { ArrowBack } from '@mui/icons-material';
import type { DiagnosisResponse } from '../services/api';

const Results: React.FC = () => {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const [result, setResult] = useState<DiagnosisResponse | null>(null);

  useEffect(() => {
    if (!sessionId) return;
    try {
      const raw = sessionStorage.getItem(`diagnosis_${sessionId}`);
      if (raw) {
        setResult(JSON.parse(raw));
      }
    } catch {}
  }, [sessionId]);

  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h4" gutterBottom>
            Analysis Results
          </Typography>
          <Button startIcon={<ArrowBack />} onClick={() => navigate('/')}>New Assessment</Button>
        </Box>

        <Alert severity="info" sx={{ mb: 2 }}>
          Session ID: {sessionId}
        </Alert>

        {!result ? (
          <Typography variant="body1">
            No stored result found. If you refreshed, please run a new assessment.
          </Typography>
        ) : (
          <Box>
            <Box display="flex" gap={2} alignItems="center" mb={2}>
              <Chip label={`Urgency: ${result.urgency_level}`} color={result.urgency_level === 'emergency' ? 'error' : result.urgency_level === 'urgent' ? 'warning' : result.urgency_level === 'moderate' ? 'primary' : 'default'} />
              <Typography variant="body2" color="text.secondary">{new Date(result.timestamp).toLocaleString()}</Typography>
            </Box>

            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6">Possible Conditions</Typography>
                    <Divider sx={{ my: 1 }} />
                    {result.possible_conditions?.length ? (
                      result.possible_conditions.map((c, i) => (
                        <Box key={i} mb={1}>
                          <Typography variant="subtitle1">{c.name}</Typography>
                          <Typography variant="body2" color="text.secondary">{c.description}</Typography>
                        </Box>
                      ))
                    ) : (
                      <Typography variant="body2">No conditions available.</Typography>
                    )}
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6">Next Steps</Typography>
                    <Divider sx={{ my: 1 }} />
                    {result.next_steps?.length ? (
                      <ul>
                        {result.next_steps.map((s, i) => (
                          <li key={i}><Typography variant="body2">{s}</Typography></li>
                        ))}
                      </ul>
                    ) : (
                      <Typography variant="body2">No guidance available.</Typography>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            <Alert severity="warning" sx={{ mt: 3 }}>
              {result.disclaimer}
            </Alert>
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default Results;
