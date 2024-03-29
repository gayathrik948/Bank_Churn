from bank_churn.components.data_ingestion import DataIngestion
from bank_churn.components.data_validation import DataValidation
from bank_churn.components.data_transformation import DataTransformation
from bank_churn.components.model_trainer import ModelTrainer
from bank_churn.components.model_evaluation import ModelEvaluation
from bank_churn.components.model_pusher import ModelPusher
from bank_churn.entity.artifacts_entity import (DataIngestionArtifacts, DataValidationArtifacts,
                                                DataTransformationArtifacts, ModelTrainerArtifacts,
                                                ModelEvaluationArtifacts,ModelPusherArtifacts)
from bank_churn.entity.config_entity import (DataIngestionConfig, DataValidationConfig,
                                             DataTransformationConfig, ModelTrainerConfig,
                                             ModelEvaluationConfig,ModelPusherConfig)
from bank_churn.configuration.mongo_operations import MongoDBOperation
from bank_churn.configuration.s3_operations import S3Operation
from bank_churn.exceptions import BankChurnException
import sys

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig()
        self.mongo_op = MongoDBOperation()
        self.s3_op = S3Operation()

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

    def start_data_transformation(self, data_ingestion_artifact:DataIngestionArtifacts)->DataTransformationArtifacts:
        try:
            data_transformation = DataTransformation(data_ingestion_artifacts=data_ingestion_artifact,
                                                     data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise BankChurnException(e, sys)

    def start_model_trainer(self, data_transformation_artifacts:DataTransformationArtifacts)->ModelTrainerArtifacts:
        try:
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifacts,
                                         model_trainer_config=self.model_trainer_config)
            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            return model_trainer_artifacts
        except Exception as e:
            raise BankChurnException(e, sys)

    def start_model_evaluation(self, model_trainer_artifact:ModelTrainerArtifacts,
                 data_ingestion_artifact:DataIngestionArtifacts)->ModelEvaluationArtifacts:
        try:
            model_evaluation = ModelEvaluation(model_trainer_artifacts=model_trainer_artifact,
                                               data_ingestion_artifacts=data_ingestion_artifact,
                                               model_evaluation_config=self.model_evaluation_config)
            model_evaluation_artifacts = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifacts
        except Exception as e:
            raise BankChurnException(e, sys)

    def start_model_pusher(
            self,
            model_trainer_artifact: ModelTrainerArtifacts,
            data_transformation_artifact: DataTransformationArtifacts,
            s3: S3Operation
    ) -> ModelPusherArtifacts:
        try:
            model_pusher = ModelPusher(
                model_pusher_config=self.model_pusher_config,
                model_trainer_artifacts=model_trainer_artifact,
                data_transformation_artifacts=data_transformation_artifact,
                s3=s3
            )
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except Exception as e:
            raise BankChurnException(e, sys)


    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifacts = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifacts = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact)
            model_trainer_artifacts = self.start_model_trainer(data_transformation_artifacts=data_transformation_artifacts)
            model_evaluation_artifacts = self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,
                                                                     model_trainer_artifact=model_trainer_artifacts
                                                                     )
            if not model_evaluation_artifacts.is_model_accepted:
                print("model not accepted")
                return None
            model_pusher_artifact = self.start_model_pusher(
                model_trainer_artifact=model_trainer_artifacts,
                data_transformation_artifact=data_transformation_artifacts,
                s3=self.s3_op)

        except Exception as e:
            raise BankChurnException(e,sys)



