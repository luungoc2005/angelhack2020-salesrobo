from datetime import datetime
import json
import pickle
import random
from os import path
from flask import (
    Blueprint, jsonify, request, 
)
from werkzeug.exceptions import (
    NotFound,
    BadRequest,
)
import numpy as np
from werkzeug.utils import secure_filename
from urllib.request import pathname2url

from .search import _search_comments

bp = Blueprint('product-features', __name__, url_prefix='/product-features')
CACHE_PATH = path.join(path.dirname(__file__), '_product_features_cache.pickle')
RESULTS_LIMIT = 20
MAX_EVAL_REVIEWS = 50
label_list = [
    "O", # Outside of a named entity
    "B-POS", # Beginning of positive property
    "I-POS", # positive property
    "B-NEG", # Beginning of negative property
    "I-NEG", # negative property
]
model_name = "bert-base-uncased"
output_dir = path.join(path.dirname(__file__), 'model') 

# NLP
from transformers import (
    AutoModelForTokenClassification, 
    AutoTokenizer,
    AutoConfig,
    Trainer,
    TrainingArguments,
)
import torch
import json
import pandas as pd
import numpy as np
from torch.utils.data import Dataset
import os
import random

model = None # AutoModelForTokenClassification.from_pretrained(output_dir)
tokenizer = None # AutoTokenizer.from_pretrained(output_dir)

def detokenize(tokens):
    def is_subtoken(word):
        if word[:2] == "##":
            return True
        else:
            return False

    restored_text = []
    for i in range(len(tokens)):
        if not is_subtoken(tokens[i]) and (i+1)<len(tokens) and is_subtoken(tokens[i+1]):
            restored_text.append(tokens[i] + tokens[i+1][2:])
            if (i+2)<len(tokens) and is_subtoken(tokens[i+2]):
                restored_text[-1] = restored_text[-1] + tokens[i+2][2:]
        elif not is_subtoken(tokens[i]):
            restored_text.append(tokens[i])
    return ' '.join(restored_text)

def infer_predict(tag_seq_batch, sent_batch, ix_to_tag):
    result = []

    for sent_ix, tokens_in in enumerate(sent_batch):
        tag_seq = [ix_to_tag[int(tag)] for tag in tag_seq_batch[sent_ix]]


        entities = {}
        entity_name = ''
        buffer = []

        for idx, tag_name in enumerate(tag_seq):
            if len(tag_name) > 2 and tag_name[:2] in ['B-', 'I-']:
                new_entity_name = tag_name[2:]
                if entity_name != '' and \
                        (tag_name[:2] == 'B-' or entity_name != new_entity_name):
                    # Flush the previous entity
                    if entity_name not in entities:
                        entities[entity_name] = []
                        entities[entity_name].append(detokenize(buffer))
                        buffer = []

                entity_name = new_entity_name

            # If idx is currently inside a tag
            if entity_name != '':
                # Going outside the tag
                if idx == len(tag_seq) - 1 or \
                        tag_name == '-' or \
                        tag_name == 'O':

                    # if end of tag sequence then append the final token
                    if idx == len(tag_seq) - 1 and tag_name != '-':
                        buffer.append(tokens_in[idx])

                    if entity_name not in entities:
                        entities[entity_name] = []
                    entities[entity_name].append(detokenize(buffer))
                    buffer = []
                    entity_name = ''
                else:
                    buffer.append(tokens_in[idx])

        # return [entities]
        result.append([{ 'name': key, 'values': value } for key, value in entities.items()])

    return result


@bp.route('/', methods=('GET',))
def get_recommended_features():
    global model, tokenizer

    query = request.args.get('q')

    cache = {}
    result = {}
    if path.isfile(CACHE_PATH):
        with open(CACHE_PATH, 'rb') as fp:
            cache = pickle.load(fp)
    if query in cache:
        result = cache[query]

    else:
        data = _search_comments(query)[-MAX_EVAL_REVIEWS:]

        if model is None:
            model = AutoModelForTokenClassification.from_pretrained(output_dir)
            tokenizer = AutoTokenizer.from_pretrained(output_dir)
            model.eval()

        data = [item['text'] for item in data]
        positives = []
        negatives = []

        for entry in data:
            tokens = tokenizer.tokenize(entry)
            with torch.no_grad():
                ids = tokenizer(entry, 
                    return_tensors="pt", 
                    max_length=128,
                    truncation=True
                )
                probs = model(**ids)[0]
                result_cls = torch.argmax(probs, axis=-1)[0][1:]

            max_length = min(len(tokens), len(result_cls))

            ix_to_tag = {}
            for ix in range(len(label_list)):
                ix_to_tag[ix] = label_list[ix]

            tokens = tokens[:max_length]
            result_cls = result_cls[:max_length]

            preds = infer_predict([result_cls], [tokens], ix_to_tag)[0]
            for item in preds:
                if item['name'] == 'POS':
                    positives.extend(item['values'])
                else:
                    negatives.extend(item['values'])
        
        result = {
            "positives": positives,
            "negatives": negatives,
        }
        cache[query] = result

        with open(CACHE_PATH, 'wb') as fp:
            pickle.dump(cache, fp)

    result["positives"] = result["positives"][:RESULTS_LIMIT]
    result["negatives"] = result["negatives"][:RESULTS_LIMIT]
    return jsonify(result)