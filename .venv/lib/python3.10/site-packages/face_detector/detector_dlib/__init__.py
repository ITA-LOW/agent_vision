import dlib
import cv2
from typing import List
import face_detector as fd

class DlibDetector:

    def __init__(self, model_addr, config=None):
        self.model_addr = model_addr
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.model_addr)
        self.config = config

    def find_faces(self, img) -> List[fd.Face]:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 0)
        faces = []

        for rect in rects:
            bb = fd.BoundingBox(rect.left(), rect.top(), rect.right()
                                - rect.left(), rect.bottom() - rect.top())
            landmarks = [fd.LandmarkPoint(l.x, l.y) for l in self.predictor(gray,
                                                                        rect).parts()]
            face = fd.Face(bb, landmarks)
            faces.append(face)

        return faces
