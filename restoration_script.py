#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime
import pickle

# Dictionary to store directory history
directory_history = {}
history_file = 'directory_history.pkl'

# Load existing history if available
try:
    with open(history_file, 'rb') as f:
        directory_history = pickle.load(f)
except FileNotFoundError:
    directory_history = {}

# Restore function with backup_path as an argument
def restore(backup_path=None):
    all_entries = os.listdir(backup_path)

    # Filter to include only date-formatted directories
    date_directories = [entry for entry in all_entries if entry.count('-') == 2]

    # Convert directory names to datetime objects for sorting
    date_objects = [datetime.strptime(date, "%Y-%m-%d") for date in date_directories]

    # Check for any new dates and find the latest date
    new_dates = [date for date in date_directories if date not in directory_history]
    if not new_dates:
        #print("No new backups to restore.")
        return  # Exit if there's nothing new to restore

    # Find the latest date among the new backups
    latest_date = max(datetime.strptime(date, "%Y-%m-%d") for date in new_dates).strftime("%Y-%m-%d")
    new_path = os.path.join(backup_path, latest_date, "accounts/")

    # Perform the restoration
    if os.path.exists(new_path):
        #print(f"Restoring latest backup for date: {latest_date}")
        new_path_contents = os.listdir(new_path)
        tar_gz_files = [item for item in new_path_contents if item.endswith('.tar.gz')]

        for item in tar_gz_files:
            item_name = item[:-7]  # Remove the '.tar.gz' extension
            backup_file_path = os.path.join(new_path, item)

            # Delete existing account
            command1 = f"sudo /scripts/removeacct {item_name} --force"
            subprocess.run(command1, shell=True)

            # restore backup
            command2 = f"sudo /scripts/restorepkg {backup_file_path}"
            subprocess.run(command2, shell=True)

        # Update the dictionary with the new backup date marked as restored
        directory_history[latest_date] = 'restored'
    else:
        pass
        #print(f"The directory {new_path} does not exist.")

if __name__ == "__main__":
    restore(backup_path="/home/systems/backup/")

    # Save the updated directory history to the file
    with open(history_file, 'wb') as f:
        pickle.dump(directory_history, f)

   ## print("Directory history:", directory_history)



