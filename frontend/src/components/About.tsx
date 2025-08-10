import React from 'react';
import { Container, Paper, Typography } from '@mui/material';

const About: React.FC = () => {
  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          About
        </Typography>
        <Typography variant="body1" paragraph>
          This AI Healthcare Assistant provides informational insights based on your symptoms using a
          multi-agent architecture and evidence-based guidelines.
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Not a substitute for professional medical advice.
        </Typography>
      </Paper>
    </Container>
  );
};

export default About;
