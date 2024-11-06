# now this file will return sample data so that we can do error checking 
import mysql.connector
import pandas as pd
import json
from datetime import datetime 
from openpyxl import load_workbook
import numpy as np
from openai import OpenAI
from flask import current_app
"""

Legacy file trying to find sample data in database, a proof of concept to show that you can feed in sample data once table structure is ammended or view is created

Here is the rundown

THIS TABLE 

Table: lims_prj_sample_types
  sample_type_id: 1
  sample_type: BovineRequestV2
  display_label: Bovine Genotyping
  sample_row: 1
  sample_col: BB
  species_row: 12
  species_col: A
  test_req_row: 12
  test_req_col: D
  data_row: 19
  future_coc: 0
  report_type: bovine_standard
  status: 0
  is_delete: 0
  created_by: 1
  created_date: 2022-10-18 06:26:11


LINKS THE COC (RENAMED TO SAMPLE_TYPE ) TO THE SAMPLE_TYPE_ID

WE THEN TAKE THE SAMPLE_TYPE_ID LOOK THRU THIS TABLE

Table: lims_project_master
  project_id: 156
  sample_type_id: None
  client_id: 0
  project_name: 
  project_desc: None
  po: None
  monday_id: None
  sow_id: None
  invoiced: 0
  completed_date: None
  status_1: 67
  is_archived: 0
  status_2: 0
  dd_1: None
  status_3: 0
  is_delete: 0
  created_by: 4125
  created_date: 2024-08-09 14:09:18

AND THEN GET THE PROJECT_NUMBER NOW WE LOOK THRU THE FOLLOWING TABLES FOR A MATCHING PROJECT_ID AND THIS IS OUR SAMPLE_DATA

Table: lims_prj_coc_master
  coc_id: 9155
  project_id: 2685
  field_1: Q01-1-None-Nonefsd
  field_2: 
  field_3: 
  field_4: 
  field_5: 
  field_6: 
  field_7: 
  field_8: 
  field_9: 
  field_10: None
  field_11: None
  field_12: None
  comment: 
  collection_date: 2016-09-27 00:00:00
  received_date: 2016-09-28 13:51:27
  status: 0
  dd_1: None
  status_3: 0
  status_4: 0
  status_5: 0
  is_delete: 0
  created_by: 0
  created_date: None
  status_1: None

Table: lims_prj_coc_tests
  coc_test_id: 17651
  project_id: 2685
  coc_id: 9155
  test_id: 46
  result_1: None
  result_2: None
  status_1: None
  comments: None
  version: None
  created_date: 2022-12-19 09:19:07
  created_by: None
  test_date: None
  ppl_1: 0
  is_delete: 0
"""

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)


