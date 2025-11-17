from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessor
from src.model_trainer import ModelTrainer


data_ingest = DataIngestion(config="src/config/config.yaml")
data_ingest.ingest_data()

data_processor = DataProcessor(config="src/config/config.yaml")
data_processor.process_data()

trainer = ModelTrainer(config="src/config/config.yaml")
trainer.run()
