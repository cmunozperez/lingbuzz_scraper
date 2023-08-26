import sys
import threading
import queue
import pandas as pd

from last_manuscript_id import last_manuscript_id
from get_page import get_page
from proxy_list import proxy_list


def lingbuzz_scrap(begin = None, end = None):
    '''
    Generates a DataFrame with the data of the Lingbuzz entries between
    two values. If no value is provided, it retrieves the data from all
    entries. The DataFrame is saved as a csv file.
    
    Parameters
    ----------
    begin (str): A number from which Lingbuzz entries will be retrieved
    
    end (str): A number until which Lingbuzz entries will be retrieved
        
    Returns
    -------
    DataFrame
        
    '''
    
    # Retrieves the minimum and maximum ids if no values are provided
    if begin is None and end is None:
        begin, end = last_manuscript_id()
    
    # Changes the str values to int
    begin = int(begin)
    end = int(end) + 1

    # This initiates the list to store the info of the manuscripts
    manuscripts = []
   
    # Queues for proxies (q) and ids (r)
    q = queue.Queue()
    r = queue.Queue()
    
    # Fills the queue with proxies
    for p in proxy_list():
        q.put(p)
    
    # List with ids
    id_range = [str(num) for num in range(begin, end)]
    
    # Fills the queue with ids
    for i in id_range:
        r.put(i)
    
    
    def scrap_cycle():
        # The function will work while there are ids to scrap
        while not r.empty():
            # In case the queue with proxies depletes, it refills it with new proxies
            if q.empty() == True:
                for p in proxy_list():
                    q.put(p)
            # If no proxy was found, go back and look again
            if q.empty() == True:
                continue
            
            # this takes an id number from the queue r
            num = r.get(timeout=1)    
            id_num = '00' + str(num)
            
            # this takes a proxy from the queue q
            proxy = q.get(timeout=1)
            print(f'Retrieving lingbuzz/{id_num} through {proxy}.')
            
            try:
                ms = get_page(id_num, proxy)
                manuscripts.append(ms)
                q.put(proxy)
                print(f'Success! {len(manuscripts)}/{len(id_range)}')
                print()
            except Exception as e:
                # Printing the type of the error using the type() function
                print('Error type:', type(e).__name__)
                print()
                r.put(num)
                # errors.append((proxy, type(e).__name__))
    
    # Threading to speed the process
    threads = []
    
    for _ in range(2):
        thread = threading.Thread(target=scrap_cycle)
        thread.start()
        threads.append(thread)
           
    for thread in threads:
        thread.join()
            
    df =  pd.DataFrame(manuscripts, columns=['Id', 'Title', 'Authors', 'Keywords', 'Published_in', 'Date', 'Downloads', 'Abstract'])
    
    # Fix for lingbuzz/001184, which has errors in origin
    index_error = df.index[df['Id'].str.contains('lingbuzz/001184')].tolist()
    if len(index_error) > 0:
        df['Title'][index_error[0]] = 'Cartography of recomplementation in Romance Languages'
        df['Authors'][index_error[0]] = 'Francesc González i Planas'
        df['Date'][index_error[0]] = 'December 2010'
    
    # This is simply to name output file
    begin = '00' + str(begin)
    end = '00' + str(end - 1)
    
    file = f'lingbuzz_{begin}_{end}.csv'
    df.to_csv(file, index=False)
    
    print('-------------')
    print(f'Saved as {file}')
    print('-------------')
    return df


# This runs the function
if __name__ == '__main__':
    _, last_id = last_manuscript_id()
    print()
    print('This program will scrape the Lingbuzz site. It will generate a csv file with the results.')
    print()
    print(f'Lingbuzz manuscripts are labelled with an id number. They go from 002 to {last_id}. You need to define a range of ids to scrape.')
    print()
    lower_id = input("Enter the lower id number to start scraping from: ")
    try:
        lower_id = int(lower_id)
    except:
        print('This is not a valid id number.')
        sys.exit(0)
        
    upper_id = input("Enter the upper id where the scraping should stop: ")
    print()
    try:
        upper_id = int(upper_id)
    except:
        print('This is not a valid id number.')
        sys.exit(0)
    
    if lower_id > upper_id or lower_id < 2 or upper_id > int(last_id):
        print('This is not a valid range.')
        sys.exit(0)
    
    lower_id = '00' + str(lower_id)
    upper_id = '00' + str(upper_id)
    confirmation = input(f"You have chosen to scrape manuscripts from \lingbuzz\{lower_id} to \lingbuzz\{upper_id}. If this is correct, enter 'y': ")
    if confirmation.lower() == 'y':
        print()
        print('Scraping started...')
        lingbuzz_scrap(lower_id, upper_id)
