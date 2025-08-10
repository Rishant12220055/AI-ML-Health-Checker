import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Grid,
  Avatar,
  Chip,
  Button,
  Switch,
  FormControlLabel,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  useTheme,
  alpha,
  LinearProgress,
} from '@mui/material';
import {
  Favorite as HeartIcon,
  Psychology as BrainIcon,
  LocalHospital as HospitalIcon,
  Notifications as NotificationIcon,
  Timeline as TimelineIcon,
  Medication as MedicationIcon,
  MonitorHeart as MonitorIcon,
  Warning as WarningIcon,
  CheckCircle as CheckIcon,
  Person as PersonIcon,
  MoreVert as MoreIcon,
} from '@mui/icons-material';

interface PatientData {
  id: string;
  name: string;
  avatar: string;
  status: 'stable' | 'warning' | 'critical';
  vitals: {
    heartRate: number;
    bloodPressure: string;
    temperature: number;
    oxygen: number;
  };
  lastUpdate: string;
}

interface Medication {
  name: string;
  dosage: string;
  time: string;
  taken: boolean;
  color: string;
}

const PatientMonitoring: React.FC = () => {
  const theme = useTheme();
  const [patients] = useState<PatientData[]>([
    {
      id: '1',
      name: 'Adriana E.',
      avatar: '/api/placeholder/40/40',
      status: 'stable',
      vitals: {
        heartRate: 72,
        bloodPressure: '120/80',
        temperature: 98.6,
        oxygen: 98,
      },
      lastUpdate: '2 mins ago',
    },
    {
      id: '2',
      name: 'Marcus T.',
      avatar: '/api/placeholder/40/40',
      status: 'warning',
      vitals: {
        heartRate: 88,
        bloodPressure: '140/90',
        temperature: 99.2,
        oxygen: 96,
      },
      lastUpdate: '5 mins ago',
    },
  ]);

  const [medications] = useState<Medication[]>([
    { name: 'Atordin', dosage: '20mg', time: 'Tue 25', taken: true, color: '#4f46e5' },
    { name: 'Vitamin D', dosage: '1000IU', time: 'Wed 26', taken: true, color: '#059669' },
    { name: 'Omega 3', dosage: '1000mg', time: 'Thu 27', taken: false, color: '#dc2626' },
    { name: 'Ibuprofen', dosage: '400mg', time: 'Fri 28', taken: false, color: '#f59e0b' },
    { name: 'Aspirin', dosage: '100mg', time: 'Sat 29', taken: false, color: '#8b5cf6' },
  ]);

  const [brainActivity, setBrainActivity] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setBrainActivity(prev => (prev + 1) % 100);
    }, 100);
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'stable': return theme.palette.success.main;
      case 'warning': return theme.palette.warning.main;
      case 'critical': return theme.palette.error.main;
      default: return theme.palette.grey[500];
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Floating 3D Elements */}
      <Box
        sx={{
          position: 'absolute',
          top: '10%',
          left: '5%',
          width: 120,
          height: 120,
          borderRadius: '50%',
          background: 'linear-gradient(45deg, #ff6b9d, #c44569)',
          opacity: 0.6,
          animation: 'float 6s ease-in-out infinite',
          filter: 'blur(1px)',
        }}
      />
      <Box
        sx={{
          position: 'absolute',
          bottom: '20%',
          right: '10%',
          width: 80,
          height: 80,
          borderRadius: '50%',
          background: 'linear-gradient(45deg, #4facfe, #00f2fe)',
          opacity: 0.4,
          animation: 'float 8s ease-in-out infinite reverse',
          filter: 'blur(1px)',
        }}
      />

      <Container maxWidth="xl" sx={{ py: 4, position: 'relative', zIndex: 1 }}>
        {/* Header */}
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography
            variant="h3"
            sx={{
              fontWeight: 700,
              color: 'white',
              mb: 2,
              textShadow: '0 2px 10px rgba(0,0,0,0.3)',
            }}
          >
            Remote Patient Monitoring Solution
          </Typography>
          <Typography
            variant="h6"
            sx={{
              color: alpha('#ffffff', 0.9),
              fontWeight: 400,
            }}
          >
            With real-time data collection and analysis, healthcare professionals
            can monitor patients' conditions and intervene when necessary.
          </Typography>
        </Box>

        <Grid container spacing={4}>
          {/* Main Dashboard */}
          <Grid item xs={12} lg={8}>
            <Paper
              elevation={0}
              sx={{
                borderRadius: 4,
                background: 'rgba(255, 255, 255, 0.95)',
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                overflow: 'hidden',
                minHeight: 600,
              }}
            >
              <Grid container sx={{ height: '100%' }}>
                {/* Patient List */}
                <Grid item xs={12} md={4} sx={{ borderRight: '1px solid rgba(0,0,0,0.1)' }}>
                  <Box sx={{ p: 3 }}>
                    <Typography variant="h6" fontWeight={600} sx={{ mb: 2 }}>
                      Patients / Doctors
                    </Typography>
                    <List>
                      {patients.map((patient) => (
                        <ListItem
                          key={patient.id}
                          sx={{
                            border: '1px solid rgba(0,0,0,0.1)',
                            borderRadius: 2,
                            mb: 2,
                            bgcolor: 'white',
                          }}
                        >
                          <ListItemIcon>
                            <Avatar sx={{ bgcolor: getStatusColor(patient.status) }}>
                              <PersonIcon />
                            </Avatar>
                          </ListItemIcon>
                          <ListItemText
                            primary={patient.name}
                            secondary={
                              <Box>
                                <Typography variant="caption" color="text.secondary">
                                  Updated quality plus pain
                                </Typography>
                                <br />
                                <Chip
                                  size="small"
                                  label={patient.status.toUpperCase()}
                                  sx={{
                                    bgcolor: alpha(getStatusColor(patient.status), 0.1),
                                    color: getStatusColor(patient.status),
                                    fontWeight: 600,
                                  }}
                                />
                              </Box>
                            }
                          />
                        </ListItem>
                      ))}
                    </List>

                    {/* Diagnosis Section */}
                    <Box sx={{ mt: 4 }}>
                      <Typography variant="h6" fontWeight={600} sx={{ mb: 2 }}>
                        Diagnosis
                      </Typography>
                      <Box sx={{ p: 2, bgcolor: alpha(theme.palette.primary.main, 0.05), borderRadius: 2 }}>
                        <Typography variant="body2" color="text.secondary">
                          Recent MRI findings show:
                        </Typography>
                        <Typography variant="body2" sx={{ mt: 1 }}>
                          • Normal brain structure
                        </Typography>
                        <Typography variant="body2">
                          • Active neural pathways detected
                        </Typography>
                        <Typography variant="body2">
                          • Recommended monitoring
                        </Typography>
                      </Box>
                    </Box>
                  </Box>
                </Grid>

                {/* 3D Brain Visualization */}
                <Grid item xs={12} md={8}>
                  <Box
                    sx={{
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'center',
                      alignItems: 'center',
                      position: 'relative',
                      background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
                      color: 'white',
                    }}
                  >
                    {/* 3D Brain Model */}
                    <Box
                      sx={{
                        width: 300,
                        height: 300,
                        position: 'relative',
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                      }}
                    >
                      <Box
                        sx={{
                          width: 250,
                          height: 250,
                          background: 'linear-gradient(45deg, #ff6b9d, #4facfe)',
                          borderRadius: '50% 50% 50% 50% / 60% 60% 40% 40%',
                          position: 'relative',
                          animation: 'pulse 2s ease-in-out infinite',
                          '&::before': {
                            content: '""',
                            position: 'absolute',
                            top: '20%',
                            left: '30%',
                            width: '40%',
                            height: '60%',
                            background: 'linear-gradient(45deg, #c44569, #764ba2)',
                            borderRadius: '50%',
                            opacity: 0.8,
                          },
                          '&::after': {
                            content: '""',
                            position: 'absolute',
                            top: '40%',
                            right: '20%',
                            width: '30%',
                            height: '40%',
                            background: 'linear-gradient(45deg, #667eea, #764ba2)',
                            borderRadius: '50%',
                            opacity: 0.6,
                          },
                        }}
                      />
                      
                      {/* Neural Activity Indicators */}
                      {[...Array(6)].map((_, i) => (
                        <Box
                          key={i}
                          sx={{
                            position: 'absolute',
                            width: 8,
                            height: 8,
                            bgcolor: '#ff6b9d',
                            borderRadius: '50%',
                            top: `${30 + Math.sin(i) * 40}%`,
                            left: `${40 + Math.cos(i) * 30}%`,
                            animation: `blink ${1 + i * 0.2}s ease-in-out infinite`,
                            boxShadow: '0 0 10px #ff6b9d',
                          }}
                        />
                      ))}
                    </Box>

                    {/* Vital Signs */}
                    <Box sx={{ mt: 4, display: 'flex', gap: 4 }}>
                      <Box sx={{ textAlign: 'center' }}>
                        <HeartIcon sx={{ fontSize: 24, color: '#ff6b9d', mb: 1 }} />
                        <Typography variant="h6">72 BPM</Typography>
                        <Typography variant="caption">Heart Rate</Typography>
                      </Box>
                      <Box sx={{ textAlign: 'center' }}>
                        <MonitorIcon sx={{ fontSize: 24, color: '#4facfe', mb: 1 }} />
                        <Typography variant="h6">98%</Typography>
                        <Typography variant="caption">Oxygen</Typography>
                      </Box>
                      <Box sx={{ textAlign: 'center' }}>
                        <TimelineIcon sx={{ fontSize: 24, color: '#67e8f9', mb: 1 }} />
                        <Typography variant="h6">120/80</Typography>
                        <Typography variant="caption">Blood Pressure</Typography>
                      </Box>
                    </Box>

                    {/* Activity Progress */}
                    <Box sx={{ position: 'absolute', bottom: 20, left: 20, right: 20 }}>
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        Neural Activity: {brainActivity}%
                      </Typography>
                      <LinearProgress
                        variant="determinate"
                        value={brainActivity}
                        sx={{
                          height: 8,
                          borderRadius: 4,
                          bgcolor: alpha('#ffffff', 0.2),
                          '& .MuiLinearProgress-bar': {
                            background: 'linear-gradient(45deg, #ff6b9d, #4facfe)',
                          },
                        }}
                      />
                    </Box>
                  </Box>
                </Grid>
              </Grid>
            </Paper>
          </Grid>

          {/* Medication Tracking */}
          <Grid item xs={12} lg={4}>
            <Paper
              elevation={0}
              sx={{
                borderRadius: 4,
                background: 'rgba(255, 255, 255, 0.95)',
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                p: 3,
                height: 'fit-content',
              }}
            >
              <Typography variant="h6" fontWeight={600} sx={{ mb: 3 }}>
                Medication
              </Typography>
              
              {/* Medication Schedule */}
              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  {['Mon 25', 'Tue 26', 'Wed 27', 'Thu 28', 'Fri 29', 'Sat 30', 'Sun 31'].map((day) => (
                    <Typography
                      key={day}
                      variant="caption"
                      sx={{
                        textAlign: 'center',
                        color: day.includes('27') ? theme.palette.primary.main : 'text.secondary',
                        fontWeight: day.includes('27') ? 600 : 400,
                      }}
                    >
                      {day}
                    </Typography>
                  ))}
                </Box>
              </Box>

              {/* Medication List */}
              <List sx={{ p: 0 }}>
                {medications.map((med, index) => (
                  <ListItem
                    key={index}
                    sx={{
                      border: '1px solid rgba(0,0,0,0.1)',
                      borderRadius: 2,
                      mb: 1,
                      p: 2,
                    }}
                  >
                    <Box
                      sx={{
                        width: 8,
                        height: 8,
                        borderRadius: '50%',
                        bgcolor: med.color,
                        mr: 2,
                      }}
                    />
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Typography variant="body2" fontWeight={500}>
                            {med.name}
                          </Typography>
                          <FormControlLabel
                            control={
                              <Switch
                                checked={med.taken}
                                size="small"
                                sx={{
                                  '& .MuiSwitch-switchBase.Mui-checked': {
                                    color: med.color,
                                  },
                                  '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
                                    backgroundColor: med.color,
                                  },
                                }}
                              />
                            }
                            label=""
                            sx={{ m: 0 }}
                          />
                        </Box>
                      }
                      secondary={
                        <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                          <Typography variant="caption" color="text.secondary">
                            {med.dosage}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {med.time}
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>

              {/* Recommendations */}
              <Box sx={{ mt: 3, p: 2, bgcolor: alpha(theme.palette.info.main, 0.05), borderRadius: 2 }}>
                <Typography variant="subtitle2" fontWeight={600} sx={{ mb: 1 }}>
                  Recommendations
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Patient shows stable vital signs. Continue current medication regimen and monitor for any changes.
                </Typography>
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Container>

      {/* CSS Animations */}
      <style>
        {`
          @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
          }
          @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
          }
          @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
          }
        `}
      </style>
    </Box>
  );
};

export default PatientMonitoring;
