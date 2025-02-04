## Main aim is to read the dataset from some data source(be created by big data team ,cloud team on mongodbor hadoob)
# (here we are using the local present data)
## We are going to split the data in train test which is the most important part and after that data transformation will happen

import os 
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformconfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

## In data ingestion there should be some inputs like where to save the train-dataortest-data 
## Those inputs are saved in another class 

@dataclass                ## --> Decorator 
class DataIngestionConfig:                                 ## Inputs req will be given through this config
    raw_data_path: str=os.path.join('artifacts',"data.csv")
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):          ## If data in some database to read from that database
        logging.info("Entered the data ingestion method or component")
        try:
            df = pd.read_csv(r'Notebook\data\stud.csv')
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("train test split initiated")
            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of the data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
        except Exception as e:
            raise CustomException(e,sys)
        

if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr,test_arr,_ = data_transformation.initiate_data_transform(train_data,test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))