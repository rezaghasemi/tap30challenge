import pandas as pd
from logger import get_logger
from pathlib import Path
from config_reader import load_config

logger = get_logger(__name__)


class DataProcessor:
    def __init__(self, config) -> None:
        self.config = load_config(config)
        self.data_path = Path(self.config["data_ingestion"]["artifact_dir"])
        self.proccessed_data_path = Path(self.data_path / "processed_data")
        if not self.proccessed_data_path.exists():
            self.proccessed_data_path.mkdir(parents=True, exist_ok=True)

    def process_data(self):
        logger.info(f"Initializing DataProcessor with data path: {self.data_path}")
        self.train_data, self.test_data, self.validation_data = self.load_data()
        (
            self.processed_train_data,
            self.processed_test_data,
            self.processed_validation_data,
        ) = self.preprocess_data(self.train_data, self.test_data, self.validation_data)
        logger.info("Data processing completed successfully!")

    def load_data(self):
        logger.info(f"Loading data from {self.data_path}")
        train_data = pd.read_csv(self.data_path / "train_data.csv")
        test_data = pd.read_csv(self.data_path / "test_data.csv")
        validation_data = pd.read_csv(self.data_path / "validation_data.csv")
        logger.info("Data loaded successfully")
        return train_data, test_data, validation_data

    def preprocess_data(self, train_data, test_data, validation_data):
        logger.info("Preprocessing data!")
        proccessed_train_data = self.one_data_preprocess(train_data)
        processed_test_data = self.one_data_preprocess(test_data)
        processed_validation_data = self.one_data_preprocess(validation_data)
        logger.info("Data preprocessing completed!")
        self.save_processed_data(
            proccessed_train_data,
            processed_test_data,
            processed_validation_data,
            self.proccessed_data_path,
        )
        return (
            proccessed_train_data,
            processed_test_data,
            processed_validation_data,
        )

    def one_data_preprocess(self, data: pd.DataFrame):
        shift = self.config["data_processing"]["shift"]
        data = data.sort_values(by=["time", "row", "column"]).reset_index(drop=True)
        # Example preprocessing step: shifting a column
        data["time"] = data["time"] + shift % 24
        data = data.assign(
            hour_of_day=data["time"] % 24,
            day_of_week=(data["time"] // 24) % 7,
        )
        return data

    def save_processed_data(
        self,
        proccessed_train_data,
        processed_test_data,
        processed_validation_data,
        output_path: str,
    ):
        logger.info(f"Saving processed data to {output_path}")
        proccessed_train_data.to_csv(
            Path(output_path) / "processed_train_data.csv", index=False
        )
        processed_test_data.to_csv(
            Path(output_path) / "processed_test_data.csv", index=False
        )
        processed_validation_data.to_csv(
            Path(output_path) / "processed_validation_data.csv", index=False
        )
        logger.info("Processed data saved successfully")


if __name__ == "__main__":
    config = Path("src/config/config.yaml")
    data_processor = DataProcessor(config)
