# -*- coding: utf-8 -*-
import os
from time import localtime, strftime
import subprocess

import matplotlib.pyplot as plt
import numpy as np

from .borders import Border, Infinite
from . import OUT_DIR, PALETTE


class Canvas:
    def __init__(self, dt, render):
        """Canvas Constructor.

        Args:
            dt (int): simulation time step.
            render (bool): predicate for video generation.

        """
        self.cond_border = True
        """bool: indicate if there is walls on the edge of the simulation"""
        self.fps = float(1 / dt)
        """float: The frame rate (in Hertz)."""
        self.__render = render
        """bool: Whether the video is rendered or not."""
        if self.render:
            # Prepare for rendering
            if not os.path.exists(OUT_DIR):
                os.mkdir(OUT_DIR)
            self.filename = OUT_DIR + strftime("%Y%m%dT%H%M%S", localtime()) + ".mp4"
            self.video = (
                f"ffmpeg -r {self.fps} -i {OUT_DIR}"
                + r"%d.svg -qscale:v 0 -c:v libvpx-vp9 -vf scale=1920:1080 -crf 20 -hide_banner " #-loglevel quiet
                + self.filename
                + f"; rm {OUT_DIR}*.svg" 
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
            subprocess.call(self.video, shell=True)

    def draw(self, border, pop, verbose):
        """Generation a new frame.

        Returns:
            pyplot.figure: The frame.

        """
        valc = plt.figure(
            figsize=(8, 4.5), tight_layout=True, facecolor=PALETTE["background"]
        ).add_subplot(111, facecolor=PALETTE["background"])
        valc.set_aspect("equal")
        valc.axis("off")

        if not isinstance(border, Infinite):  # fix border
            self.cond_border = False
            begin = border.origin - border.length
            end = border.origin + border.length
            valc.set_xlim(begin[0], end[0])
            valc.set_ylim(begin[1], end[1])

        x, y, u, v, color = pop.draw()
        y = np.array(y)-y[-1]
        x = np.array(x)-x[-1]
        self.quiver = valc.quiver(x, y, u, v, color=color, pivot="middle",units='xy')
        if verbose:
            s = "\n".join(pop.get_properties())
            self.text = valc.get_figure().text(
                0.015,
                0.975,
                s,
                bbox=dict(facecolor=PALETTE["highlight"], alpha=0.5),
                ha="left",
                va="top",
            )

        self.current_frame = valc

    def update(self, ind, pop, verbose):
        """Update the video file and the frame.

        Check whether the rendering is enabled.
        If so, write the current frame in the video file and create a
        new frame.

        """
        if self.render:
            if self.cond_border:
                self.current_frame.relim()
                self.current_frame.autoscale_view()

            self.show_pop(pop)

            if verbose:
                self.show_properties(pop.get_properties())
            self.current_frame.get_figure().savefig(f"{OUT_DIR}{ind}.svg")

    def show_properties(self, properties):
        """Get a list of string describing the properties.

        Returns:
            A list of string describing the properties.

        """

        s = "\n".join(properties)
        self.text.set_text(s)

    def show_pop(self, pop):
        """Get a list of string describing the properties.

        Returns:
            A list of string describing the properties.

        """
        x, y, u, v, color = pop.draw()
        self.quiver.remove()
        self.quiver = self.current_frame.quiver(x, y, u, v, color=color, pivot="middle",units='xy')

    def snapshot(self, filename):
        """Save a the current frame as an image.

        Args:
            filename: The given file name (aka. the path to save to).

        """
        self.current_frame.get_figure().savefig(f"{filename}.pdf", bbox_inches=0)
