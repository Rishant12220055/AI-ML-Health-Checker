import React from 'react';
import { useQuery } from 'react-query';
import { Box, Typography, Grid, Card, CardContent, Chip, CircularProgress, Alert, Button } from '@mui/material';
import healthcareAPI from '../services/api';

const SystemStatus: React.FC = () => {
  const healthQuery = useQuery(['advancedHealth'], () => healthcareAPI.getAdvancedHealth());
  const perfQuery = useQuery(['systemPerformance'], () => healthcareAPI.getSystemPerformance());

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">System Status</Typography>
        <Button onClick={() => { healthQuery.refetch(); perfQuery.refetch(); }} variant="outlined">Refresh</Button>
      </Box>

      {(healthQuery.isLoading || perfQuery.isLoading) && <CircularProgress />}
      {(healthQuery.error || perfQuery.error) && <Alert severity="error">Failed to load system status</Alert>}

      {healthQuery.data && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>Components</Typography>
            <Grid container spacing={2}>
              {Object.entries(healthQuery.data.component_status || {}).map(([key, val]: any) => (
                <Grid item xs={12} md={4} key={key}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle2" color="text.secondary">{key}</Typography>
                      <Chip label={(val as any).status} color={(val as any).status === 'operational' ? 'success' as any : 'warning' as any} size="small" />
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </CardContent>
        </Card>
      )}

      {perfQuery.data && (
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="text.secondary">CPU Usage</Typography>
                <Typography variant="h5">{perfQuery.data.cpu?.usage_percent?.toFixed ? perfQuery.data.cpu.usage_percent.toFixed(1) : perfQuery.data.cpu?.usage_percent}%</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="text.secondary">Memory Usage</Typography>
                <Typography variant="h5">{perfQuery.data.memory?.usage_percent?.toFixed ? perfQuery.data.memory.usage_percent.toFixed(1) : perfQuery.data.memory?.usage_percent}%</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="text.secondary">Disk Usage</Typography>
                <Typography variant="h5">{perfQuery.data.disk?.usage_percent?.toFixed ? perfQuery.data.disk.usage_percent.toFixed(1) : perfQuery.data.disk?.usage_percent}%</Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Box>
  );
};

export default SystemStatus;
