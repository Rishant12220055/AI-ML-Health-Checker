import React from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  Box,
  IconButton,
  alpha,
} from '@mui/material';
import { 
  LocalHospital as MedicalIcon,
  Home as HomeIcon,
  Psychology as SymptomIcon,
  MonitorHeart as MonitorIcon,
  Menu as MenuIcon
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';

const Header: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  const navigationItems = [
    { path: '/', label: 'Home', icon: <HomeIcon /> },
    { path: '/symptom-checker', label: 'Symptom Checker', icon: <SymptomIcon /> },
    { path: '/patient-monitoring', label: 'Patient Monitoring', icon: <MonitorIcon /> },
  ];

  return (
    <AppBar 
      position="static" 
      elevation={0}
      sx={{
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(20px)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.2)',
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
      }}
    >
      <Toolbar sx={{ justifyContent: 'space-between', py: 1 }}>
        {/* Logo */}
        <motion.div
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => navigate('/')}
          style={{ cursor: 'pointer' }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <MedicalIcon sx={{ fontSize: '2rem', color: '#667eea' }} />
            <Typography 
              variant="h5" 
              sx={{ 
                fontWeight: 900, 
                color: '#667eea',
                letterSpacing: '0.1em',
                fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif'
              }}
            >
              MYHEALTH
            </Typography>
          </Box>
        </motion.div>

        {/* Desktop Navigation */}
        <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 1 }}>
          {navigationItems.map((item) => (
            <motion.div
              key={item.path}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Button
                onClick={() => navigate(item.path)}
                startIcon={item.icon}
                sx={{
                  color: isActive(item.path) ? '#667eea' : '#666',
                  fontWeight: 500,
                  px: 3,
                  py: 1,
                  borderRadius: '50px',
                  background: isActive(item.path) 
                    ? 'rgba(102, 126, 234, 0.1)' 
                    : 'transparent',
                  border: '1px solid',
                  borderColor: isActive(item.path)
                    ? 'rgba(102, 126, 234, 0.3)'
                    : 'transparent',
                  '&:hover': {
                    background: 'rgba(102, 126, 234, 0.1)',
                    borderColor: 'rgba(102, 126, 234, 0.3)',
                    color: '#667eea',
                    transform: 'translateY(-2px)',
                    boxShadow: '0 8px 30px rgba(102, 126, 234, 0.2)',
                  },
                  transition: 'all 0.3s ease',
                }}
              >
                {item.label}
              </Button>
            </motion.div>
          ))}
        </Box>

        {/* Mobile Menu Button */}
        <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
          <IconButton
            sx={{
              color: '#667eea',
              background: 'rgba(102, 126, 234, 0.1)',
              '&:hover': {
                background: 'rgba(102, 126, 234, 0.2)',
              }
            }}
          >
            <MenuIcon />
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
