# # # A set containing all the indexes where the whole row is blank
# blanksSet = None
import mysql.connector
import pandas as pd
import json
from datetime import datetime 
from openpyxl import load_workbook
import numpy as np
from openai import OpenAI
from flask import current_app
import os

# # # The index at which the data starts (after headers)
# index = None

# # Main error checking function
def check(coc, real_data):

    cwd = os.path.abspath(os.path.dirname(__file__))
    os.chdir(cwd)

    # Read the Excel template
    coc = coc.split(",")
    coc = coc[0]
    file_path = f"{cwd}/cocs/{coc}"
    
    sample_data = ""
    try:
        # Open the file using a relative path
        with open(file_path, 'r') as file:
            # Read the entire contents of the file into a string
            sample_data = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except IOError as e:
        print(f"Error reading the file: {e}")
        return None

        
    # Prepare data for API
    sample_data = sample_data.split('/')
    # Get the headings and data from the sample data    
    headings = sample_data[0].strip().split('|')

    data = []

    for entry in sample_data[1].strip().split('@'):
        data.append(entry.strip().split('|'))

    # Gets the index of where headers start
    organizedData, index = organizeData(real_data, [], headings)
    whiteSpaceErrors = whitespace_check(organizedData)
    lines = real_data.split('\n')
    new_data = lines[index:]

    real_data = []
    for line in new_data:
        lineList = line.strip().split(',')

        fixedLine = []
        for data in lineList:
            if data == '':
                fixedLine.append("_")
            else:
                fixedLine.append(data.strip())
        
        if len(fixedLine) > 1:
            real_data.append(fixedLine)


    # Convert sample data to a more readable format    
    # Prepare the message for GPT
    message_content = f"""
    A submission form has the following headings : {headings}. 
    Each heading expects data of the format {data}. The data is a 2d list of format list[line number][column].
    A user entered the following data {real_data}. 
    The data is a 2d list of format list[line number][column]. The order of the columns and data matches the sample data. 
    List all format errors based on the sample data i gave you including the field and line number which is incorrect. (Assume line numbers start from {index} instead of 1)
    Report all _ as missing data else report as format error.
    You should check for every field.
    If errors come consecutively report them in ranges
    Format your response in markdown.
    """

    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=current_app.config['OPENAI_API_KEY'])

    # Make a request to the ChatCompletion API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a machine learning ai that detects errors in submission forms."},
            {"role": "user", "content": message_content}
        ]
    )

    # Extract the report from the response
    validation_report = response.choices[0].message.content.strip()

    return headings, validation_report, whiteSpaceErrors


def whitespace_check(organizedData):

    errors = []

    # # Find errors for each header
    for header in organizedData:

        # # Lists for each error
        whiteSpaceList = []

        # # contains all of the data for a given header (key)
        currentList = organizedData[header]

        n = len(currentList)

        # # Iterate through each list mapped by the header.
        for i in range(0,n):

            dataEntry = currentList[i]
            lineNumber = i + 1 + index

            # # If data entry contains whitespace add to respective list
            if dataEntry != dataEntry.strip():
                whiteSpaceList.append(lineNumber)

        # # Add each range of issues to the errors list
        addToErrors(whiteSpaceList, errors, n, header, "whitespace")
    

    return errors


