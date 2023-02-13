import datasets
import yaml
from box import Box
import pandas as pd
import csv
import evaluate
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline, pipeline
import logging

# access necessary parameters from config file
with open('config/test-params.yml', 'r') as file:
    test_config = Box(yaml.full_load(file))
    model_path = test_config.model_path
    model_name = test_config.model_name
    test_path = test_config.test_path
    testdata_path = test_config.testdata_path
    output_dir = test_config.output_dir
    preds_name = test_config.preds_name

# function to test the model on test data
def test(test_target = 'test', test_lines = 3):
    out = []
    if test_target == 'test':
        input_path = test_path
    if test_target == 'testing':
        input_path = testdata_path
    # access the finetuned model
    model_full_path = '{}/{}/'.format(model_path, model_name)
    logging.info('initiate testing from {} ...'.format(model_full_path))
    model = AutoModelForSequenceClassification.from_pretrained(model_full_path, num_labels = 3) # read in model
    tokenizer = AutoTokenizer.from_pretrained(model_full_path) # read in tokenizer
    logging.info('loading test data from {} ...'.format(input_path))
    testdata = list(pd.read_csv(input_path)['text'].head(test_lines)) # test out the first N samples from test target
    logging.info('predicting ...'.format(input_path))
    pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer, top_k=1) # return_all_scores will return dict within list 
    
    # test data prediction
    prediction = pipeline(testdata)
    
    logging.info('saving predictions to {} ...'.format(output_dir))
    myFile = open('{}/{}'.format(output_dir,preds_name), 'w')
    writer = csv.writer(myFile)
    writer.writerow(['label', 'score'])
    for i in prediction: # write the prediction label to csv file
        writer.writerow(i[0].values()) 
    myFile.close()        
                
    logging.info('testing done')
    return
