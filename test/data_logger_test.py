from src.data_logger import DataLogger
from pandas import DataFrame
if __name__ == "__main__":
    dl = DataLogger()
    data = {"test1": [1, 2, 3], "test2": [-1, -2, -3]}
    dl.test = DataFrame(data)
    print(dl.__dict__.keys())
    dl.flush()
    print(dl.test)
    dl.test = dl.test.append({"test1": 4, "test2": -4}, ignore_index=True)
    print(dl.test)
    dl.flush()
