# luis_utterances_generator
The automated generation of multiple  labeled utterances for various intents which can be fed to MS LUIS bot. 
This is a generator of utterances for LUIS bot (https://www.luis.ai).
In order to train the bot model you need to generate a json file, containing labeled intents and entities for a set of various utterances.
the generator let you perform this automatically giving only variations for some words in the phrases.
Also, it aotpmatically labels entities.
Please find examples of input and output formats in the "examples" deirectory.
In order to run the generator from the command line, please use the folloving comand with your spacifica parameters:
python utterances_generator.py  --input [your input file name here] --output [your output file name here]

PS: Due to the current limitaitons of LUIS bot interface the number of utterances per single json file is limited to 100 utterances. Hoever, this parameter can be tunned in the code.
