from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
from src.logger import get_logger
from src.config_reader import load_config
import joblib
import mlflow

logger = get_logger(__name__)


class ModelTrainer:
    def __init__(self, config: str):
        self.config = load_config(config)

    def create_model(self) -> RandomForestRegressor:
        logger.info("Creating RandomForestRegressor model")
        model = RandomForestRegressor(
            n_estimators=self.config["model_trainer"]["n_estimators"],
            max_depth=self.config["model_trainer"]["max_depth"],
            max_samples=self.config["model_trainer"]["max_samples"],
        )
        return model

    def load_data(self):
        logger.info("Loading processed data")
        proccessed_data_path = (
            Path(self.config["data_ingestion"]["artifact_dir"]) / "processed_data"
        )
        self.train_data_path = proccessed_data_path / "processed_train_data.csv"
        self.val_data_path = proccessed_data_path / "processed_validation_data.csv"
        train_data = pd.read_csv(self.train_data_path)
        val_data = pd.read_csv(self.val_data_path)
        return train_data, val_data

    def train_model(
        self, model: RandomForestRegressor, train_data: pd.DataFrame
    ) -> RandomForestRegressor:
        X_train = train_data.drop("value", axis=1)
        y_train = train_data["value"]
        model.fit(X_train, y_train)
        return model

    def evaluate_model(
        self, model: RandomForestRegressor, val_data: pd.DataFrame
    ) -> float:
        X_val = val_data.drop("value", axis=1)
        y_val = val_data["value"]
        y_pred = model.predict(X_val)
        rmse = root_mean_squared_error(y_val, y_pred)
        return rmse

    def run(self):
        mlflow.set_experiment(self.config["model_trainer"]["experiment_name"])
        with mlflow.start_run():
            mlflow.set_tag("model", "RandomForestRegressor")
            logger.info("Starting the model training")
            train_data, val_data = self.load_data()
            mlflow.log_artifact(self.train_data_path, "datasets")
            mlflow.log_artifact(self.val_data_path, "datasets")
            model = self.create_model()
            model = self.train_model(model, train_data)
            rmse = self.evaluate_model(model, val_data)
            mlflow.log_metric("rmse", rmse)
            logger.info(f"Model evaluation completed with RMSE: {rmse}")
            self.save_model(model, rmse)
            mlflow.log_artifact(self.model_saving_path, "models")
            model_parameters = model.get_params()
            mlflow.log_params(model_parameters)
            logger.info("Model training completed successfully")

    def save_model(self, model: RandomForestRegressor, rmse: float):
        logger.info(f"Saving model with RMSE: {rmse}")
        self.model_saving_path = (
            Path(self.config["model_trainer"]["save_model_path"])
            / f"model_{int(rmse)}.joblib"
        )
        self.model_saving_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, self.model_saving_path, compress=3)
        logger.info(f"Model saved to {self.model_saving_path}")


if __name__ == "__main__":
    trainer = ModelTrainer("src/config/config.yaml")
    trainer.run()
