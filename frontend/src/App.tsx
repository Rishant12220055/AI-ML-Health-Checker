import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Container } from '@mui/material';
import Header from './components/Header';
import Home from './components/Home';
import SymptomChecker from './components/SymptomChecker';
import Results from './components/Results';
import About from './components/About';
import Privacy from './components/Privacy';
import PatientMonitoring from './components/PatientMonitoring';
import './App.css';

const App: React.FC = () => {
  return (
    <div className="App">
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/patient-monitoring" element={<PatientMonitoring />} />
        <Route path="/symptom-checker" element={<SymptomChecker />} />
        <Route path="/results/:sessionId" element={<Results />} />
        <Route path="/about" element={<About />} />
        <Route path="/privacy" element={<Privacy />} />
      </Routes>
    </div>
  );
};

export default App;
