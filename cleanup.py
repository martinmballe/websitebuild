import os
import time
import logging

# Setup basic configuration for logging
log_path = '/Users/martinballe/DM-Count-1/website/delete.log'
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def cleanup_folder(folder, max_age_in_seconds):
    now = time.time()
    files_deleted = 0
    total_files = 0
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        total_files += 1
        if os.stat(file_path).st_mtime < now - max_age_in_seconds:
            try:
                os.remove(file_path)
                logging.info(f"Deleted {file_path}")
                files_deleted += 1
            except Exception as e:
                logging.error(f"Failed to delete {file_path}: {e}")
        else:
            logging.info(f"Skipped {file_path}, not old enough.")

    logging.info(f"Processed {total_files} files, deleted {files_deleted} files.")

if __name__ == '__main__':
    folder_to_clean_density_maps = '/Users/martinballe/DM-Count-1/website/static/density_maps'  # Absolute path
    folder_to_clean_uploads = '/Users/martinballe/DM-Count-1/website/uploads'  # Absolute path
    cleanup_folder(folder_to_clean_density_maps, 60)
    cleanup_folder(folder_to_clean_uploads, 60)
