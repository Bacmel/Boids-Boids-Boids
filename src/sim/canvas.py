# -*- coding: utf-8 -*-
import os
from time import localtime, strftime

import cv2
from cv2 import VideoWriter, VideoWriter_fourcc as FourCC
import numpy as np

from . import BOID_NOSE_LEN, OUT_DIR


class Canvas:
    def __init__(self, res, border, dt, render):
        """Canvas Constructor.

        Args:
            res (numpy.ndarray): resolution of the video window.
            border (Border): border of the simulation.
            dt (int): simulation time step.
            render (bool): predicate for video generation.

        """
        self.res = np.array(res, dtype="int")
        """numpy.ndarray: The video resolution (in pixels)."""
        self.fps = float(1 / dt)
        """float: The frame rate (in Hertz)."""
        self.origin = border.origin
        """numpy.ndarray: The render box center (in length units)."""
        self.box = border.length
        """numpy.ndarray: The render box dimensions (in length units)."""
        self.__render = render
        """bool: Whether the video is rendered or not."""
        self.ratios = None
        """numpy.ndarray: The conversion ratio from world to image for both axes (in pixels per length units)."""
        self.ratio = 0.0
        """float: The conversion ratio from world to image (in pixels per length units)."""

        self._compute_ratios()
        self.current_frame = self.new_frame()
        if self.render:
            # Prepare for rendering
            if not os.path.exists(OUT_DIR):
                os.mkdir(OUT_DIR)
            self.filename = OUT_DIR + strftime("%Y%m%dT%H%M%S", localtime()) + ".mp4"
            self.video = VideoWriter(
                self.filename, FourCC(*"mp4v"), int(self.fps), tuple(self.res)
            )

    @property
    def render(self):
        """Get the flag that controls the rendering.

        Returns:
            bool:  Whether the video is rendered or not.
        """
        return self.__render

    def __enter__(self):
        """Starting method.

        Returns:
            Canvas: the object itself.

        """
        return self

    def __exit__(self, *args, **kwargs):
        """Ending method.

        Output the final video.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        if self.render:
            self.video.release()

    def fit(self, pop):
        """Compute the shape and the origin which fits to the given population.

        Compute the smallest box around the population.
        Resize the box to match the resolution ration.
        Compute the conversion factor from length unit to pixels.

        Args:
            pop (Population): The population to fit to.
        """
        # Compute the smallest box around the population.
        ld_corner = np.copy(pop.pop[0].pos)
        ru_corner = np.copy(pop.pop[0].pos)
        for ind in pop.pop[1:]:
            pos = ind.pos
            for i in range(2):
                if pos[i, 0] < ld_corner[i, 0]:
                    ld_corner[i, 0] = pos[i, 0]
                if pos[i, 0] > ru_corner[i, 0]:
                    ru_corner[i, 0] = pos[i, 0]
        self.box = ru_corner - ld_corner
        self.origin = 0.5 * (ru_corner + ld_corner)

        # Resize the box to match the resolution ration.
        res_ratio = self.res[0] / self.res[1]
        if self.box[0, 0] < res_ratio * self.box[1, 0]:
            self.box[0, 0] = res_ratio * self.box[1, 0]
        else:
            self.box[1, 0] = self.box[0, 0] / res_ratio

        # Compute the conversion factor from length unit to pixels.
        self._compute_ratios()

    def _compute_ratios(self):
        """Compute the conversion ratios from length units to pixel for each axis.

        Returns:
            The conversion ratios from length units to pixel for each axis.

        """
        self.ratios = np.multiply(
            self.res, 1 / (self.box.reshape(-1) + 2 * BOID_NOSE_LEN)
        )
        self.ratio = np.min(self.ratios)

    def to_px(self, pos):
        """Convert a position from length units to pixels.

        Args:
            pos (numpy.ndarray): The position in the simulation (in length units).

        Returns:
            numpy.ndarray: position in the image space (in pixels).

        """
        x = (
            self.ratio * (pos[0] - self.origin[0] + self.box[0] / 2 + BOID_NOSE_LEN)
            + (self.ratios[0] - self.ratio) * self.box[0] / 2
        )
        y = (
            self.ratio * (-pos[1] + self.origin[1] + self.box[1] / 2 + BOID_NOSE_LEN)
            + (self.ratios[1] - self.ratio) * self.box[1] / 2
        )
        return np.array([[x], [y]], dtype=int)

    def new_frame(self):
        """Generation a new frame.

        Returns:
            numpy.ndarray: The new frame.

        """
        return np.ndarray(shape=(*self.res[::-1], 3), dtype="uint8")

    def update(self):
        """Update the video file and the frame.

        Check whether the rendering is enabled.
        If so, write the current frame in the video file and create a
        new frame.

        """
        if self.render:
            self.video.write(self.current_frame)
        self.current_frame = self.new_frame()

    def fill(self, color):
        """Fill the current frame with the given color.

        Args:
            color (Color): The color to fill the frame with.

        """
        self.current_frame[:, :] = np.array(color, dtype="uint8")

    def draw_poly(self, points, color):
        """Draw a polygon on the frame.

        Args:
            points (numpy.ndarray): The list of points for polygon (in length units).
            color (Color): The color of the polygon.

        """
        # double list as fillPoly expects a list of polygons
        px = [np.array([self.to_px(p).reshape(1, 2) for p in points], dtype=np.int32)]
        cv2.fillPoly(
            self.current_frame,
            px,
            color,
            16,
        )

    def show_properties(self, properties):
        """Get a list of string describing the properties.

        Returns:
            A list of string describing the properties.

        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (255, 255, 255)
        font_scale = 0.5
        thickness = 1

        for i in range(len(properties)):
            cv2.putText(
                self.current_frame,
                properties[i],
                (50, (i + 1) * 30),
                font,
                font_scale,
                color,
                thickness,
                cv2.LINE_AA,
            )

    def snapshot(self, filename):
        """Save a the current frame as an image.

        Args:
            filename: The given file name (aka. the path to save to).

        """
        cv2.imwrite(filename, self.current_frame)
