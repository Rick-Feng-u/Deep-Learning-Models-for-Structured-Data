import xml.etree.ElementTree as etree
import xml.etree.cElementTree as ET
import time
import re
import os

start_time = time.time()

FILE_PATH = 'enwiki-20220201-pages-articles-multistream1.xml'
CLEANED_XML_OUTPUT_PATH = 'Cleaned_wiki_folder'

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
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem

def WikiReader():
    totalCount = 0
    title = None
    
    for event, elem in etree.iterparse(FILE_PATH, events=('start', 'end')):
        tage = tag_name(elem.tag)
        
        if event == 'start':
            if tage == 'page':
                title = ''
                redirect = False
                text = ''
        else:
            if tage == 'title':
                title = elem.text
                title_ = ''.join(filter(str.isalnum, title)) 
                root = ET.Element(title_)
            elif tage == 'redirect':
                redirect = True
            elif tage == 'text':
                text = elem.text
                
                REDIRECT_CASE_1 = "#REDIRECT"
                REDIRECT_CASE_2 = "#redirect"
                if (REDIRECT_CASE_1 in text) | (redirect == True) | (REDIRECT_CASE_2 in text):
                    continue 
                
                for line in text.splitlines():
                    special_char=re.compile('[@_!$%^&*()<>?/\|}{~:;]#')
                    span = re.compile('span')
                    if line.startswith("==") & line.endswith('==') & (special_char.search(line) == None) & (span.search(line) == None):
                        if(line.count("=") == 4):
                            current_sub_1_title =  line[line.find('==') + len('=='):line.rfind('==')]
                            sub_title = ET.SubElement(root, current_sub_1_title)
                        elif(line.count("=") == 6):
                            current_sub_2_title =  line[line.find('===') + len('==='):line.rfind('===')]
                            sub_2_title = ET.SubElement(sub_title, current_sub_2_title)
                        elif(line.count("=") == 8):
                            current_sub_3_title =  line[line.find('====')+1:line.find('====')]
                            sub_3_title = ET.SubElement(sub_2_title, current_sub_3_title)
                        elif(line.count("=") == 10):
                            current_sub_4_title =  line[line.find('=====')+1:line.find('=====')]
                            sub_4_title = ET.SubElement(sub_3_title, current_sub_4_title)
                        elif(line.count("=") == 12):
                            current_sub_5_title =  line[line.find('======')+1:line.find('======')]
                            sub_5_title = ET.SubElement(sub_4_title, current_sub_5_title)
                
                tree = ET.ElementTree(indent(root))
                xml_path = os.path.join(CLEANED_XML_OUTPUT_PATH, title_ + ".xml")
                tree.write(xml_path, xml_declaration=True, encoding='utf-8')
                      
            elif tage == 'page':
                totalCount += 1     

                if totalCount > 1 and (totalCount % 100000) == 0:
                    print("{:,}".format(totalCount))
                
            elem.clear()
                
elapsed_time = time.time() - start_time
print("Elapsed time: {}".format(hms_string(elapsed_time)))

if __name__ == "__main__":
    WikiReader()
