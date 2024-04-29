import cv2
import face_recognition
import numpy as np
from time_name import add_timestamp_to_filename
import requests

def upload_to_imgbb(local_file_path):
    """Upload a file to ImgBB and return the image URL."""
    imgbb_url = "https://api.imgbb.com/1/upload"
    
    with open(local_file_path, "rb") as file:
        files = {"image": file.read()}
    
    params = {
        "key": "3ef7a65ad760fc2ee669178e7e26399b",
    }
    
    response = requests.post(imgbb_url, params=params, files=files)
    
    if response.status_code == 200:
        img_url = response.json()["data"]["url"]
        print(f"File uploaded to ImgBB. Image URL: {img_url}")
        return img_url
    else:
        print(f"Failed to upload file to ImgBB. Status Code: {response.status_code}")
        return None

def object_detect(image_x):
    # Load image
    image = cv2.imread(image_x)

    # Check if image loaded successfully
    if image is not None:
        height, width = image.shape[:2]

        # D:\ThaiArgorlink+\Argorlink_model\20240204_08_37_21_0.3931

        # Load YOLO model and class names
        net = cv2.dnn.readNet('D:\\sanbot_final\\pythonbackend\\model\\yolov3.cfg', 'D:\\sanbot_final\\pythonbackend\\model\\yolov3.weights')
        with open('D:\\sanbot_final\\pythonbackend\\model\\coco.names', 'r') as f:
            classes = f.read().strip().split('\n')

        # Preprocess image
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)

        # Set input and get output layer names
        net.setInput(blob)
        layer_names = net.getLayerNames()
        if cv2.__version__.startswith('4'):
            output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        else:
            output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        # Forward pass and process detections
        outs = net.forward(output_layers)
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.6:  # Adjust confidence threshold as needed
                    # Calculate coordinates
                    center_x, center_y, w, h = int(detection[0] * width), int(detection[1] * height), int(
                        detection[2] * width), int(detection[3] * height)
                    x, y = center_x - w // 2, center_y - h // 2
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Apply Non-Maximum Suppression
        indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.6, nms_threshold=0.5)

        # Initialize label variable
        label = ""

        # Visualize detected objects
        if len(indices) > 0:
            for i in indices.flatten():
                box = boxes[i]
                x, y, w, h = box
                class_id = class_ids[i]
                label = f'{classes[class_id]}: {confidences[i]:.2f}'
                color = (0, 255, 0)  # Green box
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
        original_filename = f"D:\\sanbot_final\\pythonbackend\\result\\{add_timestamp_to_filename('result.jpg')}" 
        cv2.imwrite(original_filename, image)
        return upload_to_imgbb(original_filename) , label

    else:
        print("Error: Unable to load the image.")

def face_reco(known_faces_paths, known_names, unknown_image_path):
    # Load known face encodings and names
    known_face_encodings = [face_recognition.face_encodings(face_recognition.load_image_file(face_path))[0] for face_path in known_faces_paths]

    # Load the image for face recognition
    unknown_image = cv2.imread(unknown_image_path)
    unknown_image_rgb = cv2.cvtColor(unknown_image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

    # Find face locations and encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image_rgb)
    face_encodings = face_recognition.face_encodings(unknown_image_rgb, face_locations)

    # Initialize an array for face names
    face_names = []

    # Compare each face found in the unknown image with the known faces
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # If a match is found, set the name to the known face name
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]

        face_names.append(name)

    # Draw rectangles and write names on the image
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        cv2.rectangle(unknown_image, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(unknown_image, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

    # D:\\sanbot_final\\pythonbackend\\result\\{add_timestamp_to_filename('result.jpg')}
    original_filename = f"D:\\sanbot_final\\pythonbackend\\result\\{add_timestamp_to_filename('result.jpg')}" 
    cv2.imwrite(original_filename, unknown_image)

    return upload_to_imgbb(original_filename), face_names

# value 
'''
# Example usage
known_faces_paths = [
    "D:\\sanbot_final\\facereco\\WIN_20240201_18_31_53_Pro.jpg",
    "D:\\sanbot_final\\facereco\\ambutakam.jpg"
]

known_names = [
    "gay",
    "ambutakam"
]

unknown_image_path = "D:\\sanbot_final\\facereco\\ambutakam.jpg"

'''

# face 
'''
detected_name, detected_names = face_reco(known_faces_paths, known_names, unknown_image_path)
print(detected_name, detected_names[0])
'''

# obj
'''
obj_detected_name, obj_detected_names = object_detect('D:\\sanbot_final\\facereco\\WIN_20240417_19_11_56_Pro.jpg')
print(obj_detected_name, obj_detected_names)
'''