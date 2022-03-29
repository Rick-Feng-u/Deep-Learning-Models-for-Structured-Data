import os
import torch
import pickle
from Util import CLEANED_WIKI_XML_FOLDER_PATH, sequence, sequence_to_index
from Script import xml_to_prufer
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if __name__ == '__main__':
    pairs = []

    input_seq_name = sequence('wiki_input')
    out_seq_name = sequence('wiki_output')

    for file in os.listdir(CLEANED_WIKI_XML_FOLDER_PATH):
        filename = os.fsdecode(file)
        if filename.endswith(".xml"):
            FILE_PATH = os.path.join(CLEANED_WIKI_XML_FOLDER_PATH, filename)
            result = xml_to_prufer(FILE_PATH)

            if result is None:
                continue

            pair = []

            target_seq = ["war"]
            input_seq = result

            input_seq_name.add_sequence(input_seq)
            out_seq_name.add_sequence(target_seq)

            input_seq = sequence_to_index(input_seq_name, input_seq)
            target_seq = sequence_to_index(out_seq_name, target_seq)

            pair.append(input_seq)
            pair.append(target_seq)

            pairs.append(pair)

    # print(random.choice(pairs))
