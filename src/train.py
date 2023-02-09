import datasets
import evaluate
import torch
import numpy as np
from box import Box
import yaml
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import logging

# access necessary parameters from config file
with open('config/train-params.yml', 'r') as file:
    train_config = Box(yaml.full_load(file))
    
input_path = train_config.input_path
output_dir = train_config.output_dir
model_name = train_config.model_name
tokenizer_name = train_config.tokenizer_name
padding = train_config.padding
evaluation_strategy = train_config.evaluation_strategy
num_train_epochs = train_config.num_train_epochs
log_level = train_config.log_level
report_to = train_config.report_to
per_device_train_batch_size = train_config.per_device_train_batch_size
metric_name = train_config.metric_name
save_strategy = train_config.save_strategy

# function to train models 
def train():
    logging.info('initiate training...')
    #torch.cuda.empty_cache()

    # run the training process on GPUs, if possible 
    if torch.cuda.is_available():
        device = torch.device('cuda')
        logging.info('There are %d GPU(s) available.' % torch.cuda.device_count())
        logging.info('We will use the GPU: ', torch.cuda.get_device_name(0))
    
    else:
        logging.info('No GPU available, using the CPU instead.')
        device = torch.device('cpu')
        
    #tokenizer = AutoTokenizer.from_pretrained('ProsusAI/finbert')
    # load tokenizer from Transformers
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    #model = AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert', num_labels = 3)
    # load model from Transformers
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels = 3)
    # create features using training daatset
    features = datasets.Features({'text': datasets.Value('string'), 'labels': datasets.ClassLabel(num_classes = 3, names = [-1, 0, 1])})
    dataset = datasets.load_dataset(input_path, features = features)
    train = dataset['train']
    test = dataset['test']
    # function to tokenize the features
    def tokenize_function(examples):
        return tokenizer(examples['text'], padding = padding, truncation = True)

    tokenized_train = train.map(tokenize_function, batched = True)
    tokenized_test = test.map(tokenize_function, batched = True)
    # arguments for training the model
    args = {
        'output_dir': output_dir,
        'evaluation_strategy': evaluation_strategy,
        'num_train_epochs': num_train_epochs,
        'log_level': log_level,
        'report_to': report_to,
        'per_device_train_batch_size' : per_device_train_batch_size,
        'save_strategy' : save_strategy
    }
    # load evaluation metric
    metric = evaluate.load(metric_name)
    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits ,axis = -1)
        return metric.compute(predictions = predictions, references = labels)
    training_args = TrainingArguments(**args)
    # train the model with the appropriate arguments
    trainer = Trainer(model = model,
                      args = training_args,
                      train_dataset = tokenized_train,
                      eval_dataset = tokenized_test,
                      tokenizer = tokenizer,
                      compute_metrics = compute_metrics)
    trainer.save_model(model_name)
    logging.info(trainer.train())
    logging.info('training done.')
    return model_name
