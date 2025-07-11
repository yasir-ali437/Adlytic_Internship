import os
import shutil
from glob import glob

# Define the source parent directory containing vehicle data folders
source_dir = './25 Vehicles of Jeddah/25 Vehicles of Jeddah'

# Define the destination directory where all the images will be combined
destination_dir = './Driver_FacesCombined'

# Ensure destination folder exists
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Initialize a driver counter for renaming the driver folders as d1, d2, d3, ...
driver_counter = 1

# Loop through each folder in the source directory
for vehicle_folder in os.listdir(source_dir):
    vehicle_folder_path = os.path.join(source_dir, vehicle_folder)
    
    # Ensure that it is a directory
    if os.path.isdir(vehicle_folder_path):
        # Loop through each driver folder (d1, d2, d3)
        for driver_folder in ['d1', 'd2', 'd3']:
            driver_folder_path = os.path.join(vehicle_folder_path, driver_folder)
            
            # Check if the driver folder exists
            if os.path.exists(driver_folder_path):
                # Collect all image files in the current driver folder (assuming images are .jpg, .jpeg, .png, etc.)
                image_files = glob(os.path.join(driver_folder_path, '*.[pj]*[np]*[g]*'))  # Searching for jpg, jpeg, png
                
                print("HERE", image_files)
                # Move each image to the destination directory
                for image_file in image_files:
                    # Construct destination path for the image
                    dest_image_path = os.path.join(destination_dir, os.path.basename(image_file))
                    
                    # Move the image file to the destination folder
                    shutil.move(image_file, dest_image_path)
                    print(f"Moved image {os.path.basename(image_file)} to {destination_dir}")
                
                # Check if the driver folder is empty after moving images
                if not os.listdir(driver_folder_path):  # Check if directory is empty
                    shutil.rmtree(driver_folder_path)  # Remove the empty driver folder
                    print(f"Deleted empty folder {driver_folder_path}")
                
                # Increment the driver counter for the next driver folder
                driver_counter += 1
