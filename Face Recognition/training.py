import os
import face_recognition
import pickle
import cv2

def train_face_encodings(dataset_path="D:\Adlytic\Face Recognition\Driver_Faces", encoding_file='CNN_driver_encodings.pkl'):
    known_encodings = []
    known_names = []

    for driver_name in os.listdir(dataset_path):
        driver_folder = os.path.join(dataset_path, driver_name)
        if not os.path.isdir(driver_folder):
            continue
        
        print(f"Processing: {driver_name}")
        for image_file in os.listdir(driver_folder):
            image_path = os.path.join(driver_folder, image_file)
            
            # Load full image with OpenCV
            image_bgr = cv2.imread(image_path)
            
            # Get image dimensions
            height, width, _ = image_bgr.shape
            mid = width // 2

            # Crop left half
            left_half = image_bgr[:, :mid]

            # Convert to RGB (face_recognition uses RGB)
            image_rgb = cv2.cvtColor(left_half, cv2.COLOR_BGR2RGB)
    
            # image = face_recognition.load_image_file(image_path)

            face_locations = face_recognition.face_locations(image_rgb, model='cnn')  # Use 'cnn' for better accuracy with larger images
            encodings = face_recognition.face_encodings(image_rgb, face_locations)

            if encodings:
                for enc in encodings:
                    known_encodings.append(enc)
                    known_names.append(driver_name)
                print(f"✓ Encoded from {image_file}")
            else:
                print(f"✗ No face found in {image_file}")

    # Save to file
    with open(encoding_file, 'wb') as f:
        pickle.dump({'encodings': known_encodings, 'names': known_names}, f)

    print("✅ All driver encodings saved.")


train_face_encodings()