import os

label_list = [
    "O", # Outside of a named entity
    "B-POS", # Beginning of positive property
    "I-POS", # positive property
    "B-NEG", # Beginning of negative property
    "I-NEG", # negative property
]

model_name = "bert-base-uncased"

output_dir = os.path.join(os.path.dirname(__file__), 'model') 