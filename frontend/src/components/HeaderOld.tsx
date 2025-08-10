import React from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  Box,
  IconButton,
  Menu,
  MenuItem,
  alpha,
  useTheme
} from '@mui/material';
import { 
  LocalHospital as MedicalIcon,
  Menu as MenuIcon,
  Info as InfoIcon,
  PrivacyTip as PrivacyIcon,
  Home as HomeIcon,
  Psychology as SymptomIcon,
  MonitorHeart as MonitorIcon
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const Header: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleNavigation = (path: string) => {
    navigate(path);
    handleMenuClose();
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <AppBar 
      position="static" 
      elevation={0}
      sx={{
        background: `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.primary.dark})`,
        backdropFilter: 'blur(20px)',
        borderBottom: `1px solid ${alpha(theme.palette.common.white, 0.1)}`
      }}
    >
      <Toolbar sx={{ py: 1 }}>
        <Box 
          sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            cursor: 'pointer',
            mr: 4
          }}
          onClick={() => navigate('/')}
        >
          <Box
            sx={{
              p: 1,
              borderRadius: 2,
              backgroundColor: alpha(theme.palette.common.white, 0.1),
              mr: 2,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <MedicalIcon sx={{ fontSize: 28, color: 'white' }} />
          </Box>
          <Typography 
            variant="h6" 
            component="div" 
            sx={{ 
              fontWeight: 700,
              fontSize: '1.3rem',
              color: 'white'
            }}
          >
            HealthAI
          </Typography>
        </Box>

        <Box sx={{ flexGrow: 1 }} />

        {/* Desktop Navigation */}
        <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 1 }}>
          <Button 
            color="inherit" 
            onClick={() => navigate('/')}
            startIcon={<HomeIcon />}
            sx={{
              px: 3,
              py: 1,
              borderRadius: 3,
              fontWeight: 600,
              backgroundColor: isActive('/') ? alpha(theme.palette.common.white, 0.15) : 'transparent',
              '&:hover': {
                backgroundColor: alpha(theme.palette.common.white, 0.1),
                transform: 'translateY(-1px)',
              },
              transition: 'all 0.2s ease'
            }}
          >
            Home
          </Button>
          <Button 
            color="inherit" 
            onClick={() => navigate('/patient-monitoring')}
            startIcon={<MonitorIcon />}
            sx={{
              px: 3,
              py: 1,
              borderRadius: 3,
              fontWeight: 600,
              backgroundColor: isActive('/patient-monitoring') ? alpha(theme.palette.common.white, 0.15) : 'transparent',
              '&:hover': {
                backgroundColor: alpha(theme.palette.common.white, 0.1),
                transform: 'translateY(-1px)',
              },
              transition: 'all 0.2s ease'
            }}
          >
            Patient Monitoring
          </Button>
          <Button 
            color="inherit" 
            onClick={() => navigate('/symptom-checker')}
            startIcon={<SymptomIcon />}
            sx={{
              px: 3,
              py: 1,
              borderRadius: 3,
              fontWeight: 600,
              backgroundColor: isActive('/symptom-checker') ? alpha(theme.palette.common.white, 0.15) : 'transparent',
              '&:hover': {
                backgroundColor: alpha(theme.palette.common.white, 0.1),
                transform: 'translateY(-1px)',
              },
              transition: 'all 0.2s ease'
            }}
          >
            Symptom Checker
          </Button>
          <Button 
            color="inherit" 
            onClick={() => navigate('/about')}
            startIcon={<InfoIcon />}
            sx={{
              px: 3,
              py: 1,
              borderRadius: 3,
              fontWeight: 600,
              backgroundColor: isActive('/about') ? alpha(theme.palette.common.white, 0.15) : 'transparent',
              '&:hover': {
                backgroundColor: alpha(theme.palette.common.white, 0.1),
                transform: 'translateY(-1px)',
              },
              transition: 'all 0.2s ease'
            }}
          >
            About
          </Button>
          <Button 
            color="inherit" 
            onClick={() => navigate('/privacy')}
            startIcon={<PrivacyIcon />}
            sx={{
              px: 3,
              py: 1,
              borderRadius: 3,
              fontWeight: 600,
              backgroundColor: isActive('/privacy') ? alpha(theme.palette.common.white, 0.15) : 'transparent',
              '&:hover': {
                backgroundColor: alpha(theme.palette.common.white, 0.1),
                transform: 'translateY(-1px)',
              },
              transition: 'all 0.2s ease'
            }}
          >
            Privacy
          </Button>
        </Box>

        {/* Mobile Navigation */}
        <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
          <IconButton
            color="inherit"
            onClick={handleMenuClick}
            sx={{
              borderRadius: 2,
              '&:hover': {
                backgroundColor: alpha(theme.palette.common.white, 0.1),
              }
            }}
          >
            <MenuIcon />
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
            PaperProps={{
              sx: {
                borderRadius: 3,
                mt: 1,
                minWidth: 200,
                boxShadow: `0 8px 32px ${alpha(theme.palette.common.black, 0.12)}`,
              }
            }}
          >
            <MenuItem 
              onClick={() => handleNavigation('/')}
              sx={{
                py: 1.5,
                px: 3,
                borderRadius: 2,
                mx: 1,
                mb: 0.5,
                backgroundColor: isActive('/') ? alpha(theme.palette.primary.main, 0.1) : 'transparent',
                '&:hover': {
                  backgroundColor: alpha(theme.palette.primary.main, 0.05),
                }
              }}
            >
              <HomeIcon sx={{ mr: 2, fontSize: 20 }} />
              Home
            </MenuItem>
            <MenuItem 
              onClick={() => handleNavigation('/patient-monitoring')}
              sx={{
                py: 1.5,
                px: 3,
                borderRadius: 2,
                mx: 1,
                mb: 0.5,
                backgroundColor: isActive('/patient-monitoring') ? alpha(theme.palette.primary.main, 0.1) : 'transparent',
                '&:hover': {
                  backgroundColor: alpha(theme.palette.primary.main, 0.05),
                }
              }}
            >
              <MonitorIcon sx={{ mr: 2, fontSize: 20 }} />
              Patient Monitoring
            </MenuItem>
            <MenuItem 
              onClick={() => handleNavigation('/symptom-checker')}
              sx={{
                py: 1.5,
                px: 3,
                borderRadius: 2,
                mx: 1,
                mb: 0.5,
                backgroundColor: isActive('/symptom-checker') ? alpha(theme.palette.primary.main, 0.1) : 'transparent',
                '&:hover': {
                  backgroundColor: alpha(theme.palette.primary.main, 0.05),
                }
              }}
            >
              <SymptomIcon sx={{ mr: 2, fontSize: 20 }} />
              Symptom Checker
            </MenuItem>
            <MenuItem 
              onClick={() => handleNavigation('/about')}
              sx={{
                py: 1.5,
                px: 3,
                borderRadius: 2,
                mx: 1,
                mb: 0.5,
                backgroundColor: isActive('/about') ? alpha(theme.palette.primary.main, 0.1) : 'transparent',
                '&:hover': {
                  backgroundColor: alpha(theme.palette.primary.main, 0.05),
                }
              }}
            >
              <InfoIcon sx={{ mr: 2, fontSize: 20 }} />
              About
            </MenuItem>
            <MenuItem 
              onClick={() => handleNavigation('/privacy')}
              sx={{
                py: 1.5,
                px: 3,
                borderRadius: 2,
                mx: 1,
                backgroundColor: isActive('/privacy') ? alpha(theme.palette.primary.main, 0.1) : 'transparent',
                '&:hover': {
                  backgroundColor: alpha(theme.palette.primary.main, 0.05),
                }
              }}
            >
              <PrivacyIcon sx={{ mr: 2, fontSize: 20 }} />
              Privacy
            </MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
