import React from 'react';
import { Box } from '@mui/material';

const BackgroundAnimation = ({ darkMode }) => {
  return (
    <Box
      sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        zIndex: 0,
        overflow: 'hidden',
        '&::before, &::after': {
          content: '""',
          position: 'absolute',
          width: '400px',
          height: '400px',
          borderRadius: '50%',
          opacity: darkMode ? 0.15 : 0.25,
          animation: 'float 20s infinite ease-in-out',
          filter: 'blur(60px)',
        },
        '&::before': {
          background: 'radial-gradient(circle, #3B9DFF, transparent 70%)',
          top: '-200px',
          left: '-200px',
        },
        '&::after': {
          background: 'radial-gradient(circle, #C0C0C0, transparent 70%)',
          bottom: '-200px',
          right: '-200px',
          animationDelay: '-10s',
        },
        '@keyframes float': {
          '0%, 100%': {
            transform: 'translate(0, 0) rotate(0deg)',
          },
          '25%': {
            transform: 'translate(50px, 50px) rotate(90deg)',
          },
          '50%': {
            transform: 'translate(0, 100px) rotate(180deg)',
          },
          '75%': {
            transform: 'translate(-50px, 50px) rotate(270deg)',
          },
        },
      }}
    />
  );
};

export default BackgroundAnimation;