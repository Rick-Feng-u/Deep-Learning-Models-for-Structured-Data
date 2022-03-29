import os.path

import spacy

nlp = spacy.load("en_core_web_lg")

SOS = 0
EOS = 1


class sequence:
    def __init__(self, name):
        self.name = name
        self.index = {}
        self.num_count_of_one_element = {}
        self.element = {0: "SOS", 1: "EOS"}
        self.size_of_index = 2
        self.highest_length = 0

    def add_sequence(self, seq):
        length = len(seq)
        if length > self.highest_length:
            self.highest_length = length

        for element in seq:
            if element not in self.index:
                is_sim = False
                for key in self.index:
                    s1 = nlp(element)
                    s2 = nlp(key)
                    sim = s1.similarity(s2)
                    if sim > 0.8:
                        self.num_count_of_one_element[key] += 1
                        if sim < 1:
                            [key if value == element else value for value in seq]
                            print("new sim")
                        is_sim = True
                        break

                if not is_sim:
                    self.index[element] = self.size_of_index
                    self.num_count_of_one_element[element] = 1
                    self.element[self.size_of_index] = element
                    self.size_of_index += 1
                    print("not new sim")

            else:
                self.num_count_of_one_element[element] += 1


def sequence_to_index(seq_name, seq):
    return [seq_name.index[element] for element in seq]


def title_id_matching(index_file, title_file, output_path):
    count = 0
    output_path = os.path.join(output_path, 'wiki_title_with_id.txt')
    title_dict = {}

    with open(title_file, 'r', encoding='utf-8') as titles:
        for title in titles:
            title_pair = title.strip().split("   ")
            try:
                title_dict[title_pair[0]] = title_pair[1]
            except:
                continue

    with open(index_file, 'r', encoding='utf-8') as titles:
        for title in titles:
            title_info = title.strip().split(':', 2)
            try:
                if title_info[2] in title_dict:
                    with open(output_path, "a+", encoding="utf-8") as file_object:
                        file_object.write(title_info[2] + "   " + title_dict[title_info[2]] + "   " + title_info[1])
                        file_object.write("\n")
                    count += 1
                    if count % 1000 == 0:
                        print(title_info[2] + "   " + title_dict[title_info[2]])
            except:
                continue


def targeting_matching(id_file, target_class_input_file, target_class_output_file):
    count = 0
    title_with_id = {}
    with open(id_file, 'r', encoding='utf-8') as titles:
        for title in titles:
            title_pair = title.strip().split("   ")
            try:
                title_with_id[title_pair[2]] = [title_pair[0], title_pair[1]]
            except:
                continue

    with open(target_class_input_file, 'r', encoding='utf-8') as titles:
        for title in titles:
            target_info = title.strip().split(',', 1)
            if target_info[1] != "??":
                try:
                    if target_info[0] in title_with_id:
                        targets = target_info[1].split(',')
                        joined_target = "   ".join([elem for elem in targets])
                        with open(target_class_output_file, "a+", encoding="utf-8") as file_object:
                            file_object.write(target_info[0] + "   " + title_with_id[target_info[0]][0] + "   " +
                                              title_with_id[target_info[0]][1] + "   " + joined_target)
                            file_object.write("\n")
                        count += 1
                        if count % 1000 == 0:
                            print(target_info[0] + "   " + title_with_id[target_info[0]][0] + "   " +
                                  title_with_id[target_info[0]][1])

                except:
                    continue
