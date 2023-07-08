from bank_churn.configuration.mongo_operations import MongoDBOperation
from bank_churn.constants import *
import pandas as pd
from bank_churn.pipeline.training_pipeline import TrainingPipeline
from bank_churn.exceptions import BankChurnException
import sys
#
# if __name__ == "__main__":
#     mongo_op = MongoDBOperation()
#     df = pd.read_csv("dataset.csv")
#     mongo_op.insert_dataframe_as_record(df, DB_NAME, COLLECTION_NAME)
#     print("data inserted successfully")


if __name__ == "__main__":
    try:
        pipline = TrainingPipeline()
        pipline.run_pipeline()
    except Exception as e:
        raise BankChurnException(e, sys)