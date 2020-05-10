import abc


class SCStemmer:
    def __init__(self):
        pass
    """
    Stemmer class.
    """
    @abc.abstractmethod
    def stem_word(self, word):
        """
        Stem word.
        :param word: the input word
        :return: the stemmed word
        """
        raise NotImplemented("Please Implement this method.")

    @abc.abstractmethod
    def stem_line(self, line):
        """
        Stem line.
        :param line: the input line
        :return: the stemmed line
        """
        raise NotImplemented("Please Implement this method.")

    def stem_file(self, input_file_path, output_file_path):
        """
        Stem txt file.
        :param input_file_path: the input file path
        :param output_file_path: the output file path
        :return: the stemmed file
        """
        with open(input_file_path, 'r', encoding='UTF-8') as file:
            text = file.read()
        stemmed = self.stem_text(text)
        with open(output_file_path, 'w', encoding='UTF-8') as file:
            file.write(stemmed)

    def stem_text(self, text):
        """
        Stem text.
        :param text: the input text
        :return: the stemmed text
        """
        output = ''
        for line in text.split('\n'):
            output += "%s\n" % self.stem_line(line)
        return output

    def stem(self, word):
        """
        Stem word.
        :param word: the input word
        :return: the stemmed word
        """
        return self.stem_word(word)