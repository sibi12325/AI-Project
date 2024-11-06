import pandas as pd
from io import StringIO

def process(csv_data):
    """
    Preprocess the CSV data.
    """
    # Read CSV data
    df = pd.read_csv(StringIO(csv_data))
    
    # Convert back to CSV string
    processed_data = df.to_csv(index=False)
    
    return processed_data