import requests
import yaml
from box import Box
import logging
import os
import gdown
from zipfile import ZipFile

# open the configuration for model loading
with open('config/model_config.yml', 'r') as file:
    model_config = Box(yaml.full_load(file))
    

def download_models():
    """
    Function to download pre-trained models from Google Drive. The pre-trained models are stored
    on a Google Drive for users to download. The function will download the zip files from the Drive
    and access necessary configurations from them. After downloading, the models will be save to 
    user preferred destinations, default destination is results. These models can be used at the 
    users descretion and allow for additional modifications.

    Return None.

    No additional arguments required for this function.
    """
    destination = model_config.outpath # the output folder for models
    models = model_config.models # list of pending models to download
    model_folder_path = "{}/{}".format(os.getcwd(), destination) # merge the file path
    model_folder_list = os.listdir(model_folder_path) # the directory list for saving folder
    
    logging.info("downloading to {}: ".format(model_folder_path))
    for (key, value) in models.items(): # for each models in the list
        file_id = value # file_id of models in Google Shared Drive
        file_name = key # zipped model file name to be extracted
        full_path = model_folder_path + '/' + file_name # full path for zipped model
        
        if file_name.rstrip('.zip') not in model_folder_list:  # detetc if required model being downloaded
            logging.info("downloading from google shared id: {}".format(file_id))
            logging.info("saving model as name: {}".format(file_name))
            logging.info("saving path: {}/{}".format(model_folder_path, file_name))
            output = "{}/{}".format(model_folder_path, file_name)
            gdown.download(id=file_id, output=output, quiet=False)  # use gdown to download zipped model
            
        
            with ZipFile(full_path, 'r') as zip: # unzip all the zipped models
                print('Extracting all the files now...')
                zip.extractall(path = model_folder_path)
                print('Done! Extracted to {}'.format(model_folder_path))
            os.remove(full_path) # delet the zipped files to save disk memory