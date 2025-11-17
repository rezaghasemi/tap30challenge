from pathlib import Path
from src.config_reader import load_config
from random import shuffle
from src.logger import get_logger

import csv
import pandas as pd

logger = get_logger(__name__)


class DataIngestion:
    def __init__(self, config: str) -> None:
        self.config = load_config(config)
        self.train_ratio = self.config["data_ingestion"]["train_ratio"]
        self.test_ratio = self.config["data_ingestion"]["test_ratio"]
        self.validation_ratio = self.config["data_ingestion"]["validation_ratio"]
        self.train_data = None
        self.test_data = None
        self.validation_data = None

    def ingest_data(self) -> None:
        if self.config["data_ingestion"]["data_source"] == "local":
            logger.info("Data source is local.")
            file_path = Path(self.config["data_ingestion"]["source"])
            if not file_path.exists():
                logger.error(f"File {file_path} does not exist.")
                raise FileNotFoundError(f"File {file_path} does not exist.")

            logger.info(f"Loading data from {self.config['data_ingestion']['source']}")
            self.train_data, self.test_data, self.validation_data = (
                self.load_loacal_data(file_path)
            )

            self.store_data(Path(self.config["data_ingestion"]["artifact_dir"]))

            logger.info("Raw data saved to artifact folder.")
        else:
            raise ValueError(
                f"Data source {self.config['data_ingestion']['data_source']} is not supported."
            )

    def load_loacal_data(self, file_path: Path):
        with open(file_path, "r") as file:
            data = file.read().splitlines()
        num_snapshots = int(data[0])
        row, column = int(data[1].split()[0]), int(data[1].split()[1])
        data = data[2:]
        test_data = []
        output_data = []
        for t in range(num_snapshots):
            # t is the time index
            # j is the row index
            # i is the column index
            for j in range(row):
                line = data[t * row + j].split()
                for i in range(column):
                    if int(line[i]) == -1:
                        test_data.append((t, j, i, int(line[i])))
                    else:
                        output_data.append((t, j, i, int(line[i])))
        shuffle(output_data)
        train_data = output_data[: int(len(output_data) * self.train_ratio)]
        validation_data = output_data[int(len(output_data) * self.train_ratio) :]
        return train_data, test_data, validation_data

    def store_data(self, path: Path = Path("./artifacts")) -> None:
        train_path = path / "train_data.csv"
        test_path = path / "test_data.csv"
        validation_path = path / "validation_data.csv"
        header = ["time", "row", "column", "value"]
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        with open(train_path, "w") as train_file:
            writer = csv.writer(train_file)
            writer.writerow(header)
            writer.writerows(self.train_data)
            logger.info(f"Train data saved to {train_path}")
        with open(test_path, "w") as test_file:
            writer = csv.writer(test_file)
            writer.writerow(header)
            writer.writerows(self.test_data)
            logger.info(f"Test data saved to {test_path}")
        with open(validation_path, "w") as validation_file:
            writer = csv.writer(validation_file)
            writer.writerow(header)
            writer.writerows(self.validation_data)
            logger.info(f"Validation data saved to {validation_path}")


if __name__ == "__main__":
    data_ingestion = DataIngestion(config="src/config/config.yaml")
    data_ingestion.store_data()
