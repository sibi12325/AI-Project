from flask import request,request, jsonify
from .modules import csv_converter, error_checker, summarizer, preprocessor
import pandas as pd
from io import StringIO
#
def init_app(app):
    @app.route('/api/analyze', methods=['POST'])
    def analyze():
        print("request received")
        # check if the post request has the file part
        if 'file' not in request.files: return jsonify({'error': 'No file part in the request'}), 400
        file = request.files['file']
        # check if the file is empty
        if file.filename == '': return jsonify({'error': 'No file selected for uploading'}), 400

        # attempt to process the file
        try:
            # get the data and csv from the csv converter
            print("converting file to csv")
            csv_data, coc_id = csv_converter.convert(file)
            # process the data into a readbale format
            print("processing file")
            processed_data = preprocessor.process(csv_data)
            # errors will be a string with mark down formatting , white space errors will be either a list of strings with the white space indexe's or None 
            print("checking for errors")
            headers, errors, white_space = error_checker.check(coc_id, processed_data)
            # either a list of strings with the white space indexe's or None 
            print("summarizing file")
            summary = summarizer.summarize(processed_data, errors)
            # read the csv data into a data frame

            # Count the number of data rows 
            data_rows = len(processed_data.split('\n')) - 1 

            data_summary = {
                # number of rows in the data
                'num_rows': data_rows,
                # number of columns in the data
                'num_columns': len(headers),
                # list of column names
                'column_names': headers,
                # dictionary of data types
                'data_types': {header: str(type(header)) for header in headers}
            }
            print("returning response")
            
            response = {
                # integer
                'coc_id': coc_id,
                # markdown formatted string
                'summary': summary,
                # markdown formatted string
                'errors': errors,
                # object with the following keys, num_rows, num_columns, column_names, data_types all of which are integers except for data_types which is an object
                'data_summary': data_summary,
                # string probably dont return
                'processed_data': processed_data, 
                # either a list of strings with the white space indexe's or a empty list 
                'white_space': white_space
            }
            # return the response
            return jsonify(response), 200
        
        # if an error occurs return the error message
        except Exception as e: 
            print(e)
            return jsonify({'error': str(e)}), 500
