import React, { useState, useEffect } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Fade from '@mui/material/Fade';
import Slide from '@mui/material/Slide';
import AnimatedFileUpload from './AnimatedFileUpload';
import ProgressIndicator from './ProgressIndicator';
import AnimatedResults from './AnimatedResults';
import ThemeSwitcher from './ThemeSwitcher';
import BackgroundAnimation from './BackgroundAnimation';
import ParticleEffect from './ParticleEffect';
import axios from 'axios';

function App() {
  const [results, setResults] = useState(null);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);
  const [darkMode, setDarkMode] = useState(false);
  const [showContent, setShowContent] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingText, setLoadingText] = useState('');

  useEffect(() => {
    setTimeout(() => setShowContent(true), 500);
  }, []);
  
  const theme = createTheme({});


  const handleFileSelect = async (selectedFile) => {
    setProgress(0);
    setError(null);
    setResults(null);
    setIsLoading(true);
    setLoadingText('Uploading file...');
    setTimeout(() => {
      setLoadingText('Processing data...');
    }, 420);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('/api/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setProgress(percentCompleted);
        }
      });
      
      setProgress(0); 
      
      setResults(response.data);
      console.log(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
    } finally {
      setIsLoading(false);
      setLoadingText('');
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BackgroundAnimation darkMode={darkMode} />
      <ParticleEffect />
      <Container maxWidth="lg">
        <Fade in={showContent} timeout={1000}>
          <Box sx={{ my: 4, textAlign: 'center', position: 'relative', zIndex: 1 }}>
            <Typography 
              variant="h2" 
              component="h1" 
              gutterBottom
              sx={{
                fontWeight: 700,
                background: 'linear-gradient(45deg, #3B9DFF 30%, #C0C0C0 90%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                mb: 4,
                textShadow: '2px 2px 4px rgba(0,0,0,0.1)',
              }}
            >
              Genotyping Australia
            </Typography>
            <Box sx={{ position: 'absolute', top: 16, right: 16 }}>
              <ThemeSwitcher darkMode={darkMode} setDarkMode={setDarkMode} />
            </Box>
          </Box>
        </Fade>
        <Slide direction="up" in={showContent} timeout={1000}>
          <Box sx={{ mt: 4, position: 'relative', zIndex: 1 }}>
            <Typography variant="h5" sx={{ mb: 3, textAlign: 'center', fontWeight: 300 }}>
              Please insert your files for analysis
            </Typography>
            <AnimatedFileUpload onFileSelect={handleFileSelect} />
            {(progress > 0 || isLoading) && (
              <ProgressIndicator 
                progress={progress} 
                isLoading={isLoading || progress === 100} 
                loadingText={loadingText || (progress === 100 ? 'Processing data...' : '')} 
              />
            )}
            {results && (
              <AnimatedResults results={results} />
            )}
          </Box>
        </Slide>
      </Container>
    </ThemeProvider>
  );
}

export default App;