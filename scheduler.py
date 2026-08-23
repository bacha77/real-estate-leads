import schedule
import time
import subprocess
import os

def run_scraper_pipeline():
    print("=======================================")
    print("[SCHEDULER] Waking up to run daily scraper pipeline...")
    print("=======================================")
    
    # Run the main pipeline
    pipeline_script = os.path.join(os.path.dirname(__file__), "main.py")
    subprocess.run(["python", pipeline_script], check=True)
    
    print("[SCHEDULER] Daily scraper pipeline finished successfully.")
    print("=======================================")

# Schedule the job every day at 2:00 AM
schedule.every().day.at("02:00").do(run_scraper_pipeline)

if __name__ == "__main__":
    print("Starting background scheduler. Waiting until 2:00 AM...")
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60) # Wait one minute before checking the schedule again
