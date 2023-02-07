#!/usr/bin/env python
 
import sys
import json
import pandas as pd
import csv
from sklearn.model_selection import train_test_split



sys.path.insert(0, 'src')
from etl import get_data, save_data

def main(targets):

    data_config = json.load(open('config/config.json'))

    if 'test' in targets:

        data = get_data(data_config)
        save_data(data_config, data) #load and train the model with test_load data
        return

    # elif 'etl' in targets:

    #     return

    # else:

    #     return

if __name__ == '__main__':

    targets = sys.argv[1:]
    # targets = 'testdata'
    main(targets)