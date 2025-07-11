import os
import shutil

# Define the source parent directory containing vehicle data folders
source_dir = './25 Vehicles of Jeddah/25 Vehicles of Jeddah'

# Define the destination directory where the renamed driver folders will be copied
destination_dir = './Driver_Faces'
# print("HEllo", os.listdir(source_dir))
# Initialize driver counter
driver_counter = 1

def safe_move(imageName, src, dst):
    
    temp = ''
    # Keep modifying the destination path until it doesn't exist
    if os.path.exists(os.path.join(dst, imageName)):
        base, ext = os.path.splitext(imageName)
        print(f"Moving ", src, dst)
        temp = f"{base}_copy{ext}"

    shutil.copy(src, os.path.join(dst, temp))
    print(f"Moved to: {dst}")
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
                # Define the new driver folder name (d1, d2, d3, d4, ...)
                new_driver_name = f'd{driver_counter}'
                
                # Define the destination path for the new driver folder
                new_driver_folder_path = os.path.join(destination_dir, new_driver_name)
                if not os.path.exists(new_driver_folder_path):
                    os.makedirs(new_driver_folder_path)
                for subfolder in os.listdir(driver_folder_path):
                    # print(f"New image Path {os.path.join(driver_folder_path,subfolder)} {os.listdir(os.path.join(driver_folder_path,subfolder))}")
                    for image in os.listdir(os.path.join(driver_folder_path,subfolder)):
                        print(f"Processing image: {image} in {subfolder}")
                        # Move the image file to the destination folder
                        safe_move(image, os.path.join(driver_folder_path,subfolder,image), new_driver_folder_path)
                # Copy the driver folder to the destination and rename it
                # shutil.copytree(driver_folder_path, new_driver_folder_path)
                
                # Check if the driver folder is empty after moving images
                if os.path.exists(new_driver_folder_path) and not os.listdir(new_driver_folder_path): # Check if directory is empty
                    shutil.rmtree(new_driver_folder_path)  # Remove the empty driver folder
                    print(f"Deleted empty folder {new_driver_folder_path}")
                else:   
                    print(f"Copied and renamed {driver_folder} to {new_driver_name}")
                        
                    # Increment the driver counter for the next folder
                    driver_counter += 1
