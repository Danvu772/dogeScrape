import requests
import json
import pandas as pd
import itertools

def main():

    modes = ['grants', 'contracts', 'leases', 'payments']

    for mode in modes:
        total_requests = 1
        max_requests = 20
        data = []

        i = 1
        total_pages = 1

        while i < total_pages + 1:
            contentDict, total_pages = tryScrapePage(mode, i, total_requests, max_requests)
            if contentDict:
                i += 1
                total_requests = 1
                data.append(contentDict['result'][mode])
            else:
                total_requests += 1

            if total_requests == max_requests + 1:
                print('\ntotal requests exceeded, exiting program')
                exit()
        
        data = list(itertools.chain.from_iterable(data))
        pd.DataFrame.from_dict(data).to_csv(f'./api_scrape_csv_output/{mode}.csv', index=False)
        print(f'finished scrape for type: {mode}')


def tryScrapePage(mode, i, total_requests, max_requests):
    link = f'https://api.doge.gov/savings/{mode}?page={i}&per_page=500'
    if mode == 'payments':
        link = f'https://api.doge.gov/{mode}?page={i}&per_page=500'
    try:
        request = requests.get(link)
        request.raise_for_status()  
        contentDict = json.loads(request.content)

        total_pages = contentDict.get('meta').get('pages')
        if i == 1:
            print(f'accessing type {mode}')
            print(f'number of pages for type {mode}: {total_pages}')
        
        print(f'got content for link {link}')
        return contentDict, total_pages

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}, trying again ({total_requests} out of {max_requests})", end='\r')
        return None, i + 1
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}, trying again ({total_requests} out of {max_requests})", end='\r')
        return None, i + 1 
main()