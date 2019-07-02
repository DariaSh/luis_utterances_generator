import os
import json
import unittest
import utterances_generator


class TestUtGenerator(unittest.TestCase):

    def test_get_item_list(self):
        expected = ["option1", "option2", "option3"]
        result = utterances_generator.get_item_list("option1|option2|option3")
        self.assertEqual(expected, result)

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
        result = utterances_generator.build_intent_utterances(intent, [utterance.split(" ")], entities)
        self.assertDictEqual(expected, result[0])

    def test_process_input(self):
        intent_input = "BotLanguage:{Which|What}{language:botLang}{can you|do you}{speak|understand}{|?}"
        expected = [{"text": "Which language can you speak", "intentName": "BotLanguage",
                     "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]},
                    {"text": "Which language can you speak ?", "intentName": "BotLanguage",
                     "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]},
                    {"text": "Which language can you understand", "intentName": "BotLanguage",
                     "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]},
                    {"text": "Which language can you understand ?", "intentName": "BotLanguage",
                     "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]},
                    {"text": "Which language do you speak", "intentName": "BotLanguage",
                     "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]}]

        result = utterances_generator.process_input(intent_input)
        self.assertEqual(expected, result)

    def test_generate_utterances(self):
        intent_input = "BotLanguage:{Which|What}{language:botLang}{can you|do you}{speak|understand}{|?}"
        input_file = "test.inp"

        with open(input_file, "w") as ifile:
            ifile.write(intent_input)

        test_file = 'test_file.json'
        with open(test_file, 'w') as tfile:
            json.dump([{"text": "Which language can you speak", "intentName": "BotLanguage",
                        "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]},
                        {"text": "Which language can you speak ?", "intentName": "BotLanguage",
                         "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]},
                        {"text": "Which language can you understand", "intentName": "BotLanguage",
                         "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]},
                        {"text": "Which language can you understand ?", "intentName": "BotLanguage",
                         "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]},
                        {"text": "Which language do you speak", "intentName": "BotLanguage",
                         "entityLabels": [{"entityName": "botLang", "startCharIndex": 6, "endCharIndex": 14}]}], tfile)

        output_file = "test.out"
        utterances_generator.generate_utterances(input_file, output_file, 5)

        with open(output_file, "r") as ofile:
            result = ofile.read()

        with open(test_file, "r") as tfile:
            expected = tfile.read()

        self.maxDiff=None
        os.remove(input_file)
        os.remove(output_file)
        os.remove(test_file)
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()