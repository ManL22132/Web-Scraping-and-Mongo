#################################################################################
# Mission to Mars Web Scrapping
#################################################################################

#--------------------------------------------------------------------------------
# Dependencies and Setup
#--------------------------------------------------------------------------------
import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser


#################################################################################
# Define the scrape function to scrape the Mars data, store it in a dictionary 
# and return from this function.
#################################################################################
def scrape():

    mars = {}

    #############################################################################
    # NASA Mars News
    # Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the 
    # latest News Title and Paragraph Text. 
    #############################################################################

    #----------------------------------------------------------------------------
    # URL of page to be scraped for the Mars News info
    #----------------------------------------------------------------------------
    url = 'https://mars.nasa.gov/news/'

    response = requests.get(url)

    #----------------------------------------------------------------------------
    # Create BeautifulSoup object; parse with 'html.parser'
    #----------------------------------------------------------------------------
    soup = BeautifulSoup(response.text, 'html.parser')

    #----------------------------------------------------------------------------
    # Find the Title & Paragraph Text for the feature news article.
    #----------------------------------------------------------------------------
    news_title = soup.find('div', class_="slide").find('div', class_='content_title').text
    news_title = news_title.replace('\n', '')

    news_p = soup.find('div', class_="slide").div.a.div.div.text
    news_p = news_p.replace('\n', '')

    #----------------------------------------------------------------------------
    # Add entries to the dictionary from MARS NEWS
    #----------------------------------------------------------------------------
    mars['news_title'] = news_title
    mars['news_paragraph'] = news_p

    #############################################################################
    # JPL Mars Space Images - Featured Image
    # Visit the url for JPL Featured Space Image at
    # https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    #############################################################################

    # executable_path = {'executable_path': 'C:\ChromeDriver\chromedriver.exe'}
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html

    #----------------------------------------------------------------------------
    # Parse HTML with Beautiful Soup
    #----------------------------------------------------------------------------
    soup = BeautifulSoup(html, 'html.parser')

    primary_feature = soup.find('section', class_="primary_media_feature")
    item = primary_feature.find('div', class_='carousel_items')
    article = item.find('article', class_='carousel_item')['style']

    article_arr = article.split("\'")
    featured_image_url = ('https://www.jpl.nasa.gov' + article_arr[1])

    #----------------------------------------------------------------------------
    # Add image entry to the dictionary from FEATURED IMAGE
    #----------------------------------------------------------------------------
    mars['featured_image_url'] = featured_image_url 

    #############################################################################
    # Mars Weather
    # Visit the Mars Weather twitter account at
    # (https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather 
    # tweet from the page. 
    #############################################################################

    url = 'https://twitter.com/marswxreport?lang=en'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    mars_weather = soup.find('p', class_="TweetTextSize").text

    #----------------------------------------------------------------------------
    # Add the weather entry to the dictionary from WEATHER TWEET
    #----------------------------------------------------------------------------
    mars['mars_weather'] = mars_weather
 
    #############################################################################
    # Mars Facts
    # Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use 
    # Pandas to scrape the table containing facts about the planet including 
    # Diameter, Mass, etc.
    #############################################################################

    url = 'http://space-facts.com/mars/'

    tables = pd.read_html(url)

    #----------------------------------------------------------------------------
    # Slice off the mars info dataframes using normal indexing.
    #----------------------------------------------------------------------------
    mars_df = tables[0]
    mars_df.columns = ['0', '1']

    #----------------------------------------------------------------------------
    # Remove header row & rename column headers
    #----------------------------------------------------------------------------
    renamed_mars_df = mars_df.rename(columns={"0":"Feature", "1":"Value"})

    #----------------------------------------------------------------------------
    # Set the index to the Feature column
    #----------------------------------------------------------------------------
    renamed_mars_df.set_index('Feature', inplace=True)

    #----------------------------------------------------------------------------
    # Use the Pandas "to_html" method to generate an HTML table from DataFrames.
    #----------------------------------------------------------------------------
    html_mars_table = renamed_mars_df.to_html()

    #----------------------------------------------------------------------------
    # Clean up the table.
    #----------------------------------------------------------------------------
    html_mars_table = html_mars_table.replace('\n', '')

    #----------------------------------------------------------------------------
    # Dictionary entry from MARS FACTS
    #----------------------------------------------------------------------------
    mars['mars_facts'] = html_mars_table

    #############################################################################
    # Mars Hemispheres
    # Visit the USGS Astrogeology site at
    # (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) 
    # to obtain high resolution images for each of Mar's hemispheres.
    #############################################################################

    #----------------------------------------------------------------------------
    # URL of page to be scraped to capture the hemisphere title/image
    #----------------------------------------------------------------------------
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    results = soup.find_all('div', class_="item")

    #----------------------------------------------------------------------------
    # Loop through returned results to capture the hemisphere title and link to 
    # the page that contains the link to the full hemisphere image
    #----------------------------------------------------------------------------
    sum = 0
    title = []
    links = []
    for result in results:

        try:

            title.append(result.find('a', class_="itemLink").text)

            links.append('https://astrogeology.usgs.gov/' + result.a['href'])

            sum += 1
        except AttributeError as e:
            print(e)

    #----------------------------------------------------------------------------
    # Loop through the pages that point to the hemisphere image and capture the url
    # of the hemisphere image.
    #----------------------------------------------------------------------------
    hemisphere_images = []
    this_item = 0

    for link in links:
        
        try:

            hemisphere = requests.get(link)

            hemi_soup = BeautifulSoup(hemisphere.text, 'html.parser')
            
            hemi_results = hemi_soup.find_all('div', class_="downloads")
            
            hemi_image = hemi_soup.find('div', class_="downloads").find('ul').find('li').a['href']
            
            hemisphere_images.append(hemi_image)

            this_item += 1

        except AttributeError as e:
            print(e)

    this_dict_item = 0
    hemisphere_image_urls = []
    for link in links:
        hemisphere_image_urls.append({'title': title[this_dict_item], 
                                      'img_url': hemisphere_images[this_dict_item]})
        this_dict_item += 1

    #----------------------------------------------------------------------------
    # Store results in the mars dictionary
    #----------------------------------------------------------------------------
    mars['hemisphere_image_urls'] = hemisphere_image_urls

    #----------------------------------------------------------------------------
    # Close the ChromeDriver Browser window
    #----------------------------------------------------------------------------
    browser.quit()

    return mars

#################################################################################
# End of function
#################################################################################