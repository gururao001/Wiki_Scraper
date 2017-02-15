#!/usr/bin/python


import optparse
import categories



FILENAME = 'items.txt' 

# get arguments from user and display the search result
def start_search(data_location,search_query,text):
    
    query = None
    repository = categories.CategorySearch(data_location)
  

    repository.load_category(text)
    docs_number = repository.category_count()
    
    
    query = search_query
    search_results = repository.search_category(query)

    print search_results


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--data', dest='data', help='Location of the data file that will be indexed', default= FILENAME)
    parser.add_option('--search',help= 'enter search query')
    parser.add_option('--text',help= 'enter whether to display text')
    options, args = parser.parse_args()
    start_search(options.data,options.search,options.text)