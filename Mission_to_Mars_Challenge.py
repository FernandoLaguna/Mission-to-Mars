

# import our scraping tools: the Browser instance from splinter, the BeautifulSoup object, and the driver object for Chrome, ChromeDriverManager
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



# With Splinter set the executable path and initialize a browser: (**executable_path is unpacking the dictionary we've stored the path in)
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)



# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
# searching for elements with a specific combination of tag (div) and attribute (list_text) 'div.list_text' o <div class="div.list">
# optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.
browser.is_element_present_by_css('div.list_text', wait_time=1)



# BeautifulSoup parses the HTML text and then stores it as an object
html = browser.html
news_soup = soup(html, 'html.parser')
# the code 'div.list_text' pinpoints the <div /> tag with the class of list_text
slide_elem = news_soup.select_one('div.list_text')



# Use the parent element to find the first `a` tag and save it as `news_title`
# When get_text() method is chained onto .find(), only the text of the element is returned
news_title = slide_elem.find('div', class_='content_title').get_text()


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()



# ### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)



# Find and click the full image button (the second one)
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# With the new page loaded onto our automated browser, it needs to be parsed with soup
html = browser.html
img_soup = soup(html, 'html.parser')



# Find the relative image url. An img tag is nested within this HTML, so we've included it. 
#.get('src') pulls the link to the image
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'



# we're creating a new DataFrame from the HTML table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
# we assign columns to the new DataFrame for additional clarity.
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)



# Convert dataframe to html
df.to_html()

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

for x in range(3, 7):
    # Find and click the full image button (the second one)
    full_image_elem = browser.find_by_tag('img')[x]
    full_image_elem.click()

    # With the new page loaded onto our automated browser, it needs to be parsed with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Find the relative image url. An img tag is nested within this HTML, so we've included it. 
    #.get('src') pulls the link to the image
    img_url_rel = img_soup.find('img', class_='wide-image').get('src')
    
    title = img_soup.find('h2', class_= 'title').text

    # Use the base URL to create an absolute URL
    img_url = f'https://marshemispheres.com/{img_url_rel}'
    
    hemispheres = {title:img_url}

    hemisphere_image_urls.append(hemispheres)

    browser.back()



# Close the browser
browser.quit()






