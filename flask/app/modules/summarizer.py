from openai import OpenAI
from flask import current_app
import pandas as pd

def summarize(data, errors, corrected_data=None):
    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=current_app.config['OPENAI_API_KEY'])

    # Make a request to the ChatCompletion API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a conversational assistant that identifies errors in submission forms"},
            {"role": "system", "content": f"The data for the submission form is {data}"},
            {"role": "system", "content": f"The errors found are {errors}"},
            {"role": "system", "content": "Ensure your response is formatted in markdown"},
            {"role": "user", "content": "What errors have I made? Describe them to me in a conversational way"}
        ]
    )
    
    # Extract the summary from the response
    summary = response.choices[0].message.content.strip()
    
    #If Corrected data provided, convert to CSV and also return it
    if corrected_data:
        df = pd.DataFrame(corrected_data)
        corrected_csv = df.to_csv(index=False)
        return summary, corrected_csv
    
    return summary
