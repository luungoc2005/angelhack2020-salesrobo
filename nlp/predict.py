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
from config import label_list, model_name, output_dir
import random

model = AutoModelForTokenClassification.from_pretrained(output_dir)
tokenizer = AutoTokenizer.from_pretrained(output_dir)


source_df = pd.read_json('reviews_amazon_lipstick.json')

source_list = np.unique(source_df['text'])

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

def infer_predict(tag_seq_batch, sent_batch, ix_to_tag, delimiter=''):
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
                        entities[entity_name].append(delimiter.join(buffer))
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
                    entities[entity_name].append(delimiter.join(buffer))
                    buffer = []
                    entity_name = ''
                else:
                    buffer.append(tokens_in[idx])

        # return [entities]
        result.append([{ 'name': key, 'values': value } for key, value in entities.items()])

    return result

if __name__ == '__main__':
    for entry in source_list:
        tokens = tokenizer.tokenize(entry)
        with torch.no_grad():
            ids = tokenizer(entry, return_tensors="pt", max_length=128)
            probs = model(**ids)[0]
            result_cls = torch.argmax(probs, axis=-1)[0][1:]

        positives = []
        negatives = []
        max_length = min(len(tokens), len(result_cls))
        running_word = []
        running_type = 0

        ix_to_tag = {}
        for ix in range(len(label_list)):
            ix_to_tag[ix] = label_list[ix]

        tokens = tokens[:max_length]
        result_cls = result_cls[:max_length]

        preds = infer_predict([result_cls], [tokens], ix_to_tag)[0]

        if len(preds) > 0:
            print(preds)