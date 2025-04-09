import requests
import json
import pandas as pd
import itertools

def main():

    modes = ['grants', 'contracts', 'leases']

    for mode in modes:
        data = []

        link = f'https://api.doge.gov/savings/{mode}?page=1&per_page=500'
        metaRequest = requests.get(link)
        total_pages = json.loads(metaRequest.content)['meta']['pages']
        print(f'pages: {total_pages}')

        for i in range(1, total_pages+1):
            link = f'https://api.doge.gov/savings/{mode}?page={i}&per_page=500'
            request = requests.get(link)
            print('accessing: ' + link)
            contentDict = json.loads(request.content)
            data.append(contentDict['result'][mode])
        
        data = list(itertools.chain.from_iterable(data))
        pd.DataFrame.from_dict(data).to_csv(f'./api_scrape_csv_output/{mode}.csv', index=False)

main()