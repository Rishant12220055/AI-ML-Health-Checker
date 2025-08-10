import React from 'react';
import { Container, Paper, Typography } from '@mui/material';

const Privacy: React.FC = () => {
  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Privacy
        </Typography>
        <Typography variant="body1" paragraph>
          We value your privacy. This application processes your input securely and does not permanently store
          identifiable data. Review our policies and terms before use.
        </Typography>
      </Paper>
    </Container>
  );
};

export default Privacy;
