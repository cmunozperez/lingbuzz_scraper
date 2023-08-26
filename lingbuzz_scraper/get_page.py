from bs4 import BeautifulSoup
import requests
import re

def get_page(manuscript_id, proxy = None):
    """
    Given a lingbuzz id number, the function retrieves the title of the manuscript,
    its author, where it was published, the date in which it was uploaded, how
    many times it was downloaded, and its abstract 
    
    Args:
        manuscript_id (str): a lingbuzz number id
        proxy (proxy): an optional proxy to make the request (e.g., 66.191.31.158:80)
    
    Returns:
        list: a list with the relevant information of the manuscript
    """
    
    url = 'https://ling.auf.net/lingbuzz/' + manuscript_id
    result = requests.get(url,
                          timeout=10,
                          proxies={'https': proxy}).text
    doc = BeautifulSoup(result, 'html.parser')
    
    ling_id = 'lingbuzz/' + manuscript_id
    
    if doc.h1 == None:
        
        title = str(doc.a.string)
        
        auth_list = []
        for i in doc.center.children:
            if '&amp;' in str(i):
                auth_list.append(str(i.string))
        author = ', '.join(auth_list)
        
        # This fixes an error with certain manuscripts
        if title in author:
            to_delete = title + ', '
            author = author.replace(to_delete, '')
        
        keywords = str(doc.table.find(text=re.compile(r'keywords:')).parent.next_sibling.string)
        try:
            published = str(doc.table.find(text=re.compile(r'Published in:')).parent.next_sibling.string)
        except AttributeError:
            published = 'None'
        date = str(list(doc.center.children)[-1])
        downloads = int(re.search(r'\d+', str(doc.table.find(text=re.compile(r'Downloaded:')).parent.next_sibling.string)).group())
        
        abstract = ''

        for i in list(doc.body)[5:]:
            if i.string == None:
                break
            abstract += i.string

        return [ling_id, title, author, keywords, published, date, downloads, abstract]

    else:
        return [ling_id] + ['NA' for _ in range(7)]
