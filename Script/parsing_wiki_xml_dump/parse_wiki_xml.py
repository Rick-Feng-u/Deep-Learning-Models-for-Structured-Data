import xml.etree.ElementTree as etree
import xml.etree.cElementTree as ET
import time
import re
import os
import gc

start_time = time.time()


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


def tag_name(t):
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t


def indent(elem, level=0):
    i = "\n" + level * "  "
    j = "\n" + (level - 1) * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem


def WikiReader(TITLE_PATH, FILE_PATH, OUTPUT_PATH):
    totalCount = 0
    title = None
    gc.enable()

    INPUT_PATH = os.path.join(FILE_PATH, 'enwiki-20220201-pages-articles-multistream.xml')

    for event, elem in etree.iterparse(INPUT_PATH, events=('start', 'end')):
        if totalCount > 1 and (totalCount % 100000) == 0:
            print("{:,}".format(totalCount))
        tage = tag_name(elem.tag)

        if event == 'start':
            if tage == 'page':
                title = ''
                redirect = False
                text = ''
        else:
            if (tage == 'title'):
                title = elem.text
                store = title
                title = re.sub('[^a-zA-Z\d\s]', '', title)
                title = re.sub('\s+', '_', title)
                try:
                    if title[0].isdigit():
                        title = "_" + title

                except:
                    continue
                root = ET.Element(title)

            elif tage == 'redirect':
                redirect = True
            elif tage == 'text':
                text = elem.text
                if text == "":
                    continue

                REDIRECT_CASE_1 = "#REDIRECT"
                REDIRECT_CASE_2 = "#redirect"
                try:
                    if (REDIRECT_CASE_1 in text) | (redirect == True) | (REDIRECT_CASE_2 in text):
                        continue
                except:
                    continue

                try:
                    for line in text.splitlines():
                        special_char = re.compile('[@#*()<>/\|}{~]')
                        span = re.compile('span')
                        if line.startswith("==") & line.endswith('==') & (special_char.search(line) == None) & (
                                span.search(line) == None) & (
                                any(c.isalpha() for c in line) | any(c.isdigit() for c in line)) & (isEnglish(line)):
                            if (line.count("=") == 4) & (line.isascii() == True):
                                current_sub_1_title = line[line.find('==') + len('=='):line.rfind('==')]
                                if current_sub_1_title != '':
                                    current_sub_1_title = re.sub('[^a-zA-Z\d\s]', '', current_sub_1_title)
                                    current_sub_1_title = re.sub('\s+', '_', current_sub_1_title)
                                    if current_sub_1_title[0].isdigit():
                                        current_sub_1_title = "_" + current_sub_1_title
                                    sub_title = ET.SubElement(root, current_sub_1_title)
                            elif (line.count("=") == 6):
                                current_sub_2_title = line[line.find('===') + len('==='):line.rfind('===')]
                                if current_sub_2_title != '':
                                    current_sub_2_title = re.sub('[^a-zA-Z\d\s]', '', current_sub_2_title)
                                    current_sub_2_title = re.sub('\s+', '_', current_sub_2_title)
                                    if current_sub_2_title[0].isdigit():
                                        current_sub_2_title = "_" + current_sub_2_title
                                    sub_2_title = ET.SubElement(sub_title, current_sub_2_title)
                            elif (line.count("=") == 8):
                                current_sub_3_title = line[line.find('====') + len('===='):line.rfind('====')]
                                if current_sub_3_title != '':
                                    current_sub_3_title = re.sub('[^a-zA-Z\d\s]', '', current_sub_3_title)
                                    current_sub_3_title = re.sub('\s+', '_', current_sub_3_title)
                                    if current_sub_3_title[0].isdigit():
                                        current_sub_3_title = "_" + current_sub_3_title
                                    sub_3_title = ET.SubElement(sub_2_title, current_sub_3_title)
                            elif (line.count("=") == 10):
                                current_sub_4_title = line[line.find('=====') + len('====='):line.rfind('=====')]
                                if current_sub_4_title != '':
                                    current_sub_4_title = re.sub('[^a-zA-Z\d\s]', '', current_sub_4_title)
                                    current_sub_4_title = re.sub('\s+', '_', current_sub_4_title)
                                    if current_sub_4_title[0].isdigit():
                                        current_sub_4_title = "_" + current_sub_4_title
                                    sub_4_title = ET.SubElement(sub_3_title, current_sub_4_title)
                            elif (line.count("=") == 12):
                                current_sub_5_title = line[line.find('======') + len('======'):line.rfind('======')]
                                if current_sub_5_title != '':
                                    current_sub_5_title = re.sub('[^a-zA-Z\d\s]', '', current_sub_5_title)
                                    current_sub_5_title = re.sub('\s+', '_', current_sub_5_title)
                                    if current_sub_5_title[0].isdigit():
                                        current_sub_5_title = "_" + current_sub_5_title
                                    sub_5_title = ET.SubElement(sub_4_title, current_sub_5_title)

                except:
                    continue

                try:
                    tree = ET.ElementTree(indent(root))
                    xml_path = os.path.join(OUTPUT_PATH, title + ".xml")
                    tree.write(xml_path, xml_declaration=True, encoding='utf-8')

                    with open(TITLE_PATH, "a+", encoding="utf-8") as file_object:
                        file_object.write(store + "   "+ title)
                        file_object.write("\n")

                except:
                    continue

            elif tage == 'page':
                totalCount += 1


            elem.clear()


elapsed_time = time.time() - start_time
print("Elapsed time: {}".format(hms_string(elapsed_time)))
