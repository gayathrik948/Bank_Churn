import sys
from typing import Dict
from pandas import DataFrame
import pandas as pd
from bank_churn.constants import *
from bank_churn.configuration.s3_operations import S3Operation
from bank_churn.exceptions import BankChurnException


class BankChurnData:
    def __init__(self,
                 LIMIT_BAL,
                 SEX,
                 EDUCATION,
                 MARRIAGE,
                 AGE,
                 PAY_0,
                 PAY_1,
                 PAY_2,
                 PAY_3,
                 PAY_4,
                 PAY_5,
                 BILL_AMT1,
                 BILL_AMT2,
                 BILL_AMT3,
                 BILL_AMT4,
                 BILL_AMT5,
                 BILL_AMT6,
                 PAY_AMT1,
                 PAY_AMT2,
                 PAY_AMT3,
                 PAY_AMT4,
                 PAY_AMT5,
                 PAY_AMT6
                 ):
        self.LIMIT_BAL= LIMIT_BAL
        self.SEX = SEX
        self.EDUCATION = EDUCATION
        self.MARRIAGE = MARRIAGE
        self.AGE = AGE
        self.PAY_0 = PAY_0
        self.PAY_1 = PAY_1
        self.PAY_2 = PAY_2
        self.PAY_3 = PAY_3
        self.PAY_4 = PAY_4
        self.PAY_5 = PAY_5
        self.BILL_AMT1 = BILL_AMT1
        self.BILL_AMT2 = BILL_AMT2
        self.BILL_AMT3 = BILL_AMT3
        self.BILL_AMT4 = BILL_AMT4
        self.BILL_AMT5 = BILL_AMT5
        self.BILL_AMT6 = BILL_AMT6
        self.PAY_AMT1 = PAY_AMT1
        self.PAY_AMT2 = PAY_AMT2
        self.PAY_AMT3 = PAY_AMT3
        self.PAY_AMT4 = PAY_AMT4
        self.PAY_AMT5 = PAY_AMT5
        self.PAY_AMT6 = PAY_AMT6


    def get_data(self)->Dict:
        try:
            input_data = {
                "LIMIT_BAL": [self.LIMIT_BAL],
                "SEX": [self.SEX],
                "EDUCATION": [self.EDUCATION],
                "MARRIAGE": [self.MARRIAGE],
                "AGE": [self.AGE],
                "PAY_0": [self.PAY_0],
                "PAY_1": [self.PAY_1],
                "PAY_2": [self.PAY_2],
                "PAY_3": [self.PAY_3],
                "PAY_4": [self.PAY_4],
                "PAY_5": [self.PAY_5],
                "BILL_AMT1": [self.BILL_AMT1],
                "BILL_AMT2": [self.BILL_AMT2],
                "BILL_AMT3": [self.BILL_AMT3],
                "BILL_AMT4": [self.BILL_AMT4],
                "BILL_AMT5": [self.BILL_AMT5],
                "BILL_AMT6": [self.BILL_AMT6],
                "PAY_AMT1": [self.PAY_AMT1],
                "PAY_AMT2": [self.PAY_AMT2],
                "PAY_AMT3": [self.PAY_AMT3],
                "PAY_AMT4": [self.PAY_AMT4],
                "PAY_AMT5": [self.PAY_AMT5],
                "PAY_AMT6": [self.PAY_AMT6],
            }
            return input_data
        except Exception as e:
            raise BankChurnException(e, sys)

    def get_input_data_frame(self) -> DataFrame:
        try:
            input_dict = self.get_data()
            return pd.DataFrame(input_dict)
        except Exception as e:
            raise BankChurnException(e, sys)



class CostPredictor:
    def __init__(self):
        self.s3 = S3Operation()
        self.bucket_name = BUCKET_NAME


    def predict(self, X)->float:
        try:
            best_model = self.s3.load_model(MODEL_FILE_NAME,
                                            self.bucket_name)
            result = best_model.predict(X)
            return result
        except Exception as e:
            raise BankChurnException(e, sys)