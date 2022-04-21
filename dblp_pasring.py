import xml.sax
import os
import pickle

from Util import sequence, sequence_to_index

DBLP_PATH = os.path.join('Data', 'raw_data', 'dblp_xml_dump', 'dblp.xml')
SEQ_PATH = os.path.join('Data', 'cleaned_data', 'cleaned_dblp_folder')

input_seq_class = sequence('dblp_input')
out_seq_class = sequence('dblp_output')


class DBLP_Handler(xml.sax.ContentHandler):
    def __init__(self):
        self.pairs = []
        self.dblp = ['article', 'inproceedings', 'proceedings', 'book', 'incollection', 'phdthesis', 'mastersthesis',
                     'www', 'person', 'data']
        self.target_count = []
        self.target = ""
        self.tags = []
        self.count = 1

    def startElement(self, tag, attributes):
        if tag in self.dblp:
            self.target = tag
            self.tags.append(tag)
        elif tag != 'dblp':
            self.tags.append(tag)

    def endElement(self, tag):
        if tag in self.dblp:
            input_seq_class.add_sequence_output(self.tags)
            out_seq_class.add_sequence_output([self.target])

            input_seq = sequence_to_index(input_seq_class, self.tags)
            target_seq = sequence_to_index(out_seq_class, [self.target])

            pair = [[input_seq, target_seq]]

            self.pairs.append(pair)
            self.tags = []
            self.target = ""

            self.count += 1

            if self.count % 3000000 == 0:
                print("here")
                training_seq = os.path.join(SEQ_PATH, 'dblp_seq_' + str(round(self.count / 3000000)) + '.pkl')
                with open(training_seq, 'wb') as f:
                    pickle.dump(self.pairs, f)

                self.pairs.clear()




if __name__ == "__main__":
    parser = xml.sax.make_parser()
    handler = DBLP_Handler()
    parser.setContentHandler(handler)
    parser.parse(DBLP_PATH)

    input_class = os.path.join(SEQ_PATH, 'dblp_input_seq_class.pkl')
    with open(input_class, 'wb') as f:
        pickle.dump(input_seq_class, f)

    output_class = os.path.join(SEQ_PATH, 'dblp_output_seq_class.pkl')
    with open(output_class, 'wb') as f:
        pickle.dump(out_seq_class, f)
