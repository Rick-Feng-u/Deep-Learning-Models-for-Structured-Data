from Script import WikiReader
from Util import WIKI_XML_DUMP_FOLDER_PATH,CLEANED_WIKI_XML_FOLDER_PATH

if __name__ == "__main__":
    WikiReader(WIKI_XML_DUMP_FOLDER_PATH, CLEANED_WIKI_XML_FOLDER_PATH)