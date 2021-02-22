# python -m venv venv
# .\venv\Scripts\activate
# pip install -r requirements.txt

from flask import Flask, request, jsonify, make_response
# from waitress import serve
import re
import nltk
import heapq
import json
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def index():
    article_text = request.form.get("message")
    print("*"*15, " Unsummarized Article", "*"*15)
    print(article_text)

    # Preprocessing
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)

    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(article_text)
    # print(sentence_list)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1


    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    print("*"*15, "Summary","*"*15)
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = " ".join(summary_sentences)
    print(summary)
    key = "summary"
    msg_return = {key : summary}
    print(msg_return)
    return summary

if __name__ == "__main__":
    # serve(app, host='192.168.43.212')
    app.run(host='0.0.0.0', port=5000)
