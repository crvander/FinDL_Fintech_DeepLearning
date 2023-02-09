import requests
import yaml
from box import Box
import logging
import os
import gdown
import subprocess

# open the configuration for model loading
with open('config/model_config.yml', 'r') as file:
    data_config = Box(yaml.full_load(file))
    

def download_models():
    destination = data_config.outpath # the output folder for models
    models = data_config.models # list of pending models to download
    model_folder_path = "{}/{}".format(os.getcwd(), destination) # merge the file path
    model_folder_list = os.listdir(model_folder_path) # the directory list for saving folder
    
    logging.info("downloading to {}: ".format(model_folder_path))
    for (key, value) in models.items(): # for each models in the list
        file_id = value # file_id of models in Google Shared Drive
        file_name = key # model name to be saved
        if file_name.rstrip('.zip') not in model_folder_list: # detetc if required model being downloaded
            logging.info("downloading from google shared id: {}".format(file_id))
            logging.info("saving model as name: {}".format(file_name))
            logging.info("saving path: {}/{}".format(model_folder_path, file_name))
            output = "{}/{}".format(model_folder_path, file_name)
            gdown.download(id=file_id, output=output, quiet=False) # use gdown to download zipped model
     
    subprocess.run('unzip {}/\*.zip -d {}'.format(destination, destination), shell = True, stdout = subprocess.PIPE) # unzip all the zipped models
    subprocess.run('rm {}/*.zip'.format(model_folder_path),shell = True) # delet all the zipped files to save disk memory
    

