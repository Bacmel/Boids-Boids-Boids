from time import localtime, strftime

import cv2
from cv2 import VideoWriter, VideoWriter_fourcc as FourCC
import numpy as np
import os

from src import OUT_DIR, BOID_NOSE_LEN


class Canvas:
    def __init__(self, res, border, dt, render):
        """Canvas Constructor.

        Args:
            res (numpy.ndarray): resolution of the video window.
            border (Border): border of the simulation.
            dt (int): simulation time step.
            render (bool): predicate for video generation.

        """
        # output related
        self.res = np.array(res, dtype="int")
        self.fps = float(1 / dt)
        self.origin = border.origin
        self.shape = border.length
        self.render = render
        self.ratios = np.multiply(self.res, 1 / (self.shape + 2 * BOID_NOSE_LEN))[0]
        self.ratio = np.min(self.ratios)

        # A verifier
        self.current_frame = self.new_frame()

        # renderer
        if self.render:
            if not os.path.exists(OUT_DIR):
                os.mkdir(OUT_DIR)
            self.filename = OUT_DIR + strftime("%Y%m%dT%H%M%S", localtime()) + ".mp4"
            self.video = VideoWriter(
                self.filename, FourCC(*"mp4v"), int(self.fps), tuple(self.res)
            )

    def __enter__(self):
        """Starting method.

        Returns:
            Canvas: the object itself.

        """
        return self

    def __exit__(self, *args, **kwargs):
        """Ending method.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        if self.render:
            self.video.release()

    @property
    def size(self):
        """get size property.

        Returns:
            numpy.ndarray: shape of the world.

        """
        return self.shape

    def to_px(self, pos):
        """Transition to px unit.

        Args:
            pos (numpy.ndarray): position in the simulation.

        Returns:
            numpy.ndarray: position in the image space.

        """
        x = (
            self.ratio * (pos[0] + self.shape[0] / 2 + BOID_NOSE_LEN)
            + (self.ratios[0] - self.ratio) * self.shape[0] / 2
        )
        y = (
            self.ratio * (-pos[1] + self.shape[1] / 2 + BOID_NOSE_LEN)
            + (self.ratios[1] - self.ratio) * self.shape[1] / 2
        )
        return np.array([[x], [y]], dtype=int)

    def from_px(self, px):
        """Transition to simulation unit.

        Args:
            pos (numpy.ndarray): position in the image space.

        Returns:
            numpy.ndarray: position in the simulation.

        """
        x = (px[0] / self.ratio) - self.shape[0] / 2
        y = (-px[1] / self.ratio) - self.shape[1] / 2
        return np.array([[x], [y]], dtype=float)

    def new_frame(self):
        """Generation a New Frame.

        Returns:
            numpy.ndarray: New frame.

        """
        return np.ndarray(shape=(*self.res[::-1], 3), dtype="uint8")

    def update(self):
        """Generation a New Frame.

        Returns:
            numpy.ndarray: New frame.

        """
        if self.render:
            self.video.write(self.current_frame)
            self.current_frame = self.new_frame()

    def fill(self, color):
        """Fill the current frame.

        Args:
            color (Color): color of the polygone.

        """
        self.current_frame[:, :] = np.array(color, dtype="uint8")

    def draw_poly(self, points, color):
        """Draw new polygone.

        Args:
            points (numpy.ndarray): list point for polygone.
            color (Color): color of the polygone.

        """
        px = [np.array([self.to_px(p).reshape(1, 2) for p in points], dtype=np.int32)]
        cv2.fillPoly(
            self.current_frame,
            px,
            # double list as fillPoly expects a list of polygons
            color,
            16,
        )  # = antialiased
