import os
import pickle
import random

from Util import CLEANED_WIKI_XML_FOLDER_PATH, WIKI_CLEANED_TITLES_TARGET_FILE_PATH, Cleaned_WIKI_SEQ_FOLDER, sequence, \
    sequence_to_index
from Script import xml_to_prufer

if __name__ == '__main__':
    count = 0
    pairs = []
    target_with_titles = {}

    input_seq_class = sequence('wiki_input')
    out_seq_class = sequence('wiki_output')

    with open(WIKI_CLEANED_TITLES_TARGET_FILE_PATH, "r", encoding="utf-8") as file_object:
        for target_title in file_object:
            target = target_title.strip().split("   ")
            try:
                target_with_titles[target[2]] = target[3:]
            except:
                continue

    for file in os.listdir(CLEANED_WIKI_XML_FOLDER_PATH):
        filename = os.fsdecode(file)
        if filename.endswith(".xml"):
            FILE_PATH = os.path.join(CLEANED_WIKI_XML_FOLDER_PATH, filename)

            title = filename.split('.')
            title = title[0]

            try:
                result = xml_to_prufer(FILE_PATH)
            except:
                continue

            if not result:
                continue

            pair = []

            try:
                target_seq = target_with_titles[title]
            except:
                continue

            input_seq = result

            input_seq = input_seq_class.add_sequence_input(input_seq)
            out_seq_class.add_sequence_output(target_seq)

            input_seq = sequence_to_index(input_seq_class, input_seq)
            target_seq = sequence_to_index(out_seq_class, target_seq)

            pair.append(input_seq)
            pair.append(target_seq)

            pairs.append(pair)
            count += 1

            if count % 1000 == 0:
                training_seq = os.path.join(Cleaned_WIKI_SEQ_FOLDER, 'wiki_seq_' + str(round(count / 1000)) + '.pkl')
                with open(training_seq, 'wb') as f:
                    pickle.dump(pairs, f)
                print(pair)
                pairs.clear()

    training_seq = os.path.join(Cleaned_WIKI_SEQ_FOLDER, 'wiki_seq_' + str(round(count / 1000) + 1) + '.pkl')
    with open(training_seq, 'wb') as f:
        pickle.dump(pairs, f)

    input_class = os.path.join(Cleaned_WIKI_SEQ_FOLDER, 'wiki_input_seq_class.pkl')
    with open(input_class, 'wb') as f:
        pickle.dump(input_seq_class, f)

    output_class = os.path.join(Cleaned_WIKI_SEQ_FOLDER, 'wiki_output_seq_class.pkl')
    with open(output_class, 'wb') as f:
        pickle.dump(out_seq_class, f)
