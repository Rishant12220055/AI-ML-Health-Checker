import React from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Container,
  Stack,
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
  TrendingUp as TrendingIcon,
  Shield as ShieldIcon,
  AccessTime as TimeIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { motion, useScroll, useTransform } from 'framer-motion';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const { scrollY } = useScroll();
  const y1 = useTransform(scrollY, [0, 300], [0, 100]);
  const y2 = useTransform(scrollY, [0, 300], [0, -100]);

  const stats = [
    { number: "50K+", label: "Patients Helped", icon: <MonitorIcon /> },
    { number: "95%", label: "Accuracy Rate", icon: <TrendingIcon /> },
    { number: "24/7", label: "Available", icon: <TimeIcon /> },
    { number: "100%", label: "Secure", icon: <ShieldIcon /> },
  ];

  const services = [
    {
      title: "AI Symptom Analysis",
      description: "Advanced AI-powered symptom checker with real-time diagnosis",
      icon: <AIIcon />,
      color: "#6366f1"
    },
    {
      title: "Health Monitoring", 
      description: "Continuous monitoring of vital signs and health metrics",
      icon: <MonitorIcon />,
      color: "#06b6d4"
    },
    {
      title: "Emergency Detection",
      description: "Instant emergency condition detection and alerts",
      icon: <SecurityIcon />,
      color: "#f59e0b"
    },
    {
      title: "Treatment Plans",
      description: "Personalized treatment recommendations based on medical guidelines",
      icon: <SpeedIcon />,
      color: "#10b981"
    }
  ];

  return (
    <Box sx={{ 
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Animated Background Elements */}
      <motion.div
        style={{ 
          y: y1,
          position: 'absolute',
          top: '20%',
          right: '10%',
          width: '300px',
          height: '300px',
          background: 'rgba(255,255,255,0.1)',
          borderRadius: '50%',
          filter: 'blur(60px)',
        }}
      />
      <motion.div
        style={{ 
          y: y2,
          position: 'absolute',
          bottom: '20%',
          left: '10%',
          width: '400px',
          height: '400px',
          background: 'rgba(147, 51, 234, 0.2)',
          borderRadius: '50%',
          filter: 'blur(80px)',
        }}
      />
      
      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <Box sx={{ 
            textAlign: 'center', 
            py: { xs: 8, md: 12 },
            position: 'relative'
          }}>
            {/* Brand */}
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <Typography 
                sx={{
                  fontSize: { xs: '2.5rem', md: '4rem' },
                  fontWeight: 900,
                  color: 'white',
                  mb: 1,
                  letterSpacing: '0.1em',
                  textShadow: '0 4px 20px rgba(0,0,0,0.3)',
                  fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif'
                }}
              >
                MYHEALTH
              </Typography>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.4 }}
            >
              <Typography 
                sx={{
                  fontSize: { xs: '1.1rem', md: '1.3rem' },
                  color: 'rgba(255,255,255,0.9)',
                  mb: 6,
                  maxWidth: '700px',
                  mx: 'auto',
                  lineHeight: 1.6,
                  fontWeight: 300
                }}
              >
                Advanced AI-powered healthcare assistant providing intelligent symptom analysis, 
                real-time monitoring, and personalized treatment recommendations.
              </Typography>
            </motion.div>

            {/* CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
            >
              <Stack 
                direction={{ xs: 'column', sm: 'row' }} 
                spacing={3} 
                justifyContent="center"
                sx={{ mb: 8 }}
              >
                <Button
                  variant="contained"
                  size="large"
                  onClick={() => navigate('/symptom-checker')}
                  endIcon={<ArrowIcon />}
                  sx={{ 
                    px: 5, 
                    py: 2.5,
                    fontSize: '1.1rem',
                    background: 'rgba(255,255,255,0.95)',
                    color: '#667eea',
                    fontWeight: 600,
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255,255,255,0.2)',
                    borderRadius: '50px',
                    '&:hover': {
                      background: 'rgba(255,255,255,1)',
                      transform: 'translateY(-3px)',
                      boxShadow: '0 15px 50px rgba(0,0,0,0.3)',
                    },
                    transition: 'all 0.3s ease',
                  }}
                >
                  Start Diagnosis
                </Button>
                
                <Button
                  variant="outlined"
                  size="large"
                  startIcon={<PlayIcon />}
                  sx={{ 
                    px: 5, 
                    py: 2.5,
                    fontSize: '1.1rem',
                    color: 'white',
                    borderColor: 'rgba(255,255,255,0.5)',
                    backdropFilter: 'blur(10px)',
                    borderRadius: '50px',
                    '&:hover': {
                      background: 'rgba(255,255,255,0.1)',
                      borderColor: 'white',
                      transform: 'translateY(-3px)',
                      boxShadow: '0 15px 50px rgba(0,0,0,0.2)',
                    },
                    transition: 'all 0.3s ease',
                  }}
                >
                  Watch Demo
                </Button>
              </Stack>
            </motion.div>

            {/* Stats */}
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.8 }}
            >
              <Grid container spacing={4}>
                {stats.map((stat, index) => (
                  <Grid item xs={6} md={3} key={index}>
                    <motion.div
                      whileHover={{ scale: 1.05 }}
                      transition={{ type: "spring", stiffness: 300 }}
                    >
                      <Box sx={{ 
                        textAlign: 'center',
                        p: 3,
                        background: 'rgba(255,255,255,0.1)',
                        backdropFilter: 'blur(20px)',
                        borderRadius: 3,
                        border: '1px solid rgba(255,255,255,0.2)',
                        cursor: 'pointer'
                      }}>
                        <Box sx={{ color: 'white', mb: 1, fontSize: '2rem' }}>
                          {stat.icon}
                        </Box>
                        <Typography 
                          sx={{ 
                            fontSize: { xs: '1.5rem', md: '2rem' }, 
                            fontWeight: 700, 
                            color: 'white',
                            mb: 0.5
                          }}
                        >
                          {stat.number}
                        </Typography>
                        <Typography 
                          sx={{ 
                            fontSize: '0.9rem', 
                            color: 'rgba(255,255,255,0.8)' 
                          }}
                        >
                          {stat.label}
                        </Typography>
                      </Box>
                    </motion.div>
                  </Grid>
                ))}
              </Grid>
            </motion.div>
          </Box>
        </motion.div>

        {/* Services Section */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
        >
          <Box sx={{ py: 8 }}>
            <Typography 
              variant="h3" 
              sx={{ 
                textAlign: 'center', 
                mb: 6, 
                color: 'white',
                fontWeight: 700,
                fontSize: { xs: '2rem', md: '3rem' }
              }}
            >
              Our Services
            </Typography>
            
            <Grid container spacing={4}>
              {services.map((service, index) => (
                <Grid item xs={12} md={6} key={index}>
                  <motion.div
                    initial={{ opacity: 0, y: 50 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: index * 0.1 }}
                    whileHover={{ scale: 1.03, y: -5 }}
                    viewport={{ once: true }}
                  >
                    <Card sx={{ 
                      height: '100%',
                      background: 'rgba(255,255,255,0.95)',
                      backdropFilter: 'blur(20px)',
                      border: '1px solid rgba(255,255,255,0.2)',
                      borderRadius: 4,
                      transition: 'all 0.3s ease',
                      cursor: 'pointer',
                      '&:hover': {
                        boxShadow: '0 25px 80px rgba(0,0,0,0.3)',
                      }
                    }}>
                      <CardContent sx={{ p: 4 }}>
                        <Box 
                          sx={{ 
                            width: 70,
                            height: 70,
                            borderRadius: '20px',
                            background: service.color,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: 'white',
                            mb: 3,
                            fontSize: '2rem'
                          }}
                        >
                          {service.icon}
                        </Box>
                        <Typography 
                          variant="h5" 
                          sx={{ mb: 2, fontWeight: 600, color: '#1a1a1a' }}
                        >
                          {service.title}
                        </Typography>
                        <Typography 
                          variant="body1" 
                          sx={{ color: '#666', lineHeight: 1.7 }}
                        >
                          {service.description}
                        </Typography>
                      </CardContent>
                    </Card>
                  </motion.div>
                </Grid>
              ))}
            </Grid>
          </Box>
        </motion.div>

        {/* Contact Section */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
        >
          <Box sx={{ py: 8 }}>
            <Typography 
              variant="h2" 
              sx={{ 
                textAlign: 'center', 
                mb: 2, 
                color: 'white',
                fontWeight: 700,
                fontSize: { xs: '3rem', md: '5rem' },
                letterSpacing: '0.05em'
              }}
            >
              CONTACT US
            </Typography>
            
            <Typography 
              sx={{ 
                textAlign: 'center', 
                mb: 6, 
                color: 'rgba(255,255,255,0.9)',
                fontSize: '1.2rem',
                fontWeight: 300
              }}
            >
              Get in touch with our healthcare professionals
            </Typography>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              viewport={{ once: true }}
            >
              <Card sx={{ 
                maxWidth: 700,
                mx: 'auto',
                background: 'rgba(255,255,255,0.95)',
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: 4,
                p: 5,
                boxShadow: '0 30px 100px rgba(0,0,0,0.3)'
              }}>
                <Stack spacing={4}>
                  <motion.div
                    whileHover={{ scale: 1.02 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
                      <Avatar sx={{ bgcolor: '#667eea', width: 60, height: 60 }}>
                        <PhoneIcon sx={{ fontSize: '1.5rem' }} />
                      </Avatar>
                      <Box>
                        <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5 }}>
                          Phone
                        </Typography>
                        <Typography color="text.secondary" sx={{ fontSize: '1.1rem' }}>
                          +1 (555) 123-4567
                        </Typography>
                      </Box>
                    </Box>
                  </motion.div>
                  
                  <motion.div
                    whileHover={{ scale: 1.02 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
                      <Avatar sx={{ bgcolor: '#10b981', width: 60, height: 60 }}>
                        <EmailIcon sx={{ fontSize: '1.5rem' }} />
                      </Avatar>
                      <Box>
                        <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5 }}>
                          Email
                        </Typography>
                        <Typography color="text.secondary" sx={{ fontSize: '1.1rem' }}>
                          support@myhealth.com
                        </Typography>
                      </Box>
                    </Box>
                  </motion.div>
                  
                  <motion.div
                    whileHover={{ scale: 1.02 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
                      <Avatar sx={{ bgcolor: '#f59e0b', width: 60, height: 60 }}>
                        <LocationIcon sx={{ fontSize: '1.5rem' }} />
                      </Avatar>
                      <Box>
                        <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5 }}>
                          Address
                        </Typography>
                        <Typography color="text.secondary" sx={{ fontSize: '1.1rem' }}>
                          123 Healthcare Ave, Medical District, NY 10001
                        </Typography>
                      </Box>
                    </Box>
                  </motion.div>
                </Stack>
              </Card>
            </motion.div>
          </Box>
        </motion.div>
      </Container>
    </Box>
  );
};

export default Home;
