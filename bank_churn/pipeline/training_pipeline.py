from bank_churn.components.data_ingestion import DataIngestion
from bank_churn.components.data_validation import DataValidation
from bank_churn.entity.artifacts_entity import (DataIngestionArtifacts, DataValidationArtifacts)
from bank_churn.entity.config_entity import (DataIngestionConfig, DataValidationConfig)
from bank_churn.configuration.mongo_operations import MongoDBOperation
from bank_churn.exceptions import BankChurnException
import sys

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.mongo_op = MongoDBOperation()

    def start_data_ingestion(self)->DataIngestionArtifacts:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config,
                                           mongo_op=self.mongo_op)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise BankChurnException(e,sys)

    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifacts)->DataValidationArtifacts:
        try:
            data_validation = DataValidation(data_validation_config=self.data_validation_config,
                                             data_ingestion_artifacts=data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_data_validation()
            return  data_validation_artifact
        except Exception as e:
            raise BankChurnException(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifacts = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise BankChurnException(e,sys)



