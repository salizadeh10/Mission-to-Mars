from splinter import Browser
from bs4 import BeautifulSoup
import requests, time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

# Create BeautifulSoup object and parse
def create_soup_obj(browser):
    
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    
    return soup

def scrape():
    # Fire up browser 
    browser = init_browser()

    # Declare the dictionary which will hold all the information scraped and rendered on HTML pages
    mars_mission_dict = {}

    ### NASA Mars News
    # Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) 
    # and collect the latest News Title and Paragraph Text. Assign the text 
    # to variables that you can reference later.

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Create BeautifulSoup object and parse
    soup = create_soup_obj(browser)

    mars_mission_dict['news_title'] = soup.find('div', class_='content_title').text
    mars_mission_dict['news_paragraph'] = soup.find('div', class_='article_teaser_body').text

    ### JPL Mars Space Images - Featured Image
    # Visit the url for JPL Featured Space Image [here]
    # (https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Moving through the pages and giving time to search and scrape
    time.sleep(2)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)

    # Create BeautifulSoup object and parse
    soup = create_soup_obj(browser)

    # Get featured image
    results = soup.find('article')
    extension = results.find('figure', 'lede').a['href']
    link = "https://www.jpl.nasa.gov"
    featured_image_url = link + extension

    mars_mission_dict['featured_image'] = featured_image_url

    #### Mars Weather
    # Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en)
    # and scrape the latest Mars weather tweet from the page. 
    # Save the tweet text for the weather report as a variable called `mars_weather`.

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    ## Create BeautifulSoup object and parse
    soup = create_soup_obj(browser)

    # Get wheather report and store in mars dict
    mars_mission_dict['mars_weather'] = soup.find('div', class_='js-tweet-text-container').text

    ### Mars Facts
    # Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and 
    # use Pandas to scrape the table containing facts about the planet 
    # including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.

    url = 'http://space-facts.com/mars/'    
    mars_facts_table = pd.read_html(url)

    # Convert to dataframe and tidy it up
    mars_facts_df = mars_facts_table[0]
    mars_facts_df.columns = ['Mars Facts', 'Value']

    mars_facts_df.set_index('Mars Facts', inplace=True)
    mars_facts_table = mars_facts_df.to_html()

    mars_mission_dict['mars_facts'] =  mars_facts_table                              

    ### Mars Hemispheres
    # Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
    # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
    # Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'   

    hemispheres = ['Cerberus Hemisphere Enhanced', 'Schiaparelli Hemisphere Enhanced',                'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced']

    hemisphere_image_urls = []
    image_urls_dict = {}
                
    for hemisphere in hemispheres:
        
        browser.visit(url)

        # Moving through pages
        time.sleep(2)
        browser.click_link_by_partial_text(hemisphere)

        #Create BeautifulSoup object and parse
        soup = create_soup_obj(browser)

        # Save link to Cerberus image
        link = soup.find('div', 'downloads').a['href']
        
        image_urls_dict = {'title': hemisphere, 'img_url': link}
        
        hemisphere_image_urls.append(image_urls_dict)
        
        #hemisphere_image_urls.append(image_urls_dict)

    mars_mission_dict['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()  

    return mars_mission_dict

# mars_info = scrape()
# print(mars_info)
