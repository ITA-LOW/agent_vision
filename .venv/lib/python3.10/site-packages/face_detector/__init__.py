import numpy as np
from functools import partial
import os
from typing import List
import cv2


class BoundingBox:

    def __init__(self, x: float, y: float, w: float, h: float):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Face:

    def __init__(self, bounding_box: BoundingBox, landmarks: dict=None):
        self.bounding_box = bounding_box
        self.landmarks = landmarks


class FaceDetector:

    def __init__(self, technique: str='mtcnn', model_addr: str=None, config: dict=None):
        from detector_dlib import DlibDetector
        from detector_mtcnn import MTCNNDetector
        self.techniques = {'mtcnn': partial(MTCNNDetector, 'data/mtcnn' if model_addr is
                                                        None else
                                                         model_addr, config),
                                   'dlib_68': partial(DlibDetector,
                                                    'data/shape_predictor_68_face_landmarks.dat',
                                                   config),
                                   'dlib_5': partial(DlibDetector,
                                                   'data/shape_predictor_5_face_landmarks.dat',
                                                  config)}

        if technique not in self.techniques:
            technique = list(self.techniques.keys())[0]

        self.detector = self.techniques[technique]()
        self.config = config
        self.technique = technique
        self.model_addr = model_addr

    def find_one_face(self, img) -> Face:
        noface = Face(BoundingBox(0,0,0,0), [])
        faces = self.detector.find_faces(img)
        bb_f = np.array([(f.bounding_box.x, f.bounding_box.y, f.bounding_box.w,
                          f.bounding_box.h) for f in faces])
        number_of_faces = np.shape(faces)[0]
        img_size = np.asarray(img.shape)[0:2]
        if number_of_faces > 0:
            if number_of_faces == 1:
                return faces[0]

            bounding_box_size = (bb_f[:,2]-bb_f[:,0])*(bb_f[:,3]-bb_f[:,1])
            img_center = img_size / 2
            offsets = np.vstack([ (bb_f[:,0]+bb_f[:,2])/2-img_center[1], (bb_f[:,1]+bb_f[:,3])/2-img_center[0] ])
            offset_dist_squared = np.sum(np.power(offsets,2.0),0)
            index = np.argmax(bounding_box_size-offset_dist_squared*2.0)
            return faces[index].bounding_box

        return noface

    def get_faces(self, img_addr) -> List[Face]:
        if not os.path.exists(img_addr):
            return []

        img = cv2.imread(img_addr)
        return self.detector.find_faces(img)


class LandmarkPoint:

    def __init__(self, x, y):
        self.x = x
        self.y = y


if __name__ == "__main__":
    img_addr = "/home/neo/dev/datasets/lfw/Yasser_Arafat/Yasser_Arafat_0003.jpg"
    #img_addr = "/home/neo/dev/datasets/lfw/Valentino_Rossi/Valentino_Rossi_0001.jpg"
    img = cv2.imread(img_addr)

    fa = FaceDetector('fl_5')
    faces = fa.get_faces(img_addr)

    for f in faces:
        bb = f.bounding_box
        lands = f.landmarks
        cv2.rectangle(img, (int(bb.x), int(bb.y)), (int(bb.x + bb.w),
                                                    int(bb.y+bb.h)), (0,255,0), 1)
        for l in lands:
            cv2.circle(img, (l.x, l.y), 2, (0,0,255))

        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
