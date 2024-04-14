import os
import time

def delete_old_files(directory, age_in_seconds):
    current_time = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > age_in_seconds:
                try:
                    os.remove(file_path)
                    print(f"Deleted {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

if __name__ == "__main__":
    upload_folder = 'uploads'  # Adjust as needed
    static_folder = 'static'   # Adjust as needed
    max_file_age = 3600        # Files older than 1 hour

    delete_old_files(upload_folder, max_file_age)
    delete_old_files(static_folder, max_file_age)
