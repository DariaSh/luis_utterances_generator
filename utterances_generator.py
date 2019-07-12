import json
import itertools


class UtterancesGenerator:

    def __init__(self, test=False):
        self.test = test

        self.json_keys = {"text_key":"text",
                          "intent_key":"intentName",
                          "entities_key": "entityLabels",
                          "entity_key" : "entityName",
                          "start_key" : "startCharIndex",
                          "end_key" : "endCharIndex"}
        if self.test:
            self.json_keys = {"text_key": "text",
                              "intent_key": "intent",
                              "entities_key": "entities",
                              "entity_key": "entity",
                              "start_key": "startPos",
                              "end_key": "endPos"}
            self.max_test_size = 1000

    def get_item_list(self, utterance_item):
        return utterance_item.split('|')

    def build_intent_utterances(self, intent, utterances, entities):
        for utterance in utterances:
            ut_dict = {}
            ut_text = ' '.join(word for word in utterance)
            ut_text = str.strip(ut_text)
            ut_text = str.replace(ut_text, '  ', ' ')
            ut_dict[self.json_keys["text_key"]] = ut_text
            ut_dict[self.json_keys["intent_key"]] = intent
            ut_dict[self.json_keys["entities_key"]] = []
            for ent in entities.keys():
                ent_words = entities[ent]
                for ent_word in ent_words:
                    if ent_word in ut_text:
                        start_i = str.find(ut_text, ent_word)
                        end_i = start_i + len(ent_word)
                        ut_dict[self.json_keys["entities_key"]].append({
                            self.json_keys["entity_key"]: ent,
                            self.json_keys["start_key"]: start_i,
                            self.json_keys["end_key"]: end_i})
            yield ut_dict

    def process_input(self, intent_input):
        intent = str.strip(intent_input.split(':')[0])
        utterance_items = intent_input.split('{')[1:]
        utterance_set = []
        entities_set = {}
        for i, item in enumerate(utterance_items):
            item = str.replace(item, '}', '')
            if ':' not in item:
                utterance_set.append(self.get_item_list(item))
            else:
                ent = item.split(':')
                ent_key = str.strip(ent[1])
                entities_set[ent_key] = []
                ent_words = self.get_item_list(ent[0])
                entities_set[ent_key] += ent_words
                utterance_set.append(ent_words)
            print("processed " + str(i) + " utterance items")
        comb = itertools.product(*utterance_set)
        return self.build_intent_utterances(intent, comb, entities_set)

    def generate_utterances(self, input_file):
        print ("Processing your input...")
        with open(input_file) as fin:
            for line in fin.readlines():
                yield from self.process_input(line)

    def write_utterances_json(self, input_file, output_file):
        with open(output_file, 'a') as fout:
            fout.write('[')
            for i, x in enumerate(self.generate_utterances(input_file)):
                if i !=0:
                    fout.write(', ')
                if i % 100 == 0:
                    print ("writing item " + str(i))
                if self.test and i == self.max_test_size:
                    break
                fout.write(json.dumps(x))
            fout.write(']')
        print ("Processing completed! Check your json.")
