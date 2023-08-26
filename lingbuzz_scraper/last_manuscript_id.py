from bs4 import BeautifulSoup
import requests
import re


def last_manuscript_id():
    '''    
    This function connects to lingbuzz and retrieves the id of the last uploaded
    manuscript
        
    Returns:
        tuple: a tuple with the ids (strings) for the first and last manuscripts
    '''
    
    url_main = 'https://ling.auf.net/'
    result_main = requests.get(url_main).text
    doc = BeautifulSoup(result_main, 'html.parser')
    
    first_ = '002'
    
    ### Getting the id of the last manuscript

    # this retrieves the row with the last manuscript
    new_row = list(doc.find(text='new').parents)[2]
    
    # This gets the link for the last manuscript
    link = list(new_row)[3].a.get('href')
    
    # And this is the id number of the last manuscript
    last_ = re.search(r'\d+', link).group()
    
    return (first_, last_)
