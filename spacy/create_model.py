import spacy
import pandas as pd
from tqdm import tqdm
from spacy.tokens import DocBin
from sklearn.model_selection import train_test_split

#Code adapted from https://www.machinelearningplus.com/nlp/custom-text-classification-spacy/

#This is uploaded to show what we did but is not used in the testing part of the data
data = pd.read_csv("shuffled_data.csv")
nlp = spacy.load("en_core_web_lg")

def make_docs(data):
    docs = []
    #Label the data based on the file
    for doc, label in tqdm(nlp.pipe(data, as_tuples=True), total = len(data)):
        if label == 1:
            doc.cats["positive"] = 1
            doc.cats["neutral"] = 0
            doc.cats["negative"] = 0
        elif label == 0:
            doc.cats["positive"] = 0
            doc.cats["neutral"] = 1
            doc.cats["negative"] = 0
        else:
            doc.cats["positive"] = 0
            doc.cats["neutral"] = 0
            doc.cats["negative"] = 1
        docs.append(doc)
    return docs

#Make training data in Spacy format
train_docs = make_docs(list(data[:15000].itertuples(index=False, name=None)))
doc_bin = DocBin(docs=train_docs)
doc_bin.to_disk("./data/train.spacy")

#Make validation data in Spacy format
valid_docs = make_docs(list(data[15000:].itertuples(index=False, name=None)))
doc_bin = DocBin(docs=valid_docs)
doc_bin.to_disk("./data/valid.spacy")