def get_sample_data(coc_id):
    host = "sparelims.mysql.database.azure.com"
    user = "b564b825520b05"
    #user = "limsadmin@xytovet.com.au"
    password = "cb5a05f1!"
    #password = "admin@1234567"
    database = "geno"

    try:
        # Establish database connection
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        if connection.is_connected():
            print("Connected to db")
            cursor = connection.cursor(dictionary=True)
            
            # Step 1: Get the sample_type_id from the coc_id (renamed to sample_type)
            cursor.execute("""
                SELECT sample_type_id 
                FROM lims_prj_sample_types 
                WHERE sample_type = %s
            """, (coc_id,))
            result = cursor.fetchone()
            if not result:
                return None, "CoC ID not found"
            sample_type_id = result['sample_type_id']
            print(sample_type_id)
            # Step 2: Get the project_ids associated with the sample_type_id
            cursor.execute("""
                SELECT project_id 
                FROM lims_project_master 
                WHERE sample_type_id = %s
            """, (sample_type_id,))

            project_ids = [row['project_id'] for row in cursor.fetchall()]
            #project_ids = project_ids[0]

            print(project_ids)
            print(len(project_ids))
             
            if not project_ids:
                return None, "No project ids found for the given sample type"
            
            # Step 3: Get one sample data for each project_id
            all_sample_data = []
            for project_id in project_ids:
                cursor.execute("""
                    SELECT * 
                    FROM lims_prj_coc_master 
                    WHERE project_id = %s
                    LIMIT 1
                """, (project_id,))
                sample_data = cursor.fetchone()
                
                if sample_data:
                    # Get associated test data
                    cursor.execute("""
                        SELECT * 
                        FROM lims_prj_coc_tests 
                        WHERE project_id = %s AND coc_id = %s
                    """, (project_id, sample_data['coc_id']))
                    test_data = cursor.fetchall()
                    
                    # Combine the data
                    sample_data['tests'] = test_data
                    all_sample_data.append(sample_data)
            
            if not all_sample_data:
                return None, "No sample data found for the associated project numbers"
            
            # Convert the sample data to a DataFrame
            df = pd.DataFrame(all_sample_data)
            
            # Write the data to output.txt
            with open("output.txt", 'w') as f:
                    f.write(f"Sample data for CoC ID: {coc_id}\n\n")
                    f.write("One sample per project:\n\n")
                    for index, row in df.iterrows():
                        f.write(f"Project ID: {row['project_id']}\n")
                        for column, value in row.items():
                            if column != 'tests':
                                # Check if the value is not empty before writing
                                if value is not None and value != '':
                                    f.write(f"{column}: {value}\n")
                        f.write("\nAssociated tests:\n")
                        if row['tests']:
                            for test in row['tests']:
                                # Filter out None or empty string values
                                filtered_test = {k: v for k, v in test.items() if v is not None and v != ''}
                                f.write(json.dumps(filtered_test, indent=2, cls=DateTimeEncoder))
                                f.write("\n")
                        else:
                            f.write("No tests found\n")
                        f.write("\n" + "="*50 + "\n\n")

            return df, "success"
        

    except mysql.connector.Error as error:
        return None, f"Error connecting to MySQL database: {error}"
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def generate_validation_report(sample_data, excel_template_path):
    # Read the Excel template
    excel_df = pd.read_excel(excel_template_path)
    
    # Prepare data for API
    excel_columns = excel_df.columns.tolist()
    sample_columns = sample_data.columns.tolist()
    
    # Convert sample data to a more readable format
    sample_data_dict = sample_data.to_dict(orient='records')
    
    # Prepare the message for GPT
    message_content = f"""
    Compare the following database sample data with the Excel template structure:

    Excel Template Columns:
    {json.dumps(excel_columns, indent=2)}

    Database Sample Data Columns:
    {json.dumps(sample_columns, indent=2)}

    Sample of Database Data (first row):
    {json.dumps(sample_data_dict[0], indent=2, default=str)}

    Please provide a detailed analysis of the data types:
    1. Identify any mismatches in data types between the Excel template and the database sample.
    2. Explain potential issues that could arise from these mismatches.
    3. Suggest appropriate data type conversions or handling methods where necessary.
    4. Comment on any data types that might need special attention (e.g., date formats, numerical precision).

    Format your response as a detailed report suitable for data analysts and developers.
    """

    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=current_app.config['OPENAI_API_KEY'])

    # Make a request to the ChatCompletion API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a data analyst assistant specializing in data validation and comparison."},
            {"role": "user", "content": message_content}
        ]
    )

    # Extract the report from the response
    validation_report = response.choices[0].message.content.strip()

    # Write the report to a file
    with open('validation_report.txt', 'w') as f:
        f.write(validation_report)

    return validation_report

# testing code
# excel_template_path = 'Wrong_line.xlsx'
# sample_data, message = get_sample_data("BovineRequestV2")

# if sample_data is not None:
#    print("Generating validation report...")
#    validation_report = generate_validation_report(sample_data, excel_template_path)
#    print("Validation report has been written to 'validation_report.txt'")
#    print(f"Number of projects found: {len(sample_data)}")
# else:
#    print(f"Error occurred: {message}")
