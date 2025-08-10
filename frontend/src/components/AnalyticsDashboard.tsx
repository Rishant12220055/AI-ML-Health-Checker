import React from 'react';
import { useQuery } from 'react-query';
import { Box, Typography, Grid, Card, CardContent, CircularProgress, Alert, ToggleButtonGroup, ToggleButton } from '@mui/material';
import healthcareAPI from '../services/api';

const AnalyticsDashboard: React.FC = () => {
  const [hours, setHours] = React.useState<number>(24);

  const { data, isLoading, error, refetch } = useQuery(['analyticsDashboard', hours], () => healthcareAPI.getAnalyticsDashboard(hours), { keepPreviousData: true });

  React.useEffect(() => { refetch(); }, [hours]);

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Analytics Dashboard</Typography>
        <ToggleButtonGroup value={hours} exclusive onChange={(_, v) => v && setHours(v)} size="small">
          <ToggleButton value={1}>1h</ToggleButton>
          <ToggleButton value={6}>6h</ToggleButton>
          <ToggleButton value={24}>24h</ToggleButton>
          <ToggleButton value={72}>3d</ToggleButton>
        </ToggleButtonGroup>
      </Box>
      {isLoading && <CircularProgress />}
      {error && <Alert severity="error">Failed to load analytics</Alert>}
      {data && (
        <Grid container spacing={2}>
          {Object.entries(data.dashboard_data?.summary || {}).map(([key, val]: any) => (
            <Grid item xs={12} md={6} lg={3} key={key}>
              <Card>
                <CardContent>
                  <Typography variant="subtitle2" color="text.secondary">{key}</Typography>
                  <Typography variant="h5">{typeof val === 'number' ? (val as number).toFixed(2) : String(val)}</Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default AnalyticsDashboard;
