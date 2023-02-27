# 2. Introduction

In recent years, deep learning has revolutionized the development of intelligent systems in many fields especially in Natural Language Processing (NLP) using state-of-the-art architectures that significantly improved many NLP tasks. With the recent progress made in NLP, researchers are starting to pay more attention to tackling numerous tasks in finance. As the amount of textual content generated in the financial domain is growing at an exponential rate, natural language processing is becoming a strategic tool for financial analysis. For example, financial practitioners are often required to use a set of NLP techniques, such as financial text classification and sentimental analysis for risk assessment, stock investment, and market trend detection.
Some of the researchers construct an end-to-end model for making the prediction. Sentiment analysis approaches are more common in this field, thus providing insights on financial decision-making. Such models include VAE, Capsule network, hybrid attention network, BERT, XLNet, etc.

While Transformer based language models are widely used for product understanding, as well as market trend prediction. The most used NLP sentiment analysis method is polarity, which classifies the input text as positive, neutral, or negative. BERT (Bidirectional Encoder Representations from Transformers) is an open-source Machine Learning (ML) model for NLP well-used for classification. However, BERT is pre-trained on general English corpora, and the financial domain has its technical jargon, which can lead to an output misinterpretation. Therefore, it’s not suitable for understanding domain-specific vocabulary. Nonetheless, FinBERT, based on the BERT model, fills the gap with a domain-specific terminology by overlapping BERT vocabulary (BaseVocab) for another (FinVocab). As the industry developed and transformer architecture being widely used, in order to standardize all the steps involved in training and using a language model, Hugging Face was founded. They’re democratizing NLP by constructing an API that allows easy access to pretrained models, datasets and tokenizing steps. Within HuggingFace, Transformers was build as an open-source library with the goal of opening up these advances to the wider machine learning community.

There are other open source libraries such as Spacy that are very helpful in creating fine-
tuned models specific for NLP tasks. Spacy uses a CNN and can perform a wide variety of tasks such as tokenization, part of speech tagging, named entity recognition, sentiment analysis, and so much more. In terms of financial applications, a Spacy model can be trained to pull keywords out of tweets and determine popularity of certain stocks and decide whether to invest or not using that information or a combination of stock history/data. Most Spacy models use word vectors, representations of different words that allow you to compare similarities between other words, in order to accurately take into account all parts of the sentence. In addition, this project will also include useful tools for financial users to utilize, in order to better capture the market trend and avoid risks. Particularly, scraping tools for tweets regarding companies will be prepared, while we will build tools for scraping federal financial reports as well. Therefore, users can identify risk factors as well as catch market sentiment in real time, thus better assisting financial decisions.
Our contributions can be summarized as follows:
* Collect financial related manually sentiment labeled data for training
* Construct handful tweets scraping tool
* Polarize part of real time tweets text using Spacy to expand training dataset
* Fine-tune 5 popular transformers based on pre-trained models in HuggingFace
    * Bert
    * FinBert
    * Financial Bert
    * XLNet
    * GPT2
* Build handy pipelines and APIs to retrieve financial information from Twitter to detect
* stock related sentiment.