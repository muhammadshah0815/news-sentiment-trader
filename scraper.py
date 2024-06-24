import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_page(url):
    """download a webpage and return a BeautifulSoup object"""
    response = requests.get(url)
    if not response.ok:
        print('Status code:', response.status_code)
        raise Exception('Failed to load page {}'.format(url))
    page_content = response.text
    doc = BeautifulSoup(page_content, 'html.parser')
    return doc

def get_news_tags(doc):
    """Get the list of tags containing news information."""
    news_class = "Ov(h) Pend(44px) Pstart(25px)" 
    news_list = doc.find_all('div', {'class': news_class})
    return news_list

BASE_URL = 'https://finance.yahoo.com'

def parse_news(news_tag):
    """Get the news data point and return dictionary."""
    news_source = news_tag.find('div').text
    news_headline = news_tag.find('a').text  
    news_url = news_tag.find('a')['href']  
    news_content = news_tag.find('p').text  
    news_image = news_tag.findParent().find('img')['src']
    return {
        'source': news_source,
        'headline': news_headline,
        'url': BASE_URL + news_url,
        'content': news_content,
        'image': news_image
    }

def scrape_yahoo_news(url, path=None):
    """get the yahoo finance market news and write them to a CSV file"""
    if path is None:
        path = 'stock-market-news.csv'

    print('Requesting HTML page')
    doc = get_page(url)

    print('Extracting news tags')
    news_list = get_news_tags(doc)

    print('Parsing news tags')
    news_data = [parse_news(news_tag) for news_tag in news_list]

    print('Saving data to CSV')
    news_df = pd.DataFrame(news_data)
    news_df.to_csv(path, index=None)

    return news_df

if __name__ == "__main__":
    YAHOO_NEWS_URL = 'https://finance.yahoo.com/topic/stock-market-news/'
    news_df = scrape_yahoo_news(YAHOO_NEWS_URL)
    print(news_df.head())