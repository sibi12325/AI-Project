import subprocess
import os
import sys
from concurrent.futures import ThreadPoolExecutor

def run_command(command, cwd=None):
    # Execute the given command in a subprocess and stream the output in real-time
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,  # Capture standard output
        stderr=subprocess.STDOUT,  # Redirect standard error to standard output
        text=True,  # Ensure the output is returned as text, not bytes
        shell=True,  # Run the command through the shell
        cwd=cwd  # Set the working directory, if provided
    )
    
    # Stream and print each line of the process output as it arrives
    for line in process.stdout:
        print(line, end='')  # Print the line without adding extra newlines
        sys.stdout.flush()  # Ensure the output is flushed immediately
        
        # Check for specific output patterns to provide user feedback
        if "Compiled successfully" in line or "Running on" in line:
            # If the output contains a URL for localhost, print a startup link
            if "localhost" in line:
                print(f"\nStartup link: {line.split('http://')[1].strip()}")
            elif "Compiled successfully" in line:
                # Notify the user when the frontend has successfully compiled
                print("\nFrontend is running. Check the console output above for the exact URL.")
    
    process.wait()  # Wait for the process to complete
    # If the process exits with a non-zero status, print an error message
    if process.returncode != 0:
        print(f"Error: {command} exited with status {process.returncode}")

def start_frontend():
    # Set the working directory to the frontend folder and run the frontend command
    frontend_path = os.path.join(os.getcwd(), 'frontend')
    run_command("npm start", cwd=frontend_path)

def start_backend():
    # Set the working directory to the backend folder and run the backend command
    backend_path = os.path.join(os.getcwd(), 'flask')
    run_command("flask run --debug", cwd=backend_path)

if __name__ == "__main__":
    print("Starting frontend and backend servers...")
    
    # Use ThreadPoolExecutor to run frontend and backend servers in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        frontend_future = executor.submit(start_frontend)  # Start the frontend in a separate thread
        backend_future = executor.submit(start_backend)  # Start the backend in another thread
        
        # Wait for both servers to finish running
        frontend_future.result()
        backend_future.result()
    
    print("Servers have been stopped.")  # Notify the user when both servers stop
