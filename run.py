#!/usr/bin/env python
 
import sys
import json
import pandas as pd

sys.path.insert(0, 'src')
from etl import get_data, save_data

def main(targets):

    data_config = json.load(open('config/config.json'))

    if 'test' in targets:

        data = get_data(data_config)
        save_data(data_config, data) #load and train the model with test_load data
        # return print("test ok")
        return

    elif 'run' in targets:

        return print("run ok")

    else:

        return print("error target")

if __name__ == '__main__':

    targets = sys.argv[1:]
    # targets = 'testdata'
    main(targets)