from Util import TESTING_XML_FOLDER_PATH
from Script import xml_to_prufer
import os

if __name__ == '__main__':
    FILE_PATH = os.path.join(TESTING_XML_FOLDER_PATH, 'test.xml')
    resulting_sequnece = xml_to_prufer(FILE_PATH)