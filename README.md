# CITS3200 PROJECT - Conversational AI System for Error Checking Submission Forms

## About
This project involves an AI-powered Excel document checker built for Genotyping Australia as part of the CITS3200 project at UWA.

## Prerequisites

The following software should be downloaded prior to installation:
* [Python - 3.12.0](https://www.python.org/downloads/)
* [Node.js](https://nodejs.org/) (for running the React app)

## Installation and Setup

In order to run the flask application you will need to install some pip packages. 

### 1. Python Environment Setup and Package Installation

You have two options for setting up your Python environment:

#### Option A: Using a Virtual Environment (Recommended)

1. Create a virtual environment:
   ```
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`

   Note: You will need to activate the environment whenever you plan to run code within the project.

3. Install packages in the virtual environment:
   ```
   pip install -r requirements.txt
   ```

#### Option B: Installing Packages Globally

If you prefer not to use a virtual environment, you can install the packages globally:

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

Note: Installing packages globally may lead to version conflicts with other Python projects on your system. We generally recommend the virtual environment option but if you're feeling brave feel free to install the packages globally (it will probably be fine). 

### 2. Set up the OpenAI API Key

1. Generate an OpenAI API key:
   - Go to [OpenAI's website](https://platform.openai.com/) and sign up or log in.
   - Navigate to the API section and create a new API key.

2. Create a `.env` file in the root directory of the Flask app.

3. Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   (See the `example.env` file for the correct structure, feel free to just paste your key in here and rename the file to .env)

### 3. Set up and Run the React App

1. Navigate to the React app directory.

2. Install dependencies:
   ```
   npm install
   ```

3. Start the React development server:
   ```
   npm start
   ```
   This will run the app in development mode. Open [http://localhost:3000](http://localhost:3000) to view it in your browser. The page will reload when you make changes.

### 4. Run the Flask Application

In a separate terminal window, navigate to the Flask app directory and run:
```
flask run --debug

```
The API is now running locally on your machine.

## Running Both Apps Simultaneously

We provide a script to start both the React and Flask apps simultaneously:

1. Ensure you're in the project root directory.
2. Run the following command:
   ```
   python start-both-apps.py
   ```

This script will start both the React app and the Flask app. The React app will be able to communicate with the Flask app when both are running locally.

## Usage Notes

- When using the application, you can upload Excel files through the React app interface.
- Processing larger files may take some time. Progress updates will be printed to the terminal running the Flask app.
- If you encounter any issues or have questions, please reach out to anyone in group 46. 

## Deployment

If you want to deploy this project, you'll need to deploy two components:

1. The Flask application that serves the API endpoint.

2. The React web app that provides a user-friendly interface to the API.

Make sure to set up the necessary environment variables, including the OpenAI API key, in your deployment environment.

For any deployment questions or assistance, please contact the group 46, we are happy to deploy the project for you. 

