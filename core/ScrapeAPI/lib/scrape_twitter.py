from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time
import pandas as pd
import datetime 
import concurrent.futures



def setup_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver


class ScrapeTwitter:
    """ Scrapping Twitter with selenium, this module will automatic open web browser,
        accessing website and scrapping based on your search input.
    """

    def __init__(self, username, password, text):
        if username is None and password is None:
            self.username = str(input("Your username : "))
            self.password = str(input("Your password : "))
        else:
            self.username = username
            self.password = password

        self.text = text
        self.timeline = ""
        self.driver = setup_driver()
        
    def login_twitter(self):
        self.driver.get("https://x.com/i/flow/login")
        
        # Automatically input username into input box
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input'))
        )
        username_field.send_keys(self.username)
        self.driver.find_element(By.XPATH, "//span[text()='Next']").click()
        
        # Automatically enter password
        password_feld = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'))
        )
        password_feld.send_keys(self.password)
        self.driver.find_element(By.XPATH, "//span[text()='Log in']").click()

        # Wait until login
        WebDriverWait(self.driver, 10).until(EC.url_contains("home"))
    
    def scrape_tweets(self, num_tweets=100):
        # driver.get(f"https://x.com/search?q={text_to_scrape}&src=typed_query")
        self.driver.get(f"https://x.com/search?q={self.text}&src=typed_query&f=live")
        tweets = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while len(tweets) < num_tweets:
            tweet_elements = self.driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")

            for tweet in tweet_elements:
                if len(tweets) >= num_tweets:
                    break
                
                try:
                    text = tweet.find_element(By.XPATH, ".//div[@lang]").text
                    tweets.append(text)
                except:
                    pass
                
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height

        # Create a DataFrame from the tweets
        df = pd.DataFrame(tweets, columns=['Tweet'])

        # Save the DataFrame to a CSV file
        df.to_csv(f'tweets-{datetime.datetime.now()}.csv', index=False)

        print(f"Scraped {len(tweets)} tweets and saved to 'tweets.csv'")
        print(df.head())  # Print the first few rows to verify



def threadScrapping(list_username, list_password, worker, text, max_tweets):
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
        scrape = ScrapeTwitter(list_username, list_password)
        executor.map(scrape.login_twitter(), range(worker))
        executor.map(scrape.scrape_tweets(max_tweets), range(worker))

def run():
    # How many inputs for username and password
    n = int(input("How many accounts : "))
    text = str(input("Input text you want to search : "))
    account = {}

    if n == 1:
        username = str(input("Username : "))
        password = str(input("Password : "))
        
        max_tweets = int(input("Max Tweets : "))
        threadScrapping(username, password, 10, text, max_tweets)

    for i in range(n):
        username = str(input(f"Username_{i} : "))
        password = str(input(f"Password_{i} : "))
        account[f"{username}_{i}"] = password