# # Function to organize the raw text into a dictionary
def organizeData(document, errors, headings):

    # # Populate these global variables
    global index, blanksSet

    # # Create a list storing each line of text
    lines = document.split('\n')

    # # The expected headers in the document
    keys = headings

    # # Convert to a set to find and compare with the headers in the document
    expectedHeaders = set(keys)

    # # Find the index at which the headers start
    index = 0
    for line in lines:
        lineList = line.strip().split(',')
        potentialHeaders = set(lineList)

        # # Check for any overlap (at least one of the elements in the current set matches the headers set)
        if bool(expectedHeaders & potentialHeaders):
            break

        index += 1

    # # Increment to set index to when data starts (1 after headers)
    index += 1

    # # If the index is not what is expected add to errors
    headersExist = True
    if index == len(lines):
        errors.append("Headers were not listed")
        headersExist = False
    elif index != 19:
        errors.append(f"The headers start on the wrong line (line {index} instead of 19)")

    # # If the headers match the data to it
    if headersExist:

        # # Compare the headers found with the headers expected
        headers = lines[index - 1].strip().split(',')
        headers = set(headers)

        differences = expectedHeaders - headers

        if len(differences) > 0:
            for missingHeader in differences:
                errors.append(f"Missing header {missingHeader}")


        # # After getting keys, start reading the lines after the keys (the data)
        lines = lines[index:]

        # # Use dictionary to organize data. The keys are the headers (eg sample id) and the data is its corresponding value in the excel sheet
        dictionary = {}

        # # Lists to keep track of when whole row is blank (excluding final rows when blanks are repeated until end of file)
        consecutiveBlanksList = []
        consecutiveBlanks = []

        # # Initialize the dictionary by mapping empty lists to each header
        for key in keys:
            dictionary.update({ key : [] })

        # # The row number currently on
        row = index

        # # Append each data entry to the list mapped by the header
        for line in lines:
            lineList = line.strip('\r').split(',')

            # # Increment row count in each iteration
            row += 1

            # # If the whole row is empty then add to list and skip this iteration
            if all(item == '' for item in lineList):
                consecutiveBlanks.append(row)
            else:
                # # When next non blank row is found then submit the the previously noted blanks to final blanks list and reset (to avoid including the repeating end lines at end of file)
                consecutiveBlanksList.append(consecutiveBlanks)
                consecutiveBlanks = []

            # # If length is one then end of data is reached
            if len(lineList) > 1:

                # # The indexing for the headers and their data are the same
                for i in range(0,len(lineList)):
                    currentKey = keys[i]
                    currentTxt = lineList[i].strip('\r')
                    dictionary[currentKey].append(currentTxt)

        blanksSet = set()

        # # Add the blank rows to the errors
        for blankList in consecutiveBlanksList:

            n = len(blankList)

            # # Only consider non empty lists (empty lists are considering the blanks at the end of the sheet)
            if(n != 0):

                # # Add the blanks to a set to prevent stating same info twice when finding ranges for individual missing data later
                for blank in blankList:
                    blanksSet.add(blank)

                if n == 1:
                    errors.append(f"Row {blankList[0]} is empty.")
                else:
                    errors.append(f"Rows {blankList[0]} to {blankList[n - 1]} is empty.")

    else:
        errors.append(f"Cannot check data due to missing headers")

    return dictionary,index


def getRangeErrorMessage(rangeStart, rangeEnd, issue, n, key):

    # # Add any remaining ranges for issue at the end
    if rangeStart is not None:

        # # Case when the error message for whole row being blank already covered this range
        while rangeStart in blanksSet:
            rangeStart += 1

        while rangeEnd in blanksSet:
            rangeEnd -= 1

        if rangeEnd < rangeStart:
            return None

        # # If non consecutive (only one element in the range)
        if rangeStart == rangeEnd:
            return (f"Column '{key}' has {issue} at line {rangeStart}.")

        # # If every data was blank
        elif (rangeEnd - rangeStart + 1) == n:
            return (f"Column '{key}' has {issue} on every line.")

        # # Regular range case
        else:
            if rangeEnd == n + index:
                return (f"Column '{key}' has {issue} from lines {rangeStart} onwards.")

            return (f"Column '{key}' has {issue} from lines {rangeStart} to {rangeEnd}.")

# # Function to convert a list of errors into a list containing ranges of the errors (for when same errors are made consecutively)
def convertToRange(list):

    # # Initial conditions
    start, end = None, None
    prev = None
    ranges = []

    for val in list:
        # # Initial case when start has no value
        if start == None:
            start = val

        # # Either the end has no value or is consecutive when compared to current value
        if end is None or end == val - 1:
            end = val

        # # If it was not consecutive then initialise start/end to the new range and append the old range to errors list
        else:
            ranges.append([start, end])
            prev = val
            start, end = prev, val

    # # Append the last range
    ranges.append([start, end])

    return ranges

# # Function to iterate through each range of a given issue and add it to errors
def addToErrors(errorList, errors, n, header, issue):

    # # Assuming errors exist
    if len(errorList) > 0:

        # # Convert into a list containing ranges of errors
        ranges = convertToRange(errorList)

        # # Get the error message for the respective range and add it to errors
        for currentRange in ranges:
            start = currentRange[0]
            end = currentRange[1]
            error = getRangeErrorMessage(start, end, issue, n, header)
            if error is not None:
                errors.append(error)



