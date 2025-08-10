import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Paper,
  Grid,
  Card,
  CardContent,
  Chip,
  Fade,
  Slide,
  IconButton,
  Dialog,
  DialogContent,
  DialogTitle,
  TextField,
  Backdrop,
} from '@mui/material';
import {
  MedicalServices,
  Psychology,
  EmergencyShare,
  Analytics,
  HealthAndSafety,
  MonitorHeart,
  LocalHospital,
  Science,
  Close,
  Phone,
  Email,
  LocationOn,
  PlayArrow,
  Menu as MenuIcon,
  Search as SearchIcon,
  AccountCircle as AccountIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { styled, keyframes } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';

const float = keyframes`
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  25% { transform: translateY(-20px) rotate(1deg); }
  50% { transform: translateY(-10px) rotate(-1deg); }
  75% { transform: translateY(-30px) rotate(1deg); }
`;

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
`;

const HeroSection = styled(Box)(({ theme }) => ({
  background: 'linear-gradient(135deg, #e8f4fd 0%, #d6e9f7 25%, #c4ddf0 50%, #b3d2e9 75%, #a1c6e2 100%)',
  minHeight: '100vh',
  display: 'flex',
  alignItems: 'center',
  position: 'relative',
  overflow: 'hidden',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'linear-gradient(45deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.05) 100%)',
    zIndex: 1,
  },
}));

const TopNavigation = styled(Box)(({ theme }) => ({
  position: 'absolute',
  top: 0,
  left: 0,
  right: 0,
  zIndex: 100,
  background: 'rgba(255, 255, 255, 0.95)',
  backdropFilter: 'blur(20px)',
  borderBottom: '1px solid rgba(0, 0, 0, 0.05)',
}));

const FloatingCard = styled(motion.div)(({ theme }) => ({
  position: 'absolute',
  background: 'rgba(255, 255, 255, 0.25)',
  backdropFilter: 'blur(15px)',
  borderRadius: '20px',
  padding: '20px',
  border: '1px solid rgba(255, 255, 255, 0.3)',
  animation: `${float} 6s ease-in-out infinite`,
}));

const ContactOverlay = styled(motion.div)(({ theme }) => ({
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  background: 'rgba(139, 123, 255, 0.95)',
  backdropFilter: 'blur(20px)',
  borderRadius: '24px',
  padding: '32px',
  border: '1px solid rgba(255, 255, 255, 0.2)',
  color: 'white',
  textAlign: 'center',
  minWidth: '300px',
  zIndex: 10,
}));

const BrandText = styled(Typography)(({ theme }) => ({
  fontSize: '8rem',
  fontWeight: 900,
  color: '#2c3e50',
  letterSpacing: '-0.02em',
  lineHeight: 0.8,
  position: 'relative',
  zIndex: 2,
  textShadow: '0 4px 20px rgba(0,0,0,0.1)',
  [theme.breakpoints.down('md')]: {
    fontSize: '4rem',
  },
  [theme.breakpoints.down('sm')]: {
    fontSize: '2.5rem',
  },
}));

const FeatureCard = styled(Card)(({ theme }) => ({
  height: '100%',
  background: 'linear-gradient(145deg, #ffffff 0%, #f8fafc 100%)',
  borderRadius: '16px',
  border: '1px solid rgba(0,0,0,0.08)',
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'translateY(-8px)',
    boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
    animation: `${pulse} 2s ease-in-out infinite`,
  },
}));

const ModernHome: React.FC = () => {
  const navigate = useNavigate();
  const [contactOpen, setContactOpen] = useState(false);
  const [showOverlay, setShowOverlay] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowOverlay(true);
    }, 2000);
    return () => clearTimeout(timer);
  }, []);

  const handleContactClose = () => {
    setContactOpen(false);
  };

  const handleOverlayClose = () => {
    setShowOverlay(false);
  };

  const features = [
    {
      icon: <Psychology sx={{ fontSize: 40, color: '#667eea' }} />,
      title: "AI Diagnosis",
      description: "Advanced AI-powered symptom analysis and diagnosis with WHO/CDC guidelines",
      color: "#667eea",
      action: () => navigate('/diagnosis')
    },
    {
      icon: <MonitorHeart sx={{ fontSize: 40, color: '#f093fb' }} />,
      title: "Patient Monitoring",
      description: "Real-time patient monitoring with live health metrics and alerts",
      color: "#f093fb",
      action: () => navigate('/patient-monitoring')
    },
    {
      icon: <EmergencyShare sx={{ fontSize: 40, color: '#ff6b6b' }} />,
      title: "Emergency Detection",
      description: "Automated emergency condition detection and immediate alert system",
      color: "#ff6b6b",
      action: () => navigate('/emergency')
    },
    {
      icon: <Science sx={{ fontSize: 40, color: '#4ecdc4' }} />,
      title: "Medical Research",
      description: "Access to latest medical research and treatment guidelines",
      color: "#4ecdc4",
      action: () => navigate('/research')
    }
  ];

  return (
    <Box>
      {/* Top Navigation */}
      <TopNavigation>
        <Container maxWidth="xl">
          <Box display="flex" alignItems="center" justifyContent="space-between" py={2}>
            <Box display="flex" alignItems="center">
              <Typography variant="h5" fontWeight="bold" color="#2c3e50">
                AI Health
              </Typography>
            </Box>
            <Box display="flex" alignItems="center" gap={1}>
              <IconButton>
                <MenuIcon />
              </IconButton>
              <IconButton>
                <SearchIcon />
              </IconButton>
              <IconButton>
                <AccountIcon />
              </IconButton>
            </Box>
          </Box>
        </Container>
      </TopNavigation>

      {/* Hero Section */}
      <HeroSection>
        <Container maxWidth="xl" sx={{ position: 'relative', zIndex: 2 }}>
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12}>
              <motion.div
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 1 }}
              >
                <Box textAlign="center" mb={8}>
                  <BrandText>
                    CONT
                    <Box component="span" sx={{ color: '#667eea' }}>
                      ACT
                    </Box>
                    US
                  </BrandText>
                  <Typography 
                    variant="h6" 
                    color="text.secondary" 
                    mt={2}
                    sx={{ maxWidth: 600, mx: 'auto' }}
                  >
                    Advanced AI Healthcare Platform for Modern Medical Practice
                  </Typography>
                </Box>
              </motion.div>
            </Grid>
          </Grid>

          {/* Floating Elements */}
          <FloatingCard
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5, duration: 0.8 }}
            style={{ top: '20%', left: '10%' }}
          >
            <MonitorHeart sx={{ fontSize: 30, color: '#667eea' }} />
            <Typography variant="body2" mt={1}>Real-time Monitoring</Typography>
          </FloatingCard>

          <FloatingCard
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.7, duration: 0.8 }}
            style={{ top: '60%', right: '15%' }}
          >
            <Psychology sx={{ fontSize: 30, color: '#f093fb' }} />
            <Typography variant="body2" mt={1}>AI Analysis</Typography>
          </FloatingCard>

          <FloatingCard
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.9, duration: 0.8 }}
            style={{ bottom: '20%', left: '20%' }}
          >
            <Science sx={{ fontSize: 30, color: '#4ecdc4' }} />
            <Typography variant="body2" mt={1}>Research Data</Typography>
          </FloatingCard>

          {/* Contact Overlay */}
          <AnimatePresence>
            {showOverlay && (
              <Backdrop open={showOverlay} sx={{ zIndex: 15 }}>
                <ContactOverlay
                  initial={{ opacity: 0, scale: 0.5 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.5 }}
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                >
                  <IconButton
                    onClick={handleOverlayClose}
                    sx={{ position: 'absolute', top: 8, right: 8, color: 'white' }}
                  >
                    <Close />
                  </IconButton>
                  <Typography variant="h6" mb={2} fontWeight="bold">
                    AI HEALTH LABORATORY
                  </Typography>
                  <Typography variant="body2" mb={1}>
                    <Phone sx={{ fontSize: 16, mr: 1 }} />
                    (555) 124-4567
                  </Typography>
                  <Typography variant="body2" mb={1}>
                    <Email sx={{ fontSize: 16, mr: 1 }} />
                    AIHEALTH@GMAIL.COM
                  </Typography>
                  <Typography variant="body2">
                    <LocationOn sx={{ fontSize: 16, mr: 1 }} />
                    678 HEALTHCARE WAY, SEATTLE
                  </Typography>
                  <Button
                    variant="contained"
                    sx={{ 
                      mt: 3, 
                      backgroundColor: 'white', 
                      color: '#667eea',
                      '&:hover': { backgroundColor: '#f8f9fa' }
                    }}
                    onClick={() => navigate('/diagnosis')}
                  >
                    Start Diagnosis
                  </Button>
                </ContactOverlay>
              </Backdrop>
            )}
          </AnimatePresence>
        </Container>
      </HeroSection>

      {/* Features Section */}
      <Box py={8} sx={{ background: '#f8fafc' }}>
        <Container maxWidth="xl">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <Typography variant="h3" textAlign="center" mb={6} fontWeight="bold" color="#2c3e50">
              Healthcare Solutions
            </Typography>
            <Grid container spacing={4}>
              {features.map((feature, index) => (
                <Grid item xs={12} sm={6} md={3} key={index}>
                  <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1, duration: 0.6 }}
                    viewport={{ once: true }}
                    whileHover={{ scale: 1.05 }}
                  >
                    <FeatureCard onClick={feature.action} sx={{ cursor: 'pointer' }}>
                      <CardContent sx={{ textAlign: 'center', p: 3 }}>
                        <Box mb={2}>
                          {feature.icon}
                        </Box>
                        <Typography variant="h6" fontWeight="bold" mb={2}>
                          {feature.title}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {feature.description}
                        </Typography>
                      </CardContent>
                    </FeatureCard>
                  </motion.div>
                </Grid>
              ))}
            </Grid>
          </motion.div>
        </Container>
      </Box>

      {/* CTA Section */}
      <Box 
        py={8} 
        sx={{ 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white'
        }}
      >
        <Container maxWidth="lg">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <Box textAlign="center">
              <Typography variant="h3" fontWeight="bold" mb={3}>
                Ready to Transform Healthcare?
              </Typography>
              <Typography variant="h6" mb={4} sx={{ opacity: 0.9 }}>
                Join thousands of healthcare professionals using our AI platform
              </Typography>
              <Button
                variant="contained"
                size="large"
                sx={{ 
                  backgroundColor: 'white', 
                  color: '#667eea',
                  px: 4,
                  py: 2,
                  fontSize: '1.1rem',
                  '&:hover': { 
                    backgroundColor: '#f8f9fa',
                    transform: 'translateY(-2px)'
                  }
                }}
                onClick={() => navigate('/diagnosis')}
              >
                Get Started Now
              </Button>
            </Box>
          </motion.div>
        </Container>
      </Box>
    </Box>
  );
};

export default ModernHome;
