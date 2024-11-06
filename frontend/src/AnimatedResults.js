import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Box, Typography, Divider, Chip, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const AnimatedResults = ({ results }) => {
  const renderList = (items, title) => (
    <Box sx={{ mt: 2 }}>
      <Typography variant="subtitle1" gutterBottom>{title}:</Typography>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
        {items.map((item, index) => (
          <Chip key={index} label={item} variant="outlined" />
        ))}
      </Box>
    </Box>
  );

  const renderDataTypesTable = (dataTypes) => (
    <TableContainer component={Paper} sx={{ mt: 2 }}>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Column Name</TableCell>
            <TableCell>Data Type</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {Object.entries(dataTypes).map(([columnName, dataType]) => (
            <TableRow key={columnName}>
              <TableCell>{columnName}</TableCell>
              <TableCell>{dataType}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );


  const renderSection = (title, content) => (
    <Box sx={{ mb: 4 }}>
      <Typography variant="h6" color="primary" gutterBottom>{title}</Typography>
      <Divider sx={{ mb: 2 }} />
      {content}
    </Box>
  );

  return (
    <Box sx={{ mt: 4, maxWidth: 800, mx: 'auto' }}>
      <Typography 
        variant="h4" 
        gutterBottom 
        sx={{ 
          textAlign: 'center',
          mb: 4,
          fontWeight: 'bold',
          color: 'primary.main'
        }}
      >
        Analysis Results
      </Typography>
      
      {renderSection("CoC ID", 
        <Typography variant="body1">{results.coc_id}</Typography>
      )}

      {renderSection("Summary", 
        <ReactMarkdown>{results.summary || 'No summary available'}</ReactMarkdown>
      )}

      {renderSection("Errors", 
        <ReactMarkdown>{results.errors || 'No errors found'}</ReactMarkdown>
      )}

      {results.data_summary && renderSection("Data Summary", 
        <>
          <Typography variant="body1">Number of rows: {results.data_summary.num_rows || 'N/A'}</Typography>
          <Typography variant="body1">Number of columns: {results.data_summary.num_columns || 'N/A'}</Typography>

          {results.data_summary.column_names && renderList(results.data_summary.column_names, "Column Names")}
          
          {results.data_summary.data_types && renderDataTypesTable(results.data_summary.data_types)}
        </>
      )}

      {results.white_space && results.white_space.length > 0 && renderSection("White Space Indexes", 
        renderList(results.white_space, "Indexes")
      )}

      {results.processed_data && renderSection("Processed Data", 
        <ReactMarkdown>{results.processed_data}</ReactMarkdown>
      )}
    </Box>
  );
};

export default AnimatedResults;