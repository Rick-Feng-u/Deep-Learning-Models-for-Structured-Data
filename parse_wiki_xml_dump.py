import os

from Script import WikiReader
from Util import WIKI_XML_DUMP_FOLDER_PATH, CLEANED_WIKI_XML_FOLDER_PATH, CLEANED_TITLE_FOLDER_PATH

if __name__ == "__main__":
    TITLE_INPUT = os.path.join(CLEANED_TITLE_FOLDER_PATH, "wiki_title.txt")
    WikiReader(TITLE_INPUT, WIKI_XML_DUMP_FOLDER_PATH, CLEANED_WIKI_XML_FOLDER_PATH)