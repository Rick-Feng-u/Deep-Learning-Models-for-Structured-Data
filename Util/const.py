import os.path

WIKI_XML_DUMP_FOLDER_PATH = os.path.join('Data', 'raw_data', 'wiki_xml_dump')
CLEANED_TITLE_FOLDER_PATH = os.path.join('Data', 'cleaned_data', 'cleaned_title')

CLEANED_WIKI_XML_FOLDER_PATH = os.path.join('Data', 'cleaned_data', 'cleaned_wiki_folder')
WIKI_CLEANED_TITLES_FILE_PATH = os.path.join(CLEANED_TITLE_FOLDER_PATH, 'wiki_title.txt')
WIKI_CLEANED_TITLES_ID_FILE_PATH = os.path.join(CLEANED_TITLE_FOLDER_PATH, 'wiki_title_with_id.txt')
WIKI_CLEANED_TITLES_TARGET_FILE_PATH = os.path.join(CLEANED_TITLE_FOLDER_PATH, 'wiki_title_with_target.txt')
WIKI_INDEX_FILE_PATH = os.path.join('Data', 'raw_data', 'wiki_xml_index', 'enwiki-20220201-pages-articles-multistream-index.txt')
WIKI_TRAINING_TARGET_FILE_PATH = os.path.join('Data', 'target_classes', 'train_categories.txt')
