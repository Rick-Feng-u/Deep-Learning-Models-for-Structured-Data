from Util import title_id_matching,targeting_matching, WIKI_TRAINING_TARGET_FILE_PATH, WIKI_INDEX_FILE_PATH, WIKI_CLEANED_TITLES_FILE_PATH, CLEANED_TITLE_FOLDER_PATH, WIKI_CLEANED_TITLES_ID_FILE_PATH, WIKI_CLEANED_TITLES_TARGET_FILE_PATH

if __name__ == '__main__':
    title_id_matching(WIKI_INDEX_FILE_PATH, WIKI_CLEANED_TITLES_FILE_PATH, CLEANED_TITLE_FOLDER_PATH)
    targeting_matching(WIKI_CLEANED_TITLES_ID_FILE_PATH, WIKI_TRAINING_TARGET_FILE_PATH, WIKI_CLEANED_TITLES_TARGET_FILE_PATH)
