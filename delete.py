import os
import time

def delete_old_files(directory, age_in_seconds):
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return

    current_time = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > age_in_seconds:
                os.remove(file_path)
                print(f"Deleted {file_path}")

if __name__ == "__main__":
    # Change to the directory the script is supposed to run from
    os.chdir('/users/martinballe/DM-Count-1/website')
    
    upload_folder = 'uploads'  # Now this path is relative to the directory set above
    max_file_age = 3600  # seconds, e.g., 1 hour

    delete_old_files(upload_folder, max_file_age)
