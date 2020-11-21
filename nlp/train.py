from transformers import (
    AutoModelForTokenClassification, 
    AutoTokenizer,
    AutoConfig,
    Trainer,
    TrainingArguments,
)
import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset
import os
from .config import label_list, model_name

model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

max_seq_length=128
train_test_split=.2
df = pd.read_csv('train.csv', index_col=None)

df['type'] = np.where(np.random.rand(len(df)) > train_test_split, 'train', 'test')


class TextDataset(Dataset):
    def __init__(self, tokenizer, data_type='train'):
        super(TextDataset).__init__()
        self.data_type = data_type
        self.data = df[df['type'] == self.data_type]
        self.tokenizer = tokenizer

        self.encodings = self.tokenizer(
            list(self.data['text']),
            truncation=True,
            max_length=max_seq_length,
            padding="max_length",
        )
        self.labels = list(self.data['class'])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item


def compute_metrics(p):
    preds = np.argmax(p.predictions, axis=1)

    return {"acc": (preds == p.label_ids).mean()}

config = AutoConfig.from_pretrained(
    model_name,
    num_labels=len(label_list),
)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name, config=config)
output_dir = os.path.join(os.path.dirname(__file__), 'model') 
args = TrainingArguments(
    output_dir,
    num_train_epochs=15,
    per_device_train_batch_size=8,
    load_best_model_at_end=True,
    learning_rate=5e-6,
)

train_dataset = TextDataset(tokenizer, 'train')
eval_dataset = TextDataset(tokenizer, 'test')

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

trainer.train()
trainer.save_model()
tokenizer.save_pretrained(output_dir)


print("*** Evaluate ***")

from datetime import datetime

result = trainer.evaluate()
result['timestamp'] = datetime.now().timestamp()
result['train_size'] = len(train_dataset)
result['eval_size'] = len(eval_dataset)
output_eval_file = os.path.join(output_dir, f"eval_results_{datetime.now().timestamp()}.txt")

results = {}
with open(output_eval_file, "w") as writer:
    print("***** Eval results *****")

    for key, value in result.items():
        print("  %s = %s" % (key, value))
        writer.write("%s = %s\n" % (key, value))

    results.update(result)