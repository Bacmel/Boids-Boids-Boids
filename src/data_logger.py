import pandas
import os
import datetime


class DataLogger:
    def __init__(self):
        super().__init__()
        now = datetime.datetime.now()
        name = now.strftime("%d-%m-%Y_%H-%M-%S")
        self.destination = f"logs/{name}/"
        self.poses = pandas.DataFrame()
        self.quantities = pandas.DataFrame()

    def flush(self):
        self._mkdir_dest()
        # Store all data frame
        for name, value in self.__dict__.items():
            if isinstance(value, pandas.DataFrame):
                path = f"{self.destination}{name}.csv"
                value.to_csv(path)

    def _mkdir_dest(self):
        from_start = ""
        for folder in self.destination.split('/')[:-1]:
            from_start += f"{folder}/"
            if not os.path.exists(from_start):
                os.mkdir(from_start)
