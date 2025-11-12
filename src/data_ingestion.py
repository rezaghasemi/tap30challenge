from logger import get_logger
from pathlib import Path
from config_reader import load_config

logger = get_logger(__name__)


class DataIngention:
    def __init__(self, config: str) -> None:
        self.config = load_config(config)
        self.train_ratio = self.config["data_ingestion"]["train_ratio"]
        self.test_ratio = self.config["data_ingestion"]["test_ratio"]
        self.val_ratio = self.config["data_ingestion"]["val_ratio"]

        if self.config["data_ingestion"]["data_source"] == "local":
            logger.info("Data source is local.")
            file_path = Path(self.config["data_ingestion"]["source"])
            if not file_path.exists():
                logger.error(f"File {file_path} does not exist.")
                raise FileNotFoundError(f"File {file_path} does not exist.")

            logger.info(f"Loading data from {self.config['data_ingestion']['source']}")
            self.raw_data_train, self.raw_data_test, self.raw_data_val = (
                self.load_loacal_data(self.file_path)
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
        pass
