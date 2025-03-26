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
