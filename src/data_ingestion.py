from logger import get_logger
from pathlib import Path
from config_reader import load_config
from random import shuffle

logger = get_logger(__name__)


class DataIngention:
    def __init__(self, config: str) -> None:
        self.config = load_config(config)
        self.train_ratio = self.config["data_ingestion"]["train_ratio"]
        self.test_ratio = self.config["data_ingestion"]["test_ratio"]
        self.validation_ratio = self.config["data_ingestion"]["validation_ratio"]
        self.train_data = None
        self.test_data = None
        self.validation_data = None

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
                        test_data.append((t, (j, i), int(line[i])))
                    else:
                        output_data.append((t, (j, i), int(line[i])))
        shuffle(output_data)
        train_data = output_data[: int(len(output_data) * self.train_ratio)]
        validation_data = output_data[int(len(output_data) * self.train_ratio) :]
        return train_data, test_data, validation_data


if __name__ == "__main__":
    data_ingestion = DataIngention(config="src/config/config.yaml")
