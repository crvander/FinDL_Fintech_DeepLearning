<h1 align="center">
  Transformers for Sentiment Analysis on Financial Text
</h1>

<h4 align="center">
  Fine-tuned Models based on pretrained Hugging Face Transformers
</h4>

## Usage

### From Command Line
```bash
# this will install necessary packages
pip install -r requirements.txt

# this will run the whole pipeline consists of downloading full dataset, generate data, 
# downloading our finetuned models from google drive, unzip model folders,
# predict sentiments on testing dataset

python run.py generate_data download_models test

# trainning process based on pretrained models from HuggingFace
python run.py generate_data train test

# for predict based on tweets data from twitter API
python run.py download_models predict

# for default testing run (submission for Quater1), 
# test run will download, unzip our finetuned models from google drive,
# predict on dummy testdata(3 samples) and output predicted labels

python run.py testing
```

### File structure and configuration
All configuration will be read from config folder, **data-params.yml** will be read when generating data, **model_config.yml** will be read when downloading, unzipping finetuned models, **train-params.yml** will be read as training hyperparameters as well as io path, **test-params.yml** consists io for test dataset and testrun dummy dataset.

Raw dataset will be scraped from data sources and saved in data/raw, processed data will be saved in data/temp predictions will be saved in data/out, all datafiles will be saved in .csv file.

Finetuned models, no matter directly output from training process, or download from google shared drive, all will be saved in results folder **train.py** will download pretrained models from Hugging Face hub, and read data from data/temp, finally save finetuned model to result folder.

**test.py** will take two argument, test_target and test_lines. test_target can be specified as testing, which will generate prediction on testing data
or default as test to predict on testrun dummy data. All prediction will be saved in data/out.

```
DSC180a-Q1-NLP                                                     //
├─ .git                                                            //
├─ config                            //
│  ├─ config.json                    //
│  ├─ data-params.yml                //
│  ├─ model-config.yml               //
│  ├─ test-params.yml                //
│  └─ train-params.yml               //
├─ data                                                            //
│  ├─ kaggle.json                                                  //
│  ├─ out                                                          //
│  │  ├─ model.joblib                                              //
│  │  └─ preds.csv                                                 //
│  ├─ raw                                                          //
│  ├─ temp                                                         //
│  │  ├─ test.csv                                                  //
│  │  └─ train.csv                                                 //
├─ myapp.log                                                       //
├─ README.md                                                       //
├─ run.py                                                          //
├─ spacy                                                           //
│  ├─ .DS_Store                                                    //
│  └─ create_model.py                                              //
├─ reports                           //
│  ├─ abstract.md                    //
│  ├─ demo.md                        //
│  ├─ discussion.md                  //
│  ├─ figures                        //
│  │  └─ logo_png.png                //
│  ├─ intro.md                       //
│  ├─ introduction.md                //
│  ├─ methods.md                     //
│  ├─ requirements_jb.txt            //
│  ├─ results.md                     //
│  ├─ _config.yml                    //
│  └─ _toc.yml                       //
├─ src                                                             //
│  ├─ data                                                         //
│  │  └─ make_dataset.py                                           //
│  ├─ test.py                                                      //
│  ├─ train.py                                                     //
│  ├─ utils                                                        //
│  │     └─ download_models.py                                     //
├─ submission.json                                                 //
├─ test                                                            //
│  └─ testdata                                                     //
│     └─ test.csv                                                  //
├─ twitter                                                         //
│  ├─ pull_tweets.py                                               //
│  └─ twitter_credentials.py                                       //
├─ _requirements.txt                                               //
└─ _run.py                                                         //
```

