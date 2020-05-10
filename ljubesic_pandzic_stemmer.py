import re

from transliterate import translit

from constants import stop_words, word_patterns, transformations
from sc_stemmer import SCStemmer


class LjubesicPandzicStemmer(SCStemmer):
    """
    Implementation of Ljubesic-Pandzic stemmer.
    """

    def stem_word(self, word):
        """
        Stem word.
        :param word: the input word
        :return: the stemmed word
        """
        word = translit(word, 'sr', reversed=True)
        if word.lower() in stop_words:
            return word
        else:
            stemmed = self._transform(word)
            for wp in word_patterns:
                match = re.match(wp, stemmed)
                if match and self._has_vowel(match.group(1)) and len(match.group(1)) > 1:
                    return match.group(1)
        return stemmed

    def stem_line(self, line):
        """
        Stem line.
        :param line: the input line
        :return: the stemmed line
        """
        words = re.split(r'\b', line)
        st = [self.stem_word(word) for word in words]
        return "".join(st).strip()

    def _transform(self, word):
        """
        Transform the word.
        :param word: the input word
        :return: the transformed word
        """
        for t in transformations:
            if word.endswith(t):
                return "%s%s" % (word[0:len(word) - len(t)], transformations[t])
        return word

    def _capitalize_syllabic_r(self, word):
        """
        Check if word has 'r'  character surrounded with consonants.
        :param word: the input word
        :return: True if word has 'r' surrounded with consonats, otherwise False
        """
        return re.sub("(^|[^aeiou])r($|[^aeiou])", r"\1R\2", word)

    def _has_vowel(self, word):
        """
        Check if word has vowel.
        :param word: the input word
        :return: True if word has a vowel, otherwise False
        """
        vowel_pattern = re.compile('[aeiouR]')
        return bool(vowel_pattern.search(self._capitalize_syllabic_r(word)))


if __name__ == '__main__':
    w1 = 'ukuse'
    w2 = 'trčati'
    w3 = 'tračara'
    w4 = 'kgb'
    l1 = 'malodušni čoveče'

    stemmer = LjubesicPandzicStemmer()
    print("Transform %s: %s" % (w1, stemmer._transform(w1)))
    print("Capitalize r in word %s: %s" % (w2, stemmer._capitalize_syllabic_r(w2)))
    print("Capitalize r in word %s: %s" % (w3, stemmer._capitalize_syllabic_r(w3)))
    print("Word %s has vowel: %s" % (w2, stemmer._has_vowel(w2)))
    print("Word %s has vowel: %s" % (w4, stemmer._has_vowel(w4)))
    print("Stemmed line %s: %s" % (l1, stemmer.stem_line(l1)))
