import cv2
import face_recognition
import pickle

def recognize_driver(image_path, encoding_file='normal_driver_encodings.pkl'):
    # Load encodings
    with open(encoding_file, 'rb') as f:
        data = pickle.load(f)
    
    known_encodings = data['encodings']
    known_names = data['names']

    # Load and encode input image
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image, model='cnn')  # Use 'cnn' for better accuracy with larger images
    face_encodings = face_recognition.face_encodings(image, face_locations)

    if not face_encodings:
        print("No face found in input image.")
        return None

    input_encoding = face_encodings[0]
    matches = face_recognition.compare_faces(known_encodings, input_encoding)
    face_distances = face_recognition.face_distance(known_encodings, input_encoding)

    if matches:
        best_match_index = face_distances.argmin()
        if matches[best_match_index]:
            matched_name = known_names[best_match_index]
            print(f"Driver identified as: {matched_name}")
            return matched_name
    print("Driver not recognized.")
    return None

def select_best_frame(video_path, every_n_frames=5, cnnflag=False):
    video = cv2.VideoCapture(video_path)

    best_frame = None
    best_score = 0
    frame_count = 0

    while True:
        ret, frame = video.read()
        if not ret:
            break

        if frame_count % every_n_frames == 0:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # cv2.imwrite('best_frame1.jpg', frame)
            if cnnflag:
                face_locations = face_recognition.face_locations(rgb_frame, model='cnn')
            else:
                face_locations = face_recognition.face_locations(rgb_frame)
                
            face_landmarks = face_recognition.face_landmarks(rgb_frame)
            # print("face_locations", face_locations, "face_landmarks", face_landmarks)
            # Basic scoring: face must exist + have eyes & nose
            if face_locations and face_landmarks:
                landmarks = face_landmarks[0]
                score = 0
                if 'left_eye' in landmarks: score += 1
                if 'right_eye' in landmarks: score += 1
                if 'nose_tip' in landmarks: score += 1
                if 'chin' in landmarks: score += 1
                if 'top_lip' in landmarks: score += 0.5
                if 'bottom_lip' in landmarks: score += 0.5

                if score >= best_score:
                    best_score = score
                    best_frame = frame.copy()
                    
            elif face_locations and face_landmarks==[]:
                best_frame = frame.copy()
                
            # elif face_locations==[] and face_landmarks==[]:
            #     print("Running again with CNN model....")
            #     select_best_frame(video_path, every_n_frames, cnnflag=True)
                
        frame_count += 1

    video.release()
    if best_frame is None:
        print("No suitable frame found.")
        print("Running again with CNN model....")
        select_best_frame(video_path, every_n_frames, cnnflag=True)
    
    cv2.imwrite('best_frame.jpg', best_frame)

select_best_frame(r"D:\Adlytic\Data\Evidence-20250708T065102Z-1-001\Evidence\3309326.mp4")
recognize_driver('best_frame.jpg')
