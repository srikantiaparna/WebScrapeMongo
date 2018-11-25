def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser('chrome', **executable_path, wait_time=60, fullscreen=False, incognito=True, headless=False)


def scrape():

    # Dependencies
    
    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    import requests
    import pymongo
    import pandas as pd
    import time

    # chromebrowser set up
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #   URL's to scrape
    news_url = 'https://mars.nasa.gov/news/'
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    facts_url = 'http://space-facts.com/mars/'
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #mars_info = {}

    # **************************************************************************
    #    NASA Mars News
    # **************************************************************************
    # Initialize browser 
    #browser = init_browser()

    # Visit Nasa news url through splinter 
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    # HTML Object
    html = browser.html

    # Parsing HTML with Beautiful Soup
    soup = bs(html, 'html.parser')


    # Scrapes the site and collects the latest News Title and Paragraph Text. 
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    print(news_title)

    print(news_p)



    # **************************************************************************
    #    JPL Mars Space Images - Featured Image
    # **************************************************************************
    # Initialize browser 
    #browser = init_browser()

    # Visit Mars Space Images through splinter
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_image, 'html.parser')

    # Retrieve background-image url from style tag 
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url 
    main_url = 'https://www.jpl.nasa.gov'

    # Assign url to the variable
    featured_image_url = main_url + featured_image_url


    # Display full link to featured image
    print(featured_image_url)

    # **************************************************************************
    #   Mars Weather 
    # **************************************************************************

    # Initialize browser 
    #browser = init_browser()

    # Visit Mars Weather Twitter through splinter 
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    # HTML Object 
    html_weather = browser.html

    # Parsing HTML with Beautiful Soup
    soup = bs(html_weather, 'html.parser')

    # Find all tweets
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

    # Get latest Mars weather tweet 
    for tweet in latest_tweets: 
        mars_weather = tweet.find('p').text
        if mars_weather.partition(' ')[0] == 'Sol':
            print(mars_weather)
            break
        else: 
            pass
    # Print Mars Weather Tweet 
    mars_weather


    # **************************************************************************
    #   Mars Facts
    # **************************************************************************
    # Visit the Mars Facts webpage & scrape the table containing facts about the planet 
    df = pd.read_html(facts_url , attrs = {'id': 'tablepress-mars'})[0]
    df = df.set_index(0).rename(columns={1:"value"})
    df

    # Convert to HTML Table string
    mars_facts = df.to_html()

    # Display Mars Facts Table in HTML Format

    print(mars_facts)


    # **************************************************************************
    #   Mars Hemispheres
    # **************************************************************************

    # Initialize browser 
    #browser = init_browser()

    # Visit hemispheres website through splinter module 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    # HTML Object
    html_hemispheres = browser.html

    # Parsing HTML with Beautiful Soup
    soup = bs(html_hemispheres, 'html.parser')

    # Retreive mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store main_ul 
    main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items
    for i in items: 
        # Store title
        title = i.find('h3').text.strip('Enhanced')

        # Storeimage website link
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit image website link  
        browser.visit(main_url + partial_img_url)
        
        # HTML Object of hemisphere information website 
        partial_img_html = browser.html
        
        # Parsing HTML with Beautiful Soup for each hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        
        # Retrieve each full image source 
        img_url = main_url + soup.find('img', class_='wide-image')['src']
        
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        
        # Create dictionary

        mars = []

        mars.append({"news_title" : news_title, "news_paragraph" : news_p, "featured_image_url" : featured_image_url,

                "mars_weather" : mars_weather, "mars_facts" : mars_facts, "hemispheres_urls" : hemisphere_image_urls})

        # return data

        return mars
