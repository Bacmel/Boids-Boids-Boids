# -*- coding: utf-8 -*-
import datetime
import os

import pandas


class DataLogger:
    def __init__(self):
        """Build a DataLogger with a default destination name."""
        now = datetime.datetime.now()
        name = now.strftime("%d-%m-%Y_%H-%M-%S")
        self.destination = f"../logs/{name}/"
        """str: The folder to save the CSV file in."""
        self.state = pandas.DataFrame()
        """pandas.DataFrame: The state information."""
        self.quantities = pandas.DataFrame()
        """pandas.DataFrame: The quantities information."""

    def flush(self):
        """Flush all the data as CSV file."""
        self._mkdir_dest()

        # Store all data frame
        for name, value in self.__dict__.items():
            if isinstance(value, pandas.DataFrame):
                path = f"{self.destination}{name}.csv"
                value.to_csv(path)

    def _mkdir_dest(self):
        """Make the required directories."""
        from_start = ""
        for folder in self.destination.split("/")[:-1]:
            from_start += f"{folder}/"
            if not os.path.exists(from_start):
                os.mkdir(from_start)
