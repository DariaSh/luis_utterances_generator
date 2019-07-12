import argparse
from  utterances_generator import UtterancesGenerator

if __name__ == '__main__':
     parser = argparse.ArgumentParser()
     parser.add_argument('--input', help='input file', required=True)
     parser.add_argument('--output', help='output json file', required=True)
     args = parser.parse_args()
     generator = UtterancesGenerator(test=False)
     generator.write_utterances_json(args.input, args.output)
