# -*- coding: utf-8 -*-
import re
import unicodedata
from search import Indexable
from search import SearchEngine





class Category(Indexable):
    

    def __init__(self,title, text, metadata):
        Indexable.__init__(self, metadata)
        self.title = title
        self.text = text

    def __repr__(self):
        return 'title: %s, text/letter: %s'%(self.title, self.text)

# preprocessing the book entries -All non-accents are removed -Special characters are replaced by whitespaces (i.e. -, [, etc.)-Punctuation marks are removed; Additional whitespaces between replaced by only one whitespaces.
class DataPreprocessor(object):
    
    _EXTRA_SPACE_REGEX = re.compile(r'\s+', re.IGNORECASE)
    _SPECIAL_CHAR_REGEX = re.compile(
        # detect punctuation characters
        r"(?P<p>(\.+)|(\?+)|(!+)|(:+)|(;+)|"
        # detect special characters
        r"(\(+)|(\)+)|(\}+)|(\{+)|('+)|(-+)|(\[+)|(\]+)|"
        # detect commas NOT between numbers
        r"(?<!\d)(,+)(?!=\d)|(\$+))")

    def preprocess(self, entry):
        
        f_entry = entry.lower()
        f_entry = f_entry.replace('\t', '|').strip()
        f_entry = self.strip_accents(unicode(f_entry, 'utf-8'))
        f_entry = self._SPECIAL_CHAR_REGEX.sub(' ', f_entry)
        f_entry = self._EXTRA_SPACE_REGEX.sub(' ', f_entry)

        category_desc = f_entry.split('|')

        return category_desc

    def strip_accents(self, text):
        return unicodedata.normalize('NFD', text).encode('ascii', 'ignore')


class CategorySearch(object):


    

    _NO_RESULTS_MESSAGE = 'Sorry, no results.'

    def __init__(self, filename):
        self.filename = filename
        self.engine = SearchEngine()

   #Load category from a file name.
    def load_category(self,text):
        
        self._CATEGORY_META_TITLE_INDEX = 1
        
        if text == "yes":
            self._CATEGORY_META_TEXT_INDEX = 2
        else:
            self._CATEGORY_META_TEXT_INDEX = 0
        

        processor = DataPreprocessor()
        with open(self.filename) as catalog:
            for entry in catalog:
                category_desc = processor.preprocess(entry)
                metadata = ' '.join(category_desc[self._CATEGORY_META_TEXT_INDEX:])

                
                title = category_desc[self._CATEGORY_META_TITLE_INDEX].strip()
                text = category_desc[self._CATEGORY_META_TEXT_INDEX].strip()

                category = Category(title, text, metadata)
                self.engine.add_object(category)

        self.engine.start()

  # Search categories according to provided query of terms
    def search_category(self, query, n_results=5):
    
        result = ''
        if len(query) > 0:
            result = self.engine.search(query, n_results)

        if len(result) > 0:
            return '\n'.join([str(indexable) for indexable in result])
        return self._NO_RESULTS_MESSAGE
# Return no of categories in index
    def category_count(self):
   
        return self.engine.count()