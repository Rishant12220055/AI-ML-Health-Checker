import React from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Container,
  Chip,
  Stack,
  useTheme,
  alpha,
  IconButton,
  Avatar,
} from '@mui/material';
import {
  Psychology as AIIcon,
  MonitorHeart as MonitorIcon,
  Speed as SpeedIcon,
  Security as SecurityIcon,
  Phone as PhoneIcon,
  Email as EmailIcon,
  LocationOn as LocationIcon,
  PlayArrow as PlayIcon,
  ArrowForward as ArrowIcon,
  Star as StarIcon,
  TrendingUp as TrendingIcon,
  Shield as ShieldIcon,
  AccessTime as TimeIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { motion, useScroll, useTransform } from 'framer-motion';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const theme = useTheme();

  const features = [
    {
      icon: <AIIcon fontSize="large" color="primary" />,
      title: "AI-Powered Analysis",
      description: "Advanced machine learning models analyze your symptoms using medical knowledge from WHO and CDC guidelines.",
      color: "#4facfe"
    },
    {
      icon: <MonitorIcon fontSize="large" color="secondary" />,
      title: "Real-time Monitoring",
      description: "Continuous patient monitoring with real-time data collection and analysis for healthcare professionals.",
      color: "#ff6b9d"
    },
    {
      icon: <SpeedIcon fontSize="large" color="success" />,
      title: "Instant Results",
      description: "Get comprehensive analysis and treatment recommendations in seconds, not hours.",
      color: "#67e8f9"
    },
    {
      icon: <VerifiedIcon fontSize="large" color="warning" />,
      title: "Evidence-Based",
      description: "All recommendations are based on established medical guidelines and peer-reviewed research.",
      color: "#c44569"
    }
  ];

  return (
    <Box sx={{ 
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      position: 'relative',
      overflow: 'hidden',
    }}>
      {/* Floating 3D Elements */}
      <Box
        sx={{
          position: 'absolute',
          top: '10%',
          right: '10%',
          width: 200,
          height: 200,
          borderRadius: '50%',
          background: 'linear-gradient(45deg, #ff6b9d, #c44569)',
          opacity: 0.6,
          filter: 'blur(40px)',
          animation: 'float 6s ease-in-out infinite',
          zIndex: 0
        }}
      />
      <Box
        sx={{
          position: 'absolute',
          bottom: '10%',
          left: '10%',
          width: 150,
          height: 150,
          borderRadius: '50%',
          background: 'linear-gradient(45deg, #4facfe, #00f2fe)',
          opacity: 0.4,
          filter: 'blur(30px)',
          animation: 'float 8s ease-in-out infinite reverse',
          zIndex: 0
        }}
      />

      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
        {/* Hero Section */}
        <Box sx={{ 
          textAlign: 'center', 
          py: { xs: 6, md: 10 },
          position: 'relative'
        }}>
          {/* Background decoration */}
          <Box
            sx={{
              position: 'absolute',
              top: '10%',
              right: '10%',
              width: 200,
              height: 200,
              borderRadius: '50%',
              background: `linear-gradient(45deg, ${alpha(theme.palette.primary.main, 0.1)}, ${alpha(theme.palette.secondary.main, 0.1)})`,
              filter: 'blur(40px)',
              zIndex: 0
            }}
          />
          <Box
            sx={{
              position: 'absolute',
              bottom: '10%',
              left: '10%',
              width: 150,
              height: 150,
              borderRadius: '50%',
              background: `linear-gradient(45deg, ${alpha(theme.palette.success.main, 0.1)}, ${alpha(theme.palette.warning.main, 0.1)})`,
              filter: 'blur(30px)',
              zIndex: 0
            }}
          />
          <Box sx={{ position: 'relative', zIndex: 1 }}>
            <Stack direction="row" spacing={1} justifyContent="center" sx={{ mb: 3 }}>
              <Chip 
                label="AI Powered" 
                color="primary" 
                variant="outlined"
                size="small"
              />
              <Chip 
                label="HIPAA Compliant" 
                color="secondary" 
                variant="outlined"
                size="small"
              />
              <Chip 
                label="24/7 Available" 
                color="success" 
                variant="outlined"
                size="small"
              />
            </Stack>
            
            <Typography 
              variant="h2" 
              component="h1" 
              gutterBottom 
              sx={{
                fontWeight: 700,
                background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                color: 'transparent',
                mb: 2
              }}
            >
              AI Healthcare Assistant
            </Typography>
            
            <Typography 
              variant="h5" 
              component="h2" 
              gutterBottom 
              color="text.secondary" 
              sx={{ mb: 4, fontWeight: 400 }}
            >
              Intelligent symptom analysis and treatment recommendations powered by medical AI
            </Typography>
            
            <Button
              variant="contained"
              size="large"
              onClick={() => navigate('/symptom-checker')}
              endIcon={<ArrowIcon />}
              sx={{ 
                px: 4, 
                py: 2, 
                fontSize: '1.2rem',
                background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                '&:hover': {
                  background: `linear-gradient(45deg, ${theme.palette.primary.dark}, ${theme.palette.secondary.dark})`,
                },
              }}
            >
              Start Symptom Analysis
            </Button>
          </Box>
        </Box>

      {/* Medical Disclaimer */}
      <Alert severity="warning" sx={{ mb: 6 }}>
        <AlertTitle>Important Medical Disclaimer</AlertTitle>
        This AI assistant is for informational purposes only and should not replace professional medical advice. 
        Always consult with qualified healthcare providers for medical diagnosis and treatment.
      </Alert>

      {/* Features Section */}
      <Typography variant="h3" component="h2" textAlign="center" gutterBottom sx={{ mb: 4 }}>
        Why Choose Our AI Assistant?
      </Typography>
      
      <Grid container spacing={4} sx={{ mb: 8 }}>
        {features.map((feature, index) => (
          <Grid item xs={12} md={6} key={index}>
            <Card sx={{ height: '100%', p: 2 }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <Box sx={{ mb: 2 }}>
                  {feature.icon}
                </Box>
                <Typography variant="h5" component="h3" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* How It Works Section */}
      <Box sx={{ bgcolor: 'background.paper', p: 4, borderRadius: 2, mb: 6 }}>
        <Typography variant="h4" component="h2" textAlign="center" gutterBottom>
          How It Works
        </Typography>
        
        <Grid container spacing={4} sx={{ mt: 2 }}>
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h6" color="primary" sx={{ mb: 1 }}>
                Step 1: Describe Symptoms
              </Typography>
              <Typography variant="body1">
                Enter your symptoms, their severity, and provide basic demographic information.
              </Typography>
            </Box>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h6" color="primary" sx={{ mb: 1 }}>
                Step 2: AI Analysis
              </Typography>
              <Typography variant="body1">
                Our multi-agent AI system processes your symptoms through specialized medical models.
              </Typography>
            </Box>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h6" color="primary" sx={{ mb: 1 }}>
                Step 3: Get Recommendations
              </Typography>
              <Typography variant="body1">
                Receive evidence-based treatment recommendations and guidance on when to seek care.
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Box>

      {/* Call to Action */}
      <Box sx={{ textAlign: 'center', py: 6 }}>
        <Typography variant="h4" component="h2" gutterBottom>
          Ready to Start?
        </Typography>
        <Typography variant="body1" sx={{ mb: 3 }}>
          Get personalized health insights in minutes with our AI-powered symptom checker.
        </Typography>
        <Button
          variant="contained"
          size="large"
          onClick={() => navigate('/symptom-checker')}
          sx={{ mr: 2 }}
        >
          Analyze Symptoms
        </Button>
        <Button
          variant="outlined"
          size="large"
          onClick={() => navigate('/about')}
        >
          Learn More
        </Button>
      </Box>
    </Container>
    </Box>
  );
};

export default Home;
