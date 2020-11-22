from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import random
import os
import pandas as pd
import numpy as np
import json
from .config import model_name
from transformers import (
    AutoTokenizer,
)
output_dir = os.path.join(os.path.dirname(__file__), 'model')
tokenizer = AutoTokenizer.from_pretrained(model_name)
# config = AutoConfig.from_pretrained(
#     output_dir,
#     num_labels=3,
# )
# if os.path.isdir(output_dir):
    # model = AutoModelForTokenClassification.from_pretrained(output_dir, config=config)
    # model.eval()

app = Flask(__name__, template_folder=os.path.dirname(__file__))
CORS(app)


@app.route('/')
def hello_world():
    return render_template('index.html')


def get_train_df():
    if os.path.isfile('train.csv'):
        target_df = pd.read_csv('train.csv', index_col=None)
    else:
        target_df = pd.DataFrame()
    return target_df


@app.route('/random_entry', methods=['GET'])
def get_random_entry():
    source_df = pd.read_json('reviews_amazon_laptop.json')
    target_df = get_train_df()

    source_list = np.unique(source_df['text'])
    random_entry = random.choice(source_list)
    if 'text' in target_df:
        while random_entry in target_df['text']:
            random_entry = random.choice(source_list)

    # with torch.no_grad():
    #     ids = tokenizer(random_entry, return_tensors="pt")
    #     probs = model(**ids)[0]
    #     result_cls = int(torch.argmax(probs))

    return jsonify({
        'text': tokenizer.tokenize(random_entry.strip()),
        # 'class': result_cls,
        # 'probs': probs.detach().numpy().tolist()[0],
    })


@app.route('/submit_entry', methods=['POST'])
def submit_result():
    data = request.json
    target_df = get_train_df()    

    new_df = target_df.append(pd.Series({
        'text': json.dumps(data['text']),
        'class': json.dumps(data['class']),
    }), ignore_index=True)
    new_df.to_csv('train.csv', index=False)

    return jsonify({
        'count': len(new_df),
    })
