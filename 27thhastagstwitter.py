# import the required packages and libraries
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
import requests
from webdriver_manager.chrome import ChromeDriverManager

# set up a new Selenium driver
chromedriver_path = r"C:\Users\bruker1\Downloads\chromedriver_win32\chromedriver.exe"

# proxy = requests.get(
#     "https://ipv4.webshare.io/",
#     proxies={
#         "http": "http://webscraping-rotate:webscraping1234@p.webshare.io:80/",
#         "https": "http://webscraping-rotate:webscraping1234@p.webshare.io:80/"
#     }
# ).text

# proxy_url = "http://webscraping-1:webscraping1234@185.168.158.51:80"
service = Service(chromedriver_path)
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' % proxy_url)
# chrome_options.add_argument('--headless')  # Hide GUI
driver = webdriver.Chrome(options=chrome_options, service=service)

# define the username of the profile to scrape and generate its URL
username = "bright_data"
URL = "https://twitter.com/" + username + "?lang=en"

# load the URL in the Selenium driver
driver.get(URL)

# wait for the webpage to be loaded
# PS: this considers a profile page to be loaded when at least one tweet has been loaded
#     it might not work well for restricted profiles or public profiles with zero tweets
try:
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="primaryColumn"]')))
except WebDriverException:
    print("Tweets did not appear! Proceeding after timeout")

# extract the information using either CSS selectors (and data-testid) or XPath
name = driver.find_element(By.XPATH,
                           '//div[@data-testid="UserName"]//span[contains(@class, "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0")]/span').text
bio = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="UserDescription"]').text
location = driver.find_element(By.CSS_SELECTOR, 'span[data-testid="UserLocation"]').text
website = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="UserUrl"]').text
join_date = driver.find_element(By.CSS_SELECTOR, 'span[data-testid="UserJoinDate"]').text
following_count = driver.find_element(By.XPATH, "//span[contains(text(), 'Following')]/ancestor::a/span").text
followers_count = driver.find_element(By.XPATH, "//span[contains(text(), 'Followers')]/ancestor::a/span").text

# print the collected information
print("Name\t\t: " + name)
print("Bio\t\t: " + bio)
print("Location\t: " + location)
print("Website\t\t: " + website)
print("Joined on\t: " + join_date)
print("Following count\t: " + following_count)
print("Followers count\t: " + followers_count)

# ... (previous code)

# initialize empty lists to store scraped data
UserTags = []
TimeStamps = []
Tweets = []
Replys = []
reTweets = []
Likes = []
Hashtags = []

# find all tweet articles on the page
articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
# loop over the articles to extract data from each tweet
tweet_count = 0  # Initialize tweet counter
while tweet_count < 50:  # Loop until 50 tweets are scraped
    for article in articles:
        # extract user handle
        UserTag = article.find_element(By.XPATH, ".//div[@data-testid='User-Name']").text
        UserTags.append(UserTag)

        # extract timestamp
        TimeStamp = article.find_element(By.XPATH, ".//time").get_attribute('datetime')
        TimeStamps.append(TimeStamp)

        # extract tweet text
        Tweet = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
        Tweets.append(Tweet)

        # extract number of replies
        Reply = article.find_element(By.XPATH, ".//div[@data-testid='reply']").text
        Replys.append(Reply)

        # extract number of retweets
        reTweet = article.find_element(By.XPATH, ".//div[@data-testid='retweet']").text
        reTweets.append(reTweet)

        # extract number of likes
        Like = article.find_element(By.XPATH, ".//div[@data-testid='like']").text
        Likes.append(Like)

        # extract hashtags
        hashtags_elements = article.find_elements(By.XPATH, ".//a[@href][starts-with(@href, '/hashtag/')]")
        hashtags = [hashtag.text for hashtag in hashtags_elements]
        Hashtags.append(hashtags)

        tweet_count += 1  # Increment tweet counter

    # scroll down to load more tweets
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    time.sleep(3)

    # find all tweet articles again to check if there are more tweets to scrape
    articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")

    # remove duplicate tweets and check if enough unique tweets have been scraped
    unique_tweets = list(set(Tweets))
    if len(unique_tweets) >= 50:
        break  # exit loop if 50 tweets have been scraped

# ... (rest of the code)


# print the first tweet information
print("UserTags : " + UserTags[0])
print("TimeStamp : " + TimeStamps[0])
print("Tweet : " + Tweets[0])
print("Replys : " + Replys[0])
print("reTweets : " + reTweets[0])
print("Likes : " + Likes[0])

# Get all tweets after scrolling
tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')

# print each collected tweet's text
for tweet in tweets:
    tweet_text = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]').text
    print("Tweet text\t: " + tweet_text)

# Get the total number of tweets
total_tweets = len(tweets)

# print the total number of tweets
print("Total Tweets\t: " + str(total_tweets))

# Create a CSV file to write the data
with open("../../../Downloads/twitter_profile.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Name", "Bio", "Location", "Website", "Joined On", "Following Count",
                  "Followers Count", "Tweet Text", "UserTags", "TimeStamp", "Tweet", "Replys",
                  "reTweets", "Likes", "Hashtags"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header row in the CSV file
    writer.writeheader()

    # Write the data rows in the CSV file
    for i in range(len(Tweets)):
        tweet_text = Tweets[i]
        writer.writerow({
            "Name": name,
            "Bio": bio,
            "Location": location,
            "Website": website,
            "Joined On": join_date,
            "Following Count": following_count,
            "Followers Count": followers_count,
            "Tweet Text": tweet_text,
            "UserTags" :  UserTags[i],
            "TimeStamp" : TimeStamps[i],
            "Tweet" : Tweets[i],
            "Replys" : Replys[i],
            "reTweets" : reTweets[i],
            "Likes" : Likes[i],
            "Hashtags": ", ".join(Hashtags[i])
        })

# Quit the WebDriver
driver.quit()
