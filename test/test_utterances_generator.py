import os
import json
import unittest
from utterances_generator import UtterancesGenerator

EXPECTED_FULL_CONTENT = [{"text": "Which language can you speak", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]},
                       {"text": "Which language can you speak ?", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]},
                       {"text": "Which language can you understand", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]},
                       {"text": "Which language can you understand ?", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]},
                       {"text": "Which language do you speak", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]},
                       {"text": "Which language do you speak ?", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]},
                       {"text": "Which language do you understand", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]},
                       {"text": "Which language do you understand ?", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]},
                       {"text": "What language can you speak", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 5, "endCharIndex": 13}]},
                       {"text": "What language can you speak ?", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 5, "endCharIndex": 13}]},
                       {"text": "What language can you understand", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 5, "endCharIndex": 13}]},
                       {"text": "What language can you understand ?", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 5, "endCharIndex": 13}]},
                       {"text": "What language do you speak", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 5, "endCharIndex": 13}]},
                       {"text": "What language do you speak ?", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 5, "endCharIndex": 13}]},
                       {"text": "What language do you understand", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 5, "endCharIndex": 13}]},
                       {"text": "What language do you understand ?", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 5, "endCharIndex": 13}]}]

EXPECTED_FULL_TEST_CONTENT = [{"text": "Which language can you speak", "intent": "BotLanguage",
                        "entities": [{"entity": "botLang", "startPos": 6, "endPos": 14}]},
                       {"text": "Which language can you speak ?", "intent": "BotLanguage",
                        "entities": [{"entity": "botLang", "startPos": 6, "endPos": 14}]},
                       {"text": "Which language can you understand", "intent": "BotLanguage",
                        "entities": [{"entity": "botLang", "startPos": 6, "endPos": 14}]},
                       {"text": "Which language can you understand ?", "intent": "BotLanguage",
                        "entities": [{"entity": "botLang", "startPos": 6, "endPos": 14}]},
                       {"text": "Which language do you speak", "intent": "BotLanguage",
                        "entities": [{"entity": "botLang", "startPos": 6, "endPos": 14}]},
                       {"text": "Which language do you speak ?", "intent": "BotLanguage",
                        "entities": [{"entity": "botLang", "startPos": 6, "endPos": 14}]},
                       {"text": "Which language do you understand", "intent": "BotLanguage",
                        "entities": [{"entity": "botLang", "startPos": 6, "endPos": 14}]},
                       {"text": "Which language do you understand ?", "intent": "BotLanguage",
                        "entities": [{"entity": "botLang", "startPos": 6, "endPos": 14}]},
                       {"text": "What language can you speak", "intent": "BotLanguage",
                        "entities": [{"entity": "botLang", "startPos": 5, "endPos": 13}]},
                       {"text": "What language can you speak ?", "intent": "BotLanguage",
                        "entities": [{"entity": "botLang", "startPos": 5, "endPos": 13}]},
                       {"text": "What language can you understand", "intent": "BotLanguage",
                        "entities": [{"entity": "botLang", "startPos": 5, "endPos": 13}]},
                       {"text": "What language can you understand ?", "intent": "BotLanguage",
                        "entities": [{"entity": "botLang", "startPos": 5, "endPos": 13}]},
                       {"text": "What language do you speak", "intent": "BotLanguage",
                        "entities": [{"entity": "botLang", "startPos": 5, "endPos": 13}]},
                       {"text": "What language do you speak ?", "intent": "BotLanguage",
                        "entities": [{"entity": "botLang", "startPos": 5, "endPos": 13}]},
                       {"text": "What language do you understand", "intent": "BotLanguage",
                        "entities": [{"entity": "botLang", "startPos": 5, "endPos": 13}]},
                       {"text": "What language do you understand ?", "intent": "BotLanguage",
                        "entities": [{"entity": "botLang", "startPos": 5, "endPos": 13}]}]

class TestUtterancesGenerator(unittest.TestCase):

    def test_get_item_list(self):
        expected = ["option1", "option2", "option3"]
        generator = UtterancesGenerator(test=False)
        result = generator.get_item_list("option1|option2|option3")
        self.assertEqual(expected, result)
        generator = UtterancesGenerator(test=True)
        result = generator.get_item_list("option1|option2|option3")
        self.assertEqual(expected, result)

    def compare_build_intent_results(self, intent, utterance, entities, expected, test=False):
        generator = UtterancesGenerator(test=test)
        result = list(generator.build_intent_utterances(intent, [utterance.split(" ")], entities))[0]
        self.assertDictEqual(expected, result)

    def test_build_intent_utterances(self):
        intent = "testIntent"
        utterance = "This is test my text"
        entities = {"testEntity_1": ["text"]}

        expected = {"text": utterance,
                    "intentName": intent,
                    "entityLabels" : [
                        {
                        "entityName": list(entities.keys())[0],
                        "startCharIndex": 16,
                        "endCharIndex" : 20}
                    ]}
        self.compare_build_intent_results(intent, utterance, entities, expected, test=False)

    def test_build_test_intent_utterances(self):
        intent = "testIntent"
        utterance = "This is test my text"
        entities = {"testEntity_1": ["text"]}

        expected = {"text": utterance,
                    "intent": intent,
                    "entities" : [
                        {
                        "entity": list(entities.keys())[0],
                        "startPos": 16,
                        "endPos" : 20}
                    ]}
        self.compare_build_intent_results(intent, utterance, entities, expected, test=True)

    def compare_process_input(self, expected, test=False):
        intent_input = "BotLanguage:{Which|What}{language:botLang}{can you|do you}{speak|understand}{|?}"
        generator = UtterancesGenerator(test=test)
        result = list(generator.process_input(intent_input))
        self.assertEqual(expected, result)

    def test_process_input(self):
        self.compare_process_input(EXPECTED_FULL_CONTENT, test=False)

    def test_process_test_input(self):
        self.compare_process_input(EXPECTED_FULL_TEST_CONTENT, test=True)


    def compare_write_utterances_json(self, expected, test=False):
        intent_input = "BotLanguage:{Which|What}{language:botLang}{can you|do you}{speak|understand}{|?}"
        input_file = "test.inp"

        with open(input_file, "w") as ifile:
            ifile.write(intent_input)

        test_file = 'test_file.json'
        with open(test_file, 'w') as tfile:
            json.dump(expected, tfile)

        output_file = "test.out"
        generator = UtterancesGenerator(test=test)
        generator.write_utterances_json(input_file, output_file)

        with open(output_file, "r") as ofile:
            result = ofile.read()

        with open(test_file, "r") as tfile:
            expected = tfile.read()

        self.maxDiff=None
        os.remove(input_file)
        os.remove(output_file)
        os.remove(test_file)
        self.assertEqual(expected, result)


    def test_write_utterances_json(self):
        self.compare_write_utterances_json(EXPECTED_FULL_CONTENT, test=False)

    def test_write_test_utterances_json(self):
        self.compare_write_utterances_json(EXPECTED_FULL_TEST_CONTENT, test=True)


if __name__ == "__main__":
    unittest.main()
