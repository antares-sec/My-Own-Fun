import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import random

def request_url(url_name):
    user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0',
    'Mozilla/5.0 (Android 11; Tablet; rv:68.0) Gecko/68.0 Firefox/88.0',
    ]

    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'DNT': '1',  # Do Not Track request header
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }
    try:
        url = requests.get(url_name, headers=headers)
    except ConnectionError as ce:
        raise ce
    except ConnectionRefusedError as  cre:
        raise cre
    
    return url

class Crawler:
    """
        Crawler for website, as you know not all of the website can be crawled.
        There's a web can block your IP because you crawled their website
    """
    def __init__(self, url):
        self.url = request_url(url)
        self.bs = BeautifulSoup(self.url.text, 'html.parser')

    @property
    def if_tables_valid(self):
        """
            This is not only a function, but a variable inside of class. 
            In this way, the variable have a processed value instead of creating
            a different function.
        """
        tables = self.bs.find_all('table')
        if not tables:
            # Returning False if there's no tables
            print("No tables found on the webpage")
            return False
        return tables # If table found, return the table tag / value

    def tables_item(self):
        """ 
            This function will returning false if tables not found inside of website
            or the data inside of tables are zero.

            If all of data are valid, this function will save the data with .csv ext.
            There's error handling as well when the system trying to save the data.
        """
        if self.if_tables_valid is False:
            return False
        
        all_data = []
        for table in self.if_tables_valid: # Iterate the tables
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['th', 'td'])
                if cols:
                    all_data.append([col.text.strip() for col in cols]) # Split and seperate all of the text.
        
        if not all_data:
            print("No data found in tables.")
            return False

        df = pd.DataFrame(all_data)
        try:
            filename = f'data_scraping_{datetime.now()}.csv'
            df.to_csv(filename, index=False)
            print(f'Data saved to {filename}')
            return True
        except Exception as e:
            print(f"Error saving data: {str(e)}")
            return False

    def get_html(self):
        """ Get HTML Code for the entire website """
        soup = BeautifulSoup(self.url.text, 'html.parser')
        filename = f"{datetime.now().strftime("%Y%m%d_%H%M%S")}_page.html"
        with open(filename, 'a') as f:
            f.write(soup.prettify())
            print(f"HTML saved to {filename}")
    
    def get_links(self):
        """ Get all links inside of website"""
        links = []
        for link in self.bs.find_all('a'):
            data = link.get('href')
            links.append(data)
           
        filename = f"{datetime.now()}.txt"
        with open(filename, 'a') as f:
            for link in links:
                f.write(link)
                f.write("\n")
        

    def text_paragraph(self, tags):
        """ Finding all of text inside of website"""
        if len(tags) > 0:
            for tag in tags:
                text_data = []
                tags_data = self.bs.find_all(tag)
                text_data.append([txt.text.strip() for txt in tags_data])

                if not text_data:
                    continue

                df = pd.DataFrame(text_data)
                try:
                    filename = f'data_{tag}_{datetime.now()}.csv'
                    df.to_csv(filename, index=False)
                    print(f"Data saved to {filename}")
                except Exception as e:
                    print(f"Error saving data: {str(e)}")
        else:
            print("There's no tag initialized or passed.")
            return False

# Testing 
if __name__ == '__main__':
    url = "https://bpkd.wonogirikab.go.id/"
    crawler = Crawler(url)
    crawler.text_paragraph(['p', 'h2', 'h1', 'h3', 'span', 'a'])
        