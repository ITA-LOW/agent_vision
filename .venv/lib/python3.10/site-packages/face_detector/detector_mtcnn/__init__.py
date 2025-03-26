import os
from face_detector.detector_mtcnn import mtcnn_aux as aux
import tensorflow as tf

class MTCNNDetector:

    def __init__(self, model_path, config={}):
        if config is None:
            config = {}

        self.device = '/cpu:0' if 'device' not in config else config['device']
        self.minsize = 10 if 'minsize' not in config else config['minsize']
        self.thresholds = (0.6, 0.7, 0.7) if 'thresholds' not in config else config['thresholds']
        self.factor = 0.709 if 'factor' not in config else config['factor']

        self.graph = tf.Graph()
        self.sess = tf.Session(graph=self.graph)

        with self.graph.as_default():
            with self.sess.as_default():
                with tf.device(self.device):
                    self.pnet, self.rnet, self.onet = aux.create_mtcnn(self.sess,
                                                           model_path)
        self.config = config


    def find_faces(self, img):
        from face_detector import Face, BoundingBox, LandmarkPoint
        faces = []
        with self.graph.as_default():
            with self.sess.as_default():
                with tf.device(self.device):
                    bbs, lndms = aux.detect_face(img, self.minsize, self.pnet, self.rnet,
                                    self.onet, self.thresholds, self.factor, self.graph,
                                    self.sess)
                    for ir in range(bbs.shape[0]):
                        r = bbs[ir]
                        bb = BoundingBox(r[0], r[1], r[2] - r[0], r[3] - r[1])
                        l = lndms[:, ir]
                        landmarks = [LandmarkPoint(l[j], l[j+5]) for j in
                                                   range(5)]
                        faces.append(Face(bb, landmarks))

        return faces
