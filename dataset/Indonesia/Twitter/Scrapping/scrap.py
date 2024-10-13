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
import threading
import concurrent.futures



def setup_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver


def login_twitter(driver, username, password):
    driver.get("https://x.com/i/flow/login")
    # Enter username
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input'))
    )
    username_field.send_keys(username)
    driver.find_element(By.XPATH, "//span[text()='Next']").click()
    
    # Enter password
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'))
    )
    password_field.send_keys(password)
    driver.find_element(By.XPATH, "//span[text()='Log in']").click()
    
    # Wait for login to complete
    WebDriverWait(driver, 10).until(EC.url_contains("home"))


def scrape_tweets(driver, text_to_scrape, num_tweets=10):
    # driver.get(f"https://x.com/search?q={text_to_scrape}&src=typed_query")
    driver.get(f"https://x.com/search?q={text_to_scrape}&src=typed_query&f=live")
    tweets = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while len(tweets) < num_tweets:
        tweet_elements = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
        
        for tweet in tweet_elements:
            if len(tweets) >= num_tweets:
                break
            
            try:
                text = tweet.find_element(By.XPATH, ".//div[@lang]").text
                tweets.append(text)
            except:
                pass
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        last_height = new_height

    # Create a DataFrame from the tweets
    df = pd.DataFrame(tweets, columns=['Tweet'])

    # Save the DataFrame to a CSV file
    df.to_csv(f'tweets-{datetime.datetime.now()}.csv', index=False)

    print(f"Scraped {len(tweets)} tweets and saved to 'tweets.csv'")
    print(df.head())  # Print the first few rows to verify

def threadScrapping(worker, driver, text, max_tweets):
    # Thread executor
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
        executor.map(scrape_tweets(driver, text, max_tweets), range(worker))

if __name__ == '__main__':
    driver = setup_driver()
    login_twitter(driver, 'yantoriu12', 'Miksa211') 
    threadScrapping(10, driver, "PutusanMK", 1000)