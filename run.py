import sys
import yaml
from box import Box
import pandas as pd
import time
sys.path.insert(0, 'src')
from data.make_dataset import download_data, generate_data, save_data, generate_tweet
from utils.download_models import download_models
from models.train import train
from models.test import test, prediction
import logging

def main(args):
    """
    Function to run the whole project. This function allows arguments for different 
    purposes. The function will make a run from top to bottom. 

    Return None.

    Parameters:
        args: **args, arguments to define the purpose of the run.
    """
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logging.info(args)

    
    if 'generate_data' in args: # will not be run in testrun for submission
        logging.info('loading data-params...')
        with open('config/data-params.yml', 'r') as file: # All config will be read in module files
            data_config = Box(yaml.full_load(file))
        logging.info(data_config) # here only for logging
        
        download_data()
        df = generate_data()
        save_data(df)
    
    if 'download_models' in args: # run for dev and testing
        with open('config/model_config.yml', 'r') as file: 
            model_config = Box(yaml.full_load(file))
        logging.info(model_config)
        
        download_models()
        
    with open('config/model_config.yml', 'r') as file: # run by default for submission requirements
        model_config = Box(yaml.full_load(file))
        logging.info(model_config)
        
        download_models()
        
        
    if 'train' in args: # will not be run in testrun for submission
        logging.info('loading training-params...')
        with open('config/train-params.yml', 'r') as file:
            train_config = Box(yaml.full_load(file))
        logging.info(train_config)

        start = time.time()
        trainer = train()
        end = time.time()
        logging.info('training time: ' + str(end - start))
    
    if 'test' in args: # test on test dataset
        logging.info('test run start...')
        test(test_target = 'test', test_lines = 3)
    elif 'test_run' in args: # test run for submission
        logging.info('testing start...')
        test(test_target = 'testing', test_lines = 20)
        
    if 'predict' in args:
        logging.info('fetching and processing twitter data...')
        generate_tweet()
        logging.info('prediction on tweets start...')
        prediction()
    return
    
    
        

if __name__ == '__main__':
    main(sys.argv[1:]) 