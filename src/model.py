import numpy as np
import evaluate
from transformers import pipeline
from transformers import AutoTokenizer

from transformers import AutoModelForSequenceClassification #for PyTorch
from transformers import TrainingArguments

model = AutoModelForSequenceClassification.from_pretrained("bert-base-cased", num_labels=5)

training_args = TrainingArguments(output_dir="test_trainer")


# classifier = pipeline(model="facebook/bart-large-mnli")
# classifier(
#     "I have a problem with my iphone that needs to be resolved asap!!",
#     candidate_labels=["urgent", "not urgent", "phone", "tablet", "computer"],
# )

# # warning! Preprocess before train the model
# tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
# sentence = "Do not meddle in the affairs of wizards, for they are subtle and quick to anger."
# encoded_input = tokenizer(sentence, padding=True, truncation=True)

# print(encoded_input)


# load data and pipeline

# tokenizer and padding

# PyTorch tensor



