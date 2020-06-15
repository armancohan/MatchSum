import os
from os.path import exists, join
import json

def read_jsonl(path):
    data = []
    with open(path) as f:
        for line in f:
            data.append(json.loads(line))
    return data

def get_data_path(train_path, dev_path, test_path):
    paths = {}
    paths['train'] = train_path
    paths['val']   = dev_path
    paths['test']  = test_path
    return paths

def get_result_path(save_path, cur_model, prefix=''):
    result_path = join(save_path, f'../result{prefix}')
    if not exists(result_path):
        os.makedirs(result_path)
    model_path = join(result_path, cur_model)
    if not exists(model_path):
        os.makedirs(model_path)
    dec_path = join(model_path, 'dec')
    ref_path = join(model_path, 'ref')
    os.makedirs(dec_path)
    os.makedirs(ref_path)
    return dec_path, ref_path
