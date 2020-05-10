from ljubesic_pandzic_stemmer import LjubesicPandzicStemmer
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input_file_path', type=str, help='Path to the input file')
parser.add_argument('output_file_path', type=str, help='Path to the output file')

if __name__ == '__main__':
    args = parser.parse_args()

    input_path = args.input_file_path
    output_path = args.output_file_path

    print("Stemming started...")
    stemmer = LjubesicPandzicStemmer()
    stemmer.stem_file(input_path, output_path)
    print("Stemming successfully completed!")