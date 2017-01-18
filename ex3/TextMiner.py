import matplotlib.pyplot as plt
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


def get_txt(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf8') as f:
        return f.read()


def get_tokens_freq(txt: str, remove_stop: bool, stem: bool) -> Counter:
    """
    return counter contains the frequency of words in a given text
    """
    if remove_stop:
        stop_words = stopwords.words('english')
        txt = ' '.join([word for word in pp_txt.split() if word not in stop_words])

    if stem:
        stemmer = PorterStemmer()
        txt = ' '.join([stemmer.stem(word) for word in pp_txt.split()])

    count = Counter()
    sents = sent_tokenize(txt)  # word_tokenize works best for sentences
    for sent in sents:
        count.update(word_tokenize(sent))
    return count


def plot_freq_of_freq(freq: Counter, title: str) -> None:
    """
    plot and save the graph of frequency word as function of their rank
    """
    freq_of_freq = Counter(freq.values())
    plt.figure()
    plt.title(title)
    plt.loglog(list(freq_of_freq.keys()), list(freq_of_freq.values()), 'b.')
    plt.ylabel('Frequency')
    plt.xlabel('Rank')
    plt.savefig(title + '.jpg')
    plt.show()


# article b:
pp_txt = get_txt('pp.txt')
pp_txt = ' '.join([word for word in pp_txt.split() if word.isalnum()])  # just clean non-alphanumeric
# raw_freq = get_tokens_freq(pp_txt, False, False)
# print(raw_freq.most_common(20))
# plot_freq_of_freq(raw_freq, 'Raw Tokens')


# article c:
# freq_without_stops = get_tokens_freq(pp_txt, True, False)
# print(freq_without_stops.most_common(20))
# plot_freq_of_freq(freq_without_stops, 'Tokens Without Stopwords')


# article d:
# freq_after_stemming = get_tokens_freq(pp_txt, False, True)
# print(freq_after_stemming.most_common(20))
# plot_freq_of_freq(freq_after_stemming, 'Tokens After Stemming')


