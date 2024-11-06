import React from 'react';
import { Box, LinearProgress, CircularProgress, Typography } from '@mui/material';

const ProgressIndicator = ({ progress, isLoading, loadingText }) => {
  return (
    <Box sx={{ width: '100%', mt: 2, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      {isLoading ? (
        <>
          <CircularProgress size={60} thickness={4} />
          <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 1 }}>
            {loadingText}
          </Typography>
        </>
      ) : (
        <>
          <LinearProgress variant="determinate" value={progress} sx={{ width: '100%' }} />
          <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 1 }}>
            {`${Math.round(progress)}%`}
          </Typography>
        </>
      )}
    </Box>
  );
};

export default ProgressIndicator;