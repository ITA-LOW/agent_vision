import cv2

def detect_face_position(frame):
    """Detecta a posição do rosto na tela dividida em 9 zonas"""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        return None

    (x, y, w, h) = faces[0]

    frame_h, frame_w = frame.shape[:2]
    col = int((x + w / 2) / (frame_w / 3))  
    row = int((y + h / 2) / (frame_h / 3)) 

    mapping = {
        (0, 0): 'up_left', (0, 1): 'up_middle', (0, 2): 'up_right',
        (1, 0): 'middle_left', (1, 1): 'center', (1, 2): 'middle_right',
        (2, 0): 'down_left', (2, 1): 'down_middle', (2, 2): 'down_right'
    }
    position = mapping.get((row, col))
    return position





def detect_face_position_yunet(frame):
    
    model = 'face_detection_yunet_2023mar.onnx'
    input_size = (640, 640)

    face_detector_yunet = cv2.FaceDetectorYN.create(
    model, "", input_size, score_threshold=0.8, nms_threshold=0.3,
    top_k=5000, backend_id=cv2.dnn.DNN_BACKEND_OPENCV, target_id=cv2.dnn.DNN_TARGET_CPU
)

    if frame is None:
        return None

    height, width = frame.shape[:2]
    if height == 0 or width == 0:
         return None

    resized_frame = cv2.resize(frame, input_size)

    face_detector_yunet.setInputSize(input_size)
    faces = face_detector_yunet.detect(resized_frame)

    if faces[1] is None or len(faces[1]) == 0:
        return None

    face = faces[1][0]
    box = face[:4].astype(int)

    x = int(box[0] * width / input_size[0])
    y = int(box[1] * height / input_size[1])
    w = int(box[2] * width / input_size[0])
    h = int(box[3] * height / input_size[1])

    face_center_x = x + w / 2
    face_center_y = y + h / 2

    cell_width = width / 3
    cell_height = height / 3

    col = int(face_center_x // cell_width)
    row = int(face_center_y // cell_height)

    col = max(0, min(col, 2))
    row = max(0, min(row, 2))

    mapping = {
        (0, 0): 'up_left', (0, 1): 'up_middle', (0, 2): 'up_right',
        (1, 0): 'middle_left', (1, 1): 'center', (1, 2): 'middle_right',
        (2, 0): 'down_left', (2, 1): 'down_middle', (2, 2): 'down_right'
    }

    position = mapping.get((row, col))
    return position



