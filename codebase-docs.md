# Genotyping Australia - Conversational AI System for Error Checking Submission Forms

## 1. Project Overview

Our AI-driven Submission Form Error Detection System is designed to simplify and streamline the data submission process for genetic analysis. This project utilises an AI model to help identify, categorise and report errors in submission forms - thus reducing time taken for manual data review and improving data quality, reliability as well as efficiency.

It aims to minimise data entry errors


## 2. System Architecture

### 2.1 Backend (Flask)

#### 2.1.1 Directory Structure

```
├── flask
│   ├── README.md
│   ├── __pycache__
│   ├── app
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
```

#### 2.1.2 Key Components

- `app/__init__.py`
- `app/routes.py`
- `config.py`
- `run.py`

#### 2.1.3 API Endpoints

- `/api/analyze` (POST)
- `/analyze` (GET, POST)

#### 2.1.4 Custom Modules

- `csv_converter`
- `preprocessor`
- `error_checker`
- `summarizer`

### 2.2 Frontend (React)

#### 2.2.1 Directory Structure

```
├── frontend
│   ├── README.md
│   ├── node_modules
│   ├── package-lock.json
│   ├── package.json
│   ├── public
│   └── src
```

#### 2.2.2 Key Components

- `App.js`
- `AnimatedFileUpload.js`
- `AnimatedResults.js`
- `DataVisualization.js`
- `ThemeSwitcher.js`
- `BackgroundAnimation.js`
- `ParticleEffect.js`


## 3. API Documentation

### 3.1 /api/analyze
Method: POST
Description: Used to analyse submitted data for errors

### 3.2 /analyze
Methods: GET,POST
Description: Provides both retrieval of analysis params (GET), and submission of data for analysis (POST)


## 4. Frontend Components

### 4.1 App

The main container for the genotyping Aus web-app. Manages main features of app, and acts as container for other components.

Returns: 

Renders entire app UI, including:
- ThemeProvidert for consistent styling
- BackgroundAnimation & particleEffect for visual enhancement
- AnimatedFileUpload for file input
- ProgressIndicator for visual upload progress/feedback
- AnimatedResults to display analysis results
- DataVisualisation for data representation
- ThemeSwitcher to toggle light/dark mode


### 4.2 AnimatedFileUpload
Provides interface to upload Excel files (via drop or select file).

Props:
 `OnFileSelect (Function)`: Triggered when file selected/dropped. Receives selected file  as arg.

Returns:
drop zone & file selection button for file upload


### 4.3 AnimatedResults
Displays analysis results from uploaded file.

Props:
- `results (object)`: contains summary, errors & data summary for uploaded file. Errors are array of error messages


Returns:
View of analysis results:
- Summary of analysis
- Data summary statistics
- Error reporting with Material UI icons as indicators

* Rendering based on existence of errors (either list of errors/sucess message)


### 4.4 BackgroundAnimation
Adds animated background effect to application. (Via radial gradients & animation based on light/dark mode)

Props:
`darkMode(boolean)`: Indicate whether app is in dark mode.

Returns:
Animated background with CSS animations.

### 4.4 ParticleEffect
Creates canvas based particle animation overlay.

Returns:
Canvas element with animated particles

## 5. Backend Modules

### 5.1 csv_converter
Converts Excel files to CSV format. Only processes specific columns and rows.

Function: `convert(file)`

Parameters: 
- file(file object): Uploaded excel file

Returns: 
csv_data(str): CSV string containing converted data
coc_ID(str): CoC ID extracted from Excel file

### 5.2 preprocessor
Preprocesses CSV data for further analysis, by removing invalid data.

Function: `process(csv_data)` 

Parameters:
csv_data(str): CSV string to be processed

Returns:
processed_data(str): Processed CSV string


### 5.3 error_checker
Checks for errors in submitted data and ensure criteria is met, by comparing against template and using AI-based analysis.

Function:`check(coc, real_data)`

Parameters:
coc(str):  Comma separated string which contains the COC(Chain of command) information
real_data(str): Data that user submits

Returns:
validation_report(str): Report of validation erros generated by AI model
whiteSpaceErrors(list): list of whitespace errors detected in data


Function: `whitespace_check(organisedData)`

Parameters:
organisedData(dict): Dictionary containing organised data

Returns:
errors(list): list of whitespace erros detected


Function: `organizeData(document,error,headings)`

Parameters:
document(str): Raw text data
Errors(list): List to store erros found during the organising process
headings(list): List of expected headings

Returns:
dictionary(dict): organised data in dictionary format
index(int): index where the data starts (after the headers)


### 5.4 summarizer
Generates summary of errors found in submission form using AI model.

Function: `summarise(data,errors,corrected_data=None)`

Parameters:
data(str): Submission form data
errors(str): errors found in data
corrected_data(list(optional)): corrected data

Returns:
If corrected_data not provided:
    summary(str): HTML formattyed summary of errors

If corrected_data provided:
    summary(str): HTML formattyed summary of errors
    corrected_csv(str): CSV string of corrected data

## 6. Configuration

### 6.1 Environment Variables
FLASK_ENV: set to development for local development, production for production deployment
OPEN_AI_API_KEY: OpenAI API key for accessing GPT model(s)


### 6.2 Theme Configuration
Material-UI utilised. To modify:
- Go to frontend/src/App.js
- Find createTheme function
- Modify as needed


## 7. Deployment
Backend
- We recommend AWS to deploy Flask app

Frontend
- Build using npm start/npm run build


## 8. Maintenance and Support
To ensure reliability of this app in the long term, consider:
- Regular updates: keep all dependencies up to date (Python + npm modules)
- Keep documentation up to date
- Implement backups of your data


## 9. Installation Guide



# for deployment 

Hey Mark,

If you like the project and want to deploy it you'll have to deploy two things 1. The flask application that serves the api endpoint and 2. The react web-app that allows an easy endpoint to the api.

You will also have to create a .env file for the flask application (see the example.env file for the correct structure) with your open-ai key that will allow you to use the open-ai api. Please see the [openai docs](https://platform.openai.com/docs/api-reference/authentication).

Any questions feel free to reach out.
