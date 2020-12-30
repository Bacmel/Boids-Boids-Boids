from time import localtime, strftime

import cv2
from cv2 import VideoWriter, VideoWriter_fourcc as FourCC
import numpy as np

from src import OUT_DIR, BOID_NOSE_LEN

class Canvas:
    def __init__(self, res, border, dt, render):
        # output related
        self.res = np.array(res, dtype="int")
        self.fps = float(1/dt)
        self.origin = border.origin
        self.shape = border.length
        self.render = render
        self.ratio = np.min(np.multiply(self.res, 1/(self.shape+2*BOID_NOSE_LEN)))

        # A verifier
        self.current_frame = self.new_frame()

        # renderer
        if self.render :
            self.filename = OUT_DIR + strftime("%Y%m%dT%H%M%S", localtime()) + ".mp4"
            self.video = VideoWriter(
                self.filename, FourCC(*"mp4v"), int(self.fps), tuple(self.res)
            )

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        if self.render:
            self.video.release()

    @property
    def size(self):
        return self.shape

    def to_px(self, pos):
        x = self.ratio*(pos[0]+self.shape[0]/2 + BOID_NOSE_LEN)
        y = self.ratio*(-pos[1]+self.shape[1]/2 + BOID_NOSE_LEN)
        return np.array([[x],[y]],dtype=int)

    def from_px(self, px):
        x = (px[0]/self.ratio)-self.shape[0]/2
        y = (-px[1]/self.ratio)-self.shape[1]/2
        return np.array([[x],[y]],dtype=float)

    def new_frame(self):
        return np.ndarray(shape=(*self.res[::-1], 3), dtype="uint8")

    def update(self):
        if self.render:
            self.video.write(self.current_frame)
            self.current_frame = self.new_frame()

    def fill(self, color):
        self.current_frame[:, :] = np.array(color, dtype="uint8")

    def draw_poly(self, points, color):
        print("Liste des points : "+str(points))
        px = [np.array([self.to_px(p).reshape(1,2) for p in points], dtype=np.int32)]
        print("Liste des pixels : "+str(px))
        cv2.fillPoly(
            self.current_frame,
            px,
            # double list as fillPoly expects a list of polygons
            color,
            16,
        )  # = antialiased
