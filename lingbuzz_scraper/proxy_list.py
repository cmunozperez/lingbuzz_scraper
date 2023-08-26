from bs4 import BeautifulSoup
import threading
import queue
import requests

    
def proxy_scraper():
    url = 'https://free-proxy-list.net/'
    result = requests.get(url).text
    doc = BeautifulSoup(result, 'html.parser')
    
    # Finding the portion of the document with the raw proxies
    block = list(doc.find(text='Raw Proxy List').parents)[2]
    proxies = str(list(block.children)[1])
    
    # Transforming the string into a list
    proxies = proxies.split('\n')
    
    # Erasing non-proxy elements
    proxies = proxies[3:-1]
    
    return proxies


def proxy_list():
    """
    Filters valid https compatible proxies obtained from free-proxy-list.net.
    
    Returns:
        list: a list of (ideally) 20 valid htts proxies
    """
    
    q = queue.Queue()
    valid_proxies = []
    
    for p in proxy_scraper():
        q.put(p)
    
    def validation():        
        # The function will run while the queue is not empty and there are less of 20 valid https proxies
        while not q.empty() and len(valid_proxies) < 20:
            proxy = q.get(timeout=1)
            try:
                res = requests.get('https://ipinfo.io/json',
                                   timeout=3,
                                    proxies={'https': proxy})
            except:
                print(f'{proxy} - failed ({q.qsize()} proxies to check)')
                continue
            if res.status_code == 200:
                valid_proxies.append(proxy)
                print(f'{proxy} - working ({len(valid_proxies)}/20)')
    
    # Threading to speed the process
    threads = []
    
    for _ in range(20):
        thread = threading.Thread(target=validation)
        thread.start()
        threads.append(thread)
           
    for thread in threads:
        thread.join()
    
    return valid_proxies
