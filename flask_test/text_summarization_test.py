import bs4 as bs
import urllib.request
import re
import nltk

nltk.download('punkt')
nltk.download('stopwords')

article_text = """
Once, there was a boy who became bored when he watched over the village sheep grazing on the hillside. To entertain himself, he sang out, “Wolf! Wolf! The wolf is chasing the sheep!”

When the villagers heard the cry, they came running up the hill to drive the wolf away. But, when they arrived, they saw no wolf. The boy was amused when seeing their angry faces.

“Don’t scream wolf, boy,” warned the villagers, “when there is no wolf!” They angrily went back down the hill.

Later, the shepherd boy cried out once again, “Wolf! Wolf! The wolf is chasing the sheep!” To his amusement, he looked on as the villagers came running up the hill to scare the wolf away.

As they saw there was no wolf, they said strictly, “Save your frightened cry for when there really is a wolf! Don’t cry ‘wolf’ when there is no wolf!” But the boy grinned at their words while they walked grumbling down the hill once more.

Later, the boy saw a real wolf sneaking around his flock. Alarmed, he jumped on his feet and cried out as loud as he could, “Wolf! Wolf!” But the villagers thought he was fooling them again, and so they didn’t come to help.

At sunset, the villagers went looking for the boy who hadn’t returned with their sheep. When they went up the hill, they found him weeping.

“There really was a wolf here! The flock is gone! I cried out, ‘Wolf!’ but you didn’t come,” he wailed.

An old man went to comfort the boy. As he put his arm around him, he said, “Nobody believes a liar, even when he is telling the truth!”
"""
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
                    
import heapq

print("*"*15, "Summary","*"*15)
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)
print(summary)