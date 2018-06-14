# Some functions for processing strings with NLP

from nltk.corpus import stopwords
import string


class NLProcessor:

    def __init__(self):
        # Build stop word list, including punctuation and "rt", "via"

        punctuation = list(string.punctuation + '¡¿“”')
        self.stop = stopwords.words('spanish') + punctuation + ['via', 'rt'] # Delete 'rt' if necessary

    def rem_stop_words(self, s):
        # Removes stop words

        terms_stop = [term for term in s if term not in self.stop]
        return terms_stop
