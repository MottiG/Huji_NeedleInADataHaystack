import nltk


tokens = []

with open('pp.txt', 'r', encoding='utf8') as f:
    raw = f.read()
    tok = nltk.word_tokenize(raw)
