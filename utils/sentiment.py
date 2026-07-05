from transformers import pipeline

classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")

def analyze_sentiment(text):
    result = classifier(text)
    return result[0]