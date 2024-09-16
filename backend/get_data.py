from Bio import Entrez
import pandas as pd
from time import sleep
from tqdm import tqdm
import concurrent.futures
import threading
import random
import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

Entrez.email = "mertcan.coskun1993@gmail.com"
lock = threading.Lock()

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(429, 500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def fetch_batch(start, batch_size, term):
    try:
        with lock:
            sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds
        
        handle = Entrez.esearch(db="pubmed", term=term, retmax=batch_size, retstart=start)
        record = Entrez.read(handle)
        ids = record['IdList']
        
        if not ids:
            return []
        
        fetch_handle = Entrez.efetch(db="pubmed", id=','.join(ids), rettype="abstract", retmode="text")
        batch_articles = fetch_handle.read().split('\n\n')
        
        return batch_articles
    except Exception as e:
        print(f"Error fetching batch starting at {start}: {e}")
        return []

def fetch_pubmed_data(term, max_results=5000, batch_size=100, max_workers=5):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_batch, start, batch_size, term) 
                   for start in range(0, max_results, batch_size)]
        
        articles = []
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Fetching articles"):
            articles.extend(future.result())
    
    return articles

# Fetch articles
term = "clinical trial AND immunology[MeSH Terms]"
articles = fetch_pubmed_data(term, max_results=5000, batch_size=100, max_workers=5)

# Save to a CSV file for future use
df = pd.DataFrame(articles, columns=['text'])
df.to_csv('backend/data/trials/immunology_clinical_trial_data.csv', index=False)
