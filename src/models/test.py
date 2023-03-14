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
    target_path = test_config.target_path
    output_dir = test_config.output_dir
    preds_name = test_config.preds_name

# function to test the model on test data
def test(test_target = 'test', test_lines = 3):
    """
    Function to test the trained model on testing data. This function will try to perform the 
    testing on GPUs if possible. The function will fetch the finetuned model from results/model_name,
    then fetch the testing data and perform predictions. The predictions will be save at user
    preferred destinations. Default destination is data/out. 

    Return None.

    Parameters:
        test_target: str, this argument defines what testing data to use. Default 'test'.
        test_lines: int, this argument defines how many predictions to make. Default 3.
    """

 # run the testing process on GPUs, if possible 
    if torch.cuda.is_available():
        device = torch.device('cuda')
        logging.info('There are %d GPU(s) available.' % torch.cuda.device_count())
        logging.info('We will use the GPU: ', torch.cuda.get_device_name(0))
    
    else:
        logging.info('No GPU available, using the CPU instead. WARNING: training may take long')
        device = torch.device('cpu')
        
        
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
    logging.info('predicting ...')
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

# prediction on the tweets
def prediction():
    """
    Function to make predictions on real-time tweets. This function will try to perform the 
    testing on GPUs if possible. This function will fetch finetuned models from 
    results/model_name. The function will make predictions for each day on tweets generated from
    Twitter API for a specific company, then average the sentiments and save the results in a 
    user defined destination. Default destination is data/out.

    Return None.

    No arguments required for this function.
    """
 # run the prediction process on GPUs, if possible 
    if torch.cuda.is_available():
        device = torch.device('cuda')
        logging.info('There are %d GPU(s) available.' % torch.cuda.device_count())
        logging.info('We will use the GPU: ', torch.cuda.get_device_name(0))
    
    else:
        logging.info('No GPU available, using the CPU instead. WARNING: training may take long')
        device = torch.device('cpu')

    out = []
    input_path = target_path
    # access the finetuned model
    model_full_path = '{}/{}/'.format(model_path, model_name)
    logging.info('initiate testing from {} ...'.format(model_full_path))
    model = AutoModelForSequenceClassification.from_pretrained(model_full_path, num_labels = 3) # read in model
    tokenizer = AutoTokenizer.from_pretrained(model_full_path) # read in tokenizer
    pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer, top_k=1) # return_all_scores will return dict within list 
    
    logging.info('loading target data from {} ...'.format(input_path))
    df = pd.read_csv(input_path) # read the processed tweets dataset
    logging.info('grouping text by day...'.format(input_path))
    dictionary = df.groupby('timestamp')['tweet'].apply(list).to_dict() # group text by day and save in list for each day
    logging.info('predicting on each day...')
    # target data prediction
    for day in dictionary: # for each day in dictionary of lists
        logging.info('predicting on {}...'.format(day))
        sum_sentiment = 0 # sum sentiment for each day
        prediction = pipeline(dictionary[day]) # pridict sentiment for each tweet
        for item in prediction: # for each tweet, if positive sum sentiment + 1, if negative then -1, neutral do nothing
            if item[0]['label'] == 'positive':
                sum_sentiment += 1 
            elif item[0]['label'] == 'negative':
                sum_sentiment -= 1
        avg_daily_prediction = sum_sentiment/len(prediction) # average sentiment for each day
        logging.info('save average sentiment {} on {}...'.format(avg_daily_prediction, day))
        out.append({"label": avg_daily_prediction, "date" : day}) # save average sentiment per day into list of dictionaries
    
    print(out)
    logging.info('saving daily average sentiment to {} ...'.format(output_dir))
    myFile = open('{}/{}'.format(output_dir,preds_name), 'w')
    writer = csv.writer(myFile)
    writer.writerow(['label', 'date'])
    for i in out: # write the prediction label to csv file
        writer.writerow(i.values()) 
    myFile.close()        
                
    logging.info('prediction done')
    return