import React, { useState } from 'react';
import { Typography, Button, Paper, Box } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { styled } from '@mui/material/styles';

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

const AnimatedFileUpload = ({ onFileSelect }) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDragIn = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragOut = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  };

  return (
    <Paper
      elevation={3}
      sx={{
        border: 3,
        borderRadius: 4,
        borderColor: isDragging ? 'secondary.main' : 'grey.300',
        borderStyle: 'dashed',
        p: 4,
        textAlign: 'center',
        transition: 'all 0.3s ease',
        '&:hover': {
          borderColor: 'primary.main',
          backgroundColor: 'action.hover',
          transform: 'translateY(-5px)',
        },
        background: (theme) =>
          `linear-gradient(45deg, ${theme.palette.background.paper} 30%, ${
            theme.palette.mode === 'dark' ? '#2a2a2a' : '#f0f0f0'
          } 90%)`,
      }}
      onDragEnter={handleDragIn}
      onDragLeave={handleDragOut}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <CloudUploadIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
        <Typography variant="h5" gutterBottom fontWeight="bold">
          Drag and drop your Excel file here
        </Typography>
        <Typography variant="body1" color="text.secondary" gutterBottom>
          or
        </Typography>
        <Button 
          component="label" 
          variant="contained" 
          startIcon={<CloudUploadIcon />}
          sx={{ 
            mt: 2,
            background: 'linear-gradient(45deg, #3B9DFF 30%, #C0C0C0 90%)',
            color: 'white',
            transition: 'all 0.3s ease',
            '&:hover': {
              background: 'linear-gradient(45deg, #357ae8 30%, #a0a0a0 90%)',
              transform: 'scale(1.05)',
            },
          }}
        >
          Select File
          <VisuallyHiddenInput type="file" onChange={(e) => onFileSelect(e.target.files[0])} accept=".xlsx,.xls" />
        </Button>
      </Box>
    </Paper>
  );
};

export default AnimatedFileUpload;