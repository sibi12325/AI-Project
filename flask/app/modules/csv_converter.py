import pandas as pd
from io import BytesIO

def convert(file):
    """
    Convert Excel file to CSV data.
    """
    # Read the Excel file
    df = pd.read_excel(BytesIO(file.read()), sheet_name='Sample Details', usecols='A:BC')

    # Find the index of the last non-blank row
    endIndex = df.last_valid_index()

    # Get the CoC ID
    coc_ID = df.iloc[0:0,53:55].to_csv(index=False)

    # Slice to include only up to the last non-blank row and only columns A-H
    df = df.iloc[:endIndex + 1, 0:8]
    
    # Convert DataFrame to CSV string
    csv_data = df.to_csv(index=False)
    
    return csv_data, coc_ID