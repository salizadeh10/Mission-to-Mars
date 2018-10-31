from splinter import Browser
from bs4 import BeautifulSoup
import requests, time
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def get_mars_news(url):
    """ NASA Mars News
        Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) 
        and collect the latest News Title and Paragraph Text. Assign the text 
        to variables that you can reference later. """
    browser = init_browser()
    browser.visit(url)

    # Create BeautifulSoup object and parse
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    mars_news = {}
    mars_news['news_title'] = soup.find('div', class_='content_title').text
    mars_news['news_paragraph'] = soup.find('div', class_='article_teaser_body').text
    
    return mars_news

def get_featured_image_link(url):
    """ JPL Mars Space Images - Featured Image
        Visit the url for JPL Featured Space Image [here]
        (https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars). """

    browser = init_browser()
    browser.visit(url)

    # Moving through the pages and giving time to search and scrape
    time.sleep(2)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)

    # Create BeautifulSoup object and parse
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    # Get featured image
    results = soup.find('article')
    extension = results.find('figure', 'lede').a['href']
    link = "https://www.jpl.nasa.gov"
    featured_image_url = link + extension
    
    return featured_image_url

def get_mars_weather(url):
    """ Mars Weather
        Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en)
        and scrape the latest Mars weather tweet from the page. 
        Save the tweet text for the weather report as a variable called `mars_weather`. """

    browser = init_browser()
    browser.visit(url)

    # Create BeautifulSoup object and parse
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    mars_weather = soup.find('div', class_='js-tweet-text-container').text

    return mars_weather

def get_mars_facts(url):
    """ Mars Facts
        Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and 
        use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
        Use Pandas to convert the data to a HTML table string. """

    mars_facts_table = pd.read_html(url)
    
    # Convert to dataframe and tidy it up
    mars_facts_df = mars_facts_table[0]
    mars_facts_df.columns = ['Mars Facts', 'Value']

    mars_facts_df.set_index('Mars Facts', inplace=True)
    
    mars_facts_table = mars_facts_df.to_html()
    mars_facts_table
    
    return mars_facts_table

def get_link_by_partial_text(url, partial_text):
    """ Function to receive url and partial text of a link and return the full link in a dictionary """
    
    browser = init_browser()
    browser.visit(url)

    # Moving through pages
    time.sleep(2)
    browser.click_link_by_partial_text(partial_text)

    # Create BeautifulSoup object and parse
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    # Save link to Cerberus image
    link = soup.find('div', 'downloads').a['href']
    
    image_link = []
    image_link = [partial_text, link]
    
    return image_link

def scrape():
    """ Main function to scrape all required mars data via function calls and return them in one dictonary.  """
    
    browser = init_browser()

    # Declare the dictionary which will hold all the information scraped
    mars_mission_dict = {}

    # Populate the dictionaly of scraped data
    mars_mission_dict['mars_news'] = get_mars_news('https://mars.nasa.gov/news/')
    mars_mission_dict['featured_image'] = get_featured_image_link('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    mars_mission_dict['mars_weather'] = get_mars_weather('https://twitter.com/marswxreport?lang=en')
    mars_mission_dict['mars_facts'] =  get_mars_facts('http://space-facts.com/mars/')

    # Get the links for each hemispher using the funtion and append to url list
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemisphere_image_urls = []
    hemisphere_image_urls.append(get_link_by_partial_text(url, 'Cerberus Hemisphere Enhanced'))
    hemisphere_image_urls.append(get_link_by_partial_text(url, 'Schiaparelli Hemisphere Enhanced'))
    hemisphere_image_urls.append(get_link_by_partial_text(url, 'Syrtis Major Hemisphere Enhanced'))
    hemisphere_image_urls.append(get_link_by_partial_text(url, 'Valles Marineris Hemisphere Enhanced'))
    
    # Add the hemispher images to the dictionary 
    mars_mission_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_mission_dict