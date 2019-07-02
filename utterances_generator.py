import json
import argparse
import itertools

def get_item_list(utterance_item):
    return utterance_item.split('|')

def build_intent_utterances(intent, utterances, entities):
    intent_utterances = []
    for utterance in utterances:
        ut_dict = {}
        ut_text = ' '.join(word for word in utterance)
        ut_text = str.strip(ut_text)
        ut_text = str.replace(ut_text, '  ', ' ')
        ut_dict["text"] = ut_text
        ut_dict["intentName"] = intent
        ut_dict["entityLabels"] = []
        for ent in entities.keys():
            ent_words = entities[ent]
            for ent_word in ent_words:
                if ent_word in ut_text:
                    start_i = str.find(ut_text, ent_word)
                    end_i = start_i + len(ent_word)
                    ut_dict["entityLabels"].append({
                        "entityName": ent,
                        "startCharIndex": start_i,
                        "endCharIndex": end_i})
        intent_utterances.append(ut_dict)
    return intent_utterances


def process_input(intent_input):
    intent = str.strip(intent_input.split(':')[0])
    utterance_items = intent_input.split('{')[1:]
    utterance_set = []
    entities_set = {}
    for item in utterance_items:
        item = str.replace(item, '}', '')
        if ':' not in item:
            utterance_set.append(get_item_list(item))
        else:
            ent = item.split(':')
            ent_key = str.strip(ent[1])
            entities_set[ent_key] = []
            ent_words = get_item_list(ent[0])
            entities_set[ent_key] += ent_words
            utterance_set.append(ent_words)
    comb = list(itertools.product(*utterance_set))
    return build_intent_utterances(intent, comb, entities_set)


def generate_utterances(input_file, output_file, n_utterances=100):
    i_u_collection = []
    with open(input_file) as fin:
        iu_lines = fin.readlines()
        for line in iu_lines:
            if len(line) > 0:
                i_u_collection.append(process_input(line))
    result = [val for sublist in i_u_collection for val in sublist]
    with open(output_file, 'w') as fout:
        json.dump(result[:n_utterances], fout)


if __name__ == '__main__':
     parser = argparse.ArgumentParser()
     parser.add_argument('--input', help='input file', required=True)
     parser.add_argument('--output', help='output json file', required=True)
     args = parser.parse_args()
     generate_utterances(args.input, args.output)
