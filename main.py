# main.py
import subprocess
import sys

sys.path.append("Frontend")

def run_streamlit_app():
    # Define the command to run Streamlit
    # The command is: streamlit run app.py
    command = [sys.executable, "-m", "streamlit", "run", "Frontend/app.py"]
    
    # Use subprocess.Popen to execute the command
    print(f"Starting Streamlit app with command: {' '.join(command)}")
    try:
        # This opens the app in a new process, the main.py script will exit/wait
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print("Error: 'streamlit' command not found. Make sure Streamlit is installed.")
        print("You can install it using: pip install streamlit")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the Streamlit app: {e}")

if __name__ == "__main__":
    run_streamlit_app()